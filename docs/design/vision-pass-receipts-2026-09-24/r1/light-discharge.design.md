judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-discharge.png)

I can see the image. Audit follows.

## Description

**Layout (top→bottom):** Cream header bar — sage logo chip (heart) + "HealthAdvocate" wordmark left; ochre "▲ 1 due soon" pill + two circular icon buttons (help "?", sun/theme) right. Below: single-row nav of 10 items (Symptoms → Library), "Discharge" active with a faint pill tint, full-width hairline under it. Main area (slightly lighter off-white): one centered double-bezel card — icon chip + "DISCHARGE TRANSLATOR" caps title, one-line gray subtitle, caps field label "PASTE DISCHARGE INSTRUCTIONS", full-width paper-tinted textarea with placeholder, sage "Translate" button (left-aligned, the only filled control — one primary action ✓). Hairline, then two-line centered gray disclaimer footer with bolded brand name. Full-bleed coral strip at the very bottom viewport edge.

**Palette as named hues:** warm paper neutrals (cream header, off-white canvas, white card, paper-tint field) ✓; sage-green reserved for logo + Translate ✓; ochre on the due-soon badge ✓; coral only at the bottom strip; slate/gray for labels and body.

**Type scale:** compressed and small throughout — wordmark ~14px bold, nav ~11px, card title/field label ~9–10px letterspaced caps, placeholder ~12px, footer ~9px. No sentence-case heading larger than body anywhere.

**Spacing rhythm:** card padding generous and even; header/nav compact; large empty paper band between footer and viewport bottom.

**Component quality:** pills, chip, and bezels are consistent; soft shadow restrained; native textarea resize grip exposed.

## Defects

1. **P1 — Viewport bottom, full-bleed coral strip (~10px), unlabeled.** Coral=danger in this system; an unexplained danger-colored band at screen edge reads as an alarm or a cut-off emergency banner. Dishonest use of the danger hue if decorative; truncated content if not.
2. **P1 — Global type scale too small for the audience.** Field label and footer sit ~9–10px, caps labels ~9px. For sick, overwhelmed users this is a legibility failure; body/placeholder should be 14–16px floor, labels ≥11px.
3. **P1 — Card header hierarchy collapse.** "DISCHARGE TRANSLATOR" and "PASTE DISCHARGE INSTRUCTIONS" are near-identical tiny letterspaced gray caps ~20px apart; the view's title doesn't outrank its field label. Make the title sentence-case, ink-colored, ~16–18px.
4. **P2 — Nav row, ~x90–530:** 10 top-level items tracked tightly with no overflow affordance; at this width "Appointments/Discharge/2nd Opinion" already crowd, and the active pill's padding makes its gaps read looser than neighbors.
5. **P2 — Card icon chip (top-left):** arrow glyph is pale gray on a barely-bordered paper square — near-invisible at 100%; raise ink or drop the chip.
6. **P2 — Textarea bottom-right:** native resize grip exposed inside a finished bezel panel; invites users to break the calm layout. Disable resize.
7. **P2 — Below-footer dead zone (y≈360→bottom):** ~70px of empty paper ending in the coral strip makes the page read unfinished; close the canvas or anchor the footer.

**Net:** on-system palette and calm structure, one-primary-action discipline holds — but the unlabeled coral band, tiny type, and flat title hierarchy need fixing before ship.
