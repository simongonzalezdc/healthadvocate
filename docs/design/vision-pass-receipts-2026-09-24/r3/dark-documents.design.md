judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-documents.png)

The image is visible. Audit below.

## What I see

**Layout, top-to-bottom**
1. App bar (~48px): sage rounded-square logo tile with heart glyph + "HealthAdvocate" wordmark, left. Right: outlined pill "⏰ 1 reminder due soon" in orange, plus two circular ghost icon buttons (scan, moon).
2. Nav row: 10 flat text items (Symptoms → Library); "Documents" active in an outlined pill with sage text; an 11th item clipped at the right viewport edge.
3. Main: one centered card (~⅔ width) — sage icon tile + "Document Decoder" heading, one-line muted subtitle, small-caps label "PASTE YOUR MEDICAL DOCUMENT TEXT", full-width empty textarea, sage filled button "Decode Document" bottom-left.
4. Hairline divider, centered 2-line disclaimer footer with bolded wordmark.

**Palette as named hues:** background is near-black warm charcoal (espresso), card one step lighter; text white → gray ramp. Sage green on logo, active nav, icon tile, primary button. Orange/coral on the reminder pill. No paper neutral anywhere; ochre and slate absent.

**Typography:** single small sans. H1 ~18–20px semibold; subtitle ~12px; label ~10px tracked caps; nav ~11px; footer ~11px. Compressed scale — h1 barely outranks body.

**Spacing:** bars tight and stacked; card padding generous (~32px); consistent vertical gaps heading→label→field→button; large empty side gutters. Calm, but small type floating in large containers.

**Component quality:** clean pills, ghost buttons, filled button, single-hairline bezels; nothing crude inside the card.

Compliant: exactly one primary action; sage used with discipline.

## Defects

- **[P0] Whole frame** — rendered in dark mode against the committed light "warm paper clinic" system; zero paper neutrals present. Theme-level system violation, not a variant.
- **[P0] Nav bar, right edge (x≈530)** — 11th nav item clipped to a sliver by the viewport: truncated element, no overflow/scroll affordance. Reads as broken.
- **[P1] App bar right, reminder pill** — orange/coral used for "reminder due soon"; reminder is caution (ochre) per the committed semantics, coral is reserved for danger.
- **[P1] Footer disclaimer** — dim gray on near-black, ~3:1 at ~11px; fails AA on legally/trust-critical copy for the exact audience (sick, overwhelmed) this tool serves.
- **[P1] Nav row** — ~11px items with tight gaps: 10+ undersized targets crowd the core IA; needs grouping or an overflow menu.
- **[P1] Card, heading block** — hierarchy collapse: 18px h1 vs 12px subtitle reads flat; the view's title doesn't command its panel.
- **[P1] Main card** — single hairline bezel; system specifies double-bezel workbench panels.
- **[P2] Card interior** — subtitle gray, label gray, placeholder gray and textarea border sit in the same tone band; label barely separates from field.
- **[P2] App bar right** — ghost icon buttons have no visible affordance and mismatch the pill's visual weight beside them.
- **[P2] Under textarea, right side** — button bottom-left leaves a dead zone across the remaining ~70% of the row; either full-width primary or intentional asymmetry worth stating.
- **[P2] Viewport** — card pinned to a narrow center column with heavy empty gutters either side; width strategy unclear at this size.

**Verdict:** fail — the P0 theme violation alone breaks the committed system; fix theme, unclip the nav, then contrast.
