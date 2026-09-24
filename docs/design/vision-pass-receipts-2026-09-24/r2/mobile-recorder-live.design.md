judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/mobile-recorder-live.png)

Read it — the attachment resolved to the 620×436 JPEG (`r2` is the file itself, not a folder). It's visible; auditing below.

## What I see

**Layout, top to bottom:**
1. Header bar (near-black): sage rounded-square badge with heart glyph + "HealthAdvocate" wordmark, left. Right: ochre pill "⚠ 1 reminder due soon" + two thin circular icon buttons (info, help).
2. Nav band: 11 flat items — Moments, Discharge, 2nd Opinion, Reconnect, Library, Directory, Scanner, Family, Tracks, Coverage, Help. "Coverage" active as a small sage pill.
3. Content: H1 "Coverage Continuity"; gray subtitle ("One calm place for your next coverage action. Local and private. No payments or submissions from this screen."); label "Case title (synthetic)"; one text input (placeholder "e.g. Synthetic job-loss coverage case"); sage filled button "Create Coverage Case".
4. Hairline divider, then a centered two-line legal disclaimer.
5. Bottom ~45% of frame: empty dark void.

**Palette as named hues:** background warm charcoal #1a1a18 (header darker, content surface marginally lighter); sage-green accent on badge, active pill, primary button; ochre/amber on reminder pill; off-white headings, mid-gray body. **No paper neutral anywhere. No coral, no slate in view.**

**Type scale:** compressed — wordmark ~13px bold, H1 ~17px, subtitle ~11px, label/nav ~10px, footer ~9px. H1 barely outguns body.

**Spacing:** consistent left axis in the form, ~12–16px stack rhythm; nav gaps tight; footer floats mid-canvas with dead space below.

**Component quality:** radii and hairlines are consistent and neat; nothing is pixel-broken. The problem is systemic, not sloppiness.

## Defects

- **P0 — entire viewport:** Dark charcoal UI shipped against a committed "warm paper clinic" palette. This is the wrong theme (or the system abandoned), not a variant — every hue relationship (warm paper + sage) is inverted. Whole screen reads as a different product.
- **P1 — content area:** No double-bezel workbench panel. The form floats naked on the background with a single hairline; the DS's signature panel component is absent.
- **P1 — nav band:** 11 undifferentiated items at ~10px, tight gaps, low-contrast gray on near-black. Journey items (Moments/Discharge), tools (Scanner/Library), and modes (Family/Tracks/Coverage) are flattened to one level — hierarchy failure for overwhelmed users.
- **P1 — nav band, "Coverage":** Active state is muted green-on-dark-green pill at ~10px — weak figure/ground; the current location doesn't pop.
- **P1 — form label + placeholder:** "(synthetic)" / "Synthetic job-loss coverage case" — internal test jargon leaks into user-facing copy, twice. Undermines trust for the exact audience (sick, anxious) that reads every word.
- **P1 — below the fold:** ~45% of frame is empty void with no empty-state, no case list region, no grounding. The page promises "Create Coverage Case" but shows no destination for results; footer disclaimer dangles mid-air.
- **P2 — header right:** Info and help circular buttons are near-identical thin outline circles, borders barely visible on dark; ambiguous affordances, crowded against the reminder pill (3-element cluster).
- **P2 — header right pill:** "1 reminder due soon" is a status rendered with button affordance (pill + icon). Also arguably slate=info, not ochre=caution — ochre over-alarms.
- **P2 — hero:** H1-to-subtitle scale ratio too tight; subtitle stacks three unrelated claims in one gray line.
- **P2 — form:** Input border and placeholder contrast are borderline-legible on charcoal (sage/paper-tuned tokens likely reused on dark).
- **P2 — primary button:** Undersized (~32px) and slightly washed sage for the view's one hero action; on dark it loses the warmth it has on paper.
- **P2 — footer:** Centered disclaimer breaks the page's otherwise strict left axis.

**Verdict:** Component craft is fine; this is a system-level failure — a dark build of a paper design system, plus missing panel/empty-state architecture and test copy in user view. Ship the paper theme, wrap the form in the double-bezel panel, prune/group the nav, and strip "synthetic" before this is presentable.
