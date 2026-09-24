judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/dark-tracks.png)

Note on the artifact: the stated path `judge-img/r2/dark-tracks.jpg` doesn't exist (`r2` is a file, not a folder). I judged `judge-img/r2`, md5-identical to `r2-view.jpg` and `r2-attached-dark-insurance.jpg`. Frame: 620×436, dark theme.

## DESCRIPTION

**Layout, top-to-bottom.** One dark slab (~y 0–58) holds a header row — sage rounded-square logo chip with darker heart glyph + "HealthAdvocate" wordmark left; ochre outline pill "⚠ 1 reminder due soon" + two dim rounded-square icon buttons (clipboard?, moon) right — then an 11-item nav row (…ments / Discharge / 2nd Opinion / Recorder / Library / Directory / Scanner / Family / Tracks / **Coverage** (sage active pill) / Help) on the same surface, no seam. Below, on a slightly darker canvas: a left-aligned column (x 101–522) with H1 "Coverage Continuity", one-line intro, a label "Case title (synthetic)", one text input, one sage pill button "Create Coverage Case". A hairline divider (y 193), then a centered two-line disclaimer, then ~190px of empty background to the bottom edge (44% of frame).

**Palette as named hues.** Page bg #181713, header/nav slab #25221b — warm near-black olive-espresso, not paper. Sage ✓ consistent in three roles: logo chip #79a884, CTA fill #76aa84, active nav #445743/#839984. Ochre present but muddy: badge text reads dusty coral-tan (peak #cfae9b), border #4c4439. Coral: absent (no danger element in view). Slate: absent (nothing informational). Text: warm off-white #f1eee7 primary, ~#777569 secondary.

**Type.** One sans family throughout. Wordmark ~13 bold; H1 ~19 bold; body/labels 12; nav 10.5; footer 11. Scale is compressed — H1 is only ~1.6× body; no display voice.

**Spacing.** Tight inside the form (label→input 4px, H1→body 6px), then 20px to divider, 40px to disclaimer, then dead space. Rhythm inverted — densest where the eye should rest.

**Component quality.** CTA pill radius vs input 9px radius mismatch; input fill (#1e1b16) and border (#2b2823) both near-identical to page bg; icon glyphs barely rise above header; divider sits at 1.03:1.

## DEFECTS

1. **P0 — Nav clips first item.** First nav label truncated mid-word to "…ments" at container edge x≈88, y≈46. 11 items overflow with no wrap/scroll affordance; label unreadable (Treatments? Payments?). Broken and dishonest navigation.
2. **P1 — Nav illegible + flat IA.** Inactive labels 3.4:1 at ~10.5px (WCAG 4.5:1 fail), 11 undifferentiated peers, "Help" mixed with feature modules. Entire nav reads as gray noise; only the active pill survives.
3. **P1 — Header icon buttons illegible.** Glyphs at 2.3:1 vs header bg (x≈483–500, y≈10–25); clipboard/bell glyph unidentifiable even at 4×. Both 3:1 non-text fail and undiscoverable actions.
4. **P1 — Invisible input boundary.** Border 1.2:1, fill 1.1:1 vs page (x 101–522, y 122–144). The screen's only form field has no perceivable edge — placeholder floats on void; sighted users can't locate the click target.
5. **P1 — Page doesn't fill the workbench.** Content ends y≈245; y 245–436 is bare background. Disclaimer floats mid-canvas instead of anchoring at the bottom, and a "Continuity" view ships with zero case list / empty-state — the view reads unfinished.
6. **P1 — Committed system absent.** No double-bezel workbench panel anywhere — bare form on raw canvas. Whole surface is a dark olive scheme, not "warm paper"; if dark is a sanctioned variant its tokens aren't derived (see #8).
7. **P2 — Three right edges.** Header cluster ends x=509, form x=522, divider x=531; divider also overshoots the column left (88 vs 101). Nothing shares a right margin; left side has competing 88/101 edges too.
8. **P2 — Badge hue straddles caution/danger.** "1 reminder due soon" renders coral-tan, between committed ochre (caution) and coral (danger), on a 1.9:1 invisible border — the view's only alert hedges its semantic.
9. **P2 — Corner-language mix in one form.** Stadium-pill CTA sits 12px under a 9px-radius input; badge/nav pill, chip/icon-button squircle — four corner treatments in 170px of height.
10. **P2 — Label indistinguishable from copy.** "Case title (synthetic)" is same size/weight/color as the paragraph above it (10.6:1 vs 12.5:1) — no cue it captions the field.
11. **P2 — Compressed hierarchy + invisible divider.** H1 ~1.6× body with no display weight; divider 1.03:1 (y 193); footer 4.4:1 at 11px, marginal fail.

**Compliant:** exactly one primary action, sage, correctly dominant; sage used only for brand/active/CTA; disclaimer present and honest; sage-on-fill CTA label ≈5:1.
