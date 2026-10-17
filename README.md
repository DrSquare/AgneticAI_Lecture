# Agentic AI Lecture

[Explore the interactive demos](https://agentic-ai-lecture.netlify.app/) or download the [lecture slides](output/pdf/Agentic_AI_Define_Design_Build.pdf).

Four examples connect Define, Design and Build to a finished result:

| Demo | Pattern | Outputs |
|---|---|---|
| Robotics competitive intelligence | Fan-out | Five company profiles, comparison workbook and IC slides |
| Fictional pitch review | Panel | Three analytical perspectives, calculations and partner briefing |
| Alphabet valuation | Single pass + skill | Formula-based Excel model and valuation methods |
| NVIDIA annual report | Pipeline | Financial evidence, trend analysis, Board summary and interactive dashboard |

Use **Walkthrough** to explore the steps, **Files** to search and open deliverables, **Sources** for scope and definitions, and **Prompt** to try the workflow yourself. Workflow nodes open the corresponding output. The timer, progress tracking, presentation view and print controls work in the browser. Press **1–4** to select a demo, **P** for presentation view and **Escape** to close a document.

PDFs and dashboards open in a new tab. Workbooks download for recalculation in Excel. The site explores saved examples; it does not execute agents or recalculate Excel files online. Demo 2 uses fictional data. Financial examples are dated teaching material, with sources and assumptions in each output.

## Offline use

Download the repository ZIP, extract it, and open `LECTURE_DEMOS.html`. Keep it inside the extracted folder so linked files remain available. Embedded documents and the NVIDIA dashboard work offline.

## Build and checks

Run `python scripts/build_site.py` to generate `dist/`. The build uses an explicit audience artifact catalog and rejects internal preparation records. `python refresh_lecture_index.py --check` checks that required audience files exist. Run `python -m unittest lecture_launcher.test_launcher -v` and `node lecture_launcher/test_browser.cjs` for automated checks (the browser tests require Playwright).

Edit `lecture_launcher/template.html` for the interface, `refresh_lecture_index.py` for the artifact catalog, and each demo's `GUIDE.md` for its walkthrough. Generated HTML is rebuilt from those sources.

Netlify builds `main` with the committed `netlify.toml`, using `python3 scripts/build_site.py` and publish directory `dist`. To preview, run `python -m http.server 8765 --directory dist`. Only the generated `dist` directory is deployed.
