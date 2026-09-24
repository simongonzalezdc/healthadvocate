judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-directory.png)

I can see the image. Audit follows.

## What I see

**Layout (top→bottom):** Slim app header — sage logo tile + "HealthAdvocate" wordmark left; ochre "1 due soon" pill, bell, gear right. Below: single-row text nav (Documents … Library, Directory active in a sage pill, then a clipped "+" at the right viewport edge). Centered paper card: "DIRECTORY" eyebrow, intro icon + paragraph, coral "DEMO DATA" pill at right; full-width search field; 7 filter chips (All active, sage); a two-line micro legend explaining provenance tags; four provider cards (Dr. Maya Patel / Riverside Imaging / Aetna member services / Corner Pharmacy), each with icon chip, title, uppercase type tag right, "Merged from…" provenance line, label–value rows with provenance pills and ghost "Confirm" buttons, and a Call / Items in Library footer row. Centered two-line micro disclaimer footer.

**Palette:** Warm paper background, slightly darker beige card panels, warm-gray ink. Sage = logo, active chip, YOU CONFIRMED pills. Coral = DEMO DATA pill, INFERRED·PATTERN/LETTER/VOICEMAIL tags, card-3 icon tint. Ochre = "1 due soon", BILL DECODE tag. Slate = CALL/DOCUMENT tags. Matches the committed system.

**Type:** One sans family; bold ~13px card titles; ~10–11px body; 8–9px uppercase eyebrows, tags, meta, footer. Everything is small.

**Spacing/component quality:** Generous, consistent card padding (~24px) and inter-card gaps; double bezel reads correctly (outer card + inner bordered panels); chips and pills have consistent radii. Calm overall. Craft is real; scale and a few semantics are the problem.

## Defects

1. **P0 — Nav, far right edge:** the last nav item ("+") is clipped mid-glyph by the viewport edge. Overflow with no scroll/overflow affordance; the add-provider action — arguably this view's primary action — is unreachable. 
2. **P1 — Global type scale:** meta/labels/tags/footer sit at ~8–10px. For the stated audience (sick, overwhelmed people) this is a usability failure, especially the provenance line, legend, and Confirm buttons — the features that carry trust.
3. **P1 — Legend vs. tag vocabulary:** legend defines only "FROM A CALL" and "INFERRED"; cards render "CALL," "VOICEMAIL," "BILL DECODE," "DOCUMENT," "INFERRED · PATTERN," "INFERRED · LETTER," "INFERRED · VOICEMAIL." Legend says "FROM A CALL," tags say "CALL." The legend under-explains the exact system it introduces, in a trust-critical mechanic.
4. **P1 — Provenance pills on the right of card headers:** "DOCTOR · ORTHOPEDICS" etc. sit right-aligned at ~9px with wide letter-spacing — lowest-legibility text on the page carrying classification info.
5. **P1 — "Confirm" ghost buttons:** ~9px light-gray text on beige; near-invisible affordance for the corrective action the intro copy explicitly invites ("Nothing to type unless you're correcting something"). Contrast likely below 4.5:1.
6. **P1 — Intro block, right side:** coral "DEMO DATA" pill misuses the danger hue for a non-danger state; in this system coral primes "something is wrong" for users who are already anxious. Slate (info) or ochre fits.
7. **P2 — Card 1, ADDRESS row:** value + "BILL DECODE" + Confirm wrap to a second line with no hanging indent; the wrapped tag/Confirm don't align to the value column. Same risk on card 2, HOURS row.
8. **P2 — All cards, row grid:** values start inline after labels of varying widths (PHONE vs APPEALS FAX), so the value column is ragged down each card. A fixed label column would scan better.
9. **P2 — Card 3 icon chip:** tint skews coral while every other card's chip is sage/neutral — reads as a danger flag on an insurer card for no stated reason.
10. **P2 — Legend block, second line:** "YOU CONFIRMED ✓" pill orphaned above "— confirmed information always wins over inference." Awkward two-line break; pull the dash text onto one line or restructure as a proper key.
11. **P2 — HOURS dash inconsistency:** card 2 uses hyphens ("7:00-19:00"), card 4 uses en dash ("8:00–21:00"). Pick one.
12. **P2 — Zero primary action:** system commits to one primary action per view; this view has none (Call is ghost ×4, add is the clipped "+"). One sage-filled "Add provider" (or a visible "+") would satisfy the system and fix #1's discoverability half.
13. **P2 — Search field:** placeholder gray on paper is low-contrast for the primary entry point of the view.

**Summary:** Structure, spacing, and palette are on-system and genuinely calm; the failures are legibility at micro scale (#2), an incomplete provenance legend (#3), and one real break — the clipped nav item (#1).
