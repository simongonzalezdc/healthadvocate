judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-drugs.png)

# Visual Audit — HealthAdvocate "Drugs" view (light)

## What I see

**Layout, top to bottom:** White header band — sage logo tile + bold "HealthAdvocate" wordmark left; ochre pill badge "#1 due soon", bell button, theme (sun) button right. Below, a single-row tab nav of 10 items (Symptoms … Library) with "Drugs" active as a sage pill. Content zone sits on warm paper greige: one white double-bezel card, centered, containing a small sage icon tile + caps title "DRUG CHECKER", one line of helper text, a caps field label "DRUG NAME", a full-width bordered input (placeholder "e.g., Lipitor, Zoloft, Advair"), and a sage "Check Drug" button. Below the card, a two-line centered gray disclaimer on the paper background. Bottom ~35% of viewport is empty paper.

**Palette:** Warm paper neutral field, white surfaces, sage-green accent (logo, active nav, primary button), ochre badge, mid-gray secondary text. Coral and slate unused on this view — acceptable, nothing here is danger/info.

**Typography:** Flat, compressed scale — everything between ~11–13px equivalents: caps letterspaced labels, small helper text, small nav. No display-size heading anywhere.

**Spacing/component quality:** Generous outer margins, card interior rhythm slightly tighter; components crisp, borders hairline, no visible rendering breaks. "One primary action per view" is respected — genuinely good.

## Defects

- **P1 — Header right cluster:** Badge copy "#1 due soon" is undecodable at a glance — is "#" a count prefix, an unparsed template, an issue number? Sick users shouldn't decode. Say "1 task due soon" and link it to the thing that's due.
- **P1 — Card header:** Type scale is flat. The view's only heading, "DRUG CHECKER," is a ~11px caps label barely larger than body — no hierarchy anchor for the page's main task. Give the view a real title weight/size.
- **P1 — Card body + footer:** Helper text, placeholder, and disclaimer are all small and low-contrast gray. For an audience of sick, overwhelmed, often low-vision users this is the wrong place to economize contrast. Bump one step and darken to ~#5x.
- **P1 — Below the fold:** Disclaimer floats mid-air with ~35% empty paper beneath it. It reads as an unanchored footer on an unfinished page, not calm. Anchor the disclaimer to the viewport bottom or pull the card into the vertical center of the work area.
- **P2 — Nav row:** 10 tabs at small size with tight gaps; no overflow affordance before it clips at narrower widths. Define a collapse behavior now.
- **P2 — Nav "Drugs":** Active state is doubled — sage pill *plus* a small stray dot beneath it. If the dot is intentional, it's redundant; if not, it reads as a rendering artifact. Pick one indicator.
- **P2 — Card header icon:** A document/page glyph introduces a *drug checker*. Icon contradicts the task — use a pill/mortar glyph.
- **P2 — Card interior:** Rhythm is uneven — helper text hugs the caps title tighter than the label-to-input gap. Normalize to the spacing scale (one step between title block and helper, consistent steps after).
- **P2 — Header right cluster:** Badge-to-bell gap is visibly tighter than bell-to-sun gap; align to one gap unit.

**System adherence:** sage-as-primary ✓, one primary action ✓, ochre-as-caution badge ✓, paper/white zoning ✓, motion unverifiable from a still. The bones are right; the failures are all in text sizing/contrast, the cryptic badge, and the bottom void.
