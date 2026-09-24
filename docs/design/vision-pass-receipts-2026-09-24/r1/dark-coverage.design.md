judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/dark-coverage.png)

## Description

**Layout, top to bottom.** Dark header bar: sage-green shield/heart logo mark + white "HealthAdvocate" wordmark (left); coral "1 due soon" pill + two round dark icon buttons (bell, moon) right. Below it, a second dark nav bar with 11 text items — Intake, Discharge, 2nd Opinion, Reconcile, Library, Directory, Scanner, Family, Tracks, Coverage, Help — "Coverage" active in a slightly lighter pill. Main canvas: left-aligned column (~x100–520) with H1 "Coverage Continuity", one-line gray subtitle ("Local and private. No payments or submissions from this screen."), a "Case title (synthetic)" label, a dark text input with placeholder, and a single sage "Create Coverage Case" pill button. A centered two-line gray disclaimer sits mid-page (~y232); below it, ~45% of the canvas is empty black.

**Palette.** Surfaces are near-black warm charcoal (three barely-differentiated dark tones: header/nav/canvas). Text: off-white heading, mid-gray body. Sage green on logo and primary button. Coral/orange badge. No paper neutrals anywhere — this is an inverted/dark rendering of the system; sage is the only committed hue that survived.

**Typography.** Single sans family. H1 ~22px semibold; body/subtitle ~13px; nav and labels ~12px; disclaimer ~12px. Scale is compressed — heading is under 2× body.

**Spacing rhythm.** Form internals are calm and regular (label→input→button stack is clean). But the page composition is unbalanced: one narrow column on the left third, vast vacancy right and below.

**Component quality.** Button, input, badge, nav pills all cleanly rendered, consistent radii. Nothing looks broken or illegible.

## Defects

- **P1 — Whole-view palette off-system.** Every surface (header y0–40, nav y40–55, canvas) is charcoal-black; committed warm-paper neutrals are absent. If dark is a sanctioned mode, the paper warmth (and material metaphor) must still translate — it didn't.
- **P1 — No double-bezel workbench panel.** Form (x100–520, y80–180) floats bare on the canvas; the committed panel treatment is entirely missing from the one view where a "workbench" card is most expected.
- **P1 — Nav wayfinding load.** 11 undifferentiated ~12px items across y≈44 with no grouping, separators, or overflow strategy — a heavy index for sick, overwhelmed users to scan.
- **P1 — Semantic color misuse, header badge (x≈425–460, y≈18).** "1 due soon" is a caution-level status rendered in saturated coral/orange. Per system it should be ochre; coral-as-danger gets diluted.
- **P1 — Orphaned disclaimer (y≈225–245).** Centered block floats mid-viewport, ~190px above the bottom edge — anchored to neither the form nor the page foot; reads as an unfinished render.
- **P1 — Dead space composition.** Right ~60% of canvas and bottom ~45% empty; calm spacing has tipped into vacancy. Anchor the disclaimer to the bottom or center the workbench column.
- **P2 — Input affordance (x100–520, y125–143).** Field border contrast against canvas is near-invisible; placeholder gray is borderline. The text-entry zone barely registers as a field.
- **P2 — Active nav state (Coverage pill, x≈450, y≈44).** Pill fill ≈ nav bar fill; the active state reads only as a faint green tint — fails at a glance.
- **P2 — Alignment inconsistency.** Disclaimer is center-aligned (y≈232) while the entire rest of the view is left-aligned.
- **P2 — Dev jargon in UI copy.** "Case title (synthetic)" label and "Synthetic job-loss coverage case" placeholder leak internal vocabulary into lay users' view.
- **P2 — Compressed type scale.** H1 ~22px vs 13px body gives a flat hierarchy; the page has no strong typographic anchor for a calm, confident entry point.

**Passes:** exactly one sage primary action; label-above-input pattern; sage button with dark label has strong contrast; restrained composition inside the form stack. (Motion is not assessable from a still.)
