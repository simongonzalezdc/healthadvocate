judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-coverage.png)

**IMAGE RECEIVED** — audited as-is (620×436 capture, reads ~2× downscaled retina; coords below in screenshot px).

## Description

**Layout, top-to-bottom:** White header bar (y0–30): sage rounded-square heart logo + bold "HealthAdvocate" wordmark left; ochre pill badge "#1 due soon" + two circular ghost icon buttons (account, theme) right. Nav rail (y≈40–52): ~11 text tabs, "Coverage" active in a sage pill, "Help" last. Content on warm paper: H1 "Coverage Continuity" (y≈89), one-line reassurance sentence, small label "Case title (synthetic)", rounded text input with placeholder, sage primary button "Create Coverage Case" (y≈153–175). Hairline divider (y≈200), then a 2-line centered disclaimer. Canvas below y≈245 is empty paper.

**Palette as named hues:** Warm paper background ✓, white header ✓, sage-green logo/primary button/active nav pill ✓, ochre badge ✓, near-ink/slate text, warm-gray hairlines. Coral correctly absent (no danger state on this view). On-system.

**Type scale:** Three clear steps — bold H1 (~15px, ≈1.6× body), ~9.5px body/UI, ~8px label/disclaimer. Nav runs small; scale is quiet and clinical, fits "calm."

**Spacing rhythm:** Tight, even stack (heading→copy→label→input→button, ~8–14px steps); generous right margin; but rhythm collapses below the divider — a large dead zone.

**Component quality:** Button, input, badge, ghost icon buttons all crisp, consistent radii, no shadow noise. One primary action per view ✓. Clean build overall.

## Defects

- **P0 — Leftmost nav tab clipped mid-word** (top nav, x≈88, y≈45): reads "…ntients," cut flush at the edge, label illegible. Nav is horizontally overflowing at this width with no scroll fade/arrow affordance.
- **P1 — Footer floats mid-canvas** (divider y≈200, disclaimer y≈223–241): ~44% of the viewport below it is blank paper. Anchor disclaimer to viewport bottom or let content region fill.
- **P1 — Dead-end empty state** (form block, y≈89–175): one input + button, but no region showing where created cases land, no example, no next-step cue. For sick/overwhelmed users this is orientation failure, not minimalism.
- **P2 — Dev jargon in user copy** (label y≈115 + placeholder y≈134): "synthetic" ×2. Say "sample"/"demo" — "synthetic" is test-fixture language.
- **P2 — Cryptic badge** (header right, x≈428, y≈14): "#1 due soon" — #1 of what? Name the thing ("Next: coverage appeal").
- **P2 — Left edges off one grid**: logo/H1/input sit at x≈100; nav and divider at x≈88. Two competing left lines.
- **P2 — No double-bezel panel** (content region): form floats bare on paper; system language promises double-bezel workbench chrome — this view has none, so the primary action feels unanchored.
- **P2 — Active nav pill contrast** (x≈352–390, y≈45): white-on-sage at ~9px — verify ≥4.5:1; sage at this lightness is borderline.
- **P2 — Header-right cluster has flat hierarchy** (x≈428–515): ochre badge and two identical icon circles read as one equal-weight blob; theme toggle doesn't deserve badge-adjacent weight.

**Verdict:** On-palette, on-type, honest copy, single primary action — the bones are right. Ship-blockers are the clipped nav tab (P0) and the orphaned footer/dead-end layout (P1).
