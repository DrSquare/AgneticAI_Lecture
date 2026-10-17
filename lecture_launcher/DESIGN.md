# Lecture workspace design

The launcher is a presenter’s desk for four saved agent workflows. Its main job is to make the next thing to show obvious, while keeping evidence and limitations within reach.

Palette: cloud #eef3f8, paper #ffffff, navy #17324d, cobalt #195ec8, leaf #22634f, amber #8b5218. Bahnschrift is the display face, with Segoe UI for reading and system fallbacks; no downloaded fonts. The page works offline.

Layout: a narrow session rail beside a broad demonstration sheet. The selected workflow is drawn as an interactive diagram above tabs for the walkthrough, files, evidence and reusable prompt. A quiet timer and presentation control stay in the header. On phones the session rail becomes a horizontal demo selector.

```
Session / demos | Lecture title                 Timer / Present
               | Selected demo       Interactive agent pattern
               | Walkthrough / Files / Evidence / Prompt
               | Timed steps         Selected step and artifact
               | Previous                         Next demo
```

The distinctive element is the workflow diagram: actual research subjects, reviewer roles and file handoffs, rather than decorative statistics. Everything is left aligned and controls have visible labels. Numbers identify the real lecture order. Blue identifies actions, while readiness has separate text and color. The design avoids dark dashboards, generic metric tiles and ornamental animation. Readiness is a dated report, never a claim that clicking a button runs agents.

Review: replaced an initial grid of four identical cards with the session rail and one active demonstration. That puts the presenter’s sequence and saved evidence first. Readable Markdown, transparent missing-file states, keyboard controls, reduced-motion behavior and a usable no-JavaScript fallback are part of the implementation.
