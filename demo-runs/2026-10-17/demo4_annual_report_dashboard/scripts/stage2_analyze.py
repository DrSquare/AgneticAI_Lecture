"""Stage 2: isolated financials.md analysis; no source-document/network reads."""
from pathlib import Path
import hashlib
import json
import re
import sys
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / 'financials.md'
raw = INPUT.read_bytes()
text = raw.decode('utf-8-sig').replace('\r\n', '\n')
rows = json.loads(re.search(r'```json\s*(\[.*?\])\s*```', text, re.S).group(1))
data = {r['id']: r for r in rows}
if '--inspect' in sys.argv:
    for i, r in enumerate(rows):
        print(i, r['id'], '|', r['value'], '|', r['metric'], '|', r['period'], '|', r['source'])
        if r['status'] == 'calc':
            print('  FORMULA', json.dumps(r['formula']), 'NOTES', r['notes'])
    raise SystemExit(0)

# This script reads no business input other than financials.md. Source references
# below are copied as data; no URL is opened and no source document is inspected.
assert len(rows) == 385 and len(data) == len(rows)
sources = {}
for sid, url, locator in re.findall(r'^\[([^\]]+)\]: (\S+) "([^"]+)"$', text, re.M):
    sources[sid] = {'id': sid, 'url': url, 'locator': locator}
assert sources
for row in rows:
    assert all(s in sources for s in row['source'].split(';')), row['id']
    if row['status'] == 'not disclosed':
        assert row['value'] is None, row['id']

derived = []
checks = []
calc_validation = []

def number(x):
    return f'{x:,.8f}'.rstrip('0').rstrip('.') if isinstance(x, float) else f'{x:,}'

def val(key):
    value = data[key]['value']
    assert isinstance(value, (int, float)) and not isinstance(value, bool), key
    return value

def source_ids(key):
    source = data[key]['source']
    return source.split(';') if isinstance(source, str) else [s['id'] for s in source]

def calculate(key, metric, keys, kind, unit, period='FY2026 vs FY2025', segment='Consolidated', notes='', replace=False):
    values = [val(k) for k in keys]
    labels = [number(v) for v in values]
    a = values[0]
    b = values[1] if len(values) > 1 else None
    x = labels[0]
    y = labels[1] if len(labels) > 1 else None
    if kind == 'ratio':
        result, expr, numeric = a / b * 100, 'numerator / denominator * 100', f'{x} / {y} * 100'
    elif kind == 'growth':
        result, expr, numeric = (a / b - 1) * 100, '(current / prior - 1) * 100', f'({x} / {y} - 1) * 100'
    elif kind == 'diff':
        result, expr, numeric = a - b, 'first - second', f'{x} - {y}'
    elif kind == 'sum':
        result, expr, numeric = sum(values), 'sum of inputs', ' + '.join(labels)
    elif kind == 'days':
        result, expr, numeric = a / b * 365, 'ending inventory / annual cost of revenue * 365', f'{x} / {y} * 365'
    elif kind in ('lower', 'upper'):
        sign = -1 if kind == 'lower' else 1
        op = '-' if sign == -1 else '+'
        result, expr, numeric = a * (1 + sign*b/100), f'midpoint * (1 {op} tolerance / 100)', f'{x} * (1 {op} {y} / 100)'
    elif kind == 'fcf':
        result, expr, numeric = a - b - values[2], 'CFO - PP&E/intangible purchases - principal payments', f'{x} - {y} - {labels[2]}'
    elif kind == 'margin_move':
        result = (a / b - values[2] / values[3]) * 100
        expr = '(current income / current revenue - prior income / prior revenue) * 100'
        numeric = f'({x} / {y} - {labels[2]} / {labels[3]}) * 100'
    elif kind in ('gm_lower', 'gm_upper'):
        sign = -1 if kind == 'gm_lower' else 1
        op = '-' if sign == -1 else '+'
        result, expr, numeric = a+sign*b/100, f'margin midpoint {op} basis points / 100', f'{x} {op} {y} / 100'
    else:
        raise AssertionError(kind)
    src_ids = list(dict.fromkeys(s for k in keys for s in source_ids(k)))
    result_row = {'id': key, 'metric': metric, 'period': period, 'segment': segment,
                  'value': round(result, 8), 'unit': unit,
                  'source': [sources[s] for s in src_ids], 'status': 'calc',
                  'formula': {'expression': expr, 'numerical_expression': numeric,
                              'inputs': [{'id': k, 'metric': data[k]['metric'], 'period': data[k]['period'],
                                          'value': val(k), 'unit': data[k]['unit']} for k in keys]},
                  'notes': notes}
    assert replace or key not in data, key
    derived.append(result_row)
    data[key] = result_row
    checks.append({'check': 'derived_numeric_' + key, 'passed': True,
                   'expression': numeric, 'result_unrounded': result,
                   'stored_value': result_row['value'], 'unit': unit})
    return result_row

# Explicit arithmetic selection: no formula from the input is evaluated as code.
for row in rows:
    if row['status'] != 'calc':
        continue
    key = row['id']
    if key.startswith('inventory_days_'):
        kind = 'days'
    elif key in ('q4_revenue_guidance_low', 'q1fy27_revenue_low'):
        kind = 'lower'
    elif key in ('q4_revenue_guidance_high', 'q1fy27_revenue_high'):
        kind = 'upper'
    elif key == 'q4_revenue_beat_pct':
        kind = 'growth'
    elif key.startswith(('all_other_bridge_', 'q4_gaap_gm_delta', 'q4_ng_gm_delta', 'q4_gaap_opex_delta', 'q4_ng_opex_delta')) or key in ('q4_revenue_beat_amount', 'q4_actual_other_ex_equity'):
        kind = 'diff'
    elif key.startswith(('cash_capex_total_', 'cash_capital_return_')) or key == 'groq_total_consideration':
        kind = 'sum'
    elif key.startswith(('rd_pct_', 'operating_margin_', 'net_margin_', 'cn_margin_', 'graphics_margin_', 'fcf_conversion_', 'capital_return_fcf_')) or key in ('h20_initial_charge_annual_pts', 'q4_gaap_etr'):
        kind = 'ratio'
    else:
        raise AssertionError('Unverified input calc: ' + key)
    original_value = row['value']
    result = calculate(key, row['metric'], row['formula']['inputs'], kind, row['unit'], row['period'], row['segment'],
                       'Independently recalculated from financials.md. ' + row['notes'], replace=True)
    difference = result['value'] - original_value
    passed = abs(difference) <= 1e-7
    calc_validation.append({'id': key, 'input_value': original_value, 'recomputed': result['value'],
                            'difference': difference, 'tolerance': 1e-7, 'passed': passed,
                            'verification': 'mechanically verified from numerical input rows',
                            'formula': result['formula'], 'source': result['source']})
    assert passed, calc_validation[-1]
