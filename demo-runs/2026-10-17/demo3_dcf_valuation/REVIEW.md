# Demo 3 readiness review

**Verdict: ready for a guided lecture demonstration under the approved EV/EBITD scope.** The frozen October 17, 2026 valuation remains DCF $212.65, with $158.92–$312.31 sensitivity bounds. The review covered formula dependencies, selected primary-source inputs, numerical boundary cases, presentation labels and the reproducibility of readiness evidence. It was not a fresh audit of every historical filing value.

| Finding | Improvement and evidence |
|---|---|
| Shared quote was duplicated | Multiples!D8 now links to Assumptions!D7; D9 links to Historicals!H47. A +$10 quote edit is tested across DCF market capitalization, peer P/E and Summary. |
| Meta capitalization used an average share count | Replaced 2,543m with the reported June 30 total of 2,548m; Class A/B components remain visible and sourced. Affected P/E and EV/Sales outputs recalculate. |
| Invalid Gordon assumptions produced numeric results | Terminal growth at or above WACC now yields #N/A, with a Summary explanation. Equality and above-WACC tests pass. |
| Grid validation tested only its center | Two off-center grid values now match independent edits to WACC and growth in the native model. |
| Range labels could be read as operating cases | Summary distinguishes discount/growth bounds and peer minimum/maximum values from the Base/Bull/Bear operating selector. |
| Visual readiness could pass from file existence | Finalizer now requires visual-review.json hashes matching the actual reviewed previews. Missing or stale evidence produces needs_attention. |
| Opening view and discussion aids were weak | Workbook saves on Summary. The runbook includes direct cell navigation, recovery steps, terminal-risk discussion and responses to likely audience questions. |

**Remaining critique.** 94.0% of EV is terminal value. The 1.15x terminal capex/D&A ratio, future margins and revenue allocations are judgments; at 1.50x the DCF is $178.87. Peer metrics are corroborating views, not an average target. CY2027 EPS is adjusted consensus and Microsoft uses equal-half calendarization. Lease mixes remain different. Share counts and balance sheets are June snapshots. These limitations are visible and appropriate for teaching model review, not hidden behind passing formula checks.

**Presenter handoff.** A live projector rehearsal is still needed. The original lecture deck was preserved, so use lecture-slide30-corrections.md before displaying its old numbers. Readiness applies to this dated demo workbook and walkthrough; it does not certify the original deck, fresh market data, or an investment recommendation.

Validation: 50/50 checks passed. Native Excel recalculation, saved-file audit and reviewed-preview hashes are recorded in the validation package.
