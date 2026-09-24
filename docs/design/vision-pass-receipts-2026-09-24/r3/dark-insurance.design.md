judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-insurance.png)

I can see the image. Audit follows.

## DESCRIPTION

**Layout, top-to-bottom:** (1) App bar: sage logo chip + "HealthAdvocate" wordmark left; right cluster = ochre outlined pill "🕐 1 reminder due soon", two circular icon buttons (bell, moon). (2) Flat nav row: Symptoms / Documents / Bills / **Insurance** (active, sage-outlined pill) / Drugs / Appointments / Discharge / 2nd Opinion / Recorder / Library / + a clipped sliver at the right edge. (3) One centered double-bezel panel (~x95–520): shield-doc icon chip, "Denial Fighter" H1, two-line subcopy, uppercase label + large textarea, uppercase label + second textarea, sage "Fight Denial" pill button, left-aligned. (4) Hairline divider, centered two-line disclaimer footer.

**Palette as named hues:** page = warm near-black espresso charcoal; panel = one step lighter warm charcoal. Sage green = logo glyph, active nav outline, CTA fill (correct primary role). Ochre = reminder pill border/text/icon (correct caution role). Coral and slate absent this view. Text = warm off-white → warm gray → dim warm gray (placeholders/labels).

**Typography:** single sans. Wordmark ~13 semibold, H1 ~18 bold, body/subcopy ~11.5–12, nav ~11, field labels ~9.5 caps tracked, footer ~10.5. Compressed scale — H1 is barely 1.5× body.

**Spacing rhythm:** chrome compact (bars ~36/26px), panel airy (~28px padding, ~24px group gaps), mostly 4/8-multiples; a dead zone under the CTA breaks the rhythm.

**Component quality:** consistent radii (pill nav, ~10px inputs, circular icon buttons), consistent 1px hairline borders; inputs and button read as one family. Build quality is decent; the failures are systemic, not craft.

## DEFECTS

**P0**
- **Nav, far-right edge after "Library" (≈x556, y45):** an item/badge is clipped mid-glyph at the container edge (stray "0" sliver). Desktop nav doesn't collapse at this ~620px viewport; overflow unmanaged. Broken.

**P1**
- **Entire canvas:** dark charcoal theme, not the committed warm-paper neutrals. Sage/ochre semantics survive, but "paper" is gone and coral/slate roles are unverifiable here. Moon toggle implies an intentional variant — either way the dark variant is unspecified in the committed system and ships unreviewed.
- **Placeholders in both textareas, both uppercase field labels, footer copy (panel center; footer y≈430–450):** dim warm gray ≈3:1 on charcoal — below WCAG AA, on the exact copy sick, overwhelmed users must read.
- **Nav row (y≈45):** 10 flat items at ~11px, tight gaps, no grouping or overflow menu — contradicts "generous calm spacing"; the clipped 11th item is the symptom.

**P2**
- **Below "Fight Denial" (y≈362–380):** ~2× the top padding as dead space; panel reads unfinished at the bottom.
- **"Fight Denial" CTA (≈x122–196, y≈340–362):** ~26px tall — undersized target for the view's single primary action.
- **Denial-letter textarea (y≈178–252):** ~74px tall for a multi-page denial letter/EoB; second textarea is shorter (~60px) for no stated reason — unequal twins.
- **Panel edge (x≈95 / x≈520):** double-bezel contrast so low the workbench boundary nearly vanishes against the page — the system's signature detail doesn't survive the dark values.
- **Left edges:** logo block (x≈68), nav first item (x≈90), panel (x≈95) sit on three different margins; no shared alignment line.
- **Field labels (~9.5px caps):** at the legibility floor, especially at this muted color.

**Compliance notes:** one primary action per view ✅, sage=primary / ochre=caution ✅, restrained static composition ✅.
