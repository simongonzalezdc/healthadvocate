judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/light-coverage.png)

I can see the image. Auditing it.

## Description

**Layout, top to bottom:** white header band — dark forest-green rounded-square logo mark + bold "HealthAdvocate" wordmark left; right cluster: coral-outlined pill "⚠ 1 reminder due soon" + two circular icon buttons (bell, sun). Below, a single-row nav of 11 text items (ointments, Discharge, 2nd Opinion, Recorder, Library, Directory, Scanner, Family, Tracks, Coverage, Help), with "Coverage" as a filled sage pill. Then the paper-toned content area, left-anchored ~440px column: green H1 "Coverage Continuity", one-line grey subtext, small bold label "Case title (synthetic)", one text input (placeholder "e.g. Synthetic job-loss coverage case"), sage filled button "Create Coverage Case". A full-width hairline divider, then a centered two-line grey disclaimer. The bottom ~45% of the viewport is blank paper.

**Palette:** warm off-white paper field, white header/nav bands, sage-green primary button and active nav pill, forest-green logo/heading, coral reminder badge, slate-grey body text. Semantics mostly on-system.

**Type & spacing:** single sans family; scale ≈ 11px nav/labels → 12–13px body → ~22px bold heading. Two steps only — flat hierarchy. Spacing inside the form is calm and consistent; the page-scale rhythm collapses into dead space below.

**Component quality:** pills, icon buttons, input, and button are cleanly drawn, flat, consistent radii — but everything sits naked on the page; none of the committed double-bezel workbench paneling appears.

## Defects

- **P1 — Reminder badge, header right:** coral (danger) on "1 reminder due soon." A due-soon reminder is caution, not danger — per system this should be ochre. As-is it fires a false alarm at fragile users on every screen.
- **P1 — Below the divider, lower half of viewport:** no workbench panel and no empty state. The disclaimer floats mid-page with ~200px of unexplained blank paper beneath it. Reads as an unfinished render; the double-bezel workbench commitment is absent entirely, and a sick first-time user gets no "no cases yet / what happens next" guidance (slate=info opportunity unused).
- **P1 — Nav row, "Coverage" pill:** active state uses the filled sage primary treatment, the same surface as the view's one primary button. Two filled-accent elements compete; the pill should be a quieter selected state (tint/underline).
- **P2 — Nav row, first item:** "ointments" lowercase against "Discharge," "2nd Opinion," etc. — capitalization bug, reads as a defect not a style.
- **P2 — Nav row overall:** 11 items at ~11px with tight gaps; tap targets are thin for the stressed/diminishing-eyesight audience this tool serves.
- **P2 — Input, form:** border is barely a step above the paper fill and placeholder grey is low-contrast; the field's affordance nearly disappears.
- **P2 — Label + placeholder:** "(synthetic)" in "Case title (synthetic)" and "Synthetic job-loss coverage case" is test-fixture language leaking into user-facing copy — meaningless to patients.
- **P2 — Footer disclaimer:** centered under a left-aligned content column; the alignment switch plus the hairline's full-bleed-vs-column mismatch makes it read as an afterthought.
- **P2 — Type scale globally:** body copy at ~12px with only a 2-step scale gives the page little hierarchy; subtext and disclaimer sit near the legibility floor.

One point genuinely on-system: the view honors "one primary action per view" — the Create button is the single clear CTA.
