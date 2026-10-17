# Demo 4: NVIDIA annual report to an evidence dashboard

Preparation date: 2026-10-17, America/Los_Angeles. Status: ready for the lecture walkthrough.

This is a historical FY2026 demonstration. FY2026 ended January 25, 2026; the 10-K was filed February 25, 2026. The Q1 FY2027 outlook shown is the historical outlook issued February 25, 2026, not current guidance on the preparation date. See `inputs/sources.json` for official URLs, retrieval date and SHA-256 hashes.

## Files to open

- `dashboard.html`: self-contained offline interactive result; open directly in a browser.
- `financials.md`, `trends.md`, `exec-summary.md`: the four-agent file handoff, in that order before the dashboard.
- `exec-summary.pdf`: the verified one-page printable Board brief.
- `inputs/10K-NVDA.pdf`: official annual-report package from NVIDIA investor relations. It contains 175 PDF pages, including front matter/proxy; the 10-K begins on PDF page 89. For numbered 10-K pages used here, PDF page = printed page + 88. Zero-based PDF index = PDF page - 1.
- `evidence/source-pdf-139.png`, `source-pdf-141.png`, `source-pdf-165.png`, `source-pdf-129.png`: prepared page views for quick on-screen source checks.
- `readiness.json`, `evidence/pipeline-log.json`, and validation/test JSON files: acceptance evidence and file hashes.

## Five-minute walkthrough

| Time | Presenter action | Point to make |
|---|---|---|
| 0:00-0:30 | Show the four intermediate/output files and the official source manifest. | Each stage was an independent agent with only its assigned files. The parent checked each output before the next stage started. |
| 0:30-1:20 | Open `financials.md` and the PDF. Spot-check revenue of USD 215,938 million on printed p.51 / PDF139; inventories of USD 21,403 million on p.53 / PDF141; Compute & Networking revenue of USD 193,479 million on p.77 / PDF165. | Values, periods, units and page systems are preserved. These are three distinct source-page checks. |
| 1:20-2:00 | Open `trends.md` at the revenue/gross-margin anomaly and its formula. | Amount growth is a percentage; a change in margin is percentage points. The filing names margin drivers but does not quantify a complete causal decomposition. |
| 2:00-2:30 | Open the Board summary. | Five headlines, three risks and three management questions retain the evidence trail. |
| 2:30-3:30 | Open `dashboard.html`; switch Board to CFO, then select Graphics. | Cards reorder for the role. Segment revenue and operating income change. Consolidated metrics remain visibly marked group only; no unsupported allocation to Graphics. |
| 3:30-4:20 | Search the evidence explorer for H20, clear the search, sort Value, and export CSV. | A claim can be traced to its period, source and formula. Export follows the visible filter. |
| 4:20-5:00 | Reset the segment filter to All. Use Print or open the saved print PDF. Close with the slide corrections below. | One offline artifact supports different readers. The source-derived limits remain visible. |

## Reusable prompt

```text
Build an annual-report dashboard using four genuinely sequential agents with isolated contexts.
Use only official, archived sources and save source URLs, retrieval dates and hashes. Record the
fiscal period separately from the run date. Preserve the supplied source and reference outputs.

Stage 1 reads the annual report and the assigned official earnings releases. Extract the
semiconductor KPI checklist to financials.md. Keep period, reported name, segment, units,
printed page, 1-based PDF page, zero-based PDF index, source heading, and comparability notes.
For HTML-only releases cite the exact heading and URL. Missing means not disclosed, never zero.
Include machine-readable rows and validate financial/segment/platform/cash-flow reconciliations.

Gate and save stage 1 before starting stage 2. Stage 2 reads ONLY financials.md and writes
trends.md. Show every calculation with formula and numerical inputs. Separate management's
stated explanation from interpretation. Keep source locators in trends.md so it stands alone.
Do not attribute an unquantified residual margin change to one named driver.

Gate and save stage 2 before stage 3. Stage 3 reads ONLY trends.md and writes a one-page
exec-summary.md: exactly 5 Board headlines, 3 risks and 3 questions, with source references.

Gate and save stage 3 before stage 4. Stage 4 reads ONLY those three intermediate files and
creates dashboard.html with embedded CSS, JavaScript and data; no server, CDN or network
dependency. Include eight annual KPI cards, Board/CFO/Investor card ordering, a reportable-
segment filter, separate dollars/ratios charts, annual and quarterly figures, historical guidance
comparisons where verified, platform revenue, Board insights, searchable/sortable evidence,
calculation formulas/inputs, CSV download and print CSS. Mark group-only metrics and preserve
the distinction between market platforms and reportable segments.

Reconcile embedded data to the intermediate files. Test actual browser interactions, offline
loading, CSV download and print rendering. Save screenshots, test evidence, RUNBOOK.md and
readiness.json. Do not schedule tasks, send communications or publish externally.
```

## Checks and reproducibility

Acceptance passed. Stage 1: 46 financial reconciliations. Stage 2: 126 checks, including independent recomputation of all 36 inherited calculations. The Board brief prints on one A4 page. The dashboard passed 16 browser checks with networking disabled, including role ordering, both segment filters, group-only labels, exact embedded-data equality, evidence search/sort, a real CSV download, print rendering and mobile width. Final screenshots and print pages were visually reviewed.

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

Source acquisition is preserved in `scripts/acquire_sources.py`. Run scripts against the archived input files to preserve this snapshot. Source acquisition needs internet and PDF/HTML parsing packages. Browser verification uses the locally installed Playwright package and Chromium executable recorded in `evidence/browser-environment.json` and `browser-tests.json`; those machine-specific paths may need adjustment elsewhere. Poppler renders PDFs to PNGs for visual review. The operating-system print dialog was not exercised; headless Chromium print media and generated PDF layout were checked.

## Lecture slide corrections

- Slides 31-32: the recovered official PDF is a 175-page annual-report package, with the 10-K starting on PDF89. Do not use PDF position as the printed page. Present the build as a pre-run demonstration; this run does not establish a guaranteed 30-minute end-to-end turnaround.
- Slides 32-33: say “each stage reads only its assigned files.” Stage 1 also needs the archived Q2/Q3/Q4 releases for quarterly values and guidance; stage 4 reads three intermediate files.
- Slides 31, 33-34: say “every figure has a page or exact source-section reference.” HTML earnings releases do not have PDF page numbers.
- Slide 35: remove “the rest is the Blackwell transition (calc).” The report names the transition and H20 charge as drivers but does not quantify the residual's causal allocation. A charge/revenue calculation is not a complete year-over-year margin bridge.
- Slide 35: replace “Q1 FY27 guided ... ex-China” with “historical Q1 FY27 outlook issued February 25, 2026; no Data Center compute revenue from China assumed.” Do not imply all China revenue was excluded.
- Slide 35: label guarantees as maximum gross contingent exposure, not a cash investment. Do not add investment flows, holdings, commitments and guarantees into one financing total.
- Slide 35: customer names are not disclosed. Largest-share comparisons do not establish that the same customer's share changed; direct and indirect customer shares can overlap.

## Known source boundaries

Prior-year commitment/guarantee comparisons, separately quantified supply prepayments, exact
insignificant investment gains and a quantified Blackwell-only margin impact are not disclosed
in the assigned source set. Headquarters geography is recast and is not billing or end-use
geography. FY2027 non-GAAP guidance changes the treatment of stock-based compensation.
Free cash flow follows NVIDIA's definition and does not subtract every investing cash outflow.
These boundaries are part of the demonstration and must not be filled with estimates.
