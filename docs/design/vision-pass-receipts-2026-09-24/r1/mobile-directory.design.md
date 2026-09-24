judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/mobile-directory.png)

I can see the image. Audit follows.

## Description

**Layout, top to bottom:** Header bar (sage rounded-square heart logo + "HealthAdvocate" wordmark, ochre "due soon" pill with a tiny count glyph, home and theme-toggle icon buttons) → horizontal tab strip (2nd Opinion / Recorder / Library / **Directory** active in a sage-tinted pill / fifth tab clipped at right edge) → one white double-bezel panel on cream ground containing: sage letterspaced eyebrow "DIRECTORY", a 9-line intro paragraph flanked left by a circular person icon and right by a dashed "DEMO DATA" badge, a search input, six filter chips wrapping across three rows (All selected), a provenance legend (slate "FROM A CALL", coral "INFERRED", sage "YOU CONFIRMED ✓" chips inline in a sentence) → four putty-gray provider cards (Dr. Maya Patel, Riverside Imaging, Aetna member services, Corner Pharmacy), each with icon tile, name, micro-caps specialty tag, "Merged from N sources…" line, labeled field rows (PHONE / ADDRESS / EMAIL / HOURS / APPEALS FAX) each with a provenance chip, occasional quiet "Confirm" outline buttons, and a Call + "Items in Library" action row → bold footer disclaimer.

**Palette:** cream/eggshell ground, putty-gray cards, dark ink headings — warm paper as committed. Sage = logo, active tab, eyebrow, confirmed chips (correct). Ochre = "due soon" (correct caution). Slate = provenance chips. Coral = "INFERRED" chips and the Aetna icon tile (misuse — see defects).

**Type scale:** compressed and top-light — wordmark and card names ~16–17px semibold; intro ~13px; provenance lines ~11px gray; field labels and chips ~10px letterspaced caps. Five-plus sizes below 13px.

**Spacing rhythm:** generous and calm between panel, cards, and sections; tighter inside cards where chip rows nearly touch value text. Consistent radii throughout.

**Component quality:** chips and buttons well-formed, consistent; cards uniform except Aetna's coral tile; two orphaned Confirm wraps break the row pattern.

## Defects

1. **P1 — Intro block (top of panel):** paragraph squeezed to a ~30–35ch measure between the person icon (left) and DEMO DATA badge (right), both vertically centered against 9 lines of text. The most important onboarding copy gets the worst measure on the page.
2. **P1 — Search input:** placeholder hard-clips mid-word — "…phone n" — no ellipsis. Reads as broken and hides the supported query types.
3. **P1 — Coral misuse:** INFERRED / INFERRED · PATTERN / INFERRED · VOICEMAIL / INFERRED · LETTER chips (Patel email, Riverside hours, Aetna fax) use coral=danger for routine provenance. In a medical app this trains users to ignore the danger channel. Compounding: Aetna's icon tile is coral-tinted while all other cards are neutral — the insurer reads as danger for no reason.
4. **P1 — Orphaned Confirm buttons:** Riverside (below the HOURS chip row) and Aetna (below the PHONE row) each wrap "Confirm" alone onto its own row — ambiguous which field it confirms. All other cards keep chip+Confirm inline; inconsistent and a mis-tap risk.
5. **P1 — Action hierarchy:** seven equal-weight "Confirm" outline buttons across four cards, competing with Call and Items in Library at the same visual weight. No batch confirm, no per-card primary. Violates the one-primary-action commitment in spirit; heavy decision load for overwhelmed users.
6. **P1 — Micro-typography legibility:** field labels (PHONE, ADDRESS, EMAIL, HOURS, APPEALS FAX), chip text, and gray provenance lines are ~10–11px letterspaced caps / small gray on cream — borderline contrast, and the densest content is set smallest for exactly the users who can't squint.
7. **P2 — Vocabulary drift:** legend teaches "FROM A CALL" but cards say "CALL" and "VOICEMAIL"; legend shows bare "INFERRED" vs. card variants. Legend chips also wrap awkwardly mid-sentence across three lines.
8. **P2 — Tab strip:** fifth tab clipped to "So…" at the right edge with no fade or scroll affordance.
9. **P2 — Patel card provenance line:** "Appointment card (Sep 12) · Call transcript (Sep 24) · Bill decode (Aug 30)" — dates not in order. Small thing, but this product lives on trust.
10. **P2 — Header crowding:** logo + wordmark + ochre pill + two icon buttons; the count glyph inside the pill is barely legible.
11. **P2 — Layering:** putty cards inside the white panel sit too close in value — the double-bezel read goes muddy, and card boundaries soften.

No P0s: nothing is dishonest, overlapping, or truly illegible; the DEMO DATA badge and provenance system are admirably honest touches. Priorities: fix coral semantics (3), Confirm orphans (4), and the intro measure (1) first.
