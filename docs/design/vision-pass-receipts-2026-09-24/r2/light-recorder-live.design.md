judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/light-recorder-live.png)

**Image resolution note:** the given path `judge-img/r2/light-recorder-live.jpg` doesn't exist (`r2` is a file, not a directory). The bytes at that location (stub `r2`) are md5-identical to `r2-view.jpg`, so I judged those bytes. Heads-up for the pipeline: those bytes are a **dark-theme Coverage view**, previously attached as "dark-insurance" — the name "light-recorder-live" is stale metadata. Judged as-seen:

## WHAT I SEE

Top-to-bottom, one column, ~620×435 frame:

- **Header bar** (warm near-black espresso): sage-green rounded logo tile with heart glyph, white bold "HealthAdvocate" wordmark. Right side: ochre pill badge "⏰ 1 reminder due soon", then two small circular dark icon buttons (dot/target glyph; moon glyph).
- **Nav row** on the same dark ground: 11 tiny grey links — Intake, Discharge, 2nd Opinion, Redactor, Library, Directory, Scanner, Family, Tracks, **Coverage** (active, sage outline pill), Help.
- **Content region** (slightly lighter warm umber field): H1 "Coverage Continuity" (white, ~20px), 2-line intro paragraph, then form label "Case title (synthetic)", a rounded dark text input with grey placeholder "e.g. Synthetic job-loss coverage case", and the primary sage pill button "Create Coverage Case". Then a hairline divider, then a small centered grey disclaimer paragraph ("…Your information stays on your device.").
- **Below that: nothing.** Bottom ~38% of the frame is empty dark field.

**Palette as named hues:** warm paper neutrals inverted — espresso/umber darks; sage-green present (logo tile, active nav, primary button); ochre present (reminder badge); **no coral, no slate in view** (nothing dangerous/informational on screen). **Type scale:** compressed — H1 ~20px, body ~11px, label/nav/disclaimer ~10px, one sans family. **Spacing:** dense header/nav, calm form block, then unstructured void. **Component quality:** pills and input are cleanly shaped, rounded, flat; one primary action only (compliant); but no panel/bezel treatment anywhere — everything sits on bare ground.

## DEFECTS

- **P0 — Wrong deliverable.** Frame shows dark theme + Coverage create view; shot is named "light recorder live". Either the capture or the theme/view wiring is broken; the committed "warm paper" light default is not shown. (Entire frame.)
- **P0 — Illegible muted text.** Form label "Case title (synthetic)", input placeholder, and footer disclaimer are dim warm-grey on near-black at 10–11px — reads well under ~4.5:1. Fatal for this product's actual audience (sick, overwhelmed, possibly low vision). (Left form block; bottom center.)
- **P1 — Dead composition.** Content ends ~60% down; bottom ~38% is empty void, and the column is left-anchored so the right half is also empty. Reads unfinished, not calm. (Below divider; right field.)
- **P1 — Committed double-bezel workbench panel absent.** Form floats directly on the page field; no bezel, no panel nesting anywhere. (Main content region.)
- **P1 — Compressed hierarchy + unusable nav.** H1 barely outranks body text; 11 nav items at ~10px with tap targets far below 44px; active "Coverage" pill is the only landmark. (Nav row; H1.)
- **P1 — Ambiguous header cluster.** Ochre alert pill sits flush against two near-identical circular icon buttons with unclear glyphs (dot, moon); the reminder is the loudest element on the view and competes with the single primary action. (Top right.)
- **P2 — Internal jargon leaks.** "(synthetic)" / "Synthetic" in label and placeholder is test-harness vocabulary shown to users. (Form block.)
- **P2 — Alignment break.** Disclaimer is center-aligned in an otherwise all-left view, and floats mid-frame above the void instead of anchoring the page bottom. (Bottom center.)
- **P2 — Weak input affordance.** Field border barely separates from fill; no visible focus styling. (Form input.)
- **P2 — Two sage tones.** Button fill is duller than the logo-tile sage; one accent should be one value. Also "Create **Coverage** Case" echoes H1 "Coverage Continuity". (Primary button vs logo; copy.)

**Bottom line:** components are individually tidy and the one-primary-action rule is respected, but this frame fails acceptance on the P0s — wrong screen/theme delivered, and body-level text is effectively illegible for the target user. Fix capture wiring, then contrast, then give the view a bezel and a real bottom anchor.
