# Demo 1 · Competitive intelligence scan — 5 robotics startups

**Pattern:** Fan-out (5 parallel sub-agents on one brief → 1 synthesis)
**Works in:** Claude Cowork / Claude Code (sub-agents), Copilot Cowork, or any agent with web research and file output
**Plugin:** `plugin/` (skill: `startup-profile`)

---

## Beat 1–2 · Define and design

| Decision | Answer |
|---|---|
| 1 · Task | Before the Q4 investment committee, we need a like-for-like view of five leading embodied-AI startups — not five differently shaped memos. |
| 2 · Success | Five profiles with identical headings, every fact dated and sourced, plus a differentiator summary. Refreshed monthly and after any funding event. |
| 3 · Sources | Company blogs and press releases · SEC filings (Agility S-4) · funding announcements · credible tech and business press · model papers and release notes |
| 4 · Skills | Built-in: deep research, Excel, Word, PowerPoint · Custom: `startup-profile` (headings, 12-month window, source rules, "reported" labels) |
| 5 · Pattern | Fan-out: five parallel sub-agents on the same brief, then one synthesis |
| 6 · Outputs & gates | One profile per company · `research/summary.md` · `research/competitor-matrix.xlsx` · three slides for the IC. A partner reviews before anything circulates. |

---

## Beat 3 · Build prompt (copy-ready)

```
Research these 5 robotics startups in parallel, using a separate sub-agent for each and the same brief.
   Sub-agent 1: Figure AI · Sub-agent 2: Physical Intelligence
   Sub-agent 3: Skild AI · Sub-agent 4: Agility Robotics · Sub-agent 5: 1X Technologies

BRIEF: Last 12 months, under these exact headings:
   1 Funding & valuation: rounds, lead investors, post-money valuation, total raised, IPO/SPAC moves
   2 Technology: robot hardware and/or foundation model (VLA, world model), key releases, open source
   3 Commercial traction: named customers, deployments, revenue or ARR, orders, pricing
   4 Manufacturing & scale: factories, units built or delivered, capacity targets
   5 Team, partners & risks: leadership changes, strategic partners, lawsuits, safety or teleoperation concerns

RULES: Cite and date every fact. Prefer company announcements and filings to media.
Label unconfirmed items "reported". Flag anything older than 12 months.

SAVE: Each profile to research/{company}.md.

SYNTHESIS: Once all 5 finish, write research/summary.md: a side-by-side table,
5 key differentiators, who is gaining or losing ground, and 3 implications for
our investment committee. Also build research/competitor-matrix.xlsx.
```

**On screen (≈5 min):** start the prompt live, then switch to the pre-run task.
1. Show the five profiles in `outputs/research/` — same headings in each.
2. Open `summary.md` — read the five differentiators and three implications.
3. Open `competitor-matrix.xlsx`.
4. Spot-check one fact live by clicking its source link.

---

## Beat 5 · Harden

**Next prompt — the IC pack**
```
Turn research/summary.md into 3 slides for the investment committee: the landscape,
the differentiators, and the implications for our fund. Use our PowerPoint template.
```

**Automate — monthly**
```
On the first Monday of each month at 7am, rerun the startup-profile brief for these five
companies and highlight what changed since the last summary (new rounds, customers, launches,
leadership moves). Put changes at the top.
```

**Save as skill:** `startup-profile` — the five headings, the 12-month window and the source rules. Reuse it for autonomous-vehicle, drone or AI-chip startups.

**Before it reaches the IC:** spot-check three facts per profile; treat "reported" valuations as unconfirmed.
