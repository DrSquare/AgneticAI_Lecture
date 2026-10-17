# Agentic AI Lecture

Open [LECTURE_DEMOS.html](LECTURE_DEMOS.html) for the four fresh demo runs and their presenter scripts. The [lecture slides (PDF)](output/pdf/Agentic_AI_Define_Design_Build.pdf) preserve the original slide layout.

To use the interactive launcher from GitHub, download the repository with **Code → Download ZIP**, extract it, and open `LECTURE_DEMOS.html` in a browser. GitHub's file view displays HTML source; it does not run the page. Keep the HTML in the extracted project folder so the PDF, workbook and dashboard links work. No server, CDN or internet connection is needed for the launcher and embedded notes.

Choose a demo from the sidebar, or press **1–4**. Click a workflow node to inspect a saved handoff. The **Walkthrough** tab follows the actual presenter runbook and remembers completed steps in this browser. **Files** searches and filters outputs, with an option to include all four demos. **Evidence** keeps readiness, limitations, validation results and slide corrections visible. **Prompt** provides the reusable runbook prompt and a copy action.

Use **Start / Pause / Reset** for the five-minute timer. Changing demos resets the timer. **Present** (or **P**) hides the sidebar; **Escape** exits. Notes open in a readable dialog with copy and download controls. PDFs and dashboards open in a new tab; XLSX files download for use in Excel. **Print** prints the current view or the open note. These controls explore saved runs; they do not launch agents or recalculate workbooks.

The repository publishes PDF handouts. Editable PowerPoint originals remain local and are excluded from Git. The [three-slide IC pack (PDF)](demo-runs/2026-10-17/demo1_competitive_intelligence/IC-pack.pdf) is available alongside the demo outputs.

The supplied ZIP was extracted to [Agentic_AI_Demos](Agentic_AI_Demos/README.md). Its original reference outputs are preserved. New work is saved under `demo-runs/2026-10-17/`, with one independently executed chat per demo under this Codex project.

| Demo | Source slides | New run folder | Chat ID |
|---|---|---|---|
| 1 - Robotics competitive intelligence | 20-24 | [demo1_competitive_intelligence](demo-runs/2026-10-17/demo1_competitive_intelligence/) | 01a14a9b-c4e5-72d1-b020-3a0efab24f47 |
| 2 - Pitch review panel | 25-27 | [demo2_pitchbook_review](demo-runs/2026-10-17/demo2_pitchbook_review/) | 01a14a9c-78e1-7c33-bb73-ef435ba9b7d8 |
| 3 - Alphabet valuation model | 28-30 | [demo3_dcf_valuation](demo-runs/2026-10-17/demo3_dcf_valuation/) | 01a14aab-bc68-7a90-96d3-b876141cbd11 |
| 4 - NVIDIA annual report dashboard | 31-35 | [demo4_annual_report_dashboard](demo-runs/2026-10-17/demo4_annual_report_dashboard/) | 01a14abb-11b4-7872-a117-2c57fea568f8 |

Each run includes its deliverables, `RUNBOOK.md`, and `readiness.json`. The [combined presenter notes](demo-runs/2026-10-17/presenter-notes.md) gather limitations and slide corrections. Do not treat the source slides' dated numbers as newly verified until the run supports them.

Run `python refresh_lecture_index.py` to refresh the local index after outputs change. Run `python refresh_lecture_index.py --check` to list statuses and missing artifacts; exit code 0 means all four saved reports say ready and all expected artifacts exist. Exit code 2 means at least one demo still needs attention. This check supplements the evidence and actual artifact validation in each run.

The refresh command rebuilds the self-contained HTML, the JSON index and the combined presenter notes. Edit `lecture_launcher/template.html` for the interface and `refresh_lecture_index.py` for the artifact catalog; do not edit generated HTML directly. A missing readiness report is displayed as **Unverified**, missing required files downgrade a ready report, and the valuation model's remaining limitations stay visible.

For maintenance, run `python -m unittest lecture_launcher.test_launcher -v`. Browser acceptance tests are in `lecture_launcher/test_browser.cjs`; run them with Node and Playwright installed (`node lecture_launcher/test_browser.cjs`). An optional `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH` selects an existing Chromium executable. Tests cover direct offline opening, hosted opening, all demo views, file search and downloads, note dialogs, clipboard fallback, timer behavior, keyboard navigation, printing, storage restrictions and mobile layouts. Screenshots and test results are saved under `.git/ui-refresh/`, or `LECTURE_QA_OUTPUT` if supplied.

The four core demos correspond to the four directories in the ZIP. The later vibe-coding prompts on slides 43-48 are separate optional classroom exercises.
