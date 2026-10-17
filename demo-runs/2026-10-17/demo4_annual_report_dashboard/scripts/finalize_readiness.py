from pathlib import Path
import json,re,hashlib,datetime
from zoneinfo import ZoneInfo
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1]
def read(name):return json.loads((R/name).read_text(encoding='utf-8-sig'))
def digest(name):return hashlib.sha256((R/name).read_bytes()).hexdigest()
checks=[]
def check(name,condition,evidence):
 checks.append(dict(name=name,status='pass' if condition else 'fail',evidence=evidence))
source=read('evidence/source-verification.json')
check('Official source hashes and four rendered source-page checks',all(x['status']=='pass' for x in source['checks']),'evidence/source-verification.json; inputs/sources.json')
s1=read('evidence/stage1-validation.json');s2=read('evidence/stage2-validation.json')
check('Stage1 financial reconciliations',s1['all_numeric_checks_passed'],f"{len(s1['checks'])} reconciliations; evidence/stage1-validation.json")
check('Stage2 numerical analysis',s2['all_checks_passed'] and s2['existing_calc_verified']==s2['existing_calc_rows'],f"{len(s2['checks'])} checks; all {s2['existing_calc_rows']} inherited calculations verified; evidence/stage2-validation.json")
s4=read('evidence/stage4-validation.json')
check('Stage4 numerical reconciliation and data preservation',all(x['passed'] for x in s4['arithmetic_checks']) and s4['original_arrays_unchanged_in_embedded_json'],f"{len(s4['arithmetic_checks'])} arithmetic checks; evidence/stage4-validation.json")
summary=(R/'exec-summary.md').read_text(encoding='utf-8')
sections={}
for label in ['5 headlines','3 risks','3 questions']:
 section=summary.split('## '+label+'\n',1)[1].split('\n## ',1)[0]
 sections[label]=len(re.findall(r'^\d+\. ',section,re.M))
check('Board summary structure',list(sections.values())==[5,3,3],sections)
summary_pages=len(PdfReader(R/'exec-summary.pdf').pages)
check('Board brief is one printed page',summary_pages==1,'exec-summary.pdf; evidence/summary-print-check.json; evidence/exec-summary-page.png')
browser=read('evidence/browser-tests.json')
check('Actual offline Chromium acceptance',browser['passed'],'evidence/browser-tests.json')
for c in browser['checks']:checks.append(c)
visual=read('evidence/visual-review.json')
check('Visual review of final screenshots and print pages',visual['passed'],'evidence/visual-review.json')
print_render=read('evidence/dashboard-print-render.json')
if visual['passed']:
 print_render['visual_review_pending']=False
 print_render['visual_review']='evidence/visual-review.json'
 (R/'evidence/dashboard-print-render.json').write_text(json.dumps(print_render,indent=2),encoding='utf-8')
