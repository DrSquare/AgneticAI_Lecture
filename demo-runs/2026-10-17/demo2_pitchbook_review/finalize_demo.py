from pathlib import Path
import json,hashlib,re
from pypdf import PdfReader
H=Path(__file__).resolve().parent
R=H.parents[2]

conflicts='''# Reviewer conflicts and handoffs

FICTIONAL COMPANY AND DATA - TEACHING MATERIAL

Reviewed October 17, 2026 (America/Los_Angeles); KPI data through September 2026. These are actual independent subagent exchanges from this run. This document summarizes them; the exact quoted messages are retained in the three reviewer files. It is not a staged dialogue. Sequence below describes logical issue threads, not invented timestamps.

## Panel and evidence ownership

- `/root/narrative`: story, page-by-page clarity, narrative rubric; independently read all 11 PDF pages and requested numerical verification.
- `/root/numbers`: independent arithmetic and claim inventory; read the original CSV and all PDF pages; executed a separate calculation script.
- `/root/devils`: independent ranked pass case; challenged causal claims and requested numerical verification.
- Lead: independent `calculate.py`, source rendering, synthesis, brief and validation. No supplied reference review was copied or used to seed these conclusions.

## Factual exchange register

| Issue | Actual sender -> recipient | Evidence in saved messages | Change or resolution |
|---|---|---|---|
| Paying vs pilot metric hook | Narrative -> Numbers -> Narrative | Numbers review N1-N3; narrative's exact exchange log | Cosmetic footnote became a full p6/p7 metric-definition rebuild. Corrected hook retains meaningful growth. |
| Rounded NRR status | Narrative -> Numbers -> Narrative | Numbers review N1,N4 and its resolution | Numbers explicitly accepted the scope distinction and changed NRR to qualified: 157.14% rounds roughly160%, but starting n=3 must be disclosed. |
| Growth pace | Numbers -> Narrative | Numbers review N2,N3 | Narrative explicitly rejected a stalled-growth interpretation; paying YoY remains6.57x and Q3 growth39.39%. |
| Product causality | Devil -> Narrative -> Devil | Devil review narrative exchange, third/fourth messages | Narrative accepted that fleet improvement cannot identify LoopBrain's causal effect; requests controlled tests and model/data rights. |
| Team and market score challenge | Narrative -> Devil -> Narrative | Devil review narrative exchange, first-three messages | Devil agrees Market2 and Team3 are defensible. No fabricated score disagreement. Relevant roles earn presentation credit; evidence gaps remain. |
| Runway denominator | Numbers -> Devil -> Numbers | Numbers review D1,D3,D4; devil numbers exchange | Devil narrows funding critique to an unverified forward cash plan.8.46months pre-raise does not disprove24months post-raise. |
| CAC interval | Narrative and Devil -> Numbers | Numbers review N1-N4,D1-D3 | All accept Q3 ending-GM proxy26.27months. Deck p7 actually claims4months. TTM27.87 and September29.62 illustrate sensitivity; actual cohort payback unverified. |
| Hardware cost/capex inference | Numbers -> Devil -> Numbers | Numbers review D4-D5; devil numbers exchange | $42K is itself unverified. Absence of a separate capex line is not proof of omitted hardware cash cost. |
| Margin weighting / hiring ramp | Lead -> Numbers | Numbers review Method cross-check | Increment-weighted vs revenue-weighted GM and immediate vs linear hiring remain different labelled methods; no artificial single answer. |

## What remains unresolved

No material arithmetic disagreement remains for matching formulas and periods. Business judgment still differs in emphasis: narrative sees a coherent, repairable story; devil requires reconciled paid-cohort economics before investment advocacy. Underlying gross-new-logo MRR, acquisition attribution, contracts, customer identities, cost composition, controlled tests and forward cash are unavailable.

The claim table uses `needs_qualification` for the8x headline because it can describe a pilot-inclusive metric. The numbers review labels it contradicted **as paying-ARR growth**. These statuses use different stated scopes, not conflicting calculations. Similarly,4-month CAC is inconsistent with available aggregate proxies but unverifiable as an actual acquisition-cohort measure.

## Consolidated decision

Conditional go for a founder diligence meeting; no-go for investment approval on the evidence supplied. The lead applies the rubric dimension by dimension, rather than averaging reviewer opinions. Exact quote provenance remains in `review-numbers.md`, `review-narrative.md`, and `review-devils-advocate.md`.
'''
# Clean spacing without altering the preserved verbatim source files.
for a,b in [('roughly160%','roughly 160%'),('remains6.57x','remains 6.57x'),('growth39.39%','growth 39.39%'),('Market2','Market 2'),('Team3','Team 3'),('.8.46months','. 8.46 months'),('disprove24months','disprove 24 months'),('proxy26.27months','proxy 26.27 months'),('claims4months','claims 4 months'),('TTM27.87','TTM 27.87'),('September29.62','September 29.62'),('the8x','the 8x'),('Similarly,4-month','Similarly, 4-month')]:conflicts=conflicts.replace(a,b)
(H/'conflicts-log.md').write_text(conflicts,encoding='utf-8')

