judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-home.png)

I can see the image. Here's the audit.

## DESCRIPTION

**Layout, top-to-bottom:** White header band (logo chip + "HealthAdvocate" wordmark left; coral "#1 due soon" pill, dark avatar circle, light sun/theme circle right). Below it, a single-row nav of 10 items (Symptoms … Library) with a stray thin vertical mark after "Library". Then the warm-paper content area: letterspaced eyebrow pill "YOUR HEALTH ADVOCATE", two-line H1 "You deserve to understand your care.", one small gray paragraph. Below, a 2-column bento: one tall left card ("Something doesn't feel right", icon chip, title, 2-line body) and two stacked right cards ("I have a document to understand", "I need help with costs"), left card's bottom edge aligning with the right stack. Then ~45% of the page is empty paper until a hairline divider and a 3-line centered gray disclaimer footer.

**Palette as named hues:** Warm paper eggshell across the content field, near-white header. Sage green appears only in the logo chip. Coral appears once, as muted rust-coral text on the pink-tinted "#1 due soon" pill. Slate gray for all secondary text. Ochre: absent from this view entirely.

**Typography scale:** One sans family. H1 ~34–36px bold, tight leading. Everything else compresses hard: eyebrow ~10px caps, hero paragraph ~13px light gray, card titles ~13px semibold, card body ~12px gray, footer ~11px. The scale collapses to two effective sizes below the H1.

**Spacing rhythm:** Calm and generous inside the hero and cards (consistent padding, soft shadows, ~12px radii, hairline-free borderless cards). Rhythm then breaks: card grid ends near mid-page and nothing follows until the footer.

**Component quality:** Cards, icon chips, pills, and avatar circles are cleanly rendered, consistent radii, soft believable shadows. No misrendered assets. Build quality is good; composition is not.

## DEFECTS

- **P0 — Empty page body:** Region between the card grid (~y 50%) and the footer (~y 92%) is bare paper. Reads as a failed/unfinished render, not "generous calm spacing" — a user will scroll and think content is missing.
- **P1 — No primary action:** Sage-green accent appears nowhere on an actionable element. Three equal-weight white cards; the stated "one primary action per view" rule is unmet. "Something doesn't feel right" — the urgent path for this audience — has zero visual primacy (no sage chip, border, or fill distinction).
- **P1 — Dead space inside the hero card:** Left card's text ends ~halfway down; bottom half is empty white. The card is stretched to match the right column instead of its content being vertically composed or the card sized to content.
- **P1 — Type too small/low-contrast for the audience:** Hero paragraph and all card body copy are ~12–13px light slate on paper. For sick, overwhelmed users this is the usability failure mode the system exists to prevent. Card titles barely out-rank their body text.
- **P2 — Stray glyph in nav:** Thin vertical bar immediately after "Library" (top-right of nav row) — looks like a stray pipe/divider or a truncated eleventh item.
- **P2 — Cryptic header chip:** "#1 due soon" gives no referent (one of what?). Coral is the correct danger hue, but the label is unparseable at that size and placement.
- **P2 — Nav density, no state:** 10 undifferentiated small items, no current-page indicator, no grouping of related items (Documents/Bills/Discharge are one cluster conceptually).
- **P2 — Accent inconsistency in icon chips:** Left card's icon chip carries a green tint; the two right cards' chips are neutral gray. Same component, two treatments, neither marked primary.
- **P2 — Ochre/caution never used:** Not a defect per se on this view, but combined with sage's absence, the page ships with only coral doing semantic work.

**Summary:** Component craft is high; the page fails on composition — a bottomless dead zone, a half-empty hero card, and no primary action anywhere, which breaks the design system's two most load-bearing commitments.