pipeline=read('evidence/pipeline-log.json')
check('Four sequential isolated agent gates',len(pipeline['gates'])==4 and [g['stage'] for g in pipeline['gates']]==[1,2,3,4],'evidence/pipeline-log.json; per-stage validation evidence')
unchanged=all(digest(f['path'])==f['sha256'] for g in pipeline['gates'] for f in g['inputs']+[g['output']])
check('Handoff hashes remain unchanged',unchanged,'All gated inputs and outputs rehashed against pipeline-log.json')
outputs=['dashboard.html','financials.md','trends.md','exec-summary.md','exec-summary.pdf','RUNBOOK.md','inputs/10K-NVDA.pdf','inputs/sources.json','evidence/pipeline-log.json','evidence/source-verification.json','evidence/stage1-validation.json','evidence/stage2-validation.json','evidence/stage3-validation.json','evidence/stage4-validation.json','evidence/browser-tests.json','evidence/visual-review.json','evidence/dashboard-board.png','evidence/dashboard-cfo-graphics.png','evidence/dashboard-evidence-search.png','evidence/dashboard-mobile.png','evidence/dashboard-print.pdf','evidence/export-graphics-revenue.csv']
outputs += ['inputs/annual-report-pages.json','inputs/annual-report.txt','inputs/q2-release.html','inputs/q2-release.txt','inputs/q3-release.html','inputs/q3-release.txt','inputs/q4-release.html','inputs/q4-release.txt','inputs/filing-index.html','inputs/filing-index.txt','evidence/dashboard-performance.png','evidence/dashboard-outlook.png','evidence/dashboard-mobile-cards.png','evidence/browser-environment.json','evidence/summary-print-check.json','evidence/exec-summary-page.png']
outputs += ['scripts/'+n for n in ['acquire_sources.py','stage1_extract.py','stage2_analyze.py','build_dashboard.py','qa_sources.py','render_summary.cjs','test_dashboard.cjs','render_dashboard_print.py','record_pipeline.py','finalize_readiness.py']]
outputs += read('evidence/dashboard-print-render.json')['rendered_pages']
outputs += ['evidence/dashboard-print-render.json']
check('Required deliverables exist',all((R/n).is_file() and (R/n).stat().st_size>0 for n in outputs),outputs)
assert all(c['status']=='pass' for c in checks),json.dumps([c for c in checks if c['status']!='pass'])
runbook=(R/'RUNBOOK.md').read_text(encoding='utf-8')
runbook=runbook.replace('Status: final acceptance testing pending.','Status: ready for the lecture walkthrough.')
runbook=runbook.replace('the one-page printable Board brief, when final rendering passes.','the verified one-page printable Board brief.')
old='Final test results and exact commands will be added after acceptance. The scripts directory\ncontains source acquisition/extraction, staged generators, source checks and browser tests.\nThe HTML itself needs no installed dependency. Browser/PDF verification uses local Python,\nPoppler, Node, Playwright and an installed Chromium executable; see the environment evidence.'
new=f'''Acceptance passed. Stage 1: {len(s1['checks'])} financial reconciliations. Stage 2: {len(s2['checks'])} checks, including independent recomputation of all {s2['existing_calc_rows']} inherited calculations. The Board brief prints on one A4 page. The dashboard passed {len(browser['checks'])} browser checks with networking disabled, including role ordering, both segment filters, group-only labels, exact embedded-data equality, evidence search/sort, a real CSV download, print rendering and mobile width. Final screenshots and print pages were visually reviewed.

See `evidence/browser-tests.json`, `visual-review.json`, the four stage-validation files, and `pipeline-log.json`. The handoff log records each assigned input and output hash; later agents used isolated contexts. The PDF source checks include printed pp.41,51,53,77 (PDF129,139,141,165).

The HTML itself needs no installed dependency. These scripts reproduce and verify this archived FY2026 run; they are not a general extractor for a different filing. For a new period, use the four-agent prompt above and review fresh sources.

From this run directory in PowerShell, the bundled Python runtime can be selected explicitly:

```powershell
$demoPython = "$env:USERPROFILE/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe"
& $demoPython scripts/qa_sources.py
& $demoPython scripts/stage1_extract.py
& $demoPython scripts/stage2_analyze.py
& $demoPython scripts/build_dashboard.py
node scripts/render_summary.cjs
node scripts/test_dashboard.cjs
```

Source acquisition is preserved in `scripts/acquire_sources.py`. Run scripts against the archived input files to preserve this snapshot. Source acquisition needs internet and PDF/HTML parsing packages. Browser verification uses the locally installed Playwright package and Chromium executable recorded in `evidence/browser-environment.json` and `browser-tests.json`; those machine-specific paths may need adjustment elsewhere. Poppler renders PDFs to PNGs for visual review. The operating-system print dialog was not exercised; headless Chromium print media and generated PDF layout were checked.'''
assert old in runbook or 'Acceptance passed.' in runbook
if old in runbook:runbook=runbook.replace(old,new)
(R/'RUNBOOK.md').write_text(runbook,encoding='utf-8')
corrections=[]
section=runbook.split('## Lecture slide corrections\n',1)[1].split('\n## ',1)[0]
for line in section.splitlines():
 if line.startswith('- '):corrections.append(line[2:])
limitations=[
 'Historical FY2026 snapshot, not latest-quarter reporting or current guidance on 2026-10-17. Q1 FY2027 guidance is labeled as issued 2026-02-25.',
 'Not-disclosed entries are retained for missing comparatives and exact figures, including supply prepayments, prior-year commitments/guarantees, exact insignificant equity gains and isolated Blackwell margin attribution. No estimates or zero substitutions fill these gaps.',
 'Quarterly and earnings-release-only data cite archived official HTML headings and URLs rather than invented PDF pages.',
 'Headquarters geography is recast and differs from billing/end-use geography; platforms do not map one-to-one to reportable segments; consolidated-only metrics are explicitly labeled.',
 'PDF printed p.40 has corrupt extracted font encoding. Clean Note16 tables supply the corresponding segment figures; key source pages were separately rendered and visually inspected.',
 'Browser testing used headless Chromium with network disabled; native operating-system print dialog was not exercised. Browser-generated print PDF and screenshots were visually checked.',
 'The lecture deck was preserved. Corrections are documented in RUNBOOK.md; this run does not certify a 30-minute end-to-end generation time.'
]
ready=dict(demo='demo4_annual_report_dashboard',title='NVIDIA FY2026 annual report pipeline',status='ready',completed_at=datetime.datetime.now(ZoneInfo('America/Los_Angeles')).isoformat(),outputs=outputs,checks=checks,limitations=limitations,slide_corrections=corrections,sources_as_of={'retrieved_on':'2026-10-17','fiscal_year_end':'2026-01-25','comparative_fiscal_year_end':'2025-01-26','filing_date':'2026-02-25','historical_q1_fy2027_outlook_issued':'2026-02-25','timezone':'America/Los_Angeles','manifest':'inputs/sources.json'})
(R/'readiness.json').write_text(json.dumps(ready,indent=2),encoding='utf-8')
manifest={n:dict(sha256=digest(n),bytes=(R/n).stat().st_size) for n in outputs+['readiness.json']}
(R/'evidence/output-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps({'status':ready['status'],'completed_at':ready['completed_at'],'checks':len(checks),'outputs':len(outputs),'summary_pages':summary_pages,'dashboard_print_pages':len(PdfReader(R/'evidence/dashboard-print.pdf').pages)},indent=2))
