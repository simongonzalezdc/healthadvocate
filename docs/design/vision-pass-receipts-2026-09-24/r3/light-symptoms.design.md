judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/light-symptoms.png)

Image is visible. Audit follows.

## Description

**Layout, top-to-bottom:** White header bar — sage rounded-square logo tile with white pulse glyph + bold "HealthAdvocate" wordmark left; right cluster: cream pill badge "⚠ 1 reminder due soon" in coral, then two small circular icon buttons (account, theme/sun). Below it, a white nav row of text tabs — Symptoms (active, sage pill), Documents, Bills, Insurance, Drugs, Appointments, Discharge, 2nd Opinion, Recorder, Library — hairline rule under the row. Main area is warm paper; one centered white card (~68% width) containing: blush icon tile with coral pulse glyph, "Symptom Assessment" heading + two-line muted description, letter-spaced caps eyebrow "WHAT ARE YOU EXPERIENCING?", a tall off-white textarea with placeholder ("e.g. I've been having chest pain and shortness of breath for the past hour…", resize grip bottom-right), sage "Assess Symptoms" primary button. Full-width hairline divider, then a centered two-line tiny gray disclaimer ("HealthAdvocate is here to support… Your information stays on your device."). Large empty paper band (~20–25% of viewport) below the footer.

**Palette:** Warm paper ground ✓, white panels, sage-green as the sole primary (active tab, button) ✓, coral on badge + icon tile, slate/gray text. No ochre present.

**Type scale:** Very compressed — heading reads ~16–18px, body/placeholder ~13px, eyebrow ~10–11px caps, footer ~10–11px. One weight jump (semibold headings/wordmark); no large display size anywhere.

**Spacing rhythm:** Header/nav tight; card padding generous and consistent; internal stack rhythm even (icon row → eyebrow → input → button); outer margins generous to the point of emptiness. Component quality is clean: pill active state, soft radii, subtle borders, no shadow noise; button aligns flush with input's left edge.

## Defects

- **P1 — Nav overflow clipped.** Far right of the nav row, past "Library," a partial glyph is cut by the viewport edge with no fade, scroll affordance, or overflow menu — a destination is visually broken/unreachable as rendered.
- **P1 — Coral misused on the assessment icon tile** (card top-left). Coral is the danger hue; a neutral entry point to symptom intake dressed in danger reads as alarm to exactly the wrong audience. Should be sage or slate; blush tile stays, glyph recolors.
- **P1 — Vertical balance is inverted.** Content is a small dense cluster in the upper half; ~25% dead paper below the footer (bottom of page). For sick, overwhelmed users the input and heading should carry the viewport — scale type/textarea up or pin footer; as-is the page reads empty.
- **P2 — Reminder badge in coral** (header right). "Reminder due soon" is caution at most — ochre per system; second coral element on screen further dilutes danger semantics.
- **P2 — Low-contrast micro-type.** Eyebrow label and textarea placeholder appear well under 4.5:1 against their fills; footer disclaimer likewise tiny + light. Verify WCAG at full res.
- **P2 — Visible textarea resize grip** (input bottom-right). A drag handle invites layout breakage in a calm, fixed-rhythm panel; disable resize or fix rows.

**System compliance:** one primary action per view ✓, sage reserved for primary ✓, paper/white double surface layering reads correctly, spacing calm. Main gaps are semantic-color discipline (coral) and scale/balance, not component craftsmanship.
