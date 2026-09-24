judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/dark-recorder.png)

Note: the stated path doesn't exist as written — `judge-img/r2` is itself the JPEG (byte-identical to `r2-attached-dark-insurance.jpg`), so I judged that image at 1x plus 3x magnifications of three regions.

## DESCRIPTION

**Layout, top-to-bottom.** (1) App bar on warm dark brown: left — sage rounded-square mark (heart-with-pulse glyph) + bold "HealthAdvocate"; right — coral-outlined pill "🔔 1 reminder due soon", then two ghost circular icon buttons (an unreadable glyph, then a crescent moon). (2) Full-width nav strip: 11 equal small items — Intake, Discharge, 2nd Opinion, Recorder, Library, Directory, Scanner, Family, Tracks, **Coverage** (active, sage pill), Help. (3) Content column (~90% width, left-aligned) on a surface that is the same near-black as the page: H1 "Coverage Continuity"; one-line intro ("One calm place… No payments or submissions from this screen."); micro-label "Case title (synthetic)"; full-width single-line input with placeholder "e.g. Synthetic job-loss coverage case"; sage pill button "Create Coverage Case". (4) Hairline divider, then a centered two-line muted disclaimer at ~52% viewport height. Bottom ~45% of frame is empty.

**Palette as named hues.** Dark rendering, not paper: page near-black warm brown (#181713), header #25221b; sage-advocate preserved (#70a878 button fill, muted sage active pill); coral-danger preserved (~#c96f5a chip); ochre and slate absent; text warm off-white #d9d8d4; muted text #6d6c68 / #54534e. Warmth survives the translation; paper does not.

**Type scale.** H1 ~26px bold; intro ~14px; label/nav/footer ~11–12px. Scale compresses hard below H1 — intro, field label, and footer are near-indistinguishable in size and weight.

**Spacing rhythm.** Generous vertical air between bar → nav → content; left margin consistent; but label→field grouping gap is absent, and the view collapses into dead space below 52%.

**Component quality.** Button is the best-built element (pill, sage fill, dark text, sole primary on the view ✓). The input is the weakest: fill ≈ page background, 1px border ≈ #2b2823. Nav active pill and reminder chip are cleanly drawn.

## DEFECTS

1. **P1 — Input affordance near-invisible.** "Case title" field (~y131, center): field fill #181810 vs page #181713, border ~1.2:1 contrast. The view's only data-capture control is barely distinguishable from the void.
2. **P1 — Field label fails contrast.** "Case title (synthetic)" (~y116): #6d6c68 on near-black ≈ 3.4:1 at ~11px — fails WCAG AA, and it is the input's only visible label.
3. **P1 — Test copy leaked to UI.** "(synthetic)" in the label and "Synthetic" in the placeholder: internal seed-data wording shipped to sick end-users; reads as broken/untranslated copy in a medical tool.
4. **P1 — Coral misuse on reminder chip.** Header right (~x385–475): coral = danger per system, but "1 reminder due soon" is a timing nudge — ochre/caution at most. Danger accent on a non-danger manufactures false alarm for an anxious audience.
5. **P1 — Invisible header utility buttons.** Two ghost circles (~x480–515): glyphs <2:1 on the header; the theme toggle and one unlabeled control are effectively invisible, with no tooltip or accessible name.
6. **P1 — Dark variant off-system.** "Warm paper neutrals" are absent — the view reads generic-dark with a brown cast. The moon toggle shows dark mode is deliberate, but it has no documented token translation of its own (no ochre/slate roles, no paper hierarchy); needs a sanctioned dark token set before shipping.
7. **P1 — Nav IA dump.** 11 equal-weight ~12px items, ungrouped, active target buried mid-row (y44). A flat 11-way choice at first paint is the opposite of calm for the stated user.
8. **P2 — Committed double-bezel panel absent.** Content surface #181013 ≈ page #181713: one continuous sheet, hierarchy carried only by the header band.
9. **P2 — Dead lower half.** ~45% empty viewport below the footer; content top-hugs. Center the column or extend a framed panel.
10. **P2 — Label not grouped to field.** "Case title (synthetic)" sits equidistant between intro and input; reads as a stray fifth sentence of the intro.
11. **P2 — Over-wide input.** Single-line title field spans ~90% of frame; cap at ~40–48ch.
12. **P2 — Footer contrast + alignment.** Centered disclaimer in a left-aligned composition; #54534e on near-black ≈ 2.5:1 — legal/medical text below AA.
13. **P2 — Type-scale compression.** Only the H1 reads as a distinct step; intro/label/footer collapse into one 11–14px band.

What's right: exactly one primary action per view, sage/coral semantics intact, warm cast preserved, honest privacy copy ("No payments or submissions from this screen"). No P0 found — nothing broken, misaligned, or dishonest; the failures are all contrast, semantics, and system adherence.
