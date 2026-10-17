# NVIDIA annual report dashboard

## Five-minute walkthrough

| Time | Explore | Key idea |
|---|---|---|
| 0:00–0:45 | Open the [annual report](inputs/10K-NVDA.pdf) and [financial evidence](financials.md). | FY2026 ended January 25, 2026. Printed 10-K page 51 is PDF page 139. |
| 0:45–1:35 | Read the [trend analysis](trends.md). | Distinguish reported figures, calculated changes and analytical interpretations. |
| 1:35–2:20 | Explore the [Board summary](exec-summary.md). | Follow five headlines, three risks and three management questions back to their evidence. |
| 2:20–3:20 | Open the [interactive dashboard](dashboard.html). Change View as and the segment filter. | Board, CFO and Investor views prioritize different information. Group-only measures remain clearly labeled. |
| 3:20–4:20 | Search the dashboard’s evidence explorer and export a CSV. | Inspect source pages, units and formulas. Percentage growth and percentage-point changes are different measures. |
| 4:20–5:00 | Reset the segment filter to All and use Print. | Connect financial performance, cash generation and commitments. The historical outlook is dated, not current guidance. |

## Sources and methods

NVIDIA FY2026 annual report and Q2, Q3 and Q4 earnings releases. FY2026 ended January 25, 2026; the 10-K was filed February 25.

Financial citations show printed 10-K pages and PDF pages. The annual-report front matter produces an 88-page offset.

Reported segments and end markets are different reporting views. Missing disclosures remain unavailable; calculations show inputs and formulas.

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
loading, CSV download and print rendering. Do not schedule tasks, send communications or publish externally.
```
