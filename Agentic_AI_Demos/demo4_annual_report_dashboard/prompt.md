# Demo 4 · Annual report to personal dashboard — NVIDIA FY2026

**Pattern:** Pipeline (4 sequential sub-agents, handed off through files)
**Works in:** Claude Cowork / Claude Code (sub-agents), Copilot Cowork
**Plugin:** `plugin/` (skill: `semis-annual-report-kpis`)
**Input:** NVIDIA Form 10-K for FY2026 (`10K-NVDA.pdf`, ~100 pages) — download from investor.nvidia.com or SEC EDGAR

---

## Beat 1–2 · Define and design

| Decision | Answer |
|---|---|
| 1 · Task | NVIDIA's FY2026 10-K is ~100 pages of dense disclosure, and every reader — board member, CFO, investor — needs a different handful of numbers from it. |
| 2 · Success | Within 30 minutes: a verified KPI table, trends and anomalies, a one-page summary and a dashboard for my role. Every figure has a page or source reference. |
| 3 · Sources | `10K-NVDA.pdf` (FY2026, filed 25 Feb 2026) · Q4 FY26 earnings release (optional, for guidance) · last year's 10-K (optional) |
| 4 · Skills | Built-in: PDF, Excel, Word, HTML/app · Custom: `semis-annual-report-kpis` (platforms, gross-margin drivers, customer concentration, supply commitments, China exposure) |
| 5 · Pattern | Pipeline: four sequential sub-agents, each reading only the previous stage's file(s). Small contexts, an auditable trail. |
| 6 · Outputs & gates | `financials.md → trends.md → exec-summary.md → dashboard.html`. Nothing is sent; I check three figures against the PDF. |

---

## Beat 3 · Build prompt (copy-ready)

```
Process NVIDIA's FY2026 annual report (10K-NVDA.pdf) in 4 sequential sub-agents to avoid
filling the context window. Each sub-agent reads only its assigned input file(s). Complete and
save each stage before starting the next. Save all files to Documents/Cowork/NVDA-FY26/.

SUB-AGENT 1 — Extract financial figures
Reads: 10K-NVDA.pdf   Output: financials.md
Extract all financial figures and KPIs, with page numbers. Cover revenue by reportable segment
(Compute & Networking, Graphics) and by market platform (Data Center compute and networking,
Gaming, Professional Visualization, Automotive, OEM & Other), gross margin and its drivers
(inventory provisions, H20 charges), R&D, SG&A, operating income by segment, other income,
effective tax rate, net income, diluted EPS, operating cash flow, free cash flow, buybacks and
dividends, cash and marketable securities, inventories, purchase obligations and supply
commitments, customer concentration and revenue by geography. Include FY2026 and FY2025.
Organize the figures into structured tables. Preserve each metric's reported name, period,
segment, unit, page reference and any restatement notes. Record both the printed report page
and the PDF page index when they differ.

SUB-AGENT 2 — Analyze trends and anomalies
Reads: financials.md   Output: trends.md
Identify YoY trends, results vs. guidance, and anomalies — for example, revenue up 65% while
gross margin fell; net income growing faster than operating income; rising customer
concentration; inventory growing faster than revenue; one-offs; restated figures.
Show formulas and input values for calculations. Distinguish explanations stated in the
report from your interpretations.

SUB-AGENT 3 — Write the executive summary
Reads: trends.md   Output: exec-summary.md
Write a 1-page executive summary for the Board: 5 headlines, 3 risks, 3 questions
management should answer. Keep source page references for all numerical claims.

SUB-AGENT 4 — Create the dashboard
Reads: financials.md, trends.md and exec-summary.md   Output: dashboard.html
Create a professional, interactive dashboard in one self-contained HTML file (embedded CSS,
JavaScript and data; opens offline). Include: executive snapshot KPI cards (this year, last
year, change, source page); financial performance charts with dollars and ratios on separate
charts; quarterly revenue and gross-margin trend; segment comparison with a segment filter;
revenue by market platform; Board insights; a searchable, sortable evidence explorer
(metric, period, segment, value, unit, page, reported/calc, formula); CSV export; print layout;
and a "View as" selector (Board / CFO / Investor) that reorders the KPI cards for my role.

RULES
Every number carries its page reference. Mark anything you calculated "calc" and show the formula.
If a figure isn't in the report, write "not disclosed" — never estimate.
Distinguish % growth from percentage-point changes in ratios.
Don't round away movements under 0.5 points.
Before delivery, reconcile the dashboard against financials.md and trends.md.
```

**On screen (≈5 min):** the run takes several minutes on a ~100-page PDF, so start it before the session.
1. Show the four files in order: `financials.md → trends.md → exec-summary.md → dashboard.html`.
2. Open `financials.md`; pick one figure and find its page in the PDF.
3. Open `trends.md`; read anomaly A1 (revenue +65% while gross margin fell 3.9 pts).
4. Open `dashboard.html`; switch "View as" from Board to CFO; filter to Graphics; export CSV.

---

## Beat 5 · Harden

**Save as skill:** `semis-annual-report-kpis` — the KPI list, definitions and red-flag checks for chip companies. Reuse it for AMD, Broadcom or TSMC.

**Automate:** when NVIDIA files its next 10-Q, re-run stages 1–4 and add a "what changed" banner.

**Before it reaches the Board:** spot-check three figures against the PDF, and confirm every "calc" formula.

> Reference outputs in `outputs/AR-FY26/` were produced from the FY2026 10-K MD&A and the Q4 FY26 earnings release. Because the PDF could not be fetched page-by-page in the build environment, they cite the 10-K section and its printed page range (Item 7, pp. 36–44) rather than single pages. A live run on the PDF records exact pages.
