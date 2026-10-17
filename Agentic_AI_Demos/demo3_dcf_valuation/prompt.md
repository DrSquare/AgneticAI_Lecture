# Demo 3 · DCF valuation — Alphabet (Google)

**Pattern:** Single pass, with a skill (one prompt → one formula-driven workbook)
**Works in:** Claude (Excel/xlsx skill), Claude Cowork, Copilot Cowork with Excel
**Plugin:** `plugin/` (skill: `dcf-model`)

---

## Beat 1–2 · Define and design

| Decision | Answer |
|---|---|
| 1 · Task | Before our tech-sector review, I need an independent view of what Alphabet is worth now that AI capex has more than doubled — not a sell-side target I can't audit. |
| 2 · Success | A working Excel model: every input blue and sourced, every output a formula, a sensitivity grid, and peer multiples — in under 20 minutes. |
| 3 · Sources | Alphabet 10-K and quarterly earnings releases (SEC) · Q2 2026 call for capex guidance and Cloud backlog · market data and peer multiples (MSFT, META, AMZN) |
| 4 · Skills | Built-in: Excel (xlsx), web search · Custom: `dcf-model` (tab structure, colour code, normalised terminal capex, checks) |
| 5 · Pattern | Single pass: one prompt, one workbook; the skill carries the know-how |
| 6 · Outputs & gates | `output/GOOGL_DCF_Valuation.xlsx` + `valuation-notes.md`. I review the drivers before anyone sees a number. |

---

## Beat 3 · Build prompt (copy-ready)

```
Create a comprehensive financial model for Alphabet (GOOGL) with:
- Historical financials FY2023–FY2025 and H1 2026 from SEC filings
- 5-year projections (2026–2030) by segment: Search, YouTube, Network,
  Subscriptions & devices, Google Cloud, Other Bets
- DCF valuation (WACC, terminal growth) with sensitivity analysis
- Multiple valuation methods (P/E, EV/Sales, EV/EBITDA vs. MSFT, META, AMZN)
- All formulas in Excel format; include assumption inputs I can modify (blue font)
- Use the latest 2026 capex guidance; cite a source for every input

OUTPUT: Write an Excel file to output/GOOGL_DCF_Valuation.xlsx
```

**On screen (≈5 min):**
1. Open the **Summary** tab — four methods vs. the current price.
2. **Assumptions** tab — show Cloud growth and capex % (yellow). Change 2027 capex from 46% to 36% and watch Summary update.
3. **Sensitivity** tab — what WACC and growth does the market price imply?
4. **Historicals** — computed operating income ties to the reported figure.

---

## Beat 5 · Harden

**Next prompt**
```
Add a bull/base/bear scenario switch on the Assumptions tab (Cloud growth, EBIT margin,
capex intensity) and a one-page memo explaining what the market price implies.
```

**Save as skill:** `dcf-model` — tab structure, colour code and checks. Reuse for MSFT, META, AMZN or NVDA by changing the ticker.

**Automate:** after each Alphabet earnings release, refresh Historicals and guidance and highlight which drivers moved.

**Before it reaches anyone:** check the three yellow drivers and the source of every blue input. A DCF is an argument, not a fact.