assert len(calc_validation) == 36

growths = [('revenue', 'Revenue'), ('cost_revenue', 'Cost of revenue'), ('gross_profit', 'Gross profit'),
           ('operating_income', 'Operating income'), ('net_income', 'Net income'), ('opex', 'Operating expenses'),
           ('rd', 'R&D'), ('sga', 'SG&A'), ('diluted_eps', 'Diluted EPS'), ('diluted_shares', 'Diluted shares'),
           ('non_gaap_oi', 'Non-GAAP operating income'), ('non_gaap_net_income', 'Non-GAAP net income'),
           ('inventory', 'Ending inventory'), ('cfo', 'Operating cash flow'), ('fcf', 'Company-defined free cash flow')]
for prefix, label in growths:
    calculate(prefix+'_growth', label+' growth', [prefix+'_fy26', prefix+'_fy25'], 'growth', '%')

for prefix, label in [('gaap_gm', 'GAAP gross-margin movement'), ('non_gaap_gm', 'Non-GAAP gross-margin movement'),
                      ('rd_pct', 'R&D/revenue movement'), ('effective_tax', 'Reported effective-tax-rate movement'),
                      ('inventory_net_gm_impact', 'Incremental net inventory/provision margin effect'),
                      ('fcf_conversion', 'FCF/net-income conversion movement'),
                      ('capital_return_fcf', 'Capital returned/FCF movement')]:
    calculate(prefix+'_move', label, [prefix+'_fy26', prefix+'_fy25'], 'diff', 'percentage points')
for prefix, income, revenue, segment in [('operating_margin', 'operating_income', 'revenue', 'Consolidated'),
                                       ('net_margin', 'net_income', 'revenue', 'Consolidated'),
                                       ('cn_margin', 'cn_oi', 'cn_revenue', 'Compute & Networking'),
                                       ('graphics_margin', 'graphics_oi', 'graphics_revenue', 'Graphics')]:
    calculate(prefix+'_move', 'Operating-margin movement' if prefix != 'net_margin' else 'Net-margin movement',
              [income+'_fy26', revenue+'_fy26', income+'_fy25', revenue+'_fy25'], 'margin_move', 'percentage points', segment=segment)
calculate('inventory_days_move', 'Ending-inventory days movement', ['inventory_days_fy26','inventory_days_fy25'], 'diff', 'days',
          notes='Ending balance convention; 365 multiplier as specified by skill, not average-inventory DIO.')
for prefix in ('operating_income','total_other_income','income_tax','net_income'):
    calculate(prefix+'_change', data[prefix+'_fy26']['metric']+' absolute change', [prefix+'_fy26',prefix+'_fy25'], 'diff', 'USD million')
calculate('net_vs_operating_growth_gap', 'Net-income growth less operating-income growth', ['net_income_growth','operating_income_growth'], 'diff', 'percentage points',
          notes='Difference between growth rates; not a margin movement.')
for year in ('fy26','fy25'):
    calculate('fcf_recomputed_'+year, 'Company-definition FCF recomputation', ['cfo_'+year,'capex_purchases_'+year,'capex_principal_'+year], 'fcf','USD million',
              period='FY2026' if year == 'fy26' else 'FY2025', notes='Excludes equity-investment purchases and separately classified Groq payment.')
for prefix, label, segment in [('cn_revenue','Compute & Networking revenue','Compute & Networking'),
                               ('graphics_revenue','Graphics revenue','Graphics'),
                               ('dc_revenue','Data Center revenue','End market'),
                               ('dc_compute','Data Center Compute revenue','Data Center subcategory'),
                               ('dc_networking','Data Center Networking revenue','Data Center subcategory'),
                               ('gaming','Gaming revenue','End market'), ('proviz','Professional Visualization revenue','End market'),
                               ('automotive','Automotive revenue','End market'), ('oem_other','OEM and Other revenue','End market')]:
    calculate(prefix+'_growth', label+' growth', [prefix+'_fy26',prefix+'_fy25'], 'growth','%',segment=segment)
for year in ('fy26','fy25'):
    calculate('dc_share_'+year, 'Data Center share of revenue', ['dc_revenue_'+year, 'revenue_'+year], 'ratio','%',
              period='FY2026' if year == 'fy26' else 'FY2025', segment='End market')
calculate('largest_direct_share_move','Largest disclosed direct-customer share movement',['direct_largest_fy26','direct_largest_fy25'],'diff','percentage points',
          segment='Primarily Compute & Networking', notes='Ranked share change only; anonymous identities do not establish the same customer in both years.')
calculate('top_two_direct_fy26','Two disclosed direct-customer shares combined',['direct_largest_fy26','direct_second_fy26'],'sum','%',period='FY2026',
          segment='Primarily Compute & Networking', notes='Two different direct customers. Do not add indirect or accounts-receivable shares.')
