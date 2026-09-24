judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/dark-directory-live.png)

# Audit — `dark-directory-live` (620×436 capture)

## Description

**Layout, top to bottom:** Warm near-black app frame. Bar 1: sage shield glyph + "HealthAdvocate" wordmark left; coral-outlined status pill "● 1 reminder due soon" plus two small icon buttons (bookmark-ish, moon) right. Bar 2: single-row nav of 11 equal items — Intake, Discharge, 2nd Opinion, Recorder, Library, Directory, Scanner, Family, Tracks, Coverage (active, sage-tinted pill), Help. Content column (~101→518px): H1 "Coverage Continuity", one-line description, a muted "Case title (synthetic)" line, full-width text input with placeholder, sage pill button "Create Coverage Case". Then a near-invisible hairline divider, centered two-line legal footer — and ~43% of the viewport is empty black below it.

**Palette as named hues:** Background is warm near-black (rgb 24,23,19), with a slightly warmer brown header strip — a dark-mode reading of "warm paper." Sage-green survives as the advocate accent (icon, active nav pill, primary button ≈ #6C9E79). Coral appears once, as the reminder pill's outline/text. No ochre or slate anywhere on screen. Ink tiers: cream heading, gray body, dimmer nav/footer.

**Type scale:** Two visible levels — a ~16–17px semibold heading and ~11px body/nav; no middle tier. Nav items are very small.

**Spacing rhythm:** Header bars are tall and calm; the form column has consistent left alignment (heading, input, button all flush at x=101). But "calm" collapses into emptiness: content ends mid-viewport with a stranded footer.

**Component quality:** Single primary button — correct. Input is one hairline bezel, no panel around it. Divider and icon-button glyphs are at the edge of visibility.

## Defects

*(No P0s — nothing illegible, nothing factually misrepresented, internal alignment is clean.)*

- **P1 — Whole-screen palette abandons the committed system.** "Warm paper clinic" is a paper-neutral system; this is warm-black dark mode with no paper surface anywhere. If dark is a sanctioned theme it needs its own spec; as shipped it reads as a different product. Biggest single divergence.
- **P1 — Double-bezel workbench panel missing.** Content column, "Coverage Continuity" form area: heading/input/button float raw on the void. The system's signature double-bezel panel appears nowhere; the input is a single faint hairline.
- **P1 — Coral misused as caution.** Header right pill "1 reminder due soon": coral is the danger hue per system; a due-soon nudge is ochre. Putting danger-color chrome on every screen of a tool for sick, anxious users is both a semantic break and an anxiety generator.
- **P1 — Field label indistinguishable from body copy.** "Case title (synthetic)" (directly above the input) is identical size/weight/color to the marketing sentence above it — it reads as a third clause of the paragraph, not a label. No bold, no ink step.
- **P1 — QA copy leaked into user-facing UI.** "Case title (synthetic)" + placeholder "e.g. Synthetic job-loss coverage case." "Synthetic" is dev-speak; to the target user it suggests their data is fake. P0 if this is a production build (filename says "live") rather than an flagged demo mode.
- **P1 — Stranded footer / dead viewport.** Content and footer terminate at ~y247 of 436; the bottom 43% is empty background. Reads as an unfinished render, not "generous spacing." Footer should anchor to the viewport bottom or the region below the divider needs an empty-state (e.g., "No coverage cases yet").
- **P1 — Nav: 11 undifferentiated items.** Second bar, full width. No grouping, no overflow, no order logic visible; equal weight and ~10px type. Wayfinding load is high for overwhelmed users; consider grouping primary vs. tools.
- **P2 — Three different left edges in the top 100px.** Nav starts at x=88, header shield at x=96, content column at x=101. Nothing shares a left rail across the three stacked regions.
- **P2 — Near-invisible divider.** Above the footer (~y193): ≤6 gray levels above background. Either intentional calm or invisible; currently reads as a rendering artifact.
- **P2 — Icon buttons unlabeled and faint.** Header right: two ~24px buttons with glyphs at the edge of legibility on dark; no visible tooltip/label. The moon (theme toggle?) is guessable; the first is not.
- **P2 — Muted text tiers sit near contrast floor.** Inactive nav items, placeholder, and footer legal text are all low-contrast gray on warm black; at real font sizes the nav row especially risks failing WCAG AA.
- **P2 — Compressed type scale.** Heading is only ~1.5× body; no section subhead or middle tier anywhere. The page hierarchy rests entirely on one small H1.
