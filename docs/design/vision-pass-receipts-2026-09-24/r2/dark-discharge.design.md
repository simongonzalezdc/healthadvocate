judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/dark-discharge.png)

Image located: the attachment path was malformed (`r2` is the JPEG itself, not a folder); `r2-view.jpg` is byte-identical, so I judged that. 620×436 capture, dark theme, page = "Coverage."

## DESCRIBE

**Layout, top-to-bottom:** Full-bleed near-black warm header bar — sage shield logo + "HealthAdvocate" wordmark left; coral-outlined pill "+1 reminder due soon" plus two ghost circular icon buttons (info, moon/theme) right. Below it a single-row nav of 11 small items ("Immers, Discharge, 2nd Opinion, Reactor, Library, Directory, Scanner, Family, Tracks, Coverage, Help"), active "Coverage" as a sage pill. Content is a narrow left-anchored column (~420/620): bold title "Coverage Continuity," a three-sentence intro paragraph whose last line is "Case title (synthetic)," a ghost text input with placeholder, a sage "Create Coverage Case" button. Then a full-bleed hairline divider, a small centered disclaimer paragraph at mid-page, and ~40% empty dark void to the bottom edge.

**Palette:** Warm-umber near-black backgrounds (#1b1510 chrome, #201912 canvas — warm-tinted darks, paper hues inverted); warm cream ink (~#f0e8dc); muted warm-gray secondary text; sage green (~#93b89a) on logo, active nav pill, and the one button; coral (~#e2725b) on the reminder pill only; ochre and slate absent. Hairlines are low-contrast warm brown.

**Type scale:** Flat — ~20px bold title, ~12px body, ~10px nav/pill/placeholder. No mid sizes; label and body are the same style.

**Spacing rhythm:** Tight 12–16px gaps in the form cluster; rhythm holds until the divider, then collapses — footer floats mid-page with dead space below.

**Component quality:** Primary button and active nav pill are well-made (solid sage, dark text, good radius). Input is a ghost field with hairline border. Reminder pill is a clean outline treatment in the wrong hue. No panels, cards, or bezels anywhere.

## DEFECTS

1. **P1 — Coral misuse, header right.** "+1 reminder due soon" pill is coral = danger. A reminder is caution/informational; for sick, overwhelmed users this reads as an emergency, and it's the loudest element on screen, out-shouting the primary action. Use ochre (caution) or slate (info).
2. **P1 — Form label fused to paragraph, content column.** "Case title (synthetic)" is set as the last line of the intro paragraph — same size, color, and leading, zero gap. It doesn't read as a label for the input below. Give it its own line, meta/eyebrow styling, and ~16–24px clearance above the field.
3. **P1 — Double-bezel workbench missing, main content.** The form sits naked on the canvas background. The system's signature double-bezel panel treatment is absent from the one surface that is actual work.
4. **P1 — Unanchored footer + dead void, bottom ~40%.** Content ends at mid-page; disclaimer floats at ~55% height with pure background beneath. Reads as an unfinished page, not "generous calm spacing." Pin the footer to the viewport bottom or frame/fill the column.
5. **P2 — Dark mode abandons paper identity, whole view.** Moon toggle shows it's deliberate and the darks are correctly warm-tinted, but there is no paper surface left — sage is the only surviving brand hue. Dark variant needs tokens that keep paper-neutral warmth (and system sign-off).
6. **P2 — Placeholder contrast, input field.** Mid-gray placeholder on dark umber is ~4:1 at small size — borderline. Same for the footer disclaimer text, which is the legally important line.
7. **P2 — "Synthetic" ×3, intro + label + placeholder.** Same qualifier in the subtitle, the label, and the placeholder. Say it once.
8. **P2 — Nav density/labels, nav row.** 11 items at ~10px, small targets; "Immers" and "Reactor" read as truncated or opaque jargon with no affordance for overflow.
9. **P2 — Header right cluster spacing.** Pill and two icon buttons packed at ~4px gaps with mismatched optical weights; needs a consistent gap unit.

**Compliant:** exactly one primary action; sage correctly reserved for it (plus logo/active nav); calm single-column focus; honest copy ("no payments or submissions from this screen").

Caveat: capture is 620px wide, so sub-10px text is fuzzy — font-metric and contrast calls above are conservative.
