judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/dark-coverage.png)

Judged `/tmp/ha-ds-shots/judge-img/r2` (the attachment path had `/dark-coverage.jpg` appended; the actual file is `judge-img/r2`, copied to a `.jpg`-named temp file to view it).

## What I see

**Layout, top to bottom:** Dark app shell. (1) Header bar: sage rounded-square heart logo + "HealthAdvocate" wordmark left; ochre pill "⏰ 1 reminder due soon" plus two small circular icon buttons (bell, theme toggle) right. (2) Nav strip: 11 text items — Moments, Discharge, 2nd Opinion, Reactor, Library, Directory, Scanner, Family, Tracks, Coverage, Help — with "Coverage" as the active sage pill, dark-on-sage. (3) Content column (~420px wide, left-aligned): H1 "Coverage Continuity"; two-line subline "One calm place… Local and private. No payments or submissions from this screen."; small label "Case title (synthetic)"; a dark bordered text input with placeholder; a single sage pill button "Create Coverage Case". (4) A faint rule, then a centered small-print disclaimer ("…support, not replace, professional medical guidance…"). (5) Below that: ~45% of the viewport is empty near-black void.

**Palette:** Charcoal near-black with slight warm undertone (not warm paper); cream/white text; sage-green primary (logo, active nav, CTA) — correct accent hue; ochre reminder pill; no coral or slate in view; no paper neutrals anywhere.

**Type:** Small compressed scale — H1 ~20px semibold, everything else clusters at ~11–12px. Hierarchy exists but the mid-scale is thin.

**Spacing:** Tight, orderly rhythm in the top 40%; the bottom 55% is dead space, so the composition collapses.

**Component quality:** Controls (pill button, input, badge) are cleanly rendered; one primary action only — good. But no double-bezel workbench panel: the form floats bare on the background.

## Defects

- **P0 — Footer/void break:** Disclaimer sits at ~52% viewport height with a vast empty black region beneath it (bottom half of page). Reads as a render failure / unpinned footer; the view looks broken, not calm.
- **P1 — Theme identity drift:** Whole page renders dark charcoal; committed system is "warm paper clinic" light neutrals. Unless a dark variant is sanctioned, this is off-system; if it is sanctioned, it's lost the warm-paper character entirely.
- **P1 — Missing workbench panel:** No double-bezel panel wrapping the create-case form (content area, y≈80–180). Form floats unprotected on the void; system's signature component is absent.
- **P1 — Nav overload:** 11 undifferentiated top-level items (Moments → Help) for sick, overwhelmed users; no grouping, labels like "Reactor" are jargon. Hierarchy problem at header row y≈30–55.
- **P2 — Ochre misuse:** "1 reminder due soon" pill (header right) uses the caution hue for routine info; dilutes the ochre=caution channel.
- **P2 — Muted text contrast:** Subline, field label, placeholder, and footer disclaimer all sit in the same low-contrast warm gray on near-black; footer small print is borderline at this size.
- **P2 — Icon-button affordance:** Bell and theme-toggle buttons (header right) are tiny dark-on-dark circles with low glyph contrast and no borders.
- **P2 — Mixed alignment:** Footer disclaimer is centered while the entire page is left-aligned; nav's left edge also appears a few px left of the brand above it — verify container padding.
- **P2 — Compressed type scale:** H1→body jumps from ~20px to ~12px with no intermediate weights/sizes; page lacks the generous, calm typographic ladder the system promises.

**Working well:** single sage primary action; honest copy ("Local and private…"); disclaimer present; sage accent hue correct wherever used.
