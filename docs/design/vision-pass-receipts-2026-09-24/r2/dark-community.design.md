judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/dark-community.png)

**Note on source:** the stated path didn't resolve — `judge-img/r2` is itself the JPEG (620×436, no extension); I audited that file. Everything below is from that image only.

## DESCRIBE

**Layout, top-to-bottom.** Three stacked bands over a near-black umber canvas: (1) header — sage rounded-square logo mark + warm-white "HealthAdvocate" wordmark left; ochre outlined pill "• 1 reminder due soon" plus two dark circular icon buttons (clock/history, moon) right. (2) nav — one row of 11 text links: "…ments" (clipped), Discharge, 2nd Opinion, Recorder, Library, Directory, Scanner, Family, Tracks, **Coverage** (active, sage pill), Help. (3) content — a left-aligned column (~100px side margins): H1 "Coverage Continuity"; one-line intro ("…Local and private. No payments or submissions from this screen."); label "Case title (synthetic)"; a ghost text input with placeholder "e.g. Synthetic job-loss coverage case"; sage filled button "Create Coverage Case". Then a hairline divider, a two-line centered legal disclaimer, and **~45% of the frame is empty canvas below it**.

**Palette as named hues.** Background dark warm umber/charcoal (#181713), header dark warm brown (#362a1c), nav midway — warm-neutral, correctly warm not blue-black. Text warm off-white / dim warm grays. Sage = logo, active-nav pill, primary button (#81a58b) — accent discipline is correct. Ochre = reminder badge (caution semantics, correct). Coral and slate absent — fine, no danger/info content. But the "warm paper" identity survives only in hue temperature; there is no paper texture, no panel treatment — dark mode reads as generic dark admin.

**Typography.** Bold sans wordmark/H1; the ramp is compressed — H1 is only ~1.3× body. Nav links, badge, and footer legal sit at the legibility floor; secondary text measures ~4:1 contrast at floor size.

**Spacing.** Horizontal margins disciplined (101px left / 102px right, header aligned to content). Vertical rhythm tight in the header (3 bands in ~58px), then the page just stops at ~40% height.

**Component quality.** Primary button is well-formed (sage fill, dark-green label, full radius). Input is a near-invisible ghost field. Header icons are dark-on-dark smears. Badge is the highest-saturation element on the page.

## DEFECTS

- **P0 — Nav clipped mid-word, left edge.** First item renders as "…ments", cut by the frame at x≈88 — left of the page's own 101px margin. The nav strip is overflowing with a leftward offset and no visible scroll affordance. A first-time user's entry point is literally illegible. (Nav band, y≈40–52, far left.)
- **P1 — Footer not bottom-anchored; ~45% dead canvas.** Disclaimer hugs the form at y≈230, leaving the entire lower half empty. Page reads unfinished/broken rather than "generous calm spacing." (y≈250–436.)
- **P1 — Ghost input has no affordance.** Fill (#1e1b16) vs background (#181713) is a near-invisible smear with a hairline bezel; a sick, overwhelmed user can't tell it's the one thing to fill in. (Content column, y≈124–143.)
- **P1 — Compressed type scale + floor-level legibility.** H1 ≈1.3× body; nav/badge/legal at ~9–10px effective and ~4:1 contrast. The system's calm-large type is not expressed anywhere. (Global; worst nav band and footer.)
- **P1 — No workbench panel.** Content sits raw on the background — the committed double-bezel panel treatment is entirely absent; the form is an unanchored stub in a void. (Content area.)
- **P2 — Divider misaligned.** Hairline above footer spans x=88–530, overshooting the content column (101–518) on both sides; aligned to neither content nor frame. (y≈193.)
- **P2 — Header icon buttons illegible.** Dark-on-dark glyphs, ambiguous shape, no label/tooltip evidence. (Header right, x≈455–520.)
- **P2 — Badge outcompetes the primary action.** The ochre "1 reminder due soon" pill is the most saturated element on screen, pulling the eye above the nav before the sage CTA. Acceptable semantics, wrong dominance. (Header right.)
- **P2 — Button label contrast suspect.** #2e4a34 on #81a58b ≈ 3.5:1 at small size — verify ≥4.5:1 or bump label lightness. (Primary button, y≈155–172.)
- **P2 — "(synthetic)" leaks internal test language.** Label and placeholder both carry it ("Case title (synthetic)" / "e.g. Synthetic job-loss coverage case") — redundant and meaningless to a patient. (Content column, y≈115–140.)
- **P2 — Flat IA: 11 peer-level nav items.** No grouping, no hierarchy — contradicts "one calm place"; combine with the P0 clip for a nav rework. (Nav band.)
- **P2 — Dark variant drops the brand.** Only the sage accents carry "warm paper clinic"; the three stacked brown/black bands read muddy, not warm. Consider a warmer paper-dark ground or a visible paper-tinted panel to re-anchor identity. (Global.)

**Verdict:** structure and accent discipline are sound (one sage primary action, correct semantic hues), but the P0 nav clip, the half-empty viewport, and the invisible input make this screen feel broken rather than calm. Fix order: nav overflow → anchor footer/panel → input affordance → type ramp.
