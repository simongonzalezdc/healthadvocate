judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/dark-insurance.png)

Provenance note: the exact attached path didn't exist (`r2/` is a file, not a directory); I viewed the attachment at `/tmp/ha-ds-shots/judge-img/r2` (620×436 JPEG, md5-identical to `r2-view.jpg`). Everything below judges that image only.

## DESCRIPTION

**Layout, top to bottom:** (1) Header bar — sage rounded-square logo mark + "HealthAdvocate" wordmark left; ochre warning pill "⚠ 1 reminder due soon" + two low-contrast icon buttons (chat, theme toggle) right. (2) Full-width nav strip, 11 flat items: Moments, Discharge, 2nd Opinion, Reactor, Library, Directory, Scanner, Family, Tracks, **Coverage** (active, sage pill), Help; hairline rule beneath. (3) Content column (~x100–520): H1 "Coverage Continuity", two-line muted lede ("One calm place… No payments or submissions from this screen."), label "Case title (synthetic)", bordered text input with placeholder, sage filled button "Create Coverage Case". (4) Full-width rule, then a small dim two-line disclaimer. (5) Empty near-black void fills the bottom ~45% of the frame.

**Palette (named hues):** ground = warm espresso/near-black (not warm paper — dark variant); surface layering reads as three slightly different warm darks (header / nav / content). Sage-green = logo mark, active nav pill, primary button — correct. Ochre = reminder pill — correct caution semantics. No coral (correct — nothing dangerous), no slate visible. Text: off-white H1, ~60% warm-gray body, ~35% gray nav/disclaimer.

**Typography:** single sans; H1 ≈22px bold, then everything else collapses into an 11–13px band (lede, label, input, nav, disclaimer) — one strong level, weak differentiation below it.

**Spacing rhythm:** calm and even within the form block (heading → lede → label → input → button), consistent ~6–8px radii; generous top offset. Rhythm dies below the footer — no cadence, just void.

**Component quality:** logo chip, reminder pill, input, and button are crisply formed and consistent; nav and icon buttons are under-weighted; no double-bezel workbench panel anywhere — content floats on bare ground.

## DEFECTS

- **P1 — Nav link contrast** (`Moments…Help`, y≈44): dim warm-gray on charcoal, at/near WCAG floor at this size. For a tool for sick, overwhelmed users this is a usability failure, not polish.
- **P1 — Flat 11-item nav, no hierarchy** (y≈44): equal-weight jargon labels with no grouping; "Reactor" reads as truncated/jargon ("Reactions"?). Also forces "Coverage" pill to split the spacing rhythm before "Help".
- **P1 — Dead below-fold void** (y≈230–436, full width): ~45% of the viewport is empty ground under the primary button — no existing-cases list, empty-state, or next-step guidance. The view ends with the form and nothing else.
- **P1 — Whole-view dark ground vs committed "warm paper neutrals"** (global): sage/ochre semantics carried over correctly, but if this dark variant isn't a tokenized sanctioned theme it's off-system; theme toggle top-right implies it is — verify tokens, don't let this be ad-hoc.
- **P2 — Footer alignment + contrast** (x≈115–505, y≈197–218): center-aligned while everything above is left-aligned; text ~35% gray, hardest-to-read copy on the page.
- **P2 — Field label hierarchy** (x≈100, y≈121): "Case title (synthetic)" is same size/color as the lede — reads as body text, not a label; "(synthetic)" is dev-speak and duplicates "Synthetic" in the placeholder one line below.
- **P2 — Grid drift** (x≈88 vs x≈100): header/nav left edge sits at x≈88, content column at x≈100 — ~12px indent mismatch on the shared left grid.
- **P2 — Double-bezel panel absent** (content area): the committed workbench treatment (double bezel) doesn't appear; form floats directly on ground with no surface layering.
- **P2 — Compressed type scale** (below H1): five distinct text roles (lede/label/input/nav/disclaimer) all land in an 11–13px mid-gray band — hierarchy is carried by position alone.
- **P2 — Header icon buttons** (x≈510–545, y≈17): tiny, very low-contrast hit targets (chat, theme) — discoverability ~zero.
- **P2 — Mixed corner language**: full-radius nav pill ("Coverage") vs ~6px radius on input/button — minor, but pick one system.

**Compliant:** one primary action per view (sage "Create Coverage Case") ✓; ochre used only for the caution reminder ✓; coral correctly absent ✓; form-block spacing calm ✓. No P0 found — nothing broken, illegible, or dishonest.
