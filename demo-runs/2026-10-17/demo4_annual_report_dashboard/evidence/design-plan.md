# Stage 4 design plan

## Brief and audience

A local historical NVIDIA FY2026 financial dashboard for a Board, CFO or investor. Its primary job is to compare annual performance, inspect the quarter sequence, and carry every material claim back to the saved source ledger. The sole business inputs are `financials.md`, `trends.md`, and `exec-summary.md` in this run folder. No network or original sources are consulted.

## Tokens and initial plan

- Paper `#FFFFFF`: reading surface.
- Mist `#EDF2F5`: page background and controls.
- Ink `#203342`: primary text and current-period amounts.
- Slate `#526979`: secondary text and prior-period bars.
- Fern `#306B56`: restrained financial-report identity and current-period emphasis.
- Rust `#9C4A38`: adverse margin movement, with signed text so color is not the only signal.
- Type: locally installed Bahnschrift for the fiscal-year mark and title, Segoe UI with Arial/sans-serif fallback for data and prose. Tabular numbers; no remote fonts. Body 15px, section titles 24px, KPI figures 29px, main title 40px. No all-caps labels or monospace badges.
- Left aligned reading and controls; numeric table columns right aligned. Maximum content width 1280px. Quiet white surfaces with meaningful dividers, no drop shadows or gradients.

Initial alternatives:

```text
A: report cover / flat overview / paired analytical panels
   [FY2026 | NVIDIA annual performance     historical date]
   [view selector] [segment selector]              [print]
   [revenue] [margin] [operating] [net]
   [EPS]    [FCF]    [liquidity] [inventory]
   [annual dollars             | annual ratios]
   [quarterly dollars          | quarterly margin]
   [segments                   | end markets]
   [historical guidance        | historical forecast]
   [five headlines             | risks and questions]
   [anomalies / caveats]
   [searchable evidence ledger and source registry]

B: fixed narrow sidebar / large chart / KPI strip
   [navigation | dominant chart]
   [           | broad ledger]
```

## Review before building

Choose A. A fixed sidebar would consume space without helping a single-file report and would complicate print/mobile. Revise the generic card grid into a flat metric sheet: no shadow, no pill decorations, period comparison and source references inside each metric. The one distinctive element is a large fiscal-year report mark in a fern-tinted header, grounding the dashboard in the actual annual report rather than a live terminal. Chart units are separated and foregrounded. Reorder only the same eight KPIs for audience views; all analytical facts remain available.

The initial plan is specific enough to proceed: factual historical date, source-first financial formatting, direct segment versus end-market distinction, GAAP emphasis, and restrained color. Use labels and values in every chart so visual inference is unnecessary. Every sourced number has a page/heading locator nearby; calculations retain numerical inputs in evidence.

## Build and critique criteria

- Eight KPI cards, two annual and two quarterly chart containers; responsive to a single column without document overflow.
- Group-only scope is explicit when segment data are unavailable. Segment totals are not combined with platform totals.
- Comparison changes use % for growth and two decimal places for pp changes, including small movements.
- Historical Q4 execution and Q1 FY2027 forecast remain visibly distinct; non-GAAP and recast headquarters geography caveats stay near their relevant content.
- Source references stay visible in print. The long evidence table may be omitted with a printed disclosure that the full ledger remains in HTML/CSV.
- Static reconciliation and JavaScript syntax checks are performed by this stage. Parent owns actual Chromium interaction, mobile, print and screenshot acceptance. Do not claim browser QA until it is performed.

## Post-build critique

The built report follows the revised plan: local Bahnschrift/Segoe UI typography, fern fiscal-year mark, flat eight-cell overview, explicitly separated money and ratio charts, and a quiet evidence surface. Inventory growth uses neutral text so an increase does not visually imply a favorable outcome. Negative dollar amounts use a leading minus sign before the currency symbol. There are no automatic animations, decorative gradients, drop shadows, remote fonts, external assets, CDN dependencies or publishing.

Static content review found that quarter-specific opex uses the saved `opex_q4fy26` identifier; this was corrected before final build. All dynamic rendering paths run against a minimal DOM stub to resolve data references and exercise filters, audience orders, search and numeric sorting. This is execution QA, not a substitute for visual QA. The output's source arrays were deep-compared with both original parsed ledgers. All 99 numerical trend expressions and 17 financial reconciliations passed. The requested previous-value and change-value hooks are driven by those same source records.

Print CSS preserves adjacent citations and explicitly discloses omission of the long interactive ledger. The browser acceptance owner will still inspect screenshots, mobile width, printed pages and real CSV download behavior. No browser interaction, screenshot or print result is claimed by this stage. Detailed checks, three input hashes and limitations are saved in `stage4-validation.json`.