for geo in ('china','us'):
    calculate('geo_'+geo+'_growth','Customer-HQ '+geo.upper()+' revenue growth',['geo_'+geo+'_fy26','geo_'+geo+'_fy25'],'growth','%',
              segment='Customer headquarters geography',notes='FY2025 recast to the FY2026 headquarters basis; not end-use geography.')
    for year in ('fy26','fy25'):
        calculate('geo_'+geo+'_share_'+year,'Customer-HQ '+geo.upper()+' share of revenue',['geo_'+geo+'_'+year,'revenue_'+year], 'ratio','%',
                  period='FY2026' if year == 'fy26' else 'FY2025',segment='Customer headquarters geography')
    calculate('geo_'+geo+'_share_move','Customer-HQ '+geo.upper()+' revenue-share movement',
              ['geo_'+geo+'_fy26','revenue_fy26','geo_'+geo+'_fy25','revenue_fy25'],'margin_move','percentage points',segment='Customer headquarters geography',
              notes='Share change, not margin; generic ratio-difference calculation. Headquarters basis, FY2025 recast.')
calculate('q4_revenue_above_upper','Q4 revenue above guidance upper bound',['revenue_q4fy26','q4_revenue_guidance_high'],'diff','USD million',
          period='Q4 FY2026 actual vs 2025-11-19 guidance')
for basis, actual, guide in [('gaap','gaap_gm_q4fy26','q4_guidance_gaap_gm'),('ng','non_gaap_gm_q4fy26','q4_guidance_ng_gm')]:
    for side in ('lower','upper'):
        calculate('q4_'+basis+'_gm_'+side,'Q4 '+basis+' gross-margin guidance '+side,[guide,'q4_guidance_gm_tolerance'],'gm_'+side,'%',
                  period='Q4 FY2026 guidance issued 2025-11-19')
calculate('q4_other_adjustments','Other adjustments between equity-excluded GAAP and non-GAAP other income',
          ['q4_actual_ng_other_income','q4_actual_other_ex_equity'],'diff','USD million',period='Q4 FY2026')
calculate('q1fy27_implied_revenue_growth','Historical Q1 FY2027 guidance midpoint vs Q4 FY2026 actual',
          ['q1fy27_guidance_revenue','revenue_q4fy26'],'growth','%',period='Q1 FY2027 guidance issued 2026-02-25 vs Q4 FY2026 actual',
          notes='Historical outlook comparison, not actual sequential growth or current guidance.')
calculate('q1fy27_gaap_gm_move','Historical Q1 FY2027 GAAP margin midpoint vs Q4 FY2026 actual',
          ['q1fy27_guidance_gaap_gm','gaap_gm_q4fy26'],'diff','percentage points',period='Q1 FY2027 guidance issued 2026-02-25 vs Q4 FY2026 actual')

def check(name, actual, expected, tolerance=0, notes=''):
    passed = abs(actual-expected) <= tolerance
    checks.append({'check':name,'actual':actual,'expected':expected,'difference':actual-expected,
                   'tolerance':tolerance,'passed':passed,'notes':notes})
    assert passed, checks[-1]

for year in ('fy26','fy25'):
    check('fcf_definition_'+year,val('fcf_recomputed_'+year),val('fcf_'+year))
    check('revenue_segments_'+year,val('cn_revenue_'+year)+val('graphics_revenue_'+year),val('revenue_'+year))
    check('end_markets_'+year,sum(val(p+'_'+year) for p in ('dc_revenue','gaming','proviz','automotive','oem_other')),val('revenue_'+year))
    check('dc_subtotal_'+year,val('dc_compute_'+year)+val('dc_networking_'+year),val('dc_revenue_'+year))
    check('operating_bridge_'+year,val('segment_oi_'+year)+sum(val(p+'_'+year) for p in ('sbc_bridge','unallocated_opex','acquisition_bridge')),val('operating_income_'+year))
    check('pretax_bridge_'+year,val('operating_income_'+year)+val('total_other_income_'+year),val('pretax_income_'+year))
    check('net_income_bridge_'+year,val('pretax_income_'+year)-val('income_tax_'+year),val('net_income_'+year))
    check('geography_'+year,sum(val('geo_'+p+'_'+year) for p in ('us','taiwan','china','other')),val('revenue_'+year))
    check('inventory_components_'+year,sum(val(p+'_'+year) for p in ('raw_materials','wip','finished_goods')),val('inventory_'+year))
check('net_income_change_bridge',val('operating_income_change')+val('total_other_income_change')-val('income_tax_change'),val('net_income_change'))
check('cloud_schedule',sum(val('cloud_due_'+str(y)) for y in range(2027,2032))+val('cloud_due_2032_and_thereafter'),val('cloud_commitments_fy26'))
for annual, quarter in [('revenue','revenue'),('gross_profit','gp'),('operating_income','oi'),('net_income','net_income'),('opex','opex')]:
    check('annual_quarters_'+annual,sum(val(quarter+'_q'+str(q)+'fy26') for q in range(1,5)),val(annual+'_fy26'))
check('annual_quarters_non_gaap_opex',sum(val('non_gaap_opex_q'+str(q)+'fy26') for q in range(1,5)),val('non_gaap_opex_fy26'),1,
      'Documented displayed-precision difference of USD 1 million; no false discrepancy or forced restatement.')
check('annual_inventory_provision_components_fy25',val('inventory_provision_fy25')+val('excess_purchase_expense_fy25'),
      val('inventory_and_commitment_provision_fy25'),100,'Components and total independently rounded to USD 0.1 billion; preserve reported figures.')

def f(key, places=2):
    return f'{val(key):,.{places}f}'

def calc(key, places=2):
    row = data[key]
    return f"**{f(key,places)} {row['unit']}** (calc: {row['formula']['numerical_expression']})"

def refs(*ids):
    return ' '.join('['+i+']' for i in ids)

