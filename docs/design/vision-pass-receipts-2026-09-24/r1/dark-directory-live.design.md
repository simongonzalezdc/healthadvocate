judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/dark-directory-live.png)

I can see the image — no file reads needed. Audit follows.

## WHAT I SEE

**Layout, top to bottom:** Charcoal header bar (sage logo mark + "HealthAdvocate" left; coral "⚡ I live soon" pill + 2 icon buttons right) → secondary tab bar (Documents…Directory, sage pill on Directory; last item clipped at right edge showing a stray "S") → one large centered dark workbench panel: "DIRECTORY" overline, intro paragraph + "DEMO DATA" outline pill, full-width search field, filter chip row (All active, sage), a two-line provenance legend ("Feels the app filled in for you…" with FROM A CALL / INFERRED / YOU CONFIRMED ✓ chips), then 4 provider cards (Dr. Maya Patel / Riverside Imaging / Aetna Member Services / Corner Pharmacy), each with tinted icon, title + right-aligned category meta, dim "Merged from N sources…" line, label:value rows (PHONE/ADDRESS/EMAIL/HOURS) each carrying a provenance chip + "Confirm" link, and Call / Items in Library buttons. A cream toast — "Saved to the Library (demo — synthetic only)" — sits on top of card 2's title. Hairline rule, then dim centered footer disclaimer.

**Palette:** background/panels are cool charcoal, not paper; sage present (logo, active tab, All chip, YOU CONFIRMED chips, icons); coral on header pill, BILL DECODE chip, Aetna icon; ochre on INFERRED·* chips; slate on VOICEMAIL/DOCUMENT chips. **Type:** one compressed band, ~9–13px — tiny uppercase chip/label voice, semibold card titles barely above body size. **Spacing:** generous, calm card rhythm; consistent radii; double-bezel panel framing is in place. **Component quality:** chips and buttons are consistent and well-made; overall craft is good.

## DEFECTS

1. **P1 — Whole view is dark mode; the committed "warm paper" neutrals are absent.** Page bg + main panel read cool graphite, not warm paper. If dark is a sanctioned variant, it still fails "warm" — nothing in this frame says paper clinic.
2. **P1 — Coral misused as provenance.** Card 1, ADDRESS row: "● BILL DECODE" chip is coral (=danger) while sibling provenance chips are ochre/slate. A decoded bill address reads as an error state.
3. **P1 — Legend doesn't match the chips it explains.** Legend (above card 1): INFERRED chip is coral-red, but every card's "INFERRED · *" chip is ochre; legend FROM A CALL is sage, but card 3 PHONE's "● CALL" chip is ochre. The trust feature is color-keyed inconsistently.
4. **P1 — Toast occludes content.** Card 2: the toast covers the title ("Riverside Imag…"), the source line, and the PHONE row's Confirm link; it's anchored mid-card instead of near its trigger or as a global toast.
5. **P1 — Clipped nav.** Header tab bar: last tab cut mid-glyph ("S") at the right edge, no fade/scroll affordance.
6. **P1 — Accent dilution, no primary action.** Sage is spent on logo, active tab, active filter, six YOU CONFIRMED chips, and row icons; the actual actions (Call, Confirm) are neutral outlines. View violates the one-primary-action rule.
7. **P1 — Contrast/size below the audience's needs.** "Merged from…" lines, field labels, Confirm links, and footer are dim gray on charcoal (~3:1); chips ~9px uppercase. Core trust microcopy is the least legible text on the page.
8. **P2 — Copy bugs.** Legend opens "Feels the app filled in for you…" (should be "Fields"); header pill "⚡ I live soon" is ungrammatical.
9. **P2 — Inconsistent confirm state.** Card 1 PHONE shows "YOU CONFIRMED ✓" *and* a Confirm link; Corner Pharmacy's confirmed rows show none.
10. **P2 — Weak type hierarchy.** Card titles barely step up from body; overline, meta, chips, body all in one size band.
11. **P2 — Category tint uses danger hue.** Aetna icon is coral; "insurer" is a category, not a danger.
12. **P2 — Ragged action column.** Confirm links float at varying x-positions after chips (cards 1–3) — can't scan confirmability down the list.

**Strengths worth keeping:** honest DEMO DATA / "synthetic only" disclosure, consistent chip grammar, calm card rhythm, double-bezel panel correctly implemented.

**Top fixes, in order:** #2/#3 (color semantics — one hue per meaning), #4 (toast placement), #1 (commit to the paper palette or define a warm dark variant), #6 (give Call the sage; demote confirmation chips to quiet outline).
