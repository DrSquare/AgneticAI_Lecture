# Demo 2 presenter runbook

**FICTIONAL COMPANY AND DATA - TEACHING MATERIAL**

Review date: October 17, 2026 (America/Los_Angeles). The CSV covers September 2025-September 2026. "Ready" means the local lecture demo and artifacts were executed and checked; it does not validate a real company or investment.

## Five-minute walkthrough

| Time | Open / do | Say / show |
|---|---|---|
|0:00-0:45|Original `Agentic_AI_Demos/demo2_pitchbook_review/inputs/pitch-deck.pdf`, pages 6-7.|"All company data is invented. This polished deck says $2.4M ARR, 68% GM and 4-month CAC. Which definitions would you test?"|
|0:45-1:25|`partner-briefing.pdf`.|Show conditional founder meeting / no investment approval. Paying ARR is $1.932M, September GM 41%, NRR 157.14% for n=3.|
|1:25-2:20|`calculate.py` and `calculation-results.md`; run the command below.|Show Q3 spend 490k, net MRR 45.5k and 41% margin -> 26.27 months. Switch attention to TTM 27.87 and September 29.62. Explain net-new-MRR proxy, not proven cohort CAC.|
|2:20-3:25|`conflicts-log.md`, then Numbers review N1/N4 and D1/D3.|Narrative challenged the NRR verdict; numbers changed it to qualified. Numbers challenged runway; devil withdrew a simple pre-raise rebuttal. These were real messages between independent reviewers.|
|3:25-4:15|`pitch-review.md`, fixes and founder questions; optionally `forward-burn-sensitivity.csv`.|Separate supported arithmetic from missing evidence. Show why 24 months needs a monthly hiring/deployment/cash plan, not a static ratio.|
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
- Full synthesis: `pitch-review.md` (scorecard, 42-claim inventory, methods, conflicts, fixes and 4 founder questions).
- Real panel evidence: `review-narrative.md`, `review-numbers.md`, `review-devils-advocate.md`, `conflicts-log.md`.
- Live teaching: `calculate.py`, `calculation-results.md`, `claims.json`, `forward-burn-sensitivity.csv`.
- Lecture correction guide: `lecture-slide27-corrections.md` (verified against physical slide 27 OOXML).
- Optional follow-up: `founder-email.md` (saved draft only).
- QA evidence: `numerical-checks.json`, `numbers-reviewer-calculations.json`, `evidence/validation.json`, `readiness.json`.
- Deck page snapshots: `evidence/deck-contact-sheet.png`; individual source renders `evidence/deck-01.png` through `deck-11.png`.

All run-folder paths above are relative to `C:/Users/h_min/repos/SNU_Agentic_AI_Lecture/demo-runs/2026-10-17/demo2_pitchbook_review/`.

## Reusable panel prompt

> Review the fictional GraspLoop AI Series A deck against its supplied CSV and data dictionary. Follow `Agentic_AI_Demos/demo2_pitchbook_review/plugin/skills/pitch-review/SKILL.md` and all three agent definitions. Spawn three genuinely independent narrative, numbers and devil's-advocate reviewers. Have them send direct, substantive challenges, revise findings when warranted and preserve actual exchanges. Recompute quantitative deck claims using source page and physical CSV row/period references; no reference-output copying. Distinguish paying revenue from pilots, best site from fleet, projections from actuals, and unavailable evidence from falsity. Test the 4-month deck CAC claim and explain exactly when an approximately 26-month proxy is reproducible. Use Q3, trailing-year and monthly intervals, and distinguish net new MRR from gross acquisition cohorts. Test runway with explicit forward-burn assumptions, not merely cash/current burn. Save one file per reviewer, a factual conflicts log, claims JSON, runnable calculation script and results, consolidated review, one-page partner brief, and optional unsent founder email. All company information must be labelled fictional teaching material. Save to a new dated run folder, preserve supplied inputs/reference artifacts, and finish with a five-minute runbook and truthful readiness checks. Do not send, schedule or publish anything.

## Checks actually performed

- Read prompt, custom skill, all three role definitions and data dictionary.
- Three independent reviewers read all 11 PDF pages and exchanged direct challenges; exact messages preserved in their outputs.
- Lead read all source text, rendered all 11 pages, checked the full contact sheet and inspected critical pages 6-7 and 10-11 at readable size.
- Lead's 53 identity/row-count/period/cash checks passed. Independent numbers script's 8 grouped checks passed.
- Cross-checked independent ARR, NRR, CAC interval and runway results against lead output.
- Checked PDF printed page numbers against physical PDF order. Header row 1 makes Sep 2025 row 2 and Sep 2026 row 14.
- Built and rendered one-page partner PDF. Checked page count, layout and text; source/reference hashes verified unchanged.
- Confirmed required output files and fictional/date disclosures. No external communications or publishing occurred.

## Lecture corrections and caveats

**Physical lecture slide 27 needs revisions.** Open `lecture-slide27-corrections.md` for a ready-to-use replacement table and actual conflict examples. Remove the unsupported 15-20-month runway, unverified target-margin label, 2.6/5 headline and scripted 4-to-2 traction score change. The source lecture deck remains unchanged.

1. The pitch deck says 4-month CAC on p7. Approximately 26 months is the **Q3 ending-GM net-new-MRR proxy**, 26.27, not an exact acquisition-cohort result. TTM is 27.87; September 29.62. State the interval and limits in the lecture.
2. Use **$1.932M paying ARR**, **$2.436M pilot-inclusive annualization**, and **$504k unpaid pilot capacity**. The column name does not establish contracted ARR.
3. Use **6.57x paying YoY**, 11 paying + 3 unpaid pilot customers; explain that roughly 8x comes from the blended series.
4. Use **41% September GM**. 68% is unsupported as a current actual and must not be silently relabelled a verified target.
5. Use **157.14% NRR for the original 3-customer cohort**; 160% is coarse rounding with a required cohort disclosure.
6. Best-site/single-SKU success 99.7% differs from mixed-SKU fleet 97.2%.
7. **24-month runway remains unverified**, not disproved by 8.46 months pre-raise. Immediate full raise with flat burn gives 33.67 months; forward hiring/capex/collections determine the real answer.
8. The original demo prompt describes a fallback with no live messaging. This run used three subagents with actual direct messaging; show the saved exchange record rather than claiming a simulated panel.
9. All dates and company metrics are invented teaching data through September 2026. This run did not obtain live 2026 business evidence. Source slides and supplied reference review were preserved, not rewritten.

## Rebuild and limitations

`inspect_source.py` uses bundled pypdf, Pillow and Poppler to extract and render the source. `build_review.py` uses bundled ReportLab and Poppler for the brief. `finalize_demo.py` writes this runbook/readiness and verifies the outputs. Preserve the reviewer files when regenerating lead artifacts. Do not rerun finalization after changing data without rerunning the independent review and visual checks.

Unverified: signed contracts, customer identities, acquisition cohorts, gross MRR adds, detailed COGS/capex/financing, controlled technical evaluations and forward budget. These are intentional diligence gaps in the fictional exercise. Source deck and partner brief were rendered locally; native PowerPoint/Excel UI behavior and a timed classroom run were not tested. The one-page briefing was created as a PDF plus editable Markdown; no XLSX was requested or authored.
