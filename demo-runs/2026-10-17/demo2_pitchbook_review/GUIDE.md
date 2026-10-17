# Pitch review panel

## Five-minute walkthrough

| Time | Explore | Key idea |
|---|---|---|
| 0:00–0:45 | Read the fictional [pitch deck](../../../Agentic_AI_Demos/demo2_pitchbook_review/inputs/pitch-deck.pdf), pages 6–7. | Compare its ARR, gross margin and CAC claims with the supplied data. All company data are invented. |
| 0:45–1:25 | Open the [partner briefing](partner-briefing.pdf). | Paying ARR is $1.932M; September gross margin is 41%. The conclusion supports a focused founder meeting. |
| 1:25–2:20 | Explore the [calculation results](calculation-results.md). | Q3 sales and marketing spend / net new MRR / ending gross margin gives 26.27 months. This is a proxy, not verified acquisition-cohort CAC. |
| 2:20–3:25 | Compare the narrative, numbers and devil’s-advocate perspectives above. | Separate a repairable story, supported arithmetic and unresolved commercial risks. |
| 3:25–4:15 | Read the [consolidated review](pitch-review.md) and [burn sensitivities](forward-burn-sensitivity.csv). | A 24-month runway requires a forward hiring, deployment and cash plan. Pre-raise cash/current burn cannot settle that claim. |
| 4:15–5:00 | Explore the [founder email example](founder-email.md). | Turn the findings into specific questions and priorities. The example is an unsent draft. |

## Sources and methods

Fictional GraspLoop AI deck: 11 pages. KPI data: September 2025 through September 2026.

Paying revenue, unpaid pilots, best-site performance and fleet averages have distinct definitions.

157.14% NRR covers the original three-customer cohort. The payback calculation uses net new MRR; acquisition-cohort inputs and a funded forward cash plan are unavailable.

## Reusable prompt

Review the fictional GraspLoop AI Series A deck against its supplied CSV and data dictionary. Follow `Agentic_AI_Demos/demo2_pitchbook_review/plugin/skills/pitch-review/SKILL.md` and all three agent definitions. Spawn three genuinely independent narrative, numbers and devil's-advocate reviewers. Have them send direct, substantive challenges, revise findings when warranted. Recompute quantitative deck claims using source page and physical CSV row/period references; no reference-output copying. Distinguish paying revenue from pilots, best site from fleet, projections from actuals, and unavailable evidence from falsity. Test the 4-month deck CAC claim and explain exactly when an approximately 26-month proxy is reproducible. Use Q3, trailing-year and monthly intervals, and distinguish net new MRR from gross acquisition cohorts. Test runway with explicit forward-burn assumptions, not merely cash/current burn. Save one file per reviewer, claims JSON, runnable calculation script and results, consolidated review, one-page partner brief, and optional unsent founder email. All company information must be labelled fictional teaching material. Save to a new dated run folder, preserve supplied inputs/reference artifacts,. Do not send, schedule or publish anything.
