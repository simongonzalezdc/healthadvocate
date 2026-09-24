judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/dark-recorder-consent-checked.png)

I can see the image — auditing it directly, no files touched.

## Description

**Layout (top-to-bottom):** App bar (logo mark + "HealthAdvocate" wordmark left; ochre "● 1 due soon" pill, bell and "?" circular icon buttons right) → secondary nav of 9 items (Symptoms … Library), active "Recorder" in a sage pill → one centered double-bezel workbench panel containing: header row (dark-maroon mic chip, "CALL RECORDER" eyebrow + 4-line intro paragraph, outlined "● DEMO MODE" pill right), a full-width sage-tinted trust banner ("Stay on this device — never uploaded, never sent"), a nested "Before you record" card (rationale paragraph, checked sage consent checkbox in an outlined row, sage-filled pill button "Start demo recording"), then a "YOUR RECORDINGS (DEMO)" list: row 1 "Anita — MRI denial call · Sep 24 · 11:03" with ghost buttons Library + Delete; row 2 "Start over with the synthetic call script." with ghost "New demo recording" → centered 2-line disclaimer footer.

**Palette:** Background and surfaces are neutral-charcoal darks, not warm paper. Sage green carries logo glyph, banner tint, checkbox, active nav pill, primary button. Ochre appears only on the due-soon badge. A muted maroon/coral-dark chip sits behind the mic. Slate-gray for the DEMO MODE pill, ghost buttons, and muted text.

**Type scale:** Everything lives in two registers — ~10–11px letter-spaced uppercase eyebrows/labels and ~11–12px body. No true heading; the view opens at label size. Nav and footer text are the smallest and dimmest.

**Spacing rhythm:** Generous and calm inside the panel (consistent card padding, clear banner/card/button gaps); the app bar and nav are comparatively tight.

**Component quality:** Pills, banners, nested bezels and buttons are consistently rounded and cleanly rendered; nothing looks broken or misrendered.

## Defects

- **P0 — Consent checkbox is shown pre-checked** (consent row, "Before you record" card). If this is the shipped default rather than user-set state, it's a pre-checked-consent dark pattern — legally hollow and dishonest for this audience. Must default unchecked.
- **P1 — Whole-theme drift from the committed system** (global). "Warm paper clinic" is a light, warm-neutral system; this render is a neutral-cool charcoal dark theme. Unless a sanctioned dark variant exists, this is off-system, and the paper warmth is entirely absent.
- **P1 — Low-contrast small type on dark surfaces** (secondary nav labels; intro paragraph under CALL RECORDER; "Before you record" paragraph; footer line). All sit around ~4:1 or below at 11–12px — below AA, and the users are described as sick and overwhelmed.
- **P1 — "Delete" styled identically to "Library"** (recordings row 1, right cluster). Destructive action carries no coral/danger semantic; a mis-tap destroys a recording.
- **P1 — Consent hierarchy inverted** (consent block). The legally load-bearing text is the smallest, dimmest copy on the page, while a sage trust banner above it gets the visual emphasis. The thing users must actually read has the least presence.
- **P2 — Coral-dark mic chip in idle state** (CALL RECORDER header, left). Danger hue used as decoration before anything is recording, and the maroon-on-maroon glyph contrast is very poor.
- **P2 — Duplicate recording verbs** ("Start demo recording" primary; "New demo recording" ghost, row 2). Two CTAs for the same action in one view weakens the one-primary-action rule.
- **P2 — Banner icon is a warning-triangle shape in sage** ("Stay on this device" strip). Warning shape + non-caution hue blurs the ochre=caution language; at this size it reads as mush.
- **P2 — Nav density** (secondary nav). Nine ~11px items with tight gaps; the active sage pill is also the only other sage fill besides the primary button, slightly diluting the accent.
- **P2 — No view title** (panel header). "CALL RECORDER" is an eyebrow, not an H1; the scale never gets bigger than 12px anywhere in the view.
- **P2 — Bell and "?" icon buttons near-invisible** (app bar, right). Dark-gray-on-dark affordances.
- **P2 — "Start over with the synthetic call script." reads as disabled copy** (recordings row 2) — placeholder-toned text sitting in an actionable row.

**Correct usages worth keeping:** ochre confined to the due-soon badge, single sage-filled primary, double-bezel nesting, calm panel spacing.
