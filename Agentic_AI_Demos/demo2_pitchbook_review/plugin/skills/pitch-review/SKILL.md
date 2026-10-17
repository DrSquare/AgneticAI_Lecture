---
name: pitch-review
description: Rubric and output format for reviewing a startup pitch deck (seed to Series B) with a panel of reviewers. Use when asked to critique, score or diligence a pitch deck or investor presentation.
---

# Pitch review

## Pattern
Panel: run three lenses in parallel (narrative, numbers, devil's advocate — see `agents/`), let them message each other when they disagree, then the lead writes one consolidated review. Surface disagreement; do not average it away.

## Scorecard (1–5 each)
| Dimension | 5 looks like | 1 looks like |
|---|---|---|
| Problem & insight | Sourced, specific pain with a non-obvious insight | Generic pain, unsourced stats |
| Product & technology | Evidence the product works and improves | Demo-only claims |
| Traction | Paying metrics that reconcile to the data room | Booked/pilot metrics presented as revenue |
| Unit economics | Actual GM, CAC payback with inputs shown | Targets shown as actuals |
| Market & competition | Bottom-up SAM; real named competitors | Top-down TAM; empty 2×2 |
| Team | Named, relevant track records | Vague bios |
| Plan & ask | Raise funds the plan with margin; drivers shown | Runway that ignores hiring or capex |

## Series A sanity benchmarks (rules of thumb, not facts about any company)
- ARR = paying recurring revenue only; pilots and LOIs are pipeline.
- NRR needs a cohort size; n < 10 must be disclosed.
- CAC payback = S&M spend ÷ (new MRR × gross margin).
- Runway = cash ÷ forward net burn, including hardware or other capex.

## Output: `output/pitch-review.md`
1. Verdict (one paragraph: meet / don't meet / conditional)
2. Scorecard table
3. Numbers reviewer claim-check table (claim, slide, data-room evidence, status)
4. Narrative notes
5. Devil's-advocate top 5
6. Conflicts log (from → to, message, resolution)
7. Top 5 fixes ranked by investor impact
8. Questions for founders
Never send anything to founders; the partner decides.
