# Demo 1 presenter runbook

Prepared 2026-10-17 in America/Los_Angeles. Research window: 2025-10-17 through 2026-10-17.

## Five-minute walkthrough

| Time | Presenter action | Point to make |
|---|---|---|
| 0:00–0:35 | Show the reusable prompt below and research/handoffs.md | Five separate researchers used one brief. Three ran first, then two, because of the concurrency limit. |
| 0:35–1:20 | Open research/figure-ai.md and research/physical-intelligence.md | The same five headings make comparison possible. Dates and sources travel with claims. |
| 1:20–2:10 | Open research/summary.md | Read the five differentiators and the three IC implications. Momentum is an analytical judgment, not a measured ranking. |
| 2:10–3:10 | Open research/competitor-matrix.xlsx | Show numeric inputs, evidence-age formulas and guarded valuation/capital formulas. Missing capital is not zero. |
| 3:10–4:00 | Open research/evidence-checks.md and click Figure's manufacturing source | Demonstrate why “produced” does not mean “delivered to paying customers.” |
| 4:00–5:00 | Open IC-pack.pptx | Show landscape, differentiators and implications. Close with the source limitations and human review gate. |

Pre-open the workbook and deck before the lecture. For a predictable offline demonstration, use the saved slide PNGs in build/ if native PowerPoint rendering differs. Browser pages can change after this dated run.

## Files to open

- research/figure-ai.md
- research/physical-intelligence.md
- research/skild-ai.md
- research/agility-robotics.md
- research/1x-technologies.md
- research/summary.md
- research/competitor-matrix.xlsx
- research/evidence-checks.md
- IC-pack.pptx

## Reusable prompt

Research Figure AI, Physical Intelligence, Skild AI, Agility Robotics and 1X Technologies using a separate researcher for each. Batch researchers if the concurrency limit requires it. Use one explicit 12-month window and cutoff date. Use these exact headings: 1 Funding & valuation; 2 Technology; 3 Commercial traction; 4 Manufacturing & scale; 5 Team, partners & risks. Date every factual bullet and end it with a numbered source citation. Prefer filings, companies and counterparties. Label unaudited operating metrics company-reported, unconfirmed transactions reported, and older latest benchmarks with a warning. Do not equate capacity, production, orders and deliveries.

Save five profiles and structured evidence. Verify at least three material facts per company. Synthesize a side-by-side comparison, five differentiators, evidence-based momentum judgments and three IC implications. Build a formula-capable workbook with numeric inputs, visible sources, guarded valuation/capital ratios and useful evidence-age calculations. Produce and visually verify exactly three IC slides. Save a dated runbook, evidence log and readiness manifest. Preserve source material. Do not activate automation, publish or send communications.

## Checks performed

- Five independent researchers completed separate profiles and structured source records.
- Each profile has the same five headings. At least three material claims per company were spot-checked.
- The evidence log distinguishes company reports, counterparty confirmation, reported talks and partial SEC retrieval.
- Workbook formulas were recalculated. Evidence ages matched independent date arithmetic. A temporary date change and temporary ratio inputs tested dependency updates, zero handling and blank handling; originals were restored.
- Workbook formula-error scan and visual review cover both sheets and the source area.
- The three-slide pack uses editable tables. Package, geometry, font and import checks run through the artifact finalizer. Each final slide is rendered and visually checked.
- The source lecture slide 24 was rendered through a one-slide reference copy. The original full-deck import had an unrelated invalid chart-axis identifier, so the source deck was left untouched.
- No native Excel or PowerPoint UI test, API call to the robotics products, robot demonstration or physical delivery inspection was performed. Consult readiness.json for the final check results.

## Lecture corrections

1. Change the as-of date from October 16 to October 17, 2026 for this run.
2. Figure: retain $39B only as a September 2025 historical baseline. Its factory output is not paid customer deliveries. The Nscale compute commitment is not funding proceeds.
3. PI: use “Revenue not disclosed” instead of “pre-revenue.” The $5.6B investor baseline has an unspecified valuation basis; later reported rounds remain unresolved.
4. Skild: retain >$100M ARR and 60+ customers only as company-reported. January revenue is not an ARR baseline. The acquired robotics business makes “model-only” incomplete.
5. Agility: the $2.5B SPAC value and proceeds remain proposed. November 2 is a scheduled vote, not a completed listing. The $1.782M figure is FY2025 sales; >$300M order value is conditional and multi-year. Digit 5 availability targets 2027.
6. 1X: ~$6B describes reported acquisition talks, not a verified closed round. Factory capacity and potential EQT rollout do not establish deliveries. Use “external deliveries not independently verified,” not zero deliveries.
7. Remove claims that model firms raised faster or that the SPAC vote will necessarily set a public-market price. This run lacks comparable capital totals and the transaction outcome is future.
8. Momentum labels are qualified judgments. This run treats Figure as gaining on milestones and 1X as holding pending delivery evidence.

The source lecture deck and supplied reference outputs are preserved. No recurring automation was activated.

## Rebuild

Use bundled Node.js and the node_modules junction in build/. The scripts live entirely inside this run directory:
- build/build-artifacts.mjs creates the workbook and deck. The optional argument “deck” rebuilds only the pack.
- build/assemble-research.py assembles the synthesis, handoffs and evidence checks from the research JSON.
- The builder creates fresh timestamped validation folders and receipts, then copies the checked deck to IC-pack.pptx. Archive the delivered workbook/deck first if you need to preserve a prior version.
