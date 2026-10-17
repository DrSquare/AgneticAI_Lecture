---
name: dcf-model
description: Build a formula-driven DCF and trading-multiples valuation workbook for a public company from its filings. Use when asked for a DCF, valuation model, price target, or financial model with projections and sensitivity analysis.
---

# DCF model

## Workbook structure (tab names fixed, in this order)
1. **README** — purpose, units, colour legend, sources with URLs, caveats
2. **Assumptions** — market data; WACC inputs; terminal inputs; yearly drivers by segment (growth, EBIT margin, D&A %, capex %, NWC %), each with a one-line rationale tied to reported data
3. **Summary** — low / base / high per share by method vs. current price, plus a bar chart
4. **Historicals** — last 3 fiscal years + latest interim period, reported figures only; reconcile computed operating income to the reported figure
5. **Projections** — segment revenue → EBIT → NOPAT → + D&A − capex − ΔNWC = unlevered FCF
6. **DCF** — CAPM cost of equity, market-value weights, WACC; stub-period + mid-year discounting from the valuation date; Gordon terminal value with normalised capex; EV → equity → per share; TV % of EV
7. **Sensitivity** — per-share value across WACC (rows) × terminal growth (columns), each cell a live formula (SUMPRODUCT of PVs + TV), not a data table
8. **Multiples** — 3+ peers: P/E, forward P/E, EV/Sales, EV/EBITDA; median/low/high; implied value per share

## Rules
- Every hardcoded number is blue and has a source note; every calculation is a formula (black); cross-sheet links green; key assumptions yellow-filled.
- Use the company's latest guidance for near-term capex and state where each driver comes from.
- Normalise terminal capex (e.g., capex = D&A × ratio) when the forecast period ends mid-investment-cycle; say so.
- Treat stock-based compensation as a real cost (do not add it back) unless asked.
- Flag what the model leaves out (equity stakes, convertibles, litigation) in README.
- After building, recalculate and confirm zero formula errors; check computed historicals tie to reported totals.
- Report the result with its sensitivity range, never as a single "target price". Not investment advice.
