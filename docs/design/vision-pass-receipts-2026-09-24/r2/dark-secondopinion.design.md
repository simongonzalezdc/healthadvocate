judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/dark-secondopinion.png)

Audited. (Path note: the attached path `judge-img/r2/dark-secondopinion.jpg` didn't exist — `r2` is itself a file, a 620×436 JPEG byte-identical to `r2-attached-dark-insurance.jpg`. I judged that image.)

## DESCRIBE

**Layout, top→bottom.** Dark header band: left — sage rounded-square logo tile (heart glyph) + "HealthAdvocate" wordmark; right — ochre-outlined status pill "• 1 reminder due soon" + two ghost icon buttons (bell, moon/theme-toggle). Below it, a single-row nav of 11 small text items (…ments → Discharge → 2nd Opinion → Recorder → Library → Directory → Scanner → Family → Tracks → Coverage [active pill] → Help). Content column (~centered, wide side margins): H1 "Coverage Continuity", one-line gray subtitle, small label "Case title (synthetic)", full-column-width rounded input with placeholder, sage pill button "Create Coverage Case". Hairline divider, then a small centered two-line disclaimer footer — which floats at ~55% viewport height; the bottom ~45% is empty background.

**Palette (as rendered).** This is a DARK rendering, not warm paper: page bg warm charcoal-black ≈ `#181713`; header band `#232019`; input fill `#1F1B17`. All darks carry a warm (yellow-brown) undertone — internally consistent. Sage accent on the button ≈ `#73A87E` (fill) with dark text; active-nav sage ≈ `#849A85` on a dark-olive pill. Caution ochre kept on the reminder pill (amber text, brown border). Text: warm white `#FEFDF9` (H1), warm gray `#D6D5D1` (subtitle), `#7C7974` (placeholder).

**Typography.** Compressed scale, ~4 visible steps: H1 ~18px bold; body/label/input/button ~10–11px (button semibold); nav ~10px; footer ~9px. H1:body ratio ≈ 1.6 — hierarchy carried almost entirely by weight/color, not size.

**Spacing.** Page side margins generous (~16% each side); component-level gaps tight (~7–14px between subtitle/label/input/button); then a huge unstructured void below the footer.

**Component quality.** Consistent fully-rounded "pill" language across nav-active, reminder chip, button, and input — the input reads as a second button. No double-bezel workbench panel anywhere; content sits bare on the canvas with one hairline divider. No visible elevation or focus affordances.

## DEFECTS

- **P0 — Nav first item clipped at left viewport edge** (nav row, far left): label renders as "…iments" — "Appointments" (or similar) is cut off with no truncation affordance. Nav row also ignores the page grid: it bleeds edge-to-edge while logo tile, H1, and form align to the ~16% side margins.
- **P1 — Dark theme contradicts the committed system** (entire canvas): "warm paper clinic" is a light warm-paper system; this renders near-black charcoal. Warm undertones are kept and a moon-toggle exists, so it may be a sanctioned dark variant — but the paper identity is lost; needs explicit design-system signoff, otherwise this is a brand-level violation.
- **P1 — Double-bezel workbench panel missing** (content zone): the form sits naked on the background with only a hairline divider; the committed panel component is absent from the view.
- **P1 — ~45% viewport dead void** (below disclaimer, bottom half): footer is not bottom-anchored and floats mid-page above a large empty field; reads unfinished rather than calm.
- **P1 — Oversized input competes with the primary action** (form zone): full-column-width (~2/3 viewport) pill-shaped empty field for a short case title; it out-sizes the sage CTA below it and pulls first attention. Needs a max-width form group; CTA should dominate.
- **P2 — Placeholder contrast below WCAG for small text** (input, form zone): `#7C7974` on `#1F1B17` ≈ 3.9:1 (< 4.5:1 at ~11px).
- **P2 — Active nav contrast borderline** (nav row, "Coverage"): sage `#849A85` on dark-olive pill ≈ 4.6:1 at ~10px — passes by a hair; darken pill bg or lighten text.
- **P2 — Header icon buttons weak affordances** (header right): bell and moon glyphs are dark-warm-gray on dark; at a glance they vanish into the band.
- **P2 — Cramped nav** (nav row): 11 items of ~10px labels at ~14px gaps with no grouping or overflow treatment (the P0 clip is the symptom).
- **P2 — Rhythm inconsistency in form zone**: subtitle→label gap ~12px vs label→input ~7px vs input→button ~14px — three different steps in one small block; label momentarily reads as a third subtitle line.
- **P2 — Footer disclaimer centered** (footer band): two lines of ~9px centered gray text across the full column; long centered text is harder to scan — left-align to the content grid.

**What's right:** exactly one primary action (sage, correct accent); ochre/coral semantics not misused; coral correctly absent (no danger on this view); warm undertone maintained across all dark surfaces; L/R content margins align header-to-form; copy tone matches the advocacy mission.
