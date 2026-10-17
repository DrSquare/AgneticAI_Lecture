# GraspLoop AI — Series A pitch review (agent team)

*Inputs: `pitch-deck.pdf` (11 slides) · `data-room/kpi-monthly.csv` (Sep 2025 – Sep 2026) · Reviewed 16 Oct 2026*
*Team: Lead (synthesis) · Narrative reviewer · Numbers reviewer · Devil's advocate*
*⚠ GraspLoop AI is a fictional company; all data is invented for a teaching demo.*

---

## Verdict

**Take the partner meeting — conditionally. Do not issue a term sheet on this deck.**
The product signal is real (mixed-SKU pick success up from 94.1% to 97.2% in 12 months; teleoperation interventions down from 41 to 14 per 1,000 picks). But four headline numbers on the Traction and Business-model slides are overstated against the company's own data room, and the plan is not financed by the raise. The founders should fix the numbers before the meeting; how they respond is the real diligence test.

## Scorecard (1–5)

| Dimension | Score | One-line rationale |
|---|:-:|---|
| Problem & insight | 4 | Clear pain for mid-size warehouses; unsourced stats on slide 2 |
| Product & technology | 4 | Learning curve in the data room is strong and improving monthly |
| Traction (as presented) | 2 | ARR, growth and pick-success headlines don't reconcile to the data room |
| Unit economics | 1 | 68% GM and 4-month CAC payback vs. 41% and ~26 months in the data |
| Market & competition | 2 | TAM is not the market they sell into; competitor map omits real alternatives |
| Team | 3 | Relevant operators; bios are vague ("a big-tech lab") |
| Plan & ask | 2 | 24-month runway claim doesn't survive the hiring plan or hardware capex |
| **Overall** | **2.6** | **Investable story, unreliable deck** |

---

## Numbers reviewer — claim check

| # | Deck claim (slide) | Data room shows | Status |
|---|---|---|---|
| 1 | **$2.4M ARR** (6) | Paying MRR $161,000 → **$1.93M ARR**. $2.4M = $2.436M "booked ARR" that prices 12 robots in **unpaid pilots** at list | ❌ Overstated by 26% |
| 2 | **8× YoY ARR growth** (6) | Paying MRR $24,500 → $161,000 = **6.6×**. 8.3× only on booked ARR incl. pilots | ⚠ Use 6.6× |
| 3 | **14 customers** (6) | 11 paying + 3 unpaid pilots | ⚠ Say "11 paying, 3 in pilot" |
| 4 | **99.7% pick success** (6) | 99.7% = best single-SKU site. Fleet mixed-SKU = **97.2%** | ❌ Cherry-picked |
| 5 | **160% NRR** (6) | Sep-2025 cohort MRR $24,500 → $38,500 = **157%**, based on **3 customers** | ⚠ Disclose n=3 |
| 6 | **68% gross margin** (7) | **41%** in Sep 2026 (from 12% a year ago) | ❌ Target shown as actual |
| 7 | **4-month CAC payback** (7) | Last 3 months: avg S&M $163K/mo ÷ (new MRR $15.2K/mo × 41% GM) ≈ **26 months** | ❌ Off by ~6× |
| 8 | **24 months of runway** (11) | Cash $6.04M, net burn $714K/mo → 8.5 months today. With $18M and headcount 38 → 85: **~20 months** before robot hardware, **~15 months** including $42K per new robot | ❌ Overstated |
| 9 | ">100% turnover", "3×", "$0.42 per pick" (2) | No source in deck or data room | ⚠ Unsourced |

**Missing data an investor will ask for:** logo churn, contract terms on the 3 pilots (paid conversion date?), teleoperator cost per pick (14 interventions per 1,000 picks ≈ 69,000 interventions/month at 4.93M picks), hardware financing.

## Narrative reviewer — story and clarity

- **Strong hook, weak bridge.** Slides 2–3 land the problem and the "arm + brain + safety net" idea well. Slide 4 ("Why now") is generic — every robotics deck says foundation models and cheap arms.
- **The best evidence is missing from the deck.** The 12-month learning curve (pick success up, interventions down 3×) is the most persuasive chart they own; it should replace the vanity tiles on slide 6.
- **Market slide undermines credibility.** A $120B "global warehouse automation" TAM is not the market a piece-picking RaaS sells into. Lead with the $9B SAM and a bottom-up count of mid-size sites.
- **Path to $100M ARR (slide 10) has no drivers.** Show robots deployed × price, sites per AE and ramp time.
- **Team bios hide the strongest facts.** "A big-tech lab" and "2 prior exits" — name them or drop them.

## Devil's advocate — why a partner would pass

1. **"The deck flatters the data room."** Four headline metrics are inflated. If the founders did this knowingly, it is a trust problem; if not, it is a finance-function problem. Either way it is a pass until fixed.
2. **It's a services business until teleoperation falls further.** 41% gross margin with humans resolving 1.4% of picks looks like a staffing company with robots.
3. **Capital intensity is ignored.** Each robot costs $42K. $100M ARR (2029) ≈ 2,400 robots ≈ $100M of hardware. The $18M use of funds has no line for it.
4. **The moat is rented.** Generalist robot brains (e.g., Skild AI, Physical Intelligence) are being licensed to arm makers. If grasping commoditises, GraspLoop is a systems integrator.
5. **The competition slide is a 2×2 with no competitors.** No dedicated piece-picking vendors, no model-layer entrants.

---

## Conflicts log (agent-team messages)

| From → To | Message | Resolution |
|---|---|---|
| Numbers → Narrative | "You praised slide 6 as a strong traction story. 3 of its 5 numbers fail reconciliation." | Narrative downgraded Traction from 4 to 2; recommends replacing tiles with the learning-curve chart |
| Narrative → Devil's advocate | "Calling the founders untrustworthy goes beyond the evidence; 'booked ARR' is common in robotics decks." | Agreed wording: overstated **as presented**; test intent in the meeting |
| Devil's advocate → Numbers | "Is 41% GM after teleoperator cost? If not, real margin is worse." | Numbers: data room doesn't say → added to diligence list |
| Numbers → Lead | "Runway depends on hardware financing; 15–20 months is a range, not a point." | Lead reports the range and flags hardware financing as a key question |

---

## Top 5 fixes before the partner meeting (ranked by investor impact)

1. **Restate traction from paying data:** $1.93M ARR, 6.6× YoY, 11 paying + 3 pilots, 97.2% mixed-SKU success.
2. **Show gross margin as actual vs. target** (41% today → 68% at what volume and intervention rate?) and include teleoperator cost.
3. **Replace "4-month CAC payback"** with the calculation and its inputs; if it's ~26 months, explain the path down.
4. **Add a hardware-financing plan** (lease line, OEM partner, or customer-owned option) and rebuild the runway with it.
5. **Rebuild the market and competition slides** bottom-up, naming real alternatives.

## Questions for the founders
- When do the 3 pilots convert, and at what price?
- What does a teleoperator cost per 1,000 picks, and is it in COGS?
- Why did you include unpaid pilots in ARR?
- Which customers drive the 157% NRR, and what did they add?

---
*Not sent to founders. Partner decides next step. Draft founder-feedback email can be generated on request.*
