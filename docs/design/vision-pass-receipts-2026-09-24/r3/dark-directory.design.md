judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-directory.png)

The image is visible — auditing it now. No files read or written.

## What I see

**Layout, top-to-bottom:** Fixed header (logo + wordmark left; ochre "Reminder due soon" pill, plus-button, history-button right) → horizontal nav of 11 tabs, "Directory" active in a sage pill → large inset workbench panel containing: "Directory" heading with small icon + "DEMO DATA" outline pill, two-line intro paragraph, full-width search field, filter chip row ("All" active in sage), an inline legend sentence with three colored source chips, then four provider cards (Dr. Maya Patel / doctor; Riverside Imaging / imaging center; Aetna member services / insurer; Corner Pharmacy / pharmacy), each with provenance line, PHONE/ADDRESS/HOURS-style rows each followed by a source chip + "Confirm" ghost action, and footer ghost buttons ("Call", "Items in Library") → centered dim disclaimer footer.

**Palette as named hues:** This is a *dark* rendering: near-black warm charcoal page, slightly lifted dark-brown panel, dark inset cards. Sage green = logo tile, active nav pill, active "All" chip, "YOU CONFIRMED ✓" chips. Ochre = reminder pill, "INFERRED" chips. Slate = "FROM A CALL"/"VOICEMAIL" chips, category labels, metadata. Coral: absent on this view. Text: off-white headings, mid-gray body, very dim gray metadata/actions.

**Type scale:** Compressed. One modest heading (~2 steps above nothing else); everything else lives in two small sizes — 12–13px body and ~10px letterspaced caps/chips. Hierarchy is carried almost entirely by opacity, not size or weight.

**Spacing rhythm:** Genuinely calm and consistent — generous panel inset, even card gaps, aligned label/value rows. This is the strongest dimension.

**Component quality:** Cards, chips, and pills are cleanly drawn and internally consistent; ghost buttons uniform. Craft is decent; contrast and semantic color discipline are the failures.

## Defects

1. **P0 — Global palette betrayal.** Entire view is charcoal-on-black; the committed "warm paper neutrals" identity is nowhere present. As a dark variant it may be intentional, but nothing here (no warm paper tint, no tone mapping note) says "same clinic, lights off" — it reads as a different product. Biggest systemic deviation on the page.
2. **P0 — Illegible micro-text.** Provenance lines ("Merged from 3 sources: Appointment card (Sep 12)…", card 1) and every per-row "Confirm" action are dim gray at ~10–11px on dark cards — well below readable contrast for the overwhelmed, possibly low-vision users this tool is for. The single most important action in the view (Confirm) is the weakest thing on the page.
3. **P1 — Clipped nav item.** Last tab after "Directory" is cut at the right viewport edge ("Se…") with no scroll affordance or fade — reads as broken, and "Settings" being unreachable is a usability failure.
4. **P1 — Sage double-duty.** Sage is both the advocate/action accent (active nav, active filter) and the "YOU CONFIRMED ✓" status color. The system defines slate/ochre/coral semantics but no success hue, so confirmation status and "this is selected/primary" are visually identical — dilutes "one primary action per view."
5. **P1 — No primary action, loudest thing is a notification.** The content area has zero filled primary actions (all ghosts), while the ochre "Reminder due soon" pill is the most saturated element on screen, parked above the nav. Attention inverts: chrome shouts, work whispers.
6. **P1 — Legend sentence clutter.** The inline chips (FROM A CALL / INFERRED / YOU CONFIRMED ✓) inside the explanatory paragraph render larger than the text around them, breaking baseline and reading rhythm; the legend would read better as a compact key row under the chips.
7. **P2 — Compressed type scale.** "Directory" heading barely outranks body copy; category labels ("DOCTOR · ORTHOPEDICS", card 1) and nav tabs (~10px caps) are below comfortable size for this audience.
8. **P2 — Chip repetition noise.** Corner Pharmacy card carries three identical "YOU CONFIRMED ✓" chips in a row; per-field status could collapse to a single card-level "all confirmed" state.
9. **P2 — Possible truncated address.** Card 1 ADDRESS reads "410 Center St, Big C, Portland OR" — "Big C" looks like a truncation without an ellipsis, which would be dishonest data display. Verify.
10. **P2 — Real brand in demo data.** "Aetna member services" alongside a "DEMO DATA" badge; swap for a fictional insurer so demo mode can't be mistaken for a real record.
11. **P2 — Ambiguous header icons.** The circular "+" button (plus what?) and history clock right of the reminder pill are dim, unlabeled, and semantically unrelated to each other.
12. **P2 — Provenance dates unsorted.** Card 1 merges "Sep 12, Sep 24, Aug 30" — not chronological; trivially sortable, currently reads sloppy.

**Net:** structure, spacing, and honesty model (source-per-field, DEMO DATA badge) are genuinely good. The view fails the design system on palette (dark vs. warm paper) and fails its users on micro-text contrast — fix #1–#3 before anything else.
