judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-community.png)

## What I see

**Layout, top to bottom:** White header band: sage rounded-square logo tile + bold "HealthAdvocate" wordmark left; right cluster = ochre pill badge ("# 1 due soon"), avatar circle, hairline divider, sun/theme toggle. Below it a single-row horizontal nav of ~12 items (Bills … Scanner, ending in a clipped "Fami"), active "Scanner" in a pale sage pill. Then the warm-paper page: one centered white card containing a coral-glyph icon tile, uppercase title "COMMUNITY HEALTH SCANNER" + one-line gray subtitle, an uppercase field label, a tall warm-gray textarea with placeholder text and a visible resize grip, and a dark-green "Scan" pill button. Below the card: a hairline rule, two lines of centered gray disclaimer text with bolded brand, then ~90px of empty paper to the page bottom.

**Palette as named:** paper oatmeal background, white shells, sage in two values (mid sage logo/active pill, dark forest button), ochre on the due-soon badge, a coral/orange glyph in the card header, warm-gray body text. No slate-blue present (nothing info-flavored on screen).

**Type scale:** Wordmark ~15px is the largest text; view title and field label are the same small letterspaced caps (~9–10px); body/placeholder ~10–11px. Flat hierarchy.

**Spacing/components:** Generous, calm card padding; single card, soft shadow (double-bezel not clearly in effect — the textarea is the only inner bezel); one primary action only; no motion clutter.

## Defects

1. **P0 — Nav truncation.** Last nav item renders as "Fami," clipped mid-word at the right viewport edge (top nav, far right), no ellipsis or scroll affordance. Label is incomplete.
2. **P1 — Nav overload.** 12 equal-weight top-level items in one tight row; no grouping or priority. Directly hostile to the "overwhelmed user" this tool serves.
3. **P1 — Flat type hierarchy.** The view title "COMMUNITY HEALTH SCANNER" is the same size as the "PASTE A…" label; there is no page-level heading. The view reads as a stack of labels.
4. **P1 — Coral misuse.** The scanner icon glyph (left of card title) is coral/orange — the reserved danger hue — used decoratively on a neutral action. Semantics leak.
5. **P1 — Badge copy reads wrong.** Header pill "# 1 due soon" parses as a "#1 ranking" claim. Intended meaning ("1 item due soon") is miscommunicated; drop the "#".
6. **P2 — Two greens.** Scan button is dark forest while logo/active pill are mid sage; the primary action doesn't read as the brand accent value. Pick one ramp step.
7. **P2 — Resizable textarea.** Visible resize grip (bottom-right of the textarea) lets users break the calm card; disable resize.
8. **P2 — Bottom dead zone.** ~90px of empty paper below the centered footer; card hugs the top, page feels unfinished rather than calm.
9. **P2 — Placeholder contrast.** Light-gray placeholder on the warm-gray textarea fill is barely legible at 100%.
10. **P2 — Header right cluster noise.** Badge, avatar, and toggle are three similarly-sized pills cheek-by-jowl; the badge (a task cue) competes with utility buttons. Group or demote.

**Passes:** exactly one primary action; consistent paper neutral; clear active-nav pill; disclaimer present with honest framing; restrained motion.
