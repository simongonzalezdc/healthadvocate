**1. Three highest-leverage moves (ranked)**

**A. Kill the misalignment system-wide (adversarial 5.4 is your ceiling).** Every defect is the same defect: no shared measure. Lock a 12-column grid on a 24px gutter at 1072px max-width (logo, nav, cards, card-rows all snap to x=209/1071), and one 8px spacing scale with named tokens (`s-2=8, s-3=16, s-4=24, s-6=48`). Concrete fixes: nav row x=209 not 221; header right cluster ends x=1071 not 1060; directory card rows share a 200px label column (title "Dr. Maya Patel" and "PHONE"/"ADDRESS" both at x=279); library card titles at x=279 like body; card gaps = internal padding (24px, not 17px or the 2.5x dead zone on home-light); equal card widths (50/50 with 24px gutter). This alone moves adversarial 5.4→8.5, spacing 8.3→9.5, taste 7.3→8.5.

**B. Rebuild the header cluster + theme swatches (it appears in 6 of 9 adversarial shots and taste/a11y/deslop).** Make theme swatches real controls: 28px circles, 2px gap, inside one 36px pill container with `aria-label="Theme: Gold"` and a 2px active ring; all four equal diameter (the gold 25px vs 15px dots read as a bug). Unified 44px hit targets, one baseline row (fix the 40px reminder pill vs 32px neighbors). This converts "colorful filler dots" (deslop) into legible product features.

**C. Contrast + type-scale pass (a11y 6.0, typography 7.5).** Dark theme: hero headline to ≥4.5:1 (warm cream on brown, not muted beige), "Fight a denial" as a real secondary button (1px warm border, 15px/600) — currently near-invisible; placeholder tan to 4.5:1; reminder pill text ≥14px at 4.5:1. Five-step scale, strict: 13px meta / 15px body / 18px lede+nav (fix "Help"/"More" rendering smaller) / 22px heading → raise to 28px for real hierarchy / 40px display. Script font only ≥16px, only for the hero accent — never captions or numerals.

**2. Per-dimension, the one closing change**
- **taste (7.3→10):** one radius language — 999px pills for actions/chips only, 16px cards, 8px tiles — and one icon-tile fill (warm tan) across all cards; mute the reminder pill so it stops out-shining the CTA.
- **color (9.0→10):** dark-mode warmth without contrast loss: lift lightness 6–8% on text tokens, keep hues; verify AA in all four themes, not just gold.
- **typography (7.5→10):** numerals in the numbered steps get a 12px gutter (not 24) at 1.6 line-height; kill the "Assess  Symptoms" tracking bug (double space or `word-spacing` leak).
- **spacing (8.3→10):** trim the card's oversized bottom padding below "Assess Symptoms" to match top; hero→cards gap = 2× intra-hero gap, not 3×.
- **deslop (8.8→10):** paper grain (3–5% noise) + hairline edge on card surfaces so layers read as stacked paper, and give each avatar dot a presence state (name + status) instead of anonymous color.
- **a11y (6.0→10):** 44px targets on the avatar dots and home button, visible 2px focus rings, and skip-link; contrast per C above.
- **artdirection (7.0→10):** replace the flat empty desk with the literal narrative — a hand placing a stamped, coffee-ringed denial letter beside the lamp; replace the monospace "FREE · OPEN SOURCE" with a rubber-stamp treatment; draw warm custom icons (ECG as a stitched heartline, not a clinical squiggle).
- **adversarial (5.4→10):** mobile nav gets scroll affordance (fade + chevron, no "Ap" clipping) and wraps to two rows under 390px; fix the cut-off pill/avatar grouping at the viewport edge; column-align all "Confirm" buttons to a shared right rail.

**3. STOP doing**
Monospace/dev-speak badges; dashed one-off style vocab ("DEMO MODE"); generic clinical glyphs in squares; script type at meta sizes; unequal sibling cards and mixed radii; flat textureless surfaces claiming "plush"; treating alignment as per-page eyeballing.

**4. The biggest risk**
Chasing pixel-sameness into a sterile design-system museum — 10/10 geometry with zero warmth fails the actual brief ("a friend helps you"). S+ is *felt care plus invisible rigor*; if the hand, the stamps, and the tea disappear in service of the grid, you've built the cold SaaS portal users are already scared of.