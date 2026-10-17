# Peer comparability — October 17, 2026

## Selected lecture treatment

The presenter selected **EV/EBITD = EV / (EBIT + PP&E depreciation)** in place of EV/EBITDA, alongside resolved forward P/E. This is an explicit metric substitution. Full reported TTM intangible amortization cannot be reconciled for Alphabet and Amazon from the collected filings. Every company's intangible amortization stays expensed; no missing amortization is estimated. The workbook, chart, notes and slide corrections consistently call this EBITD.

## Dated forward P/E

All four archived forecast pages identify S&P Global, adjusted non-GAAP EPS and an October 16, 2026 update date. Prices are the same October 16 closes used elsewhere in the model. GOOGL, META and AMZN FY2027 end December 31. Microsoft CY2027 EPS = 50% × FY2027 $19.78 + 50% × FY2028 $23.72 = $21.75. This assumes equal half-year earnings; it is not quarterly consensus. Adjusted EPS can exclude items such as SBC under provider-specific conventions, unlike the DCF earnings definition.

| Company | CY2027 adjusted EPS | Forward P/E | Consensus updated |
|---|---:|---:|---|
| GOOGL | 15.25 | 22.33x | 2026-10-16 |
| MSFT | 21.75 | 24.32x | 2026-10-16 |
| META | 34.63 | 20.48x | 2026-10-16 |
| AMZN | 10.45 | 23.92x | 2026-10-16 |

Peer MIN/MEDIAN/MAX use MSFT, META and AMZN only. Implied Alphabet price = peer forward P/E × GOOGL CY2027 EPS. The median is **$364.83**. Source inputs and fiscal conversion: Multiples!D73:G78; outputs: rows 48, 57 and 62; Summary row 13.

## Consistent EBITD denominators

Every company uses **July 1, 2025–June 30, 2026**. Calendar issuers use FY2025 − H1 2025 + H1 2026; Microsoft FY2026 already matches the interval. EBITD adds only PP&E depreciation. No SBC, content amortization, intangible amortization, operating-lease asset amortization or miscellaneous cash-flow adjustments are added back.

| Company | TTM EBIT | TTM PP&E depreciation | TTM EBITD | EV/EBITD |
|---|---:|---:|---:|---:|
| GOOGL | 147,628 | 25,237 | 172,865 | 23.38x |
| MSFT | 155,237 | 34,300 | 189,537 | 20.54x |
| META | 86,926 | 21,550 | 108,476 | 16.57x |
| AMZN | 93,712 | 49,741 | 143,453 | 18.86x |

USD millions. The source arithmetic is:

- GOOGL: 21,136 − 9,485 + 13,586 = 25,237.
- MSFT: 34,300 for the year ended June 30, 2026.
- META: 18,000 − 8,120 + 11,670 = 21,550, using rounded reported PP&E depreciation.
- AMZN: 41,860 − 18,822 + 26,703 = 49,741.

This replaces the old mixed addbacks of 25,237 / 38,534 / 22,729 / 75,200. Those old broad cash-flow lines no longer feed peer valuations. Peer-median EV/EBITD implies **$273.30** per GOOGL share, applying the same EV-to-common-equity bridge as the DCF. Inputs: Multiples rows 35–43; output: rows 45, 50, 56 and 61; reconciliation: rows 84–95; Summary row 12.

## Evidence and practical limits

- [GOOGL consensus EPS](https://stockanalysis.com/stocks/googl/forecast/); [SEC filing facts](https://data.sec.gov/api/xbrl/companyfacts/CIK0001652044.json).
- [MSFT consensus EPS](https://stockanalysis.com/stocks/msft/forecast/); [SEC filing facts](https://data.sec.gov/api/xbrl/companyfacts/CIK0000789019.json).
- [META consensus EPS](https://stockanalysis.com/stocks/meta/forecast/); [SEC filing facts](https://data.sec.gov/api/xbrl/companyfacts/CIK0001326801.json).
- [AMZN consensus EPS](https://stockanalysis.com/stocks/amzn/forecast/); [SEC filing facts](https://data.sec.gov/api/xbrl/companyfacts/CIK0001018724.json).

Raw pages and SEC JSON are archived in sources/peer-refresh with SHA-256 hashes. peer-inputs.json records taxonomy tags, filing accession, filing date, period and extracted value. No filing later than October 17 is used. Forward EPS dates and non-GAAP caveats are preserved in the archived text.

EV excludes lease liabilities uniformly; different lease mixes and useful lives still affect comparison. June balances are not rolled to October, Meta shares remain a weighted-average proxy, and GAAP P/E contains investment gains. These are valuation limitations, separate from the resolved mismatch in addback definitions. This is a teaching comparison, not a claim of economically identical peers or standardized GAAP EBITD.
