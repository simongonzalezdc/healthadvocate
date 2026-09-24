judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-coverage.png)

I can see the image. Audit follows.

## Description

**Layout, top to bottom:** Header bar — sage shield logo + "HealthAdvocate" wordmark left; ochre outlined pill "⚠ 1 reminder due soon" plus two ghost circle icon buttons (info, moon) right. Below it, a single-row tab strip of 11 nav items, active "Coverage" rendered as a sage-filled pill with dark text. Main canvas: a left-anchored content column (~55% width) containing an h1 "Coverage Continuity", a two-line subhead ("One calm place… No payments or submissions from this screen."), a small field label "Case title (synthetic)", one bare text input with placeholder, and a sage pill button "Create Coverage Case". Then a full-width hairline divider, a centered two-line legal disclaimer in dim small type, and roughly the bottom 45% of the viewport is empty canvas.

**Palette (as seen):** dark-mode variant of the system — near-black warm umber canvas, slightly lighter warm-brown header band, warm off-white primary text, warm-gray secondary text, sage accent on active tab + CTA, ochre on the reminder badge. No coral or slate present. Warm tint is consistent, so it reads as the paper palette inverted, not a foreign theme.

**Typography:** one sans family. H1 ~2× body but the hierarchy leans on weight more than size; nav and disclaimer are very small. Scale is compressed overall (roughly 22 / 12 / 11 / 10px at this render).

**Spacing:** label→input→CTA rhythm is tight and fine; CTA→divider gap is much looser; then a dead void. Vertical rhythm is uneven rather than calm.

**Component quality:** CTA pill and active-tab pill are consistent; ghost icon buttons match. But the form floats bare on the canvas — no panel, no double bezel anywhere; the input is a lone unfathered field.

## Defects

1. **P0 — Header nav, far left:** first tab is clipped mid-word at the container edge ("…ointments", presumably "Appointments"). Content is illegible/unreachable and there's no scroll affordance or chevron on an 11-item strip that overflows.
2. **P1 — Main canvas:** committed "double-bezel workbench panel" is absent; a label + input + button sit naked on the page. The single bare input looks unfinished, not minimal.
3. **P1 — Bottom half of page:** disclaimer floats mid-canvas with ~45% dead space below it. Reads as a broken layout, not generous spacing; footer should anchor to the viewport bottom or the canvas needs a panel to close the composition.
4. **P1 — Disclaimer, centered under divider:** smallest, lowest-contrast text on the page carries the safety-critical message ("not replace… consult a qualified provider") for sick, overwhelmed users. Fails the audience; bump size/contrast.
5. **P1 — Field label + placeholder:** "(synthetic)" and "Synthetic job-loss coverage case" leak internal demo vocabulary into the UI. If it's an intentional demo-mode marker, use a badge, not the field label.
6. **P2 — Header right:** the ochre reminder pill is the loudest element in the viewport and uses a raw "⚠" glyph, competing with the view's one primary action. Ochre=caution is arguably correct, but dial salience down and use the icon font.
7. **P2 — Active tab + CTA:** two sage-filled pills in one viewport ("Coverage" tab, "Create Coverage Case") slightly dilute "one primary action per view". Acceptable since one is nav state, but consider outlining the active tab.
8. **P2 — Input field:** border is near-invisible against the umber canvas; the field barely registers as interactive.
9. **P2 — Alignment:** form column is left-anchored, disclaimer is centered, divider is a third width — three alignment systems in one view. Pick the column.
10. **P2 — Header seam:** the header band's bottom edge cuts immediately under the nav pills; the strip is cramped against the seam and the tabs are set very small. Give the nav row breathing room.

**Compliant:** one primary action, sage reserved for advocacy actions, ochre caution semantics, warm-neutral darks, no motion offenses visible, honest copy ("Local and private. No payments…").
