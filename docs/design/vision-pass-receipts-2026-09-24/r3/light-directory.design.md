judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/light-directory.png)

I can see the image — judging it directly, no files touched.

## Description

**Layout, top-to-bottom:** White top bar (logo + wordmark left; coral "1 reminder due soon" pill + two icon-only buttons right). Below it, a horizontal nav row of ~11 items, "Directory" active as a filled sage pill, with a partial item clipped at the right edge. Main content is one centered double-bezel workbench panel on warm paper: panel header ("Directory" + 3-line explainer with icon, "DEMO DATA" badge top-right), full-width search field, filter chip row (All active in sage), a two-line provenance legend with inline sample badges, then four stacked provider cards (Dr. Maya Patel, Riverside Imaging, Aetna member services, Corner Pharmacy). Each card: icon + title left, tiny type label top-right, "merged from N sources" line, then field rows (label · value · provenance badge · "Confirm" ghost link), footer with Call + "Items in Library." Centered disclaimer footer.

**Palette:** Warm paper ground, off-white card surfaces, sage-green as the working accent (logo, active chip, confirmed badges, check icons), slate-blue info badges (CALL, DOCUMENT, VOICEMAIL, BILL DECODE), ochre inferred badges, coral on the reminder pill and Aetna's card icon, charcoal/brown ink text. Semantically consistent: slate=provenance, ochre=inferred, sage=confirmed.

**Typography:** Humanist sans. Scale is heavily compressed at the bottom: page title ~20px bold, card titles ~13px semibold, everything else — micro-labels, badges, source lines, footer — crammed into ~9–11px, mostly caps for labels/badges.

**Spacing rhythm:** Generous and calm; card padding ample, even ~12–16px card gaps, clear bezel separation. The strongest part of the screen.

**Component quality:** Chips, badges, and pills are well-formed with consistent radii; fields read as confident rows. Icon usage across cards is inconsistent (see defects).

## Defects

- **P0 — Nav row, right edge:** the item after "Directory" is clipped mid-glyph at the container edge, no scroll/overflow affordance. Broken + misaligned.
- **P0 — Card 1 (Dr. Patel), EMAIL row:** value renders as literal `[email protected]`. If that string is in the product it's a broken placeholder; if it's a screenshot-redaction artifact, disregard this one.
- **P1 — Card headers, icon column:** three different icon semantics across sibling cards — green check (Patel, Corner Pharmacy), neutral (Riverside), coral alert (Aetna). Patel's check implies fully verified while her EMAIL row is INFERRED — a dishonest summary signal; Aetna's coral spends the danger hue on "merely unconfirmed."
- **P1 — Whole view:** no single primary action. Eight repeated "Confirm" ghost links + per-card "Call" + chips + search + reminder pill all compete; violates the one-primary-action rule and dilutes the actual next step (confirm the inferred fields).
- **P1 — All field rows, micro-labels and badges:** ~9px caps labels (PHONE, ADDRESS, APPEALS FAX) and badge text in light warm gray — borderline legible even in this render; below where contrast should be for sick, overwhelmed, likely older users.
- **P2 — Top bar right:** coral (danger) pill for "1 reminder due soon" — that's caution-grade; ochre is the system's caution hue.
- **P2 — Panel header, top right:** "DEMO DATA" badge text wraps to two lines inside its pill, and sage tinting makes it read like a positive/confirmed state; should be neutral or ochre, one line.
- **P2 — Legend, below chips:** provenance badges inline mid-sentence across two lines ("YOU CONFIRMED ✓ — Confirmed information…") is cluttered; this explainer belongs in a quieter block or help affordance.
- **P2 — Top bar right:** two adjacent unlabeled icon-only buttons (grid, theme toggle) — ambiguous targets, no tooltips visible.
- **P2 — Card 1, rows:** "Confirm" links trail each badge at varying x — no aligned action column; reads ragged inside every card.
- **P2 — Search field:** placeholder-only labeling; no visible label or clear affordance for screen-reader/first-run users.
- **P2 — Render quality:** whole capture is soft (JPEG mush); micro-type suffers most — re-shoot at 2x before next review.

Net: calm, on-system spacing and honest field-level provenance are the strengths; fix the clipped nav and the status-icon dishonesty first, then collapse the Confirm noise into one clear primary action per card.
