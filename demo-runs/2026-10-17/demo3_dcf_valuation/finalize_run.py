"""Audit the saved Excel package and regenerate the lecture handoff documents.

Run after build_dcf.mjs and recalculate_and_test.ps1. Reads XLSX XML only;
does not author or rewrite the workbook. Uses Python's standard library.
"""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
import json
import posixpath
import zipfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
report = json.loads((ROOT/'validation-report.json').read_text(encoding='utf-8-sig'))
if report['status'] != 'pass':
    prior=json.loads((ROOT/'readiness.json').read_text(encoding='utf-8')) if (ROOT/'readiness.json').exists() else {}
    prior.update(status='needs_attention',mechanical_validation='fail',blocking_reason='Latest native Excel validation did not pass.')
    (ROOT/'readiness.json').write_text(json.dumps(prior,indent=2),encoding='utf-8')
    raise AssertionError('Excel checks must pass before handoff')
s = report['summary']
capex_test = next(c['evidence'] for c in report['checks'] if c['name'].startswith('2027 capex 46%'))
provenance = json.loads((ROOT/'input-provenance.json').read_text(encoding='utf-8'))
artifact = json.loads((ROOT/'artifact-validation.json').read_text(encoding='utf-8'))
manifest = json.loads((ROOT/'sources/manifest.json').read_text(encoding='utf-8'))
peer_inputs = json.loads((ROOT/'peer-inputs.json').read_text(encoding='utf-8'))
peer_manifest = json.loads((ROOT/'sources/peer-refresh/manifest.json').read_text(encoding='utf-8'))
ns = {'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
checks = []
def check(name, passed, evidence):
    checks.append({'name':name,'status':'pass' if passed else 'fail','evidence':evidence})

with zipfile.ZipFile(ROOT/'GOOGL_DCF_Valuation.xlsx') as z:
    book = ET.fromstring(z.read('xl/workbook.xml'))
    rels = {r.attrib['Id']:r.attrib['Target'] for r in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
    sheets = {}
    for item in book.find('m:sheets',ns):
        target = rels[item.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']]
        target = target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/'+target)
        sheets[item.attrib['name']] = ET.fromstring(z.read(target))
    expected = ['README','Assumptions','Summary','Historicals','Projections','DCF','Sensitivity','Multiples']
    check('Fixed eight-tab order', list(sheets)==expected, list(sheets))
    styles = ET.fromstring(z.read('xl/styles.xml'))
    xfs = list(styles.find('m:cellXfs',ns))
    fonts = list(styles.find('m:fonts',ns))
    def font_color(cell):
        font = fonts[int(xfs[int(cell.attrib.get('s',0))].attrib['fontId'])]
        color = font.find('m:color',ns)
        return '' if color is None else color.attrib.get('rgb','')[-6:]
    def cell(sheet, address):
        return sheets[sheet].find(f'.//m:c[@r="{address}"]',ns)
    def cached(sheet,address):
        return cell(sheet,address).findtext('m:v',namespaces=ns)
    numeric_keys = set()
    color_issues = []
    cache_missing = []
    errors = []
    formulas = 0
    for name, sheet in sheets.items():
        for c in sheet.findall('.//m:sheetData/m:row/m:c',ns):
            key = (name,c.attrib['r'])
            formula = c.find('m:f',ns)
            value = c.find('m:v',ns)
            if c.attrib.get('t')=='e': errors.append(key)
            if formula is not None:
                formulas += 1
                if value is None: cache_missing.append(key)
                expected_color = '008000' if '!' in (formula.text or '') else '17212B'
                if font_color(c)!=expected_color: color_issues.append([*key,font_color(c),expected_color])
            elif value is not None and c.attrib.get('t','n')=='n':
                numeric_keys.add(key)
                if font_color(c)!='0000FF': color_issues.append([*key,font_color(c),'0000FF'])
    documented = {(i['sheet'],i['cell']) for i in provenance['inputs'] if i.get('source')}
    check('Every numeric input has cell-level provenance', numeric_keys <= documented,
          {'numeric_cells':len(numeric_keys),'uncovered':sorted(numeric_keys-documented)})
    check('Blue inputs, black formulas and green cross-sheet formulas', not color_issues, color_issues)
    check('Saved formulas have recalculated caches and no errors', not cache_missing and not errors,
          {'formula_cells':formulas,'missing_caches':cache_missing,'errors':errors})
    grid = [cell('Sensitivity',f'{col}{row}') for row in range(10,17) for col in 'DEFGH']
    check('All 35 sensitivity cells are live SUMPRODUCT formulas',
          all('SUMPRODUCT' in c.findtext('m:f',default='',namespaces=ns) for c in grid),
          'Sensitivity!D10:H16; no What-If data table')
    check('Saved Base and 46% capex restored',
          float(cached('Assumptions','D4'))==1 and float(cached('Assumptions','E84'))==0.46,
          {'selector':cached('Assumptions','D4'),'capex':cached('Assumptions','E84')})
    check('Saved Summary matches Excel validation',
          abs(float(cached('Summary','E9'))-s['base_dcf'])<1e-6,
          {'cached_summary':cached('Summary','E9'),'validated_summary':s['base_dcf']})
    check('Saved peer outputs match the selected EBITD policy',
          abs(float(cached('Summary','E12'))-s['peer_ebitd_verified'])<1e-6
          and abs(float(cached('Summary','E13'))-s['peer_forward_pe'])<1e-6,
          {'forward_pe':s['peer_forward_pe'],'verified_ebitd':s['peer_ebitd_verified']})
    check('No external-workbook links or VBA',
          not any(x.startswith('xl/externalLinks/') or 'vbaProject' in x for x in z.namelist()),
          'Source URLs are documentation; calculations are contained in the workbook.')
    grid_near_market = []
    for row in range(10,17):
        for col in 'DEFGH':
            val = float(cached('Sensitivity',f'{col}{row}'))
            grid_near_market.append((abs(val-s['market']),float(cached('Sensitivity',f'C{row}')),
                                     float(cached('Sensitivity',f'{col}9')),val))
    nearest = min(grid_near_market)

visual_path=ROOT/'visual-review.json'
visual=json.loads(visual_path.read_text(encoding='utf-8')) if visual_path.exists() else {'images':{}}
def reviewed_image(name):
    p=ROOT/'previews'/f'{name}.png'
    return p.exists() and visual.get('images',{}).get(name,{}).get('sha256')==hashlib.sha256(p.read_bytes()).hexdigest()
check('All eight sheets have current visual-review evidence',
      not artifact['render_errors'] and all(reviewed_image(n) for n in expected),
      {'reviewed_at':visual.get('reviewed_at'),'method':visual.get('method'),'scope':'Exact hashes of reviewed previews; file existence alone cannot pass.'})
check('Forward and EBITD detail previews have current visual-review evidence',
      all(reviewed_image(n) for n in ['Multiples-forward','Multiples-bridge']),
      'Dated EPS, Meta period-end shares and EBITD reconciliation reviewed; preview hashes must match.')
source_hashes=[]
for source in peer_manifest:
    suffix='.html' if source['id'].startswith('forecast_') else '.json'
    archived=ROOT/'sources/peer-refresh'/(source['id']+suffix)
    source_hashes.append({'id':source['id'],'matches':archived.exists() and hashlib.sha256(archived.read_bytes()).hexdigest()==source['sha256']})
check('All eight peer source snapshots match their recorded hashes',
      len(source_hashes)==8 and all(x['matches'] for x in source_hashes),source_hashes)
check('Peer facts use the intended periods and contain no later filings',
      all(x['filed']<='2026-10-17' and x['end']<='2026-06-30' for x in peer_inputs['source_facts']),
      {'fact_count':len(peer_inputs['source_facts']),'consensus_as_of':peer_inputs['consensus_as_of']})
completed = datetime.now(ZoneInfo('America/Los_Angeles')).isoformat(timespec='seconds')
package = {'completed_at':completed,'status':'pass' if all(c['status']=='pass' for c in checks) else 'fail',
           'checks':checks,'xlsx_sha256':hashlib.sha256((ROOT/'GOOGL_DCF_Valuation.xlsx').read_bytes()).hexdigest()}
(ROOT/'package-audit.json').write_text(json.dumps(package,indent=2),encoding='utf-8')
if package['status'] != 'pass':
    prior=json.loads((ROOT/'readiness.json').read_text(encoding='utf-8')) if (ROOT/'readiness.json').exists() else {}
    prior.update(status='needs_attention',mechanical_validation='fail',blocking_reason='Latest saved-file or visual evidence audit failed.',checks=report['checks']+checks)
    (ROOT/'readiness.json').write_text(json.dumps(prior,indent=2),encoding='utf-8')
    raise AssertionError(json.dumps(checks,indent=2))

limitations = [
 'EV/EBITD explicitly replaces EV/EBITDA at the user\'s request: EBIT plus reported PP&E depreciation, with intangible amortization expensed for every company. Complete reported TTM EBITDA remains unavailable for Alphabet and Amazon; no estimated amortization enters the peer comparison.',
 'Forward P/E uses October 16 S&P Global adjusted non-GAAP consensus via Stock Analysis. Microsoft CY2027 EPS is 50% FY2027 plus 50% FY2028, an equal-half approximation rather than quarterly consensus. Provider EPS adjustments differ from the DCF, which expenses SBC.',
 'EV excludes lease liabilities consistently; lease mixes, asset lives and business models still affect economic comparability. Meta PP&E depreciation is reported in rounded amounts.',
 'October 16 quotes were verified on Google Finance vendor displays, not exchange-direct data. All Alphabet classes use the GOOGL quote. Share counts and balance sheets are June 30 snapshots, not October share-count estimates.',
 'Risk-free rate 4.5%, beta 1.20 and equity risk premium 4.5% are teaching assumptions. Debt and preferred costs use coupon proxies.',
 'Services subcategory margins and segment D&A, capex and working capital are model allocations, not company disclosures.',
 'The balance-sheet bridge is dated June 30 with no July–October roll-forward. Private stakes have zero Base realization; deferred tax and legal claims are deducted. Preferred conversion and capped-call optionality are not modeled.',
 'The remaining 2026 stub assumes H2 cash flow is earned evenly. Terminal capex at 1.15x D&A is a judgment and drives most of the valuation.',
 'Some original SEC HTML downloads returned HTTP 403; the peer refresh now archives all four SEC companyfacts JSON files plus all four consensus pages with hashes.',
 'Native Excel calculation and reopening were tested programmatically. A complete interactive lecture rehearsal and the original under-20-minute execution target have not been measured.'
]
downside=s['base_dcf']/s['market']-1
scenario_text='; '.join(f"{x['name']} ${x['dcf']:.2f}" for x in report['scenarios'])
forward_rows='\n'.join(f"| {x['ticker']} | {x['eps']:.2f} | {x['pe']:.2f}x | {x['date']} |" for x in report['forward_comparables'])
bridge_rows='\n'.join(f"| {x['ticker']} | {x['ebit']:,.0f} | {x['ppe']:,.0f} | {x['ebitd']:,.0f} | {x['multiple']:.2f}x |" for x in report['ebitd_bridge'])
source_links='\n'.join(f"- [{ticker} consensus EPS]({peer_inputs['forward'][ticker]['url']}); [SEC filing facts]({next(x['api_url'] for x in peer_inputs['source_facts'] if x['ticker']==ticker)})." for ticker in ['GOOGL','MSFT','META','AMZN'])
methodology=f"""# Peer comparability — October 17, 2026

## Selected lecture treatment

The presenter selected **EV/EBITD = EV / (EBIT + PP&E depreciation)** in place of EV/EBITDA, alongside resolved forward P/E. This is an explicit metric substitution. Full reported TTM intangible amortization cannot be reconciled for Alphabet and Amazon from the collected filings. Every company's intangible amortization stays expensed; no missing amortization is estimated. The workbook, chart, notes and slide corrections consistently call this EBITD.

## Dated forward P/E

All four archived forecast pages identify S&P Global, adjusted non-GAAP EPS and an October 16, 2026 update date. Prices are the same October 16 closes used elsewhere in the model. GOOGL, META and AMZN FY2027 end December 31. Microsoft CY2027 EPS = 50% × FY2027 $19.78 + 50% × FY2028 $23.72 = $21.75. This assumes equal half-year earnings; it is not quarterly consensus. Adjusted EPS can exclude items such as SBC under provider-specific conventions, unlike the DCF earnings definition.

| Company | CY2027 adjusted EPS | Forward P/E | Consensus updated |
|---|---:|---:|---|
{forward_rows}

Peer MIN/MEDIAN/MAX use MSFT, META and AMZN only. Implied Alphabet price = peer forward P/E × GOOGL CY2027 EPS. The median is **${s['peer_forward_pe']:.2f}**. Source inputs and fiscal conversion: Multiples!D73:G78; outputs: rows 48, 57 and 62; Summary row 13.

## Consistent EBITD denominators

Every company uses **July 1, 2025–June 30, 2026**. Calendar issuers use FY2025 − H1 2025 + H1 2026; Microsoft FY2026 already matches the interval. EBITD adds only PP&E depreciation. No SBC, content amortization, intangible amortization, operating-lease asset amortization or miscellaneous cash-flow adjustments are added back.

| Company | TTM EBIT | TTM PP&E depreciation | TTM EBITD | EV/EBITD |
|---|---:|---:|---:|---:|
{bridge_rows}

USD millions. The source arithmetic is:

- GOOGL: 21,136 − 9,485 + 13,586 = 25,237.
- MSFT: 34,300 for the year ended June 30, 2026.
- META: 18,000 − 8,120 + 11,670 = 21,550, using rounded reported PP&E depreciation.
- AMZN: 41,860 − 18,822 + 26,703 = 49,741.

This replaces the old mixed addbacks of 25,237 / 38,534 / 22,729 / 75,200. Those old broad cash-flow lines no longer feed peer valuations. Peer-median EV/EBITD implies **${s['peer_ebitd_verified']:.2f}** per GOOGL share, applying the same EV-to-common-equity bridge as the DCF. Inputs: Multiples rows 35–43; output: rows 45, 50, 56 and 61; reconciliation: rows 84–95; Summary row 12.

## Evidence and practical limits

{source_links}

Raw pages and SEC JSON are archived in sources/peer-refresh with SHA-256 hashes. peer-inputs.json records taxonomy tags, filing accession, filing date, period and extracted value. No filing later than October 17 is used. Forward EPS dates and non-GAAP caveats are preserved in the archived text.

Meta market capitalization now uses 2,548 million June 30 shares: 2,206 million Class A + 342 million Class B, from the [10-Q balance sheet](https://www.sec.gov/Archives/edgar/data/1326801/000162828026050705/meta-20260630.htm). Multiples!F68:F69 contain the sourced components; F9 sums them. The old 2,543 million quarterly weighted-average proxy was removed. Alphabet price and share count now link to the same authoritative inputs used by the DCF.

EV excludes lease liabilities uniformly; different lease mixes and useful lives still affect comparison. June balances and share counts are not rolled to October, and GAAP P/E contains investment gains. These are valuation limitations, separate from the resolved mismatch in addback definitions. This is a teaching comparison, not a claim of economically identical peers or standardized GAAP EBITD.
"""
(ROOT/'peer-methodology.md').write_text(methodology,encoding='utf-8')
notes=f"""# Alphabet valuation memo — October 17, 2026

**Base DCF ${s['base_dcf']:.2f} per common share; sensitivity ${s['low_dcf']:.2f}–${s['high_dcf']:.2f}, versus the October 16 close of ${s['market']:.2f}.** The Base difference is {downside:.1%}. This is a teaching model, not investment advice. Financials run through June 30; prices are vendor sourced.

Revenue grows from $402.8bn in 2025 to ${s['revenue2030']/1000:.1f}bn in 2030, with Cloud at {s['cloud_share2030']:.1%} of revenue. Six revenue categories feed allocated operating profits and unlevered FCF. Services subcategory margins and investment allocations are assumptions. SBC remains an operating cost.

The [Q2 2026 call]({provenance['sources']['S3'][1]}) guides capex to $195–205bn; the model uses $200bn. Base 2027 capex is 46% of revenue, or ${s['capex2027']/1000:.1f}bn. Annual 2026–2030 FCF: {', '.join(f'${x/1000:.1f}bn' for x in s['fcf'])}. Changing 2027 capex to 36% increases DCF by ${capex_test['delta']:.2f} to ${capex_test['after']:.2f}; 46% was restored after testing.

WACC is {s['wacc']:.2%}, using assumed risk-free rate 4.5%, beta 1.20 and ERP 4.5%; terminal growth is {s['terminal_growth']:.1%}. The DCF includes the remaining 2026 stub and midyear discounting. Terminal capex = 1.15x D&A is a judgment; terminal value represents {s['terminal_share']:.1%} of EV. At Base WACC/g, market price requires {s['required_terminal_fcf_ratio']:.2f}x modeled terminal FCF. The nearest displayed grid point is ${nearest[3]:.2f} at {nearest[1]:.2%} WACC / {nearest[2]:.1%} growth, not an exact implied pair. Operating cases: {scenario_text}.

Peer-median implied prices: **forward P/E ${s['peer_forward_pe']:.2f}; EV/EBITD ${s['peer_ebitd_verified']:.2f}**; GAAP P/E ${s['peer_pe']:.2f}; EV/Sales ${s['peer_sales']:.2f}. Forward P/E uses CY2027 adjusted consensus dated October 16 with Microsoft calendarized. EV/EBITD adds only reported PP&E depreciation to EBIT for all four companies. **At the presenter's request, EBITD replaces EBITDA; intangible amortization remains expensed and no missing amortization is estimated.** See [peer-methodology.md](peer-methodology.md).

The terminal-capex ratio deserves a live discussion: increasing it from 1.15x to 1.50x D&A lowers the DCF to **${s['terminal_capex_stress']:.2f}**, holding the remaining assumptions fixed. The test restored 1.15x. The Gordon model now displays #N/A and an explanation when terminal growth is at or above WACC. Summary low/high values are discount-rate/growth bounds for the selected operating case; peer low/high values are minimum/maximum peer multiples, not operating Bull/Bear cases.

Do not blend these methods into one target. GAAP earnings include investment gains; provider adjusted EPS conventions differ; lease mixes still matter. June balances are not rolled forward, private stakes are excluded in Base, and preferred conversion optionality is not modeled. **Lecture readiness: ready under the selected EBITD scope**, with these limitations visible.
"""
(ROOT/'valuation-notes.md').write_text(notes,encoding='utf-8')
corrections=[
 {'slide':30,'existing':'2025 revenue $403B → ~$823B in 2030; Cloud ~35%', 'replacement':f"2025 revenue $402.8bn → ${s['revenue2030']/1000:.1f}bn in 2030; Cloud {s['cloud_share2030']:.1%}."},
 {'slide':30,'existing':'2026 capex ~$199B; 2027 ~$262B','replacement':f"2026 capex $200bn midpoint of $195–205bn guide; 2027 ${s['capex2027']/1000:.1f}bn. FCF becomes positive in 2028."},
 {'slide':30,'existing':'WACC 9.5%; terminal value ~95% of EV','replacement':f"WACC {s['wacc']:.2%}; terminal growth 3.0%; terminal value {s['terminal_share']:.1%} of EV."},
 {'slide':30,'existing':'DCF $230 (−32%); blended four-method base $284 (−17%)','replacement':f"DCF ${s['base_dcf']:.2f} ({downside:.1%}); sensitivity ${s['low_dcf']:.2f}–${s['high_dcf']:.2f}. Remove blended target. Separately show forward P/E ${s['peer_forward_pe']:.2f} and EV/EBITD ${s['peer_ebitd_verified']:.2f}."},
 {'slide':30,'existing':'Market needs WACC ~8.0%, growth 3.5%','replacement':f"Market requires {s['required_terminal_fcf_ratio']:.2f}x modeled terminal FCF at Base WACC/g. Nearest grid: ${nearest[3]:.2f} at {nearest[1]:.2%} WACC / {nearest[2]:.1%} growth; approximate."},
 {'slide':30,'existing':'EV/EBITDA peer comparison','replacement':'EV/EBITD = EV / (EBIT + PP&E depreciation). Same TTM July 2025–June 2026 and same addback policy for all peers. All intangible amortization stays expensed.'},
 {'slide':30,'existing':'StockAnalysis.com prices (16 Oct 2026)','replacement':'Google Finance quotes October 16; SEC/issuer financials through June 30; S&P Global adjusted CY2027 EPS via Stock Analysis updated October 16. Microsoft uses equal-half fiscal-year calendarization.'}
]
correction_table='\n'.join(f"| {x['existing']} | {x['replacement']} |" for x in corrections)
(ROOT/'lecture-slide30-corrections.md').write_text('# Slide 30 corrections\n\nThe original lecture deck is preserved. Use these replacements when presenting this run.\n\n| Existing text | Replacement |\n|---|---|\n'+correction_table+'\n',encoding='utf-8')
runbook=f"""# Demo 3 — Alphabet DCF runbook

**Readiness: ready under the presenter-selected EV/EBITD scope.** Forward P/E is dated and calendar-aligned. EBITD uses EBIT plus reported PP&E depreciation across all four companies and explicitly replaces EBITDA. Do not call it EBITDA. Peer earnings contain no estimated amortization.

## Prepare

Open GOOGL_DCF_Valuation.xlsx in desktop Excel with Automatic calculation. The file opens on Summary. Confirm Base (Assumptions!D4 = 1), 2027 capex 46% (E84), DCF ${s['base_dcf']:.2f}, forward P/E implied price ${s['peer_forward_pe']:.2f}, and EV/EBITD implied price ${s['peer_ebitd_verified']:.2f}. The saved file has native Excel caches, restored inputs, no macros and no external-workbook formula links. Adjust zoom for the projector. Keep valuation-notes.md, peer-methodology.md and validation-report.md available. Use Ctrl+G with a quoted sheet reference, for example 'Assumptions'!E84, to jump directly to a live-edit cell.

## Five-minute walkthrough

| Time | On screen | Action |
|---|---|---|
| 0:00–0:45 | Summary!C6:G23 and chart | Show DCF ${s['base_dcf']:.2f}, range ${s['low_dcf']:.2f}–${s['high_dcf']:.2f}, market ${s['market']:.2f}. Peer methods are separate checks. |
| 0:45–1:45 | Assumptions!E84 → Summary!E9 | Change 46% to 36%; value becomes ${capex_test['after']:.2f}, up ${capex_test['delta']:.2f}. Restore 46%. Edit E84, not active formula E83. |
| 1:45–2:30 | Assumptions!D4 | Select 2 Bull, 3 Bear, then 1 Base. Tested cases: {scenario_text}. One forecast changes; actuals stay fixed. |
| 2:30–3:15 | Sensitivity!C9:H23 | Center equals DCF. Terminal value is {s['terminal_share']:.1%} of EV; market requires {s['required_terminal_fcf_ratio']:.2f}x modeled terminal FCF at Base WACC/g. |
| 3:15–4:10 | Multiples!C72:J82 | Show October 16 CY2027 adjusted EPS. Explain Microsoft FY2027/FY2028 equal-half approximation. Peer median implies ${s['peer_forward_pe']:.2f}. |
| 4:10–5:00 | Multiples!C84:J95 → Summary!C12:G13 | Define EBITD: EBIT + PP&E depreciation, with intangible amortization still expensed. Same TTM and addback policy for all; median implies ${s['peer_ebitd_verified']:.2f}. Explain why fully reconciled EBITDA was replaced. |

Historical revenue/EBIT tie-outs are in Historicals rows 16/24; the equity bridge is in DCF rows 41–51. If a live edit misbehaves, restore Base and 46%, recalculate, and confirm the values above. Without Excel, use the reviewed previews and call the capex result a recorded test. A full interactive rehearsal has not been measured.

## Questions to prepare for

- **Why does terminal value dominate?** The explicit forecast includes heavy AI investment and early negative cash flow. At {s['terminal_share']:.1%} of EV, terminal economics deserve more attention than the second decimal of the share value. Optional demonstration: Assumptions!D15 from 1.15x to 1.50x lowers value to ${s['terminal_capex_stress']:.2f}; restore 1.15x.
- **Does reducing capex preserve revenue growth?** The 2027 capex edit is a mechanical sensitivity. Revenue and D&A drivers are held fixed; it does not establish that lower real-world investment leaves future growth unchanged.
- **Why not EBITDA?** The chosen EBITD metric keeps intangible amortization expensed for every issuer and avoids invented interim amortization. Different lease mixes and asset lives still matter.
- **Why does growth show #N/A?** A Gordon perpetuity requires WACC greater than growth. Summary gives the reason. Restore terminal growth to 3.0%; do not read a value from invalid combinations.

Before presenting, rehearse the five-minute sequence once on the actual projector and use the slide 30 corrections below. These environment and timing checks are presenter tasks, not claimed as completed by programmatic Excel tests.

## Slide 30 corrections

Original deck preserved; apply these replacements before using its old numbers:

| Existing text | Replacement |
|---|---|
{correction_table}

## Reproduce this dated run

Run these commands from the repository root. They overwrite only this demo's generated outputs. The demo's node_modules junction points to the bundled runtime. Desktop Excel is required for native calculation.

```powershell
$dcfRun = 'C:/Users/h_min/repos/SNU_Agentic_AI_Lecture/demo-runs/2026-10-17/demo3_dcf_valuation'
$dcfNode = 'C:/Users/h_min/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
$dcfPython = 'C:/Users/h_min/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
& $dcfPython (Join-Path $dcfRun 'prepare_peer_inputs.py')
& $dcfNode (Join-Path $dcfRun 'build_dcf.mjs')
& (Join-Path $dcfRun 'recalculate_and_test.ps1')
& $dcfPython (Join-Path $dcfRun 'finalize_run.py')
```

After rebuilding, inspect the changed previews and refresh visual-review.json with the exact reviewed image hashes before finalizing. The finalizer rejects missing or stale visual evidence; it no longer equates image existence with visual review. collect_peer_sources.py refreshes downloads; prepare_peer_inputs.py extracts dated consensus and SEC facts from the archive. The original DCF inputs remain manually verified in the builder. For a new date, update periods, quotes, assumptions and stub dates deliberately; downloading files alone does not refresh the whole model.

## Evidence

readiness.json records the selected metric substitution, results and remaining limitations. validation-report.json records native Excel tests, package-audit.json checks final XLSX XML and source hashes, and input-provenance.json maps all numeric inputs. sources/peer-refresh archives four consensus pages and four SEC JSON files. The source dates and calendarization remain visible in the workbook.
"""
(ROOT/'RUNBOOK.md').write_text(runbook,encoding='utf-8')
all_checks=report['checks']+checks
validation=f"# DCF validation report\n\nCompleted {completed}. Native engine: Microsoft Excel {report['excel_version']} via COM; authoring/render engine: @oai/artifact-tool.\n\n**{sum(c['status']=='pass' for c in all_checks)}/{len(all_checks)} checks passed. Lecture-ready under the selected EBITD scope.**\n\n"
validation+='| Check | Result |\n|---|---|\n'+'\n'.join(f"| {c['name']} | {c['status']} |" for c in all_checks)+'\n\n'
validation+=f"Capex edit: ${capex_test['before']:.6f} → ${capex_test['after']:.6f}; delta ${capex_test['delta']:.6f}, independently expected ${capex_test['expected_delta']:.6f}. Original 46% restored. Cases: {scenario_text}.\n\n"
validation+=f"Forward P/E implied value: ${s['peer_forward_pe']:.6f}; EV/EBITD: ${s['peer_ebitd_verified']:.6f}. Microsoft EPS and Amazon depreciation edits propagated correctly, sources were restored, and the DCF remained unchanged.\n\n"
validation+=f"Review regression tests also cover a single Alphabet price input, Meta period-end shares, two off-center WACC/growth combinations, growth equal to and above WACC, and terminal capex at 1.50x D&A (${s['terminal_capex_stress']:.6f}). All temporary edits were restored.\n\n"
validation+='All eight sheet previews and two added peer-detail previews were inspected. The XLSX was saved, closed and reopened; formula caches were inspected directly. All eight archived peer-source hashes matched.\n\n## Remaining limitations\n\n'+'\n'.join('- '+x for x in limitations)+'\n'
(ROOT/'validation-report.md').write_text(validation,encoding='utf-8')
review=f"""# Demo 3 readiness review

**Verdict: ready for a guided lecture demonstration under the approved EV/EBITD scope.** The frozen October 17, 2026 valuation remains DCF ${s['base_dcf']:.2f}, with ${s['low_dcf']:.2f}–${s['high_dcf']:.2f} sensitivity bounds. The review covered formula dependencies, selected primary-source inputs, numerical boundary cases, presentation labels and the reproducibility of readiness evidence. It was not a fresh audit of every historical filing value.

| Finding | Improvement and evidence |
|---|---|
| Shared quote was duplicated | Multiples!D8 now links to Assumptions!D7; D9 links to Historicals!H47. A +$10 quote edit is tested across DCF market capitalization, peer P/E and Summary. |
| Meta capitalization used an average share count | Replaced 2,543m with the reported June 30 total of 2,548m; Class A/B components remain visible and sourced. Affected P/E and EV/Sales outputs recalculate. |
| Invalid Gordon assumptions produced numeric results | Terminal growth at or above WACC now yields #N/A, with a Summary explanation. Equality and above-WACC tests pass. |
| Grid validation tested only its center | Two off-center grid values now match independent edits to WACC and growth in the native model. |
| Range labels could be read as operating cases | Summary distinguishes discount/growth bounds and peer minimum/maximum values from the Base/Bull/Bear operating selector. |
| Visual readiness could pass from file existence | Finalizer now requires visual-review.json hashes matching the actual reviewed previews. Missing or stale evidence produces needs_attention. |
| Opening view and discussion aids were weak | Workbook saves on Summary. The runbook includes direct cell navigation, recovery steps, terminal-risk discussion and responses to likely audience questions. |

**Remaining critique.** {s['terminal_share']:.1%} of EV is terminal value. The 1.15x terminal capex/D&A ratio, future margins and revenue allocations are judgments; at 1.50x the DCF is ${s['terminal_capex_stress']:.2f}. Peer metrics are corroborating views, not an average target. CY2027 EPS is adjusted consensus and Microsoft uses equal-half calendarization. Lease mixes remain different. Share counts and balance sheets are June snapshots. These limitations are visible and appropriate for teaching model review, not hidden behind passing formula checks.

**Presenter handoff.** A live projector rehearsal is still needed. The original lecture deck was preserved, so use lecture-slide30-corrections.md before displaying its old numbers. Readiness applies to this dated demo workbook and walkthrough; it does not certify the original deck, fresh market data, or an investment recommendation.

Validation: {sum(c['status']=='pass' for c in all_checks)}/{len(all_checks)} checks passed. Native Excel recalculation, saved-file audit and reviewed-preview hashes are recorded in the validation package.
"""
(ROOT/'REVIEW.md').write_text(review,encoding='utf-8')
outputs=['GOOGL_DCF_Valuation.xlsx','valuation-notes.md','RUNBOOK.md','readiness.json','validation-report.md','validation-report.json','package-audit.json','input-provenance.json','artifact-validation.json','lecture-slide30-corrections.md','build_dcf.mjs','recalculate_and_test.ps1','collect_sources.py','finalize_run.py','sources/manifest.json','peer-inputs.json','peer-methodology.md','collect_peer_sources.py','prepare_peer_inputs.py','sources/peer-refresh/manifest.json','REVIEW.md','visual-review.json']
readiness={'demo':'demo3_dcf_valuation','title':'Alphabet formula-driven DCF valuation','status':'ready',
 'readiness_scope':'Lecture demo using user-selected EV/EBITD in place of EV/EBITDA, alongside sourced forward P/E.',
 'metric_substitution':{'requested_metric':'EV/EBITDA','selected_metric':'EV/EBITD','definition':'EV / (EBIT + reported PP&E depreciation)','authorized_by':'User explicitly selected verified EV/EBITD, clearly labeled, alongside resolved forward P/E.','intangible_amortization_policy':'Retained as expense for every issuer; no estimates.'},
 'resolved_gaps':{'forward_pe':'October 16 adjusted consensus; CY2027 for all four companies; Microsoft calendarized with visible equal-half assumption.','peer_earnings_comparability':'Same July 2025–June 2026 period and EBIT plus PP&E depreciation policy for all; explicitly labeled EBITD.'},
 'reported_ebitda_data_complete':False,'completed_at':completed,'outputs':outputs,'checks':all_checks,'limitations':limitations,'slide_corrections':corrections,
 'sources_as_of':{'valuation':'2026-10-17','market_close':'2026-10-16','financial_period_end':'2026-06-30','capex_guidance_call':'2026-07-22','consensus_updated':'2026-10-16','downloaded_source_count':sum(x['status']=='downloaded' for x in manifest),'peer_refresh_snapshots':len(peer_manifest)},
 'mechanical_validation':package['status'],'workbook_sha256':package['xlsx_sha256'],'summary':s}
readiness['review']={'report':'REVIEW.md','reviewed_at':completed,'blockers':[] if package['status']=='pass' else [c['name'] for c in checks if c['status']!='pass'],'presenter_actions':['Rehearse once on the actual projector.','Apply slide 30 corrections before displaying the original deck.']}
readiness['status']='ready' if package['status']=='pass' else 'needs_attention'
(ROOT/'readiness.json').write_text(json.dumps(readiness,indent=2),encoding='utf-8')
assert package['status']=='pass',json.dumps(checks,indent=2)
assert all((ROOT/x).exists() for x in outputs)
print(json.dumps({'status':readiness['status'],'checks_passed':len(all_checks),'base_dcf':s['base_dcf'],'forward_pe':s['peer_forward_pe'],'ev_ebitd':s['peer_ebitd_verified'],'outputs':len(outputs)},indent=2))
