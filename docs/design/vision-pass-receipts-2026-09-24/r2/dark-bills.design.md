judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/dark-bills.png)

Note on attachment: the stated path `…/r2/dark-bills.jpg` doesn't exist — `r2` is itself the JPEG (620×436). I copied it to a `.jpg` name to view it, then deleted the copy. No other files read or written.

# Audit — "dark-bills" (Coverage view, dark variant)

## What I see

**Layout, top to bottom:** (1) Warm-charcoal header bar: sage-green shield/heart logo tile, "HealthAdvocate" wordmark; right side an ochre-outline pill "+1 reminder due soon", two faint square icon buttons, one circular icon button. (2) Full-width nav strip: Moments · Discharge · 2nd Opinion · Reactor · Library · Directory · Scanner · Family · Tracks · **Coverage** (active, sage pill, dark text) · Help. (3) Narrow centered content column: H1 "Coverage Continuity"; two-sentence subtitle ending "No payments or submissions from this screen."; muted line "Case title (synthetic)"; dark bordered text input, placeholder "e.g. Synthetic job-loss coverage case"; sage filled button "Create Coverage Case". (4) ~45% of viewport empty. (5) Centered muted disclaimer footer ("…Always consult a qualified healthcare provider…"), floating mid-viewport with dead space below.

**Palette:** This is a dark inversion — near-black warm charcoal ground, off-white text, sage-green accent on logo/active pill/primary button, ochre badge. No warm paper neutrals present. Coral/slate not in play (nothing danger/info on this view).

**Typography:** All sans, compressed scale — H1 ≈ 17–18px, body/label ≈ 10–11px, nav ≈ 8–9px at this capture width. Weight does most of the work; size steps are shallow.

**Spacing rhythm:** Tight header/nav; small heading→subtitle→label→input gaps; then one huge unstructured void (form→footer) and again footer→bottom. Rhythm is inverted: smallest gap sits exactly where a boundary is needed (subtitle vs field label).

**Component quality:** Input and button share radius, button contrast is good, active nav pill is clear — these are fine. Icon buttons and label/placeholder fall below contrast comfort.

## Defects

- **P1 — Whole-view dark inversion violates the committed system.** "Warm paper clinic" is the identity; this page renders as warm charcoal. If dark is a sanctioned variant, it isn't in the named system — as shipped it reads as a different product. Location: entire frame.
- **P1 — Badge copy reads as broken interpolation.** Top-right header pill: "+1 reminder due soon" — the "+1" prefix reads like a templating artifact ("1 reminder due soon" intended). Also weak pluralization ("reminders due" if count grows).
- **P1 — Field label merges into the paragraph above it.** "Case title (synthetic)" (below subtitle) is the same muted tone and near-identical size as the subtitle, so it reads as a wrapped sentence fragment, not a label. Needs size/weight/casing separation from subtitle, proximity to input.
- **P1 — Sub-4.5:1 text on dark.** Placeholder "e.g. Synthetic job-loss coverage case" and the label line are dim gray on charcoal — below comfortable legibility for the stated audience (sick, overwhelmed users). Location: form input + label.
- **P1 — Nav is overcrowded with undersized targets.** 11 items at this width, ~8–9px text, ~20px target height. Moments…Help, nav strip. For this audience that's a usability failure; needs grouping or overflow at narrow widths.
- **P1 — Dev-speak leaking to users.** "synthetic" appears twice as user-facing copy (label + placeholder). If this is demo-seed language, it shouldn't ship; if it's a real privacy claim, it's the wrong word. Location: label line + input placeholder.
- **P2 — Committed double-bezel workbench panel is absent.** The form floats bare on the ground; no bezelled panel anywhere. Either apply the panel or this view reads unfinished. Location: content column.
- **P2 — Type hierarchy too flat.** H1 barely clears body size; nav is smaller still but the heading/subtitle/label trio sits in one tonal band. Location: content column.
- **P2 — Footer floats mid-viewport with dead space below.** Content ends ~55% down; disclaimer sits unanchored, then ~45% empty ground. Bottom third of frame, and form→footer gap.
- **P2 — Header icon buttons have near-zero affordance.** Two square + one circular button, dark icons on dark ground, no labels/tooltips visible. Header top-right.

**Complies:** exactly one primary action (sage "Create Coverage Case", correct accent role); ochre used only for the caution badge; coral/slate correctly absent; sage reserved for primary/active states.
