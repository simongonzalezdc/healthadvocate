judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/dark-symptoms-emergency.png)

I can see the image. Audit follows.

## Description

**Layout (top→bottom):** Header bar (sage shield logo + "HealthAdvocate" wordmark; right: green "+ 1 due soon" pill, two ghost icon buttons) → horizontal nav tab row (Symptoms active, 9 more tabs) → one large centered charcoal card containing: coral icon + "SYMPTOM ASSESSMENT" eyebrow with intro line, "WHAT ARE YOU EXPERIENCING?" label + textarea (pre-filled "chest pain and shortness of breath for the past hour"), coral "Assess Symptoms" pill CTA, then a red result panel ("This needs a human decision" + helpline bullets + links), then stacked result sections: URGENCY LEVEL (red "● HIGH" pill), EXPLANATION paragraph, POSSIBLE CONDITIONS (two text rows with percentages), ACTION ITEMS (numbered list), NAME OVERLAP (INFORMAL) with a "low" badge, and a red "Urgency disagreement detected" banner → centered dim footer disclaimer bar.

**Palette:** Cool near-black page, slightly lighter charcoal card, coral/salmon as the loudest hue (icon chip, CTA, urgency, banners), muted sage only in logo + "1 due soon" pill, mid-grey secondary text. Effectively a dark mode; no warm paper neutrals present.

**Type scale:** Flat — tiny uppercase letter-spaced eyebrows, body ~13–14px, bold wordmark; almost no size hierarchy between labels, body, and section content.

**Spacing rhythm:** Generous and consistent vertical gaps between sections; calm, single-column, one CTA — the best thing in the shot.

**Component quality:** Pills, textarea, and panels share consistent radii and subtle borders; the red alert panel and banner are cleanly built but text-heavy.

## Defects

- **P0 — Dishonest data:** POSSIBLE CONDITIONS shows "chest pain (87%)" / "shortness of breath (85%)" while EXPLANATION two lines above states the model is unavailable/blocked. Percentages have no source — false precision in a medical tool.
- **P0 — Garbled copy:** ACTION ITEMS item 2: "Schedule a follow-up only made routine only if you need generated drafts." Broken sentence.
- **P0 — Internal jargon leaking to users:** Result panel bullet: "Find and contact a human using the stripped validation errors." (raw error text); link: "Your insurance resource department — varies byogos" (truncated/garbled, panel, "Find help near you" list).
- **P1 — CTA color breaks the system:** "Assess Symptoms" is coral; system commits sage=primary, coral=danger. The one primary action and the emergency panel share the same hue ~150px apart, so danger signaling and primary action compete.
- **P1 — Palette off-system:** Entire view is cool graphite/black; no warm-paper neutral anywhere. Even as a dark variant, surfaces lose the "warm clinic" identity.
- **P1 — Danger saturation:** Five coral/red elements in one column (section icon chip, CTA, alert panel, HIGH pill, disagreement banner). Nothing reads as *the* most urgent thing — hierarchy collapses exactly when the user is panicking.
- **P1 — Dev telemetry as UI:** NAME OVERLAP (INFORMAL) section — "overlap check between two extraction methods — not a check of clinical accuracy" is meaningless to patients and erodes trust; cut or translate.
- **P1 — Legibility for the audience:** EXPLANATION body, inactive nav tabs, and the "low" badge are mid-grey on charcoal — marginal contrast for sick, possibly older users.
- **P2 — Flat type scale:** Six same-weight eyebrow labels (WHAT ARE YOU EXPERIENCING? → NAME OVERLAP) all within ~2px of body size; "SYMPTOM ASSESSMENT" is an eyebrow, not a heading — no anchor for the page.
- **P2 — POSSIBLE CONDITIONS has no visual encoding:** bare text rows with a hairline divider; 87% vs 85% indistinguishable at a glance.
- **P2 — Weak link affordance in the alert panel:** the clinic-finder / insurance / patient-advocate links read as bold body text; these are the most important actions on the page.
- **P2 — Active tab under-specified:** "Symptoms" differs from inactive tabs only by a faint pill fill.
- **P2 — Header right cluster noise:** "+ 1 due soon" pill, keyboard icon, and moon icon are near-equal weight, competing with the wordmark.

**Net:** structure, spacing, and single-CTA discipline are good; the failures are honesty (unsourced percentages, garbled/internal copy) and color semantics (coral doing five jobs including the primary action). Fix the three P0s before any visual polish.
