judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/dark-help.png)

I can see the image. Audit follows.

## Description

**Layout (top→bottom):** Dark charcoal app shell. (1) Header bar: sage-green logo tile with white shield-check, "HealthAdvocate" wordmark left; right side has an orange/coral pill chip "⏱ 1 due soon", plus two ghost icon buttons (book, moon). (2) A single horizontal nav row of 11 text items (Intake … Coverage), with "Help" at far right in a sage-green active pill. (3) One centered card occupying most of the viewport, containing four micro-headed sections: "HELP & REAL HUMANS" (intro paragraph), "CRISIS SUPPORT (US)" (two hotline bullets), "FIND HELP WITH COVERAGE AND CARE" (three bullets, two sage links), "HOW HEALTHADVOCATE REPORTS ITSELF" (long paragraph). A thin sage strip sits at the card's bottom-center edge. (4) Hairline rule, then a centered two-line disclaimer footer.

**Palette:** Cool near-black/charcoal field (~#1a1c1a), slightly lighter raised card, white/near-white primary text, mid-gray secondary, sage-green accent (logo, active pill, links, bottom strip), one orange/coral chip. No warm paper neutrals anywhere — this reads as an inverted-cool dark theme, not a warmed dark counterpart.

**Type:** Single small sans scale; section heads are ~10–11px letterspaced uppercase in dim gray; body ~12–13px muted gray; no display-size heading exists on the page — the largest type is the logo wordmark. Hotline numbers are inline, same body size, differentiated only by bold and an underline.

**Spacing/components:** Generous, even section rhythm inside the card; consistent pill/radius language; hairline dividers. Nav active state is a filled pill. Ghost icon buttons are low-contrast but consistent.

## Defects

- **P0 — Clipped/broken element, card bottom-center (~x 300, y 383):** a thin sage strip protrudes at the card's bottom edge, vertically crushed (~6px tall). It reads as a clipped or collapsed button — broken rendering, not a divider.
- **P0 — Crisis numbers not scannable, "CRISIS SUPPORT (US)" bullets:** 988 and 1-800-662-4357 are body-size, muted-gray inline text with only bold/underline. For this product's core audience (sick, overwhelmed users), crisis numbers must be the largest, highest-contrast elements on the page. Current treatment is a safety-level legibility failure.
- **P1 — Committed theme violated, entire page:** "warm paper clinic" specifies warm paper neutrals; the screenshot is a cool charcoal dark theme with no warm cast. If dark mode is a sanctioned variant, it wasn't derived from the paper palette (no warm-tinted surfaces, no paper-equivalent ink tones).
- **P1 — No primary action on the view:** "one primary action per view" — this view has zero usable primary action (the only sage action-like element is the clipped strip in P0). The only colored CTA-looking element is the "1 due soon" chip, which is a status, not an action.
- **P1 — Semantic color misuse, header chip:** "1 due soon" is rendered in coral/orange. System says coral=danger, ochre=caution; an upcoming due item is caution at most. As rendered it broadcasts alarm on a calm help page.
- **P1 — Section headers nearly illegible:** all four letterspaced uppercase heads ("HELP & REAL HUMANS" etc.) are dim gray at ~10px on dark — contrast is marginal and they fail as wayfinding.
- **P2 — Links under-differentiated, "FIND HELP" bullets:** sage link text relies on hue alone (no underline); sage-on-charcoal is mid-contrast and won't survive color-vision or glare conditions.
- **P2 — Nav crowding, header/nav:** 11 same-weight items in one row; active "Help" pill is at the extreme right, farthest from scan start. No grouping of related items.
- **P2 — Flat typographic scale, whole page:** no h1/display level anywhere; the page opens at label size. Content hierarchy is carried entirely by color and spacing.
- **P2 — Ghost icon buttons, header right:** book/moon icons are very low contrast against the header; affordance barely reads.

**Verdict:** Structurally calm and consistent, but not shippable — the clipped sage element and the crisis-number treatment are must-fix before this screen faces users.