annual_lines = []
for prefix, label in [('revenue','Revenue'),('cost_revenue','Cost of revenue'),('gross_profit','Gross profit'),
                      ('operating_income','Operating income'),('net_income','Net income'),('opex','Operating expenses'),('rd','R&D'),('sga','SG&A')]:
    annual_lines.append(f"| {label} | {f(prefix+'_fy25',0)} | {f(prefix+'_fy26',0)} | {calc(prefix+'_growth')} | [AR51] |")
platform_lines = []
for prefix,label in [('dc_revenue','Data Center total'),('dc_compute','↳ Compute'),('dc_networking','↳ Networking'),
                      ('gaming','Gaming'),('proviz','Professional Visualization'),('automotive','Automotive'),('oem_other','OEM and Other')]:
    platform_lines.append(f"| {label} | {f(prefix+'_fy25',0)} | {f(prefix+'_fy26',0)} | {calc(prefix+'_growth')} | [AR79] |")

body = f'''# NVIDIA FY2026 trends and decision points

Stage 2 analysis | Run date **2026-10-17**, America/Los_Angeles. Sole business input: `financials.md` (385 rows). FY2026 ended **2026-01-25**; FY2025 ended **2025-01-26**. Filing date: **2026-02-25** [AR51] [SEC_INDEX]. This is a historical annual-report snapshot. Q4 FY2026 is a historical actual; Q1 FY2027 is the outlook issued at that filing date, not the latest quarter or current outlook on the run date.

Amounts are **USD million** unless stated otherwise. Amount growth is `%`; changes in margins, shares and conversion ratios are **percentage points (pp)**. Every bold derived result is **calc**; its numerical formula is shown here or in the machine-readable ledger. Source IDs resolve to the full URL and exact locator below. No source documents or websites were read in this stage.

## 1. Revenue scale rose faster than operating profit; preserve small margin movements

| GAAP metric | FY2025 | FY2026 | YoY growth, formula with numerical inputs | Source |
|---|---:|---:|---|---|
{chr(10).join(annual_lines)}

| Ratio | FY2025 → FY2026 | Movement and calculation | Source |
|---|---|---|---|
| Reported GAAP gross margin | 75.0% → 71.1% | {calc('gaap_gm_move')} | [AR41] |
| Operating margin | {calc('operating_margin_fy25')} → {calc('operating_margin_fy26')} | {calc('operating_margin_move')} | [AR51] |
| Net margin | {calc('net_margin_fy25')} → {calc('net_margin_fy26')} | {calc('net_margin_move')} | [AR51] |
| R&D / revenue | {calc('rd_pct_fy25')} → {calc('rd_pct_fy26')} | {calc('rd_pct_move')} | [AR51] |
| Reported non-GAAP gross margin | 75.5% → 71.3% | {calc('non_gaap_gm_move')} | [Q4_RECON] |
| Reported effective tax rate | 13.3% → 15.1% | {calc('effective_tax_move')} | [AR42] |

Diluted EPS was **$4.90 vs $2.94**, {calc('diluted_eps_growth')}; diluted shares were **24,514 vs 24,804 million**, {calc('diluted_shares_growth')} [AR51]. The share count contributes to EPS growth but does not explain operating performance.

| Management's stated explanation | Independent interpretation | Unknown / limitation |
|---|---|---|
| Gross-margin decline reflects transition from Hopper HGX to Blackwell full-scale datacenter solutions and H20 charges [AR41]. R&D compensation/benefits rose 29%, and compute/infrastructure expense rose 79%; SG&A growth was primarily compensation/benefits [AR41] [AR42]. | Revenue grew faster than operating expenses, helping absorb part of the gross-margin decline. Operating margin still fell, and the **{f('net_margin_move',2)} pp** net-margin decline must not disappear through whole-point rounding (formula above). | No complete quantitative margin bridge or isolated Blackwell impact is disclosed. Do not assign the residual decline wholly to Blackwell. |

## 2. Inventory charges are material, overlapping, and partly reversed

Broad inventory/excess-purchase-obligation provisions were **7,200 vs 3,700**; releases were **1,500 vs 689**. These are rounded disclosures and the broad provisions already include H20 [AR41]. Management reports net margin effects of **−2.6 pp vs −2.3 pp**, an incremental **{f('inventory_net_gm_impact_move',2)} pp** headwind (calc: −2.6 − (−2.3)); this small change is material to a faithful bridge [AR41].

The annual narrative's **4,500** initial H20 charge equates to {calc('h20_initial_charge_annual_pts',4)} of annual revenue, **only as a scale illustration** [AR36] [AR51]. It is not the net annual H20 effect or a normalized margin. The more precise quarterly charge was **4,538 in Q1**, followed by a **180 release in Q2**; Q3/Q4 effects were described as insignificant, with exact amounts **not disclosed**, not zero [Q2_RECON] [Q4_RECON]. Do not add the H20 charge to the broad provisions.

Reported GAAP quarterly gross margins recovered **60.5% → 72.4% → 73.4% → 75.0%** from Q1 through Q4 [Q2_SUMMARY] [Q3_SUMMARY] [Q4_SUMMARY]. Standard non-GAAP Q1/Q2 margins were **61.0% / 72.7%**, while separately disclosed H20-adjusted non-GAAP margins were **71.3% / 72.3%** [Q2_RECON]. These are different measures; neither replaces annual GAAP margin.

**Interpretation:** inventory reserves and releases complicate quarter-to-quarter comparisons; later margin recovery does not establish that annual transition costs are fully quantified or permanently resolved. **Unknown:** exact net annual H20 effect and isolated Blackwell margin attribution [AR41] [Q4_RECON].

## 3. Investment gains helped net income outgrow operating income

Net-income growth exceeded operating-income growth by {calc('net_vs_operating_growth_gap')} (difference between growth rates, not a margin change) [AR51]. The absolute earnings bridge is fully reconciled:

| Component of FY2026 versus FY2025 net-income change | Numerical calculation | Source |
|---|---|---|
| Operating-income increase | {calc('operating_income_change',0)} | [AR51] |
| Total other-income increase | {calc('total_other_income_change',0)} | [AR51] |
| Less: income-tax increase | {calc('income_tax_change',0)} | [AR51] |
| Net-income increase | {calc('net_income_change',0)}; bridge: 48,934 + 8,490 − 10,237 = 47,187 | [AR51] |

Total other income rose to **11,063 from 2,573**, including other income, net of **9,022 vs 1,034** [AR51]. Management attributes the rise primarily to unrealized equity gains, including Intel stock [AR42]. The cash-flow statement reverses **8,918** of net equity gains from FY2026 earnings, versus **1,030** in FY2025 [AR55]. Public equity unrealized gains held at year end were approximately **6,600**; private unrealized gains were **2,369**, with **101** of impairments/unrealized losses [AR65] [AR67]. These differing precisions/scopes do not provide an exact full realized/unrealized bridge.

Non-GAAP operating income was **137,300 vs 86,789**, {calc('non_gaap_oi_growth')}; non-GAAP net income was **116,997 vs 74,265**, {calc('non_gaap_net_income_growth')} [Q4_RECON]. GAAP net income exceeded non-GAAP net income in FY2026, consistent with investment gains being excluded in the reconciliation; do not assume non-GAAP always increases profit.

| Management's stated explanation / facts | Independent interpretation | Unknown / limitation |
|---|---|---|
| Higher effective tax rate reflects lower tax benefits relative to pretax income. A **711** state deferred-tax valuation-allowance release benefited FY2026; the reconciliation identifies **48** of OBBBA tax expense [AR42] [AR75] [Q4_RECON]. | Investment marks and discrete tax effects complicate repeatability of reported earnings. Assess operating profit and cash conversion alongside net income. | Exact comprehensive realized/unrealized gain split is not disclosed. Do not create an after-tax adjusted earnings estimate without a supported tax allocation. FY2026 tax-disclosure categories differ from FY2025 [AR72] [AR73] [AR74]. |

## 4. Cash generation is strong, but conversion softened and FCF excludes major investments

| Cash measure | FY2025 | FY2026 | Change / interpretation | Source |
|---|---:|---:|---|---|
| Operating cash flow | 64,089 | 102,718 | {calc('cfo_growth')} growth | [AR55] |
| Company-defined FCF | {calc('fcf_recomputed_fy25',0)} | {calc('fcf_recomputed_fy26',0)} | {calc('fcf_growth')} growth | [AR55] [Q4_RECON] [Q4_MEASURES] |
| FCF / net income | {calc('fcf_conversion_fy25')} | {calc('fcf_conversion_fy26')} | {calc('fcf_conversion_move')} | [AR51] [Q4_RECON] |
| Cash repurchases + dividends | {calc('cash_capital_return_fy25',0)} | {calc('cash_capital_return_fy26',0)} | Cash repurchases are **33,706 / 40,086**, dividends **834 / 974** | [AR55] |
| Cash capital returned / FCF | {calc('capital_return_fcf_fy25')} | {calc('capital_return_fcf_fy26')} | {calc('capital_return_fcf_move')} | [AR55] [Q4_RECON] |

FCF subtracts PP&E/intangible purchases and related principal payments; it excludes **17,502** of private equity purchases and the **13,000** Groq payment, both separately classified investing outflows in FY2026 [AR55] [Q4_MEASURES]. Groq stated cash plus future consideration totals {calc('groq_total_consideration',0)}; the future **4,000** includes imputed interest, and no equity interests, products or customer contracts were purchased [AR61]. Do not label this total a cash outflow already paid.

Cash plus marketable securities totaled **62,556 vs 43,210** [AR42]. Public equity holdings of **17,726** include **12,886 already within marketable securities** and **4,840 in Other assets**; adding all public holdings to cash plus marketable securities double-counts assets. Short-term lock-up restrictions affected approximately **10,500**, and the **4,840** had a lock-up through December 2027 [AR65]. Remaining buyback authorization was **58,500** at year end [AR76]. Accounting repurchase cost (**40,388**) is distinct from cash repurchase payments (**40,086**) [AR54] [AR55].

**Management:** higher CFO reflects higher revenue; investing outflows increased with equity purchases and Groq [AR43]. **Interpretation:** capital return consumed a smaller portion of FCF, but FCF is not cash remaining after all investments and portfolio balances are not uniformly unrestricted cash. **Unknown:** a full counterparty-level funding/liquidity sensitivity is not disclosed.

## 5. Supply and customer concentration warrant a joint downside scenario

Ending inventory rose to **21,403 from 10,080**, {calc('inventory_growth')}, versus revenue growth of **{f('revenue_growth')}%** and cost-of-revenue growth of **{f('cost_revenue_growth')}%** (formulas in section 1) [AR53] [AR51]. Inventory days increased from {calc('inventory_days_fy25')} to {calc('inventory_days_fy26')}: {calc('inventory_days_move')} [AR53] [AR51]. This uses ending inventory divided by annual cost times **365**, per the KPI convention; it is not average-inventory DIO. Work in process was **8,822 vs 3,399**, and finished goods **8,774 vs 3,273** [AR67].

| Exposure, as of FY2026 year end unless stated | Sourced fact | Analytical treatment |
|---|---|---|
| Manufacturing/supply/capacity commitments | **95,200**; substantially all expected through FY2027 [AR70] | Manufacturing at datacenter scale and longer ordering horizons are management's explanation. FY2025 comparable is not disclosed; no verified commitment-growth percentage. Some agreements can be adjusted before firm orders, potentially with costs. |
| Cloud services | **27,000** multi-year commitments, including **7,000** scheduled FY2027 [AR70] | Supports R&D. Capacity reduction/termination/sale can reduce commitments. Schedule is future contractual payments, not current-period spending. |
| Investment and other commitments | **11,400** investment commitments; **3,400** other commitments [AR70] | Investment commitments have contingencies. Do not add unlike measures into a debt total. |
| Facility guarantees and escrow | **3,500** maximum gross exposure; partner escrow **712**; terms **5–7 years** [AR69] | In exchange for warrants; escrow mitigates contingent exposure. Do not present gross exposure less escrow as recognized net debt or expected loss. |
| Future leases not yet commenced | **22,700**, expected to commence FY2027–FY2030 [AR79] | Distinct from recognized lease liabilities and from the other commitment categories. |
| Direct-customer revenue | FY2026 **22% and 14%**; FY2025 **12%, 11%, 11%** [AR78] | FY2026 two-customer total: {calc('top_two_direct_fy26',0)}. Largest-ranked share rose {calc('largest_direct_share_move',0)}; identities are anonymous, so this is not the same customer's growth. |
| Indirect and receivables concentration | Some individual indirect customers at least **10%**; exact shares not disclosed [AR41]. FY2026 receivables shares **25%, 18%, 13%** [AR67] | Direct, indirect and receivables denominators differ; do not sum them or infer identities. |

Management says private companies/funds include AI model makers that purchase NVIDIA products directly or through cloud service providers [AR37]. The **22,251** non-marketable equity balance, **17,502** annual purchases, **11,400** investment commitments and **3,500** guarantees measure different things [AR53] [AR55] [AR70] [AR69]. **Interpretation:** overlapping customer, investment and capacity relationships create correlated exposure to a demand or financing slowdown. The disclosures do **not** establish artificial/circular revenue. **Unknowns:** customer-level overlap, funded demand, exact prepaid-supply balance, prior-year commitment comparisons, and infrastructure-fund-only commitments. The OpenAI transaction was still being finalized at the filing date, with amount not disclosed and no assurance of completion [AR44].

## 6. Reportable segments and end markets answer different questions

| Reportable segment | Revenue FY2025 → FY2026 | Growth | Segment operating margin FY2025 → FY2026 | Movement | Source |
|---|---|---|---|---|---|
| Compute & Networking | 116,193 → 193,479 | {calc('cn_revenue_growth')} | {calc('cn_margin_fy25')} → {calc('cn_margin_fy26')} | {calc('cn_margin_move')} | [AR77] |
| Graphics | 14,304 → 22,459 | {calc('graphics_revenue_growth')} | {calc('graphics_margin_fy25')} → {calc('graphics_margin_fy26')} | {calc('graphics_margin_move')} | [AR77] |

Total segment operating income was **139,297** in FY2026 and **87,960** in FY2025 [AR77]. The aggregate unallocated bridge was {calc('all_other_bridge_fy26',0)} and {calc('all_other_bridge_fy25',0)}, respectively [AR51] [AR78]. FY2026 bridge components were **−6,386** SBC, **−1,997** unallocated operating expense, and **−527** acquisition/other costs [AR78]. This calculated aggregate is an analytical “All Other equivalent,” not a third segment or a separately reported line; segment expenses and margins exclude selected corporate costs.

| End market / subcategory | FY2025 revenue | FY2026 revenue | Growth and numerical formula | Source |
|---|---:|---:|---|---|
{chr(10).join(platform_lines)}

Data Center represented {calc('dc_share_fy26')} of FY2026 revenue versus {calc('dc_share_fy25')} [AR79] [AR51]. **Interpretation:** platform dependence is high and Networking grew faster than Compute, while Graphics segment profitability improved. **Boundary:** Data Center is not Compute & Networking; its Compute and Networking subcategories add to Data Center, not on top of it. These are separate reporting views and cannot be combined into one revenue total.

## 7. Geography must use the recast headquarters basis

| Headquarters-based geography | FY2025 → FY2026 revenue | Growth / shares | Source |
|---|---|---|---|
| United States | 77,482 → 149,617 | Growth {calc('geo_us_growth')}; shares {calc('geo_us_share_fy25')} → {calc('geo_us_share_fy26')}; {calc('geo_us_share_move')} | [AR78] [AR51] |
| China, including Hong Kong | 25,048 → 19,677 | Growth {calc('geo_china_growth')}; shares {calc('geo_china_share_fy25')} → {calc('geo_china_share_fy26')}; {calc('geo_china_share_move')} | [AR78] [AR51] |
| Taiwan | 23,600 → 42,345 | Company estimates **76% of Taiwan-headquartered Data Center revenue** is attributable to US/Europe end customers; denominator is not all Taiwan revenue. | [AR78] |

The company changed to direct-customer headquarters geography in Q3 FY2026 and recast the prior year [AR78]. Annual billing-location revenue is **not disclosed** in the input. Headquarters is not shipping, deployment or end-use location. **Interpretation:** the China-HQ decline is relevant alongside export restrictions, but does not quantify the export-control effect on worldwide end demand. H20 revenue under August 2025 licenses was **60** in FY2026; no revenue under the February 2026 H200 program had been generated at filing [AR36]. A geographic shift alone is not a causal revenue bridge.

## 8. Historical execution beat revenue guidance; FY2027 non-GAAP comparisons change

Q4 FY2026 guidance was issued **2025-11-19** and actuals **2026-02-25** [Q3_OUTLOOK] [Q4_SUMMARY].

| Measure | Prior Q4 FY2026 guidance | Q4 FY2026 actual and variance | Assessment |
|---|---|---|---|
| Revenue | **65,000 ±2%**; lower {calc('q4_revenue_guidance_low',0)}, upper {calc('q4_revenue_guidance_high',0)} [Q3_OUTLOOK] | **68,127**; midpoint beat {calc('q4_revenue_beat_pct')}, or {calc('q4_revenue_beat_amount',0)}; above upper bound {calc('q4_revenue_above_upper',0)} [Q4_SUMMARY] | Above midpoint and range. |
| GAAP gross margin | **74.8% ±50 basis points**; bounds {calc('q4_gaap_gm_lower')} / {calc('q4_gaap_gm_upper')} [Q3_OUTLOOK] | **75.0%**, {calc('q4_gaap_gm_delta')} [Q4_SUMMARY] | Above midpoint, within band; preserve the 0.20 pp movement. |
| Non-GAAP gross margin | **75.0% ±50 basis points**; bounds {calc('q4_ng_gm_lower')} / {calc('q4_ng_gm_upper')} [Q3_OUTLOOK] | **75.2%**, {calc('q4_ng_gm_delta')} [Q4_SUMMARY] | Above midpoint, within band. FY2026 basis excludes SBC but includes H20. |
| GAAP / non-GAAP opex | **6,650 / 5,000** [Q3_OUTLOOK_RECON] | **6,794 / 5,102**; over guidance {calc('q4_gaap_opex_delta',0)} / {calc('q4_ng_opex_delta',0)} [Q4_SUMMARY] | Use precise table 6,650, not the approximately 6,700 narrative. |
| Other income | Approximately **500**, excluding equity gains/losses [Q3_OUTLOOK] | GAAP **6,098** less equity gains **5,491** = {calc('q4_actual_other_ex_equity',0)}; non-GAAP **620**, with {calc('q4_other_adjustments',0)} of other adjustments [Q4_RECON] | The 6,098 GAAP total is not comparable with equity-excluded guidance. |
| Effective tax rate | **17% ±1 pp**, excluding discrete items [Q3_OUTLOOK] | {calc('q4_gaap_etr')} [Q4_INCOME] | Actual includes discrete items; not a clean beat/miss comparison. |

The **historical Q1 FY2027 outlook issued 2026-02-25** was revenue **78,000 ±2%**, or {calc('q1fy27_revenue_low',0)} to {calc('q1fy27_revenue_high',0)}, assuming **zero China Data Center compute revenue** [Q4_OUTLOOK]. Midpoint versus Q4 actual implies {calc('q1fy27_implied_revenue_growth')}; this is an outlook comparison, not realized growth. GAAP/non-GAAP gross-margin midpoints were **74.9% / 75.0%**, each ±50 basis points; GAAP midpoint versus Q4 actual is {calc('q1fy27_gaap_gm_move')} [Q4_OUTLOOK] [Q4_SUMMARY].

GAAP/non-GAAP opex outlook was **7,700 / 7,500**. Starting FY2027, non-GAAP includes SBC; both opex measures include **1,900** of SBC, and margin guidance includes **0.1 pp** of SBC [Q4_OUTLOOK_RECON]. Do not compute like-for-like non-GAAP growth versus FY2026 without a restated bridge. The **17%–19%** tax range is for **full FY2027**, not Q1 alone. Q1-specific tax rate and other-income guidance are **not disclosed** [Q4_OUTLOOK].

## Board handoff priorities and unresolved questions

The decision-relevant themes are scale versus margin, investment-driven earnings quality, cash conversion versus broader cash deployment, concentrated customers and supply exposure, and historical execution/outlook comparability. The tables above supply both the facts and calculation inputs for a one-page summary.

| Risk for the Board to assess | Management question grounded in the evidence |
|---|---|
| Inventory/capacity commitments could be exposed if concentrated demand slows [AR53] [AR70] [AR78]. | What demand-downside scenario, cancellation rights and inventory-reserve bridge support the 95,200 supply commitments and 21,403 inventory balance? |
| Equity-investment marks and linked customer/partner financing expose earnings and liquidity to a common AI-market shock [AR37] [AR42] [AR65] [AR69]. | What is the counterparty-level overlap among sales, equity holdings, investment commitments and facility guarantees, and how much exposure remains after contractual protection? |
| Export controls and changing measurement bases can obscure operating progress [AR36] [AR41] [AR78] [Q4_OUTLOOK_RECON]. | Can management provide a quantified margin bridge and a consistent FY2026-to-FY2027 non-GAAP bridge including SBC, while separating export effects from headquarters-geography changes? |

No amount is estimated for an absent disclosure; no “insignificant” amount is replaced by zero. Non-GAAP data include H20 unless the separately H20-adjusted measure is explicitly named. The exact annual H20 net charge and isolated Blackwell effect remain not disclosed. FY2025 headquarters geography was recast; equity presentation and prospective tax-disclosure changes are not a profit restatement [AR56] [AR72] [AR78]. Share/per-share values reflect the prior ten-for-one split [AR33].

## Calculation validation and precision

All **36 existing calc rows** from the sole input were independently recalculated from their numerical inputs, with absolute tolerance **0.0000001** in the row's unit; **36 passed**, none were skipped or only narratively verified. The ledger below contains those recalculations plus new trend calculations. Additional checks reconcile segment revenue/profit, end markets, geography, inventory components, the net-income bridge, annual/quarterly GAAP totals, FCF and the cloud-payment schedule.

The disclosed quarterly non-GAAP opex figures sum to **16,695** (3,583 + 3,795 + 4,215 + 5,102), versus annual **16,694**: a **1** difference (16,695 − 16,694) at displayed million-dollar precision, preserved as a limitation rather than reported as an error [Q2_SUMMARY] [Q3_SUMMARY] [Q4_ANNUAL]. FY2025 rounded inventory provision components **1,600 + 2,000 = 3,600**, versus rounded broad total **3,700**; independent rounding explains why they should not be forced to agree [AR41] [AR67] [AR68]. Margin calculations use annual income/revenue; rounded quarterly margins are not averaged. Underlying source accuracy is inherited from the supplied extraction and is not independently source-verified in this isolated stage.

## Derived metric ledger

Each row is `status: calc`. `formula.inputs` embeds numerical values and units, so no other business file is needed to recompute it. `source` uses IDs resolved by the complete official URLs and exact locators in this file's source references below. Values are stored to eight decimal places; prose rounds only for readability and retains movements below 0.5 pp.

```json
'''

