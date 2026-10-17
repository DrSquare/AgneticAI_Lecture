# Demo 2 · Multi-agent pitch book review

**Pattern:** Panel / agent team (three lenses → challenge each other → one verdict)
**Works in:** Claude Code agent teams (or sub-agents), Claude Cowork
**Plugin:** `plugin/` (agents: `narrative-reviewer`, `numbers-reviewer`, `devils-advocate`; skill: `pitch-review`)
**Inputs (fictional):** `inputs/pitch-deck.pdf`, `inputs/data-room/kpi-monthly.csv`

---

## Beat 1–2 · Define and design

| Decision | Answer |
|---|---|
| 1 · Task | A partner has 20 minutes before a founder meeting and needs a sharp, balanced read of a Series A deck — not one reviewer's opinion. |
| 2 · Success | Every numeric claim checked against the data room; disagreements surfaced, not averaged away; a scorecard, top 5 fixes and a go/no-go on one page. |
| 3 · Sources | `pitch-deck.pdf` (11 slides) · `data-room/kpi-monthly.csv` (13 months of KPIs) · our Series A rubric |
| 4 · Skills | Built-in: PDF, Excel · Custom: `pitch-review` (rubric, benchmarks, output format) + three reviewer agent definitions |
| 5 · Pattern | Panel: three reviewers in parallel who message each other to challenge findings; the lead writes the verdict |
| 6 · Outputs & gates | `output/pitch-review.md` (+ one file per reviewer). Nothing goes to the founders; the partner decides. |

---

## Beat 3 · Build prompt (copy-ready)

```
Create an agent team to review GraspLoop's Series A pitch deck (pitch-deck.pdf)
against its data room (data-room/kpi-monthly.csv). Spawn three reviewers:
- Narrative reviewer: assess story flow, clarity, investor hook
- Numbers reviewer: recompute every claim from the data room; flag weak or missing data
- Devil's advocate: argue why an investor would pass (be harsh)
Have them message each other with conflicts (e.g., if the narrative praises a claim
the numbers reviewer finds unsupported).

OUTPUT: Write a consolidated critique to output/pitch-review.md: a 1–5 scorecard,
a claim-check table, a conflicts log, top 5 fixes ranked by investor impact,
and a go/no-go for the partner meeting.
```

> Agent teams: see Claude Code docs, "Orchestrate teams of Claude Code sessions", for how to enable them in your version. Without teams, the same prompt runs as three sub-agents plus a lead synthesis (no live messaging; the lead reconciles conflicts instead).

**On screen (≈5 min):**
1. Flip through the fake deck — "looks fundable, right?"
2. Open `outputs/pitch-review.md` — read the verdict and the claim-check table ($2.4M ARR → $1.93M paying; 68% GM → 41%; 4-month CAC payback → ~26 months).
3. Show the conflicts log — that's the value of a panel over a single reviewer.

---

## Beat 5 · Harden

**Next prompt**
```
Draft a short, constructive email to the founders with the top 5 fixes and the 4 questions.
Do not send it — save it to output/founder-email.md for my review.
```

**Save as skill:** `pitch-review` — the rubric, benchmarks and output format. Reuse it for any stage or sector by swapping the benchmarks.

**Automate:** when a new deck lands in the `Inbound decks` folder, run the panel and post the scorecard to the deal channel.

**Before it reaches the partner meeting:** re-run the numbers reviewer if the founders send a revised data room.
