# Demo 3 — Alphabet DCF runbook

**Readiness: ready under the presenter-selected EV/EBITD scope.** Forward P/E is dated and calendar-aligned. EBITD uses EBIT plus reported PP&E depreciation across all four companies and explicitly replaces EBITDA. Do not call it EBITDA. Peer earnings contain no estimated amortization.

## Prepare

Open GOOGL_DCF_Valuation.xlsx in desktop Excel with Automatic calculation. Start on Summary. Confirm Base (Assumptions!D4 = 1), 2027 capex 46% (E84), DCF $212.65, forward P/E $364.83, and EV/EBITD $273.30. The saved file has native Excel caches, restored inputs, no macros and no external-workbook formula links. Adjust zoom for the projector. Keep valuation-notes.md, peer-methodology.md and validation-report.md available.

## Five-minute walkthrough

| Time | On screen | Action |
|---|---|---|
| 0:00–0:45 | Summary!C6:G23 and chart | Show DCF $212.65, range $158.92–$312.31, market $340.59. Peer methods are separate checks. |
| 0:45–1:45 | Assumptions!E84 → Summary!E9 | Change 46% to 36%; value becomes $217.17, up $4.52. Restore 46%. Edit E84, not active formula E83. |
| 1:45–2:30 | Assumptions!D4 | Select 2 Bull, 3 Bear, then 1 Base. Tested cases: Base $212.65; Bull $301.67; Bear $119.18. One forecast changes; actuals stay fixed. |
| 2:30–3:15 | Sensitivity!C9:H23 | Center equals DCF. Terminal value is 94.0% of EV; market requires 1.66x modeled terminal FCF at Base WACC/g. |
| 3:15–4:10 | Multiples!C72:J82 | Show October 16 CY2027 adjusted EPS. Explain Microsoft FY2027/FY2028 equal-half approximation. Peer median implies $364.83. |
| 4:10–5:00 | Multiples!C84:J95 → Summary!C12:G13 | Define EBITD: EBIT + PP&E depreciation, with intangible amortization still expensed. Same TTM and addback policy for all; median implies $273.30. Explain why fully reconciled EBITDA was replaced. |

Historical revenue/EBIT tie-outs are in Historicals rows 16/24; the equity bridge is in DCF rows 41–51. If a live edit misbehaves, restore Base and 46%, recalculate, and confirm the values above. Without Excel, use the reviewed previews and call the capex result a recorded test. A full interactive rehearsal has not been measured.

## Slide 30 corrections

Original deck preserved; apply these replacements before using its old numbers:

| Existing text | Replacement |
|---|---|
| 2025 revenue $403B → ~$823B in 2030; Cloud ~35% | 2025 revenue $402.8bn → $880.1bn in 2030; Cloud 36.1%. |
| 2026 capex ~$199B; 2027 ~$262B | 2026 capex $200bn midpoint of $195–205bn guide; 2027 $271.6bn. FCF becomes positive in 2028. |
| WACC 9.5%; terminal value ~95% of EV | WACC 9.75%; terminal growth 3.0%; terminal value 94.0% of EV. |
| DCF $230 (−32%); blended four-method base $284 (−17%) | DCF $212.65 (-37.6%); sensitivity $158.92–$312.31. Remove blended target. Separately show forward P/E $364.83 and EV/EBITD $273.30. |
| Market needs WACC ~8.0%, growth 3.5% | Market requires 1.66x modeled terminal FCF at Base WACC/g. Nearest grid: $347.73 at 8.25% WACC / 4.0% growth; approximate. |
| EV/EBITDA peer comparison | EV/EBITD = EV / (EBIT + PP&E depreciation). Same TTM July 2025–June 2026 and same addback policy for all peers. All intangible amortization stays expensed. |
| StockAnalysis.com prices (16 Oct 2026) | Google Finance quotes October 16; SEC/issuer financials through June 30; S&P Global adjusted CY2027 EPS via Stock Analysis updated October 16. Microsoft uses equal-half fiscal-year calendarization. |

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

Inspect regenerated previews after layout changes before declaring visual QA current. collect_peer_sources.py refreshes downloads; prepare_peer_inputs.py extracts dated consensus and SEC facts from the archive. The original DCF inputs remain manually verified in the builder. For a new date, update periods, quotes, assumptions and stub dates deliberately; downloading files alone does not refresh the whole model.

## Evidence

readiness.json records the selected metric substitution, results and remaining limitations. validation-report.json records native Excel tests, package-audit.json checks final XLSX XML and source hashes, and input-provenance.json maps all numeric inputs. sources/peer-refresh archives four consensus pages and four SEC JSON files. The source dates and calendarization remain visible in the workbook.