# Keep the human-readable section concise relative to the 385-row input;
# include only the analysis and derived rows, not a duplicate raw dataset.
ledger = []
for row in derived:
    item = dict(row)
    item['source'] = ';'.join(s['id'] for s in row['source'])
    item['formula'] = dict(row['formula'])
    item['formula']['inputs'] = [{k: inp[k] for k in ('id','value','unit')} for inp in row['formula']['inputs']]
    ledger.append(item)
body += '[\n' + ',\n'.join(json.dumps(row,ensure_ascii=False,separators=(',',':')) for row in ledger) + '\n]\n```\n\n## Source references carried from financials.md\n\n'
used = set(re.findall(r'\[([A-Z0-9_]+)\]', body))
used.update(s['id'] for r in derived for s in r['source'])
for sid, source in sources.items():
    if sid in used:
        body += f"[{sid}]: {source['url']} \"{source['locator']}\"\n"
assert used.issubset(sources), sorted(used-set(sources))
assert len({r['id'] for r in derived}) == len(derived)
assert len(re.findall(r'```json',body)) == 1
assert all(r['status']=='calc' and r['formula']['inputs'] and r['formula']['numerical_expression'] for r in derived)

output = ROOT/'trends.md'
evidence = ROOT/'evidence'/'stage2-validation.json'
output.write_text(body,encoding='utf-8',newline='\n')
# Only read the newly owned artifact to verify the exact serialization on disk.
saved = output.read_text(encoding='utf-8')
saved_rows = json.loads(re.search(r'```json\s*(\[.*?\])\s*```',saved,re.S).group(1))
assert saved == body and saved_rows == ledger
assert hashlib.sha256(INPUT.read_bytes()).hexdigest() == hashlib.sha256(raw).hexdigest()
report = {
    'stage':2,'status':'passed','client_run_date':'2026-10-17','client_timezone':'America/Los_Angeles',
    'validated_at_utc':datetime.now(timezone.utc).isoformat(),
    'business_input':{'path':str(INPUT),'sha256':hashlib.sha256(raw).hexdigest(),'rows':len(rows),'unchanged_during_stage':True},
    'source_isolation':{'business_inputs_read':[str(INPUT)],'other_business_inputs_read':[],
                        'instruction_only_skill':'C:/Users/h_min/repos/SNU_Agentic_AI_Lecture/Agentic_AI_Demos/demo4_annual_report_dashboard/plugin/skills/semis-annual-report-kpis/SKILL.md',
                        'no_web_or_source_document_reads':True,'no_stage1_script_or_evidence_reads':True,
                        'owned_artifact_readback':[str(output)]},
    'existing_calc_rows':len(calc_validation),'existing_calc_verified':sum(c['passed'] for c in calc_validation),
    'existing_calc_nonmechanically_verified':[], 'existing_calc_validation':calc_validation,
    'derived_metric_rows':len(derived),'checks':checks,'all_checks_passed':all(c['passed'] for c in checks),
    'source_locator_validation':{'all_input_source_ids_resolved':True,'all_output_sources_have_url_and_locator':True},
    'precision_limitations':[
        {'item':'Quarterly non-GAAP opex vs annual','quarter_sum':16695,'annual':16694,'difference':1,'unit':'USD million','decision':'Keep both reported figures; displayed precision limitation, not a financial discrepancy.'},
        {'item':'FY2025 inventory/excess-obligation provision components','component_sum':3600,'broad_total':3700,'unit':'USD million','decision':'Values independently rounded to 0.1 billion; do not force equality.'},
        {'item':'GAAP annual GM','decision':'Reported 71.1%/75.0% used for reported movement; exact annual ratios used for operating/net margins; no unweighted quarterly average.'}],
    'genuine_challenges_and_decisions':[
        {'challenge':'Initial parent shorthand run/ was interpreted as an extra directory; file did not exist there.','decision':'Parent confirmed run root; read only the intended financials.md business file.'},
        {'challenge':'Inline Python through cmd -c failed shell quoting without reading files.','decision':'Used Get-Content for permitted reads, then a dedicated owned Python script for reproducible analysis.'},
        {'challenge':'Full input display was truncated.','decision':'Read bounded portions of the same file and inspected compact parsed rows; did not substitute another source.'},
        {'challenge':'Default sandbox denied saving the authorized stage2 artifacts.','decision':'Narrow escalation executed only the owned stage2 script; authorized outputs saved successfully.'},
        {'challenge':'H20 charge overlaps broad provisions and exact annual net effect is missing.','decision':'Preserve gross charge, releases and rounded precision; do not double-count or assign residual to Blackwell.'},
        {'challenge':'Anonymous customer order differs across years.','decision':'Compute largest-ranked share movement only; do not infer customer identities or continuity.'},
        {'challenge':'FCF excludes major investment outflows and repurchase cost differs from cash payments.','decision':'Follow company FCF definition including principal payments and cash-flow-basis capital return.'},
        {'challenge':'HQ geography recast, non-GAAP SBC change and historical guidance have different bases.','decision':'Use recast HQ comparatives; label FY2027 outlook historical and non-GAAP comparison break.'},
        {'challenge':'Supply/guarantee prior-year comparatives and prepaid-supply balance missing.','decision':'No growth estimate or zero substitution; describe separate exposure types without a circularity accusation.'}],
    'limitations':['No independent verification of original source documents: stage limited to financials.md.',
                   'Qualitative management explanations and missing disclosures are assessed from input text, not mechanically proven.'],
    'outputs':{'trends':str(output),'script':str(Path(__file__).resolve()),'evidence':str(evidence)},
    'save_verified':True
}
evidence.parent.mkdir(parents=True,exist_ok=True)
evidence.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
assert json.loads(evidence.read_text(encoding='utf-8'))['save_verified']
print(json.dumps({'saved':str(output),'bytes':len(body.encode('utf-8')),'input_sha256':report['business_input']['sha256'],
                  'existing_calc_verified':len(calc_validation),'derived_rows':len(derived),'checks':len(checks),
                  'all_checks_passed':report['all_checks_passed'],'evidence':str(evidence)},indent=2))
