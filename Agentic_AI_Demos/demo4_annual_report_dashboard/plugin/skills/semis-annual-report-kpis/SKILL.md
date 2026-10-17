---
name: semis-annual-report-kpis
description: KPI definitions, extraction checklist and red-flag checks for semiconductor and AI-hardware annual reports (10-K / 20-F). Use when extracting, analysing or summarising a chip company's annual report, or building a dashboard from one.
---

# Semiconductor annual-report KPIs

## Extraction checklist (Stage 1)
For this year and last year, with printed page + PDF page index:
- **Revenue** total; by reportable segment; by market platform / end market (e.g., Data Center compute vs networking, Gaming, Pro Viz, Automotive, OEM & Other); by geography (billing location and customer HQ)
- **Gross margin** (GAAP; non-GAAP if disclosed) and every stated driver: inventory provisions, excess purchase-obligation charges, releases of reserved inventory, export-control charges, product-transition mix
- **Opex:** R&D, SG&A; R&D % of revenue
- **Operating income** total and by segment; unallocated ("All Other") costs
- **Below the line:** interest income/expense, other income (split realised vs unrealised gains), effective tax rate and one-off tax items
- **Net income, diluted EPS, diluted shares**
- **Cash:** operating cash flow, capex (PP&E + intangibles), free cash flow (company definition), buybacks, dividends, remaining authorisation, cash + marketable securities
- **Working capital & commitments:** inventories, prepaid supply agreements, purchase obligations, multi-year cloud/capacity commitments, guarantees
- **Concentration:** each direct customer ≥10% of revenue; indirect customers called out
- **Export controls / China:** licence requirements, charges, revenue assumed in guidance
- **Ecosystem investments:** equity stakes in private companies, fund commitments, guarantees to customers or partners
- **Guidance:** next-quarter revenue, gross margin, opex, tax rate; prior guidance vs. actual

## Standard calculations (mark "calc", show formula)
- Operating margin = operating income ÷ revenue; segment margin likewise
- Days of inventory = inventory ÷ cost of revenue × 365
- FCF conversion = FCF ÷ net income; capital returned ÷ FCF
- One-off impact on margin (pts) = charge ÷ revenue × 100
- Beat vs. guidance = actual ÷ guidance midpoint − 1

## Red-flag checks (Stage 2)
1. Revenue growth with falling gross margin — separate one-offs from mix
2. Net income growing faster than operating income — unrealised gains?
3. Top customer share rising — name the trend, not the customer, unless disclosed
4. Inventory or purchase commitments growing faster than cost of revenue
5. Investments in or guarantees to companies that are also customers (circularity)
6. Geography mix shifts linked to export controls
7. Changes in non-GAAP definitions that break comparability

## Output rules
- Every number carries a page reference; "not disclosed" instead of estimates.
- % growth for amounts; percentage points (pts) for ratios.
- Keep stated explanations and your interpretations in separate columns.