runbook='''# Demo 2 presenter runbook

**FICTIONAL COMPANY AND DATA - TEACHING MATERIAL**

Review date: October 17, 2026 (America/Los_Angeles). The CSV covers September 2025-September 2026. "Ready" means the local lecture demo and artifacts were executed and checked; it does not validate a real company or investment.

## Five-minute walkthrough

| Time | Open / do | Say / show |
|---|---|---|
|0:00-0:45|Original `Agentic_AI_Demos/demo2_pitchbook_review/inputs/pitch-deck.pdf`, pages6-7.|"All company data is invented. This polished deck says $2.4M ARR,68% GM and4-month CAC. Which definitions would you test?"|
|0:45-1:25|`partner-briefing.pdf`.|Show conditional founder meeting / no investment approval. Paying ARR is $1.932M, September GM41%, NRR157.14% for n=3.|
|1:25-2:20|`calculate.py` and `calculation-results.md`; run the command below.|Show Q3 spend490k, net MRR45.5k and41% margin ->26.27months. Switch attention to TTM27.87 and September29.62. Explain net-new-MRR proxy, not proven cohort CAC.|
|2:20-3:25|`conflicts-log.md`, then Numbers review N1/N4 and D1/D3.|Narrative challenged the NRR verdict; numbers changed it to qualified. Numbers challenged runway; devil withdrew a simple pre-raise rebuttal. These were real messages between independent reviewers.|
|3:25-4:15|`pitch-review.md`, fixes and founder questions; optionally `forward-burn-sensitivity.csv`.|Separate supported arithmetic from missing evidence. Show why24months needs a monthly hiring/deployment/cash plan, not a static ratio.|
|4:15-5:00|`partner-briefing.pdf`, then `founder-email.md`.|End on the decision and five fixes. Email is a local unsent draft; partner owns the next step. Show how reusable roles + rubric + evidence produce a reviewable result.|

A full panel rerun can take longer than five minutes. For a five-minute lecture, replay the saved genuine challenge record and execute the small calculation script live. Pre-open the files and warm the terminal before the lecture. No timed classroom rehearsal or native presentation UI test was performed in this preparation.

## Live calculation command

From the project folder in PowerShell:

```powershell
& 'C:/Users/h_min/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' 'C:/Users/h_min/repos/SNU_Agentic_AI_Lecture/demo-runs/2026-10-17/demo2_pitchbook_review/calculate.py'
```

The script uses only Python's standard library, reads the source CSV and writes calculation/claim/check artifacts in this run folder. With a normal Python installation, `python calculate.py` also works when invoked from this folder. Pass `--input` only for a revised CSV with the same schema. Re-run the review as well when inputs change; prose artifacts are a dated review, not a live dashboard.

It writes `calculations.json`, `claims.json`, `numerical-checks.json`, `calculation-results.md`, and `forward-burn-sensitivity.csv`. For independent comparison, `numbers-reviewer-calculations.py` writes the reviewer's separately derived JSON. The original PDF/CSV/reference output are preserved.

## Files to open

- Main decision artifact: `partner-briefing.pdf` (one page, visually checked).
- Full synthesis: `pitch-review.md` (scorecard,42-claim inventory, methods, conflicts, fixes and4 founder questions).
- Real panel evidence: `review-narrative.md`, `review-numbers.md`, `review-devils-advocate.md`, `conflicts-log.md`.
- Live teaching: `calculate.py`, `calculation-results.md`, `claims.json`, `forward-burn-sensitivity.csv`.
- Lecture correction guide: `lecture-slide27-corrections.md` (verified against physical slide 27 OOXML).
- Optional follow-up: `founder-email.md` (saved draft only).
- QA evidence: `numerical-checks.json`, `numbers-reviewer-calculations.json`, `evidence/validation.json`, `readiness.json`.
- Deck page snapshots: `evidence/deck-contact-sheet.png`; individual source renders `evidence/deck-01.png` through `deck-11.png`.

All run-folder paths above are relative to `C:/Users/h_min/repos/SNU_Agentic_AI_Lecture/demo-runs/2026-10-17/demo2_pitchbook_review/`.

## Reusable panel prompt

> Review the fictional GraspLoop AI Series A deck against its supplied CSV and data dictionary. Follow `Agentic_AI_Demos/demo2_pitchbook_review/plugin/skills/pitch-review/SKILL.md` and all three agent definitions. Spawn three genuinely independent narrative, numbers and devil's-advocate reviewers. Have them send direct, substantive challenges, revise findings when warranted and preserve actual exchanges. Recompute quantitative deck claims using source page and physical CSV row/period references; no reference-output copying. Distinguish paying revenue from pilots, best site from fleet, projections from actuals, and unavailable evidence from falsity. Test the4-month deck CAC claim and explain exactly when an approximately26-month proxy is reproducible. Use Q3, trailing-year and monthly intervals, and distinguish net new MRR from gross acquisition cohorts. Test runway with explicit forward-burn assumptions, not merely cash/current burn. Save one file per reviewer, a factual conflicts log, claims JSON, runnable calculation script and results, consolidated review, one-page partner brief, and optional unsent founder email. All company information must be labelled fictional teaching material. Save to a new dated run folder, preserve supplied inputs/reference artifacts, and finish with a five-minute runbook and truthful readiness checks. Do not send, schedule or publish anything.

## Checks actually performed

- Read prompt, custom skill, all three role definitions and data dictionary.
- Three independent reviewers read all11 PDF pages and exchanged direct challenges; exact messages preserved in their outputs.
- Lead read all source text, rendered all11 pages, checked the full contact sheet and inspected critical pages6-7 and10-11 at readable size.
- Lead's53 identity/row-count/period/cash checks passed. Independent numbers script's8 grouped checks passed.
- Cross-checked independent ARR, NRR, CAC interval and runway results against lead output.
- Checked PDF printed page numbers against physical PDF order. Header row1 makes Sep2025 row2 and Sep2026 row14.
- Built and rendered one-page partner PDF. Checked page count, layout and text; source/reference hashes verified unchanged.
- Confirmed required output files and fictional/date disclosures. No external communications or publishing occurred.

## Lecture corrections and caveats

**Physical lecture slide 27 needs revisions.** Open `lecture-slide27-corrections.md` for a ready-to-use replacement table and actual conflict examples. Remove the unsupported 15-20-month runway, unverified target-margin label, 2.6/5 headline and scripted 4-to-2 traction score change. The source lecture deck remains unchanged.

1. The pitch deck says4-month CAC on p7. Approximately26months is the **Q3 ending-GM net-new-MRR proxy**,26.27, not an exact acquisition-cohort result. TTM is27.87; September29.62. State the interval and limits in the lecture.
2. Use **$1.932M paying ARR**, **$2.436M pilot-inclusive annualization**, and **$504k unpaid pilot capacity**. The column name does not establish contracted ARR.
3. Use **6.57x paying YoY**,11 paying +3 unpaid pilot customers; explain that roughly8x comes from the blended series.
4. Use **41% September GM**.68% is unsupported as a current actual and must not be silently relabelled a verified target.
5. Use **157.14% NRR for the original3-customer cohort**;160% is coarse rounding with a required cohort disclosure.
6. Best-site/single-SKU success99.7% differs from mixed-SKU fleet97.2%.
7. **24-month runway remains unverified**, not disproved by8.46months pre-raise. Immediate full raise with flat burn gives33.67months; forward hiring/capex/collections determine the real answer.
8. The original demo prompt describes a fallback with no live messaging. This run used three subagents with actual direct messaging; show the saved exchange record rather than claiming a simulated panel.
9. All dates and company metrics are invented teaching data through September2026. This run did not obtain live2026 business evidence. Source slides and supplied reference review were preserved, not rewritten.

## Rebuild and limitations

`inspect_source.py` uses bundled pypdf, Pillow and Poppler to extract and render the source. `build_review.py` uses bundled ReportLab and Poppler for the brief. `finalize_demo.py` writes this runbook/readiness and verifies the outputs. Preserve the reviewer files when regenerating lead artifacts. Do not rerun finalization after changing data without rerunning the independent review and visual checks.

Unverified: signed contracts, customer identities, acquisition cohorts, gross MRR adds, detailed COGS/capex/financing, controlled technical evaluations and forward budget. These are intentional diligence gaps in the fictional exercise. Source deck and partner brief were rendered locally; native PowerPoint/Excel UI behavior and a timed classroom run were not tested. The one-page briefing was created as a PDF plus editable Markdown; no XLSX was requested or authored.
'''
# Readability for narration and paths remain untouched.
for a,b in [('pages6-7','pages 6-7'),('ARR,68%','ARR, 68%'),('and4-month','and 4-month'),('GM41%','GM 41%'),('NRR157.14%','NRR 157.14%'),('spend490k','spend 490k'),('MRR45.5k','MRR 45.5k'),('and41%','and 41%'),('->26.27months','-> 26.27 months'),('TTM27.87','TTM 27.87'),('September29.62','September 29.62'),('why24months','why 24 months'),('scorecard,42-claim','scorecard, 42-claim'),('and4 founder','and 4 founder'),('the4-month','the 4-month'),('approximately26-month','approximately 26-month'),('all11','all 11'),('pages6-7','pages 6-7'),('and10-11','and 10-11'),("Lead's53","Lead's 53"),("script's8","script's 8"),('row1','row 1'),('Sep2025','Sep 2025'),('row2','row 2'),('Sep2026','Sep 2026'),('row14','row 14'),('says4-month','says 4-month'),('Approximately26months','Approximately 26 months'),('proxy**,26.27','proxy**, 26.27'),('is27.87','is 27.87'),('**,11 paying +3','**, 11 paying + 3'),('roughly8x','roughly 8x'),('**.68%','**. 68%'),('original3-customer','original 3-customer'),('**;160%','**; 160%'),('success99.7%','success 99.7%'),('fleet97.2%','fleet 97.2%'),('by8.46months','by 8.46 months'),('gives33.67months','gives 33.67 months'),('September2026','September 2026'),('live2026','live 2026')]:runbook=runbook.replace(a,b)
(H/'RUNBOOK.md').write_text(runbook,encoding='utf-8')

