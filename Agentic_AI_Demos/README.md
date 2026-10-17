# Agentic AI: Define-Design-Build — demo kit

Companion folder for the deck [lecture PDF](../output/pdf/Agentic_AI_Define_Design_Build.pdf). Each demo has the same layout:

```
demoN_.../
  prompt.md          ← Define/Design table, copy-ready build prompt, on-screen script, harden prompts
  plugin/            ← Claude Code / Cowork plugin: .claude-plugin/plugin.json + skills/ (+ agents/)
  inputs/            ← demo inputs (Demo 2 only — fictional deck and data room)
  outputs/           ← pre-run reference outputs to show live
```

| # | Demo | Pattern | Plugin | Reference outputs |
|---|---|---|---|---|
| 1 | Competitive intelligence — Figure AI, Physical Intelligence, Skild AI, Agility Robotics, 1X | Fan-out | `startup-intel` → skill `startup-profile` | `outputs/research/` 5 profiles, `summary.md`, `competitor-matrix.xlsx` |
| 2 | Multi-agent pitch-book review — GraspLoop AI (fictional) | Panel / agent team | `pitch-review-panel` → 3 agents + skill `pitch-review` | `outputs/pitch-review.md` |
| 3 | DCF valuation — Alphabet (GOOGL) | Single pass + skill | `equity-valuation` → skill `dcf-model` | `outputs/GOOGL_DCF_Valuation.xlsx`, `valuation-notes.md` |
| 4 | Annual report → personal dashboard — NVIDIA FY2026 10-K | Pipeline | `annual-report-pipeline` → skill `semis-annual-report-kpis` | `outputs/AR-FY26/` financials → trends → exec-summary → `dashboard.html` |

## Using the plugins
- **Claude Code:** copy a demo's `plugin/` folder into a local marketplace or point `/plugin` at it; or copy `skills/*` into `~/.claude/skills/` and `agents/*` into `~/.claude/agents/`.
- **Claude / Cowork:** upload each `skills/<name>/` folder as a custom skill (zip the folder).

## Notes and caveats
- Research and market data are as of **16 Oct 2026**; re-run Demo 1 and refresh Demo 3 prices before presenting.
- Demo 2's company, people and numbers are **invented** for teaching; the deck carries a "fictional" footer.
- Demo 3 is a teaching model, **not investment advice**. Key drivers are yellow on the Assumptions tab.
- Demo 4 reference outputs cite the 10-K section and its printed page range (Item 7, pp. 36–44) plus the Q4 FY26 earnings release, because the PDF could not be fetched page by page while building the kit. A live run on `10K-NVDA.pdf` records exact pages. Download the 10-K from investor.nvidia.com or SEC EDGAR.
- `dashboard.html` opens offline in any browser.
