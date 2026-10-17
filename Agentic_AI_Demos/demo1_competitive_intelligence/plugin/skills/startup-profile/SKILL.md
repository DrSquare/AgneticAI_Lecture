---
name: startup-profile
description: Write a like-for-like profile of a private (or newly public) technology startup under five fixed headings with dated, sourced facts. Use when asked to research, profile or compare startups, competitors or portfolio companies, especially several at once.
---

# Startup profile

Produce one Markdown profile per company. Every profile in a set must use **exactly** the same headings, window and rules, so profiles can be compared side by side.

## Header block
```
# {Company} — startup profile
*Window: {start} – {end} · Prepared {date} · Brief: startup-profile v1*
*HQ · Founded · CEO · Approach (one line: what layer of the stack they play in)*
```

## The five headings (never rename, reorder or merge)
1. **Funding & valuation** — rounds (amount, lead, post-money), total raised, secondary/IPO/SPAC moves
2. **Technology** — hardware and/or model; named releases with dates; open-source; benchmark claims (label as company claims)
3. **Commercial traction** — named customers, deployments, revenue/ARR, orders/backlog, pricing. If revenue is not disclosed, write **"Revenue: not disclosed."**
4. **Manufacturing & scale** — factories, units built/delivered, capacity targets. Write "Not applicable" for software-only companies and say how they reach scale instead.
5. **Team, partners & risks** — leadership changes, strategic partners, lawsuits, regulatory or safety issues, and the two or three risks an investor should probe

## Source rules
- Every bullet ends with a date in *(italics)* and a numbered citation `[n]`; list sources with URLs at the bottom.
- Source preference: company filings (SEC) > company announcements > top-tier press (Bloomberg, Reuters, WSJ, FT, TechCrunch) > trackers and wikis.
- **"reported"** = a single-source or unconfirmed claim (e.g., a round "in talks"). Never present it as closed.
- **"company-reported"** = metrics the company states but no third party has audited (ARR, units, success rates).
- Flag anything older than the window with ⚠ and keep it only if it is the latest data point of its kind.
- Never estimate a number that is not in a source. Write "not disclosed".

## Synthesis (when profiling a set)
Write `summary.md` with: a side-by-side table (layer, valuation, capital, flagship, revenue signal, customers, scale, top risk), five differentiators, gaining/holding/under-pressure, three implications for the reader, and a caveats section. Build a matching Excel matrix with numbers as numbers (valuation $B, capital $B) and simple formulas (valuation ÷ capital).