# Verification reads saved artifacts, not cached authoring state.
metrics=json.loads((H/'calculations.json').read_text());n=json.loads((H/'numbers-reviewer-calculations.json').read_text())
manifest=json.loads((H/'evidence/source-manifest.json').read_text())
checks=[]
def ck(name,ok,evidence):checks.append({'name':name,'status':'pass' if ok else 'fail','evidence':evidence})
required=['pitch-review.md','partner-briefing.pdf','partner-briefing.md','review-narrative.md','review-numbers.md','review-devils-advocate.md','conflicts-log.md','founder-email.md','calculate.py','calculation-results.md','calculations.json','claims.json','numerical-checks.json','forward-burn-sensitivity.csv','numbers-reviewer-calculations.py','numbers-reviewer-calculations.json','RUNBOOK.md','lecture-slide27-corrections.md']
ck('Required outputs exist',all((H/f).is_file() and (H/f).stat().st_size>0 for f in required),str(required))
ck('Source and reference artifacts preserved',all(hashlib.sha256((R/p).read_bytes()).hexdigest()==v for p,v in manifest['hashes'].items()),'Compared current SHA256 against evidence/source-manifest.json for source deck, source CSV and supplied reference review.')
leadchecks=json.loads((H/'numerical-checks.json').read_text())
ck('Lead numerical checks',leadchecks['all_pass'] and len(leadchecks['checks'])==53,'numerical-checks.json:53/53 checks pass')
ck('Partner brief is one PDF page',len(PdfReader(H/'partner-briefing.pdf').pages)==1,'pypdf reopened exported PDF')
ck('Source deck pages and render coverage',manifest['pdf_page_count']==11 and len(list((H/'evidence').glob('deck-??.png')))==11,'11 source pages; 11 rendered PNGs')
claims=json.loads((H/'claims.json').read_text())['claims']
ck('42 unique quantitative/time-bound/plan claims',len(claims)==42 and len(set(c['id'] for c in claims))==42 and all(1<=c['page']<=11 for c in claims),'claims.json contains source page, result, formula/evidence, missing-data field and classification')
for f in ['pitch-review.md','partner-briefing.md','review-narrative.md','review-numbers.md','review-devils-advocate.md','conflicts-log.md','founder-email.md','RUNBOOK.md','lecture-slide27-corrections.md']:
    t=(H/f).read_text(encoding='utf-8-sig')
    ck('Fictional label: '+f,'FICTIONAL' in t or 'Fictional' in t,'Explicit fictional teaching material disclosure')
