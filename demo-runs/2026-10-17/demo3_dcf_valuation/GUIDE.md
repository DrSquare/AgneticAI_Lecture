# Alphabet valuation model

## Five-minute walkthrough

| Time | Explore | Key idea |
|---|---|---|
| 0:00–0:45 | Open [the workbook](GOOGL_DCF_Valuation.xlsx) on Summary. | Base DCF is $212.65; sensitivity is $158.92–$312.31. The dated market price is $340.59. |
| 0:45–1:45 | In Excel, change Assumptions!E84 from 46% to 36%, then restore 46%. | 2027 capex sensitivity increases DCF to $217.17 while holding other assumptions fixed. |
| 1:45–2:30 | Use Assumptions!D4: 2 Bull, 3 Bear, then 1 Base. | Base is $212.65; Bull $301.67; Bear $119.18. Forecast assumptions change while historical actuals stay fixed. |
| 2:30–3:15 | Explore Sensitivity!C9:H23. | Terminal value is 94.0% of enterprise value. Market price requires 1.66x modeled terminal FCF at Base WACC and growth. |
| 3:15–4:10 | Read [peer methodology](peer-methodology.md) and Multiples!C72:J82. | Forward P/E uses dated CY2027 adjusted EPS. Microsoft uses an equal-half fiscal-year approximation. Peer median implies $364.83. |
| 4:10–5:00 | Inspect Multiples!C84:J95 and the [valuation memo](valuation-notes.md). | EV/EBITD uses EBIT plus PP&E depreciation, keeping intangible amortization expensed. Peer median implies $273.30. |

## Sources and methods

Snapshot: October 17, 2026. Market quotes and adjusted EPS consensus are dated October 16; financial inputs run through June 30.

The workbook contains sources, explicit assumptions and live formulas. Open it in Excel for recalculation. This is a teaching model, not investment advice.

WACC is 9.75%; terminal growth is 3.0%. Peer methodologies and economic limitations are explained in the valuation memo and peer methodology.

## Reusable prompt

Create a sourced Alphabet valuation workbook with historical financials, editable assumptions, a five-year forecast, DCF and sensitivity, and comparable peer methods. Cite the date and source of each financial input. Separate assumptions from reported results. Use EV/EBITD (EBIT plus PP&E depreciation) consistently across peers, and explain the calendarization of forward earnings. Show a range and the economic limitations of each method.
