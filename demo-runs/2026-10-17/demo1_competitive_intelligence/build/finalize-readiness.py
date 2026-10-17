from pathlib import Path
import json,zipfile,hashlib,xml.etree.ElementTree as E
from datetime import datetime,timezone
run=Path(__file__).resolve().parents[1]
receipt=json.loads((run/'build/IC-pack.validation.json').read_text(encoding='utf-8'))
assert receipt['packageIntegrity']['status']=='pass'
assert receipt['presentationLayout']['finding_count']==0
assert receipt['firstPartyImport']['passed']
assert receipt['presentationLayout']['warning_count']==0
assert (run/'IC-pack.pptx').exists()
sha=hashlib.sha256((run/'IC-pack.pptx').read_bytes()).hexdigest()
assert sha==receipt['finalSha256']
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
with zipfile.ZipFile(run/'IC-pack.pptx') as z:
 slides=[x for x in z.namelist() if x.startswith('ppt/slides/slide') and x.endswith('.xml')]
 assert len(slides)==3
 assert z.testzip() is None
 notes='\n'.join(' '.join(e.text or '' for e in E.fromstring(z.read(x)).findall('.//a:t',ns)) for x in z.namelist() if x.startswith('ppt/notesSlides/notesSlide') and x.endswith('.xml'))
 assert 'live.euronext.com/en/financial-news/softbank-talks' in notes
 assert 'https://www.pi.website/blog/api-beta' in notes
for f in ['slide-1.png','slide-2.png','slide-3.png','matrix.png','matrix-sources.png','landscape-left.png','landscape-right.png']:
 assert (run/'build'/f).exists()
profiles=json.loads((run/'build/profile-checks.json').read_text())
xlsx=json.loads((run/'build/saved-xlsx-checks.json').read_text())
outputs=['RUNBOOK.md','IC-pack.pptx','research/summary.md','research/competitor-matrix.xlsx','research/evidence-checks.md','research/handoffs.md']+[f'research/{s}.md' for s in ['figure-ai','physical-intelligence','skild-ai','agility-robotics','1x-technologies']]
for p in outputs:assert (run/p).is_file(),p
corrections=[
'Use 2026-10-17 as this run cutoff, replacing slide 24 dated 2026-10-16.',
'Figure $39B is a September 2025 historical financing baseline outside the window; output at BotQ is not paid customer deliveries. Nscale compute commitment is not funding proceeds.',
'PI revenue is not disclosed, not established as zero or pre-revenue. $5.6B is a dated investor baseline with unspecified valuation basis; later financing records conflict.',
'Skild >$100M ARR and 60+ customers are company-reported. January revenue is not a comparable ARR starting point. Acquired robotics operations make model-only incomplete.',
'Agility $2.5B value and SPAC proceeds are proposed. November 2 is a scheduled vote, not a completed listing. FY2025 sales and conditional multi-year orders are not current ARR.',
'Digit 5 availability targets 2027. Capacity and operating-hour claims are not actual new-robot delivery counts.',
'1X ~$6B is reported acquisition talks, not a closed financing. Capacity and potential EQT rollout are not deliveries or firm orders. External deliveries remain unverified.',
'Remove unsupported claims that model firms raised faster or that a SPAC vote necessarily sets a public-market price.',
'Momentum is analyst judgment. This run treats Figure as gaining on milestones and 1X as holding pending delivery evidence.'
]
limitations=[
'Full Agility definitive SEC filing retrieval failed. $1.782M FY2025 sales is corroborated using primary indexed table text, not a full-file financial audit.',
'Exact current cumulative capital is unavailable for all five. Ratios remain Not comparable; no missing capital is treated as zero.',
'Reported acquisitions, proposed SPAC transactions and company-reported operational metrics remain explicitly qualified.',
'No native Excel or PowerPoint UI test, API product test, robot execution, physical delivery inspection or exhaustive legal docket review was performed.',
'Public-source research is bounded by the stated cutoff. Nondisclosure does not establish zero or absence.',
'Native font rendering is not verified in PowerPoint. Artifact Tool renders and the saved slide previews were visually reviewed.'
]
checks=[
{'name':'Independent fan-out and handoffs','status':'passed','evidence':'Five distinct company researchers in two batches; research/handoffs.md and per-company evidence JSON.'},
{'name':'Common five-heading profiles','status':'passed','evidence':'build/profile-checks.json: all five passed.'},
{'name':'Material fact spot-checks','status':'passed_with_limitations','evidence':str(sum(p['spot_checks'] for p in profiles))+' checks documented in research/evidence-checks.md, including reported/unconfirmed verdicts. Three additional coordinator checks in build/coordinator-source-checks.json.'},
{'name':'Workbook formula recalculation and sensitivity','status':'passed','evidence':'build/workbook-checks.json; ages 17, 4, 18, 2, 52 days. Changed input tests and zero/blank guards passed; originals restored.'},
{'name':'Workbook saved package and errors','status':'passed','evidence':'build/saved-xlsx-checks.json verifies 10 formulas, cached values and typed numbers. build/workbook-error-scan.ndjson has zero error matches.'},
{'name':'Workbook visual review','status':'passed','evidence':'Matrix, source area and both Landscape sections rendered and reviewed in build/*.png; no clipped cells or formula errors observed.'},
{'name':'Three-slide package, layout and import','status':'passed','evidence':'build/IC-pack.validation.json: 3 slides, 2 native editable tables, 0 findings, 0 layout warnings, IBM Plex Sans font policy and first-party import passed.'},
{'name':'Slide visual review and citations','status':'passed','evidence':'All three rendered slide layouts reviewed. Subsequent notes-only revision adds complete primary/secondary source bibliography; saved PPTX notes checked for PI API and 1X reported transaction links.'},
{'name':'Final deck copied without alteration','status':'passed','evidence':'Final SHA256 matches validation receipt: '+sha},
{'name':'Native Office UI testing','status':'not_performed','evidence':'No native Excel or PowerPoint interaction is claimed.'},
{'name':'Scope preservation','status':'passed','evidence':'All created outputs and scripts remain in Demo 1 run folder. Supplied reference outputs and source lecture deck were only read. No recurring automation, publication or communications activated.'}
]
manifest={'demo':1,'title':'Competitive intelligence fan-out: five robotics startups','status':'ready','completed_at':datetime.now(timezone.utc).isoformat(),'outputs':outputs,'checks':checks,'limitations':limitations,'slide_corrections':corrections,'sources_as_of':{'research_window_start':'2025-10-17','research_window_end':'2026-10-17','prepared_date':'2026-10-17','timezone':'America/Los_Angeles','latest_dated_evidence_by_company':{p['company']:p['latest_evidence_date'] for p in profiles}},'artifact_hashes':{p:hashlib.sha256((run/p).read_bytes()).hexdigest() for p in outputs}}
(run/'readiness.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(run/'build/visual-review.md').write_text('# Visual review\n\nReviewed source slide 24, all three IC slide layouts, Matrix, Matrix source area and both halves of Landscape at readable scale. Tables, titles, notes and source qualifiers are legible. No clipping or overlap observed. Final notes-only update leaves layout unchanged. Native Office UI was not tested.\n',encoding='utf-8')
print(json.dumps({'status':manifest['status'],'outputs':len(outputs),'checks':len(checks),'deck_sha256':sha,'completed_at':manifest['completed_at']},indent=2))