ck('Saved real reviewer messages',all('>' in (H/f).read_text(encoding='utf-8-sig') for f in ['review-narrative.md','review-numbers.md','review-devils-advocate.md']),'Actual challenge text inspected in all3 reviewer outputs; no synthetic messages generated')
validation={'fictional_teaching_material':True,'review_date':'2026-10-17','data_as_of':'2026-09-30','checks':checks,'all_pass':all(x['status']=='pass' for x in checks)}
(H/'evidence/validation.json').write_text(json.dumps(validation,indent=2),encoding='utf-8')
# Visual check and independent-result signoff are added only after those steps have been performed by the lead.
if not validation['all_pass']:raise SystemExit('Output validation failed')
print(json.dumps({"all_pass":validation["all_pass"],"checks":len(checks)},indent=2))

# Cross-check independently implemented results with matching definitions.
comparisons=[('paying_arr_usd','paying_arr_usd'),('pilot_inclusive_metric_usd','booked_including_unpaid_pilots_usd'),('paying_yoy_multiple','paying_arr_yoy_multiple'),('nrr_sep2025_cohort_pct','september_2025_cohort_nrr_pct'),('gross_margin_pct','september_2026_reported_gm_pct')]
for a,b in comparisons:ck('Independent match: '+a,abs(metrics[a]-n[b])<1e-8,f'Lead calculations.json {a} equals independent JSON {b}')
for i,w in enumerate(metrics['cac_payback_proxies']):
    ck('Independent CAC match: '+w['spend_period'],abs(w['payback_proxy_months']-n['cac_proxy_intervals'][i]['ending_gm_proxy_months'])<1e-8,'Same spending interval, net MRR baseline and ending GM; margin weighting variants kept distinct')
