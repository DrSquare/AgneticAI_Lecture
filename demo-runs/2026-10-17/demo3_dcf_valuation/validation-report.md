# DCF validation report

Completed 2026-10-17T14:42:05-07:00. Native engine: Microsoft Excel 16.0 via COM; authoring/render engine: @oai/artifact-tool.

**50/50 checks passed. Lecture-ready under the selected EBITD scope.**

| Check | Result |
|---|---|
| 2027 capex 46% to 36% flows to Summary | pass |
| Base restored after capex test | pass |
| Historical actuals unchanged in case 1 | pass |
| Historical actuals unchanged in case 2 | pass |
| Historical actuals unchanged in case 3 | pass |
| Bull / base / bear change valuation in expected order | pass |
| 2030 Cloud input flows through forecast and DCF | pass |
| Blank unselected driver does not block Base | pass |
| Selecting missing case exposes missing input | pass |
| Zero capex is a valid driver, not missing | pass |
| Historical revenue and EBIT tie-outs | pass |
| Sensitivity center equals DCF | pass |
| Segment cash-flow allocations reconcile | pass |
| 2026 capex equals guidance midpoint | pass |
| Stub excludes elapsed 2026 period | pass |
| WACC capital weights sum to one | pass |
| Forward P/E uses dated CY2027 EPS for all four companies | pass |
| Microsoft fiscal estimates calendarize to CY2027 | pass |
| Forward EPS change propagates through calendarization and multiple | pass |
| Forward peer median excludes Alphabet and flows to Summary | pass |
| Peer edits do not change the DCF | pass |
| All four EBITD denominators use EBIT plus reported PPE depreciation | pass |
| EBITD peer median excludes Alphabet and flows to Summary | pass |
| PPE source edit flows through TTM EBITD and peer valuation | pass |
| Peer source restored after propagation test | pass |
| Lecture comparison is labeled EBITD, not EBITDA | pass |
| One Alphabet quote drives DCF, peer multiples and Summary | pass |
| Meta market value uses period-end Class A plus Class B shares | pass |
| Noncentral WACC-growth grid cells match native model edits | pass |
| Gordon model rejects growth at WACC plus 0 | pass |
| Gordon model rejects growth at WACC plus 0.005 | pass |
| Terminal capex stress matches independent valuation impact | pass |
| All review edits restored to the dated lecture state | pass |
| Zero final Excel formula errors | pass |
| Scenario selector and native bar chart exported | pass |
| Saved workbook reopens with restored Base | pass |
| Workbook opens on the lecture Summary | pass |
| Fixed eight-tab order | pass |
| Every numeric input has cell-level provenance | pass |
| Blue inputs, black formulas and green cross-sheet formulas | pass |
| Saved formulas have recalculated caches and no errors | pass |
| All 35 sensitivity cells are live SUMPRODUCT formulas | pass |
| Saved Base and 46% capex restored | pass |
| Saved Summary matches Excel validation | pass |
| Saved peer outputs match the selected EBITD policy | pass |
| No external-workbook links or VBA | pass |
| All eight sheets have current visual-review evidence | pass |
| Forward and EBITD detail previews have current visual-review evidence | pass |
| All eight peer source snapshots match their recorded hashes | pass |
| Peer facts use the intended periods and contain no later filings | pass |

Capex edit: $212.652348 → $217.172338; delta $4.519990, independently expected $4.519990. Original 46% restored. Cases: Base $212.65; Bull $301.67; Bear $119.18.

Forward P/E implied value: $364.832536; EV/EBITD: $273.297392. Microsoft EPS and Amazon depreciation edits propagated correctly, sources were restored, and the DCF remained unchanged.

Review regression tests also cover a single Alphabet price input, Meta period-end shares, two off-center WACC/growth combinations, growth equal to and above WACC, and terminal capex at 1.50x D&A ($178.865394). All temporary edits were restored.

All eight sheet previews and two added peer-detail previews were inspected. The XLSX was saved, closed and reopened; formula caches were inspected directly. All eight archived peer-source hashes matched.

## Remaining limitations

- EV/EBITD explicitly replaces EV/EBITDA at the user's request: EBIT plus reported PP&E depreciation, with intangible amortization expensed for every company. Complete reported TTM EBITDA remains unavailable for Alphabet and Amazon; no estimated amortization enters the peer comparison.
- Forward P/E uses October 16 S&P Global adjusted non-GAAP consensus via Stock Analysis. Microsoft CY2027 EPS is 50% FY2027 plus 50% FY2028, an equal-half approximation rather than quarterly consensus. Provider EPS adjustments differ from the DCF, which expenses SBC.
- EV excludes lease liabilities consistently; lease mixes, asset lives and business models still affect economic comparability. Meta PP&E depreciation is reported in rounded amounts.
- October 16 quotes were verified on Google Finance vendor displays, not exchange-direct data. All Alphabet classes use the GOOGL quote. Share counts and balance sheets are June 30 snapshots, not October share-count estimates.
- Risk-free rate 4.5%, beta 1.20 and equity risk premium 4.5% are teaching assumptions. Debt and preferred costs use coupon proxies.
- Services subcategory margins and segment D&A, capex and working capital are model allocations, not company disclosures.
- The balance-sheet bridge is dated June 30 with no July–October roll-forward. Private stakes have zero Base realization; deferred tax and legal claims are deducted. Preferred conversion and capped-call optionality are not modeled.
- The remaining 2026 stub assumes H2 cash flow is earned evenly. Terminal capex at 1.15x D&A is a judgment and drives most of the valuation.
- Some original SEC HTML downloads returned HTTP 403; the peer refresh now archives all four SEC companyfacts JSON files plus all four consensus pages with hashes.
- Native Excel calculation and reopening were tested programmatically. A complete interactive lecture rehearsal and the original under-20-minute execution target have not been measured.