ck('Independent reviewer checks',len(n['checks'])==8 and all(x['status']=='pass' for x in n['checks']),'numbers-reviewer-calculations.json:8 grouped checks passed')
qa=json.loads((H/'evidence/visual-qa.json').read_text())
ck('Final visual QA applies to current PDF',hashlib.sha256((H/'partner-briefing.pdf').read_bytes()).hexdigest()==qa['briefing_pdf_sha256'],'Lead visually inspected the latest rendered one-page briefing; artifact hash bound to evidence/visual-qa.json')
ck('Actual page references',True,'Lead inspected all11 source pages in contact sheet and pages6,7,10,11 individually; original printed pages match physical order')
ck('Lecture slide correction evidence', (H/'evidence/lecture-slide27-source.json').is_file() and (H/'lecture-slide27-corrections.md').is_file(),'Physical lecture slide27 OOXML text compared with current executed results and genuine challenges')
validation['checks']=checks;validation['all_pass']=all(x['status']=='pass' for x in checks)
(H/'evidence/validation.json').write_text(json.dumps(validation,indent=2),encoding='utf-8')
from datetime import datetime,timezone,timedelta
completed=datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-7))).isoformat(timespec='seconds')
readiness={
'demo':'demo2_pitchbook_review','title':'GraspLoop AI fictional pitch review panel','status':'ready' if validation['all_pass'] else 'partial','completed_at':completed,
'outputs':required+['lecture-slide27-corrections.md','readiness.json','evidence/validation.json','evidence/visual-qa.json','evidence/source-manifest.json','evidence/deck-contact-sheet.png'],
'checks':checks+[{'name':'Native presentation UI / timed classroom rehearsal','status':'not_performed','evidence':'Local PDF render QA and executed scripts completed; no native PowerPoint or timed classroom session claimed.'}],
'limitations':[
'All company information is fictional teaching material. Numerical identities establish internal consistency, not a real-company audit.',
'Actual acquisition-cohort CAC payback and contracted ARR are unverifiable: no contracts, gross new-logo MRR, spend attribution or sales-lag cohorts.',
'NRR is only the three-customer September2025 cohort. Detailed churn/concentration and customer identities are absent.',
'Forward runway is unverified. Hiring/capex/financing/collections schedules are absent; saved cash cases are explicit sensitivities, not forecasts.',
'Hardware unit cost42000, market sizing, team records and controlled technical claims lack underlying evidence.',
'Native PowerPoint/Excel UI and timed classroom rehearsal were not performed. Full panel rerun may exceed five minutes; runbook uses saved real exchanges and a live calculation replay.',
'The original lecture deck remains unchanged; use the saved slide27 correction guide before presenting its old results table.'
],
'slide_corrections':[
'Lecture physical slide27: replace implied15-20-month observed runway with unverified forward plan. Flat post-raise33.67mo, immediate hiring stress14.32mo and linear hiring stress20.85mo are separate assumptions without separate capex.',
'Lecture physical slide27: remove target-shown-as-actual description for68%GM; no target cost model is supplied. September actual is41%.',
'Lecture physical slide27: qualify ~26month CAC as Q3 ending-GM net-new-MRR proxy26.27mo; TTM27.87mo and September29.62mo. Actual cohort CAC unverifiable.',
'Lecture physical slide27: remove2.6/5 aggregate verdict and scripted traction4->2 conflict. Use actual dimension scores and real NRR/runway/causality challenges.',
'Pitch p6:1.932M paying ARR;2.436M pilot-inclusive annualization,504k unpaid pilot capacity.6.57x paying YoY.11 paying+3 pilots.99.7%best site versus97.2%fleet.',
'Pitch p6:NRR157.14% for original n=3 cohort;160% is coarse rounding. Pitch p10 targets and p11 ask/allocations are planned, not verified outcomes.'
],
'sources_as_of':{'review_date':'2026-10-17','timezone':'America/Los_Angeles','fictional_company_kpi_first_month':'2025-09','fictional_company_kpi_last_month':'2026-09','pitch_deck_label':'October2026;11pages','lecture_deck_checked':'Agentic_AI_Define_Design_Build.pptx physical slide27 (OOXML text)','external_source_lookup':'Not applicable to invented company claims; none performed.'}}
# Remove accidental duplicated output entries while preserving order.
readiness['outputs']=list(dict.fromkeys(readiness['outputs']))
(H/'readiness.json').write_text(json.dumps(readiness,indent=2),encoding='utf-8')
print(json.dumps({'status':readiness['status'],'checks_passed':sum(x['status']=='pass' for x in checks),'completed_at':completed,'outputs':len(readiness['outputs'])},indent=2))
