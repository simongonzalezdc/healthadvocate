judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/mobile-home.png)

Can see the image — audit follows.

## What I see

**Layout (top→bottom):** Header bar (dark-green heart logo + "HealthAdvocate" wordmark; right cluster: "•1 due soon" pill, outlined home button, circular theme toggle) → hairline → horizontal nav tabs (Symptoms / Documents / Bills / Insurance / fifth item clipped at edge) → large gap → sage eyebrow pill "YOUR HEALTH ADVOCATE" → two-line H1 "You deserve to understand your care." → gray body paragraph → three stacked white entry cards (sage pulse icon / slate document icon / ochre dollar icon, each with title + 2–3 line body) → **~60% of page height is empty paper** → small bold-lead disclaimer footer.

**Palette:** Cream paper ground, white card surfaces, warm-black text, mid-gray body copy. Accents: dark forest green (logo), sage (eyebrow pill, card-1 tile), slate blue (card-2 tile), ochre/tan (status pill, card-3 tile). Coral only as the tiny status dot, ambiguously rendered.

**Type:** Letterspaced uppercase eyebrow; large humanist H1 (~2 lines); ~14–15px body; micro footer. Scale steps read clean, no crowding in text blocks.

**Spacing/quality:** Card radius, hairline borders, and icon tiles are consistent and well-made. Spacing is generous above the hero, then the page simply stops — the calm reads as vacancy, not rest.

## Defects

- **P1 — Below card 3 to footer (~60% of page):** dead blank paper. Page renders as one-third content, two-thirds void — reads broken/unfinished, like missing content or an unconstrained min-height. The single worst issue.
- **P1 — Whole view:** no primary action. System commits to "one primary action per view"; the three cards are chromatically identical surfaces with equal weight, so nothing reads as *the* next step. Card 1's sage tile hints at it but the card chrome doesn't confirm.
- **P1 — Header, top-right pill:** "•1 due soon" collapses into two cramped micro-lines; numeral and label sit on broken baselines. Illegible at arm's length — restructure (e.g., "1 due soon" single line, or dot-only with label as sub-text).
- **P2 — Same pill:** dot hue sits coral/orange inside an ochre pill — mixes danger+caution semantics. "Due soon" is caution: ochre dot, full stop.
- **P2 — Top-right cluster:** home button (rounded-square outline) vs theme toggle (circle outline) — mismatched shape language side by side; home is also redundant on the home view.
- **P2 — Nav row, right edge:** fifth tab clips at ~one glyph ("Dru…") with no fade/scroll hint — reads as a typo, not a scroll affordance. Add an edge fade or wider peek.
- **P2 — Card 3 icon tile:** ochre (caution) assigned to "help with costs" — cost help is not a warning state; ochre leaks its semantics. Use neutral or sage.
- **P2 — Hero body paragraph:** mid-gray on cream is borderline contrast for the product's stated audience (sick, overwhelmed, possibly low-vision). One step darker.
- **P2 — Global rhythm:** gap between tab bar and eyebrow is ~2–3× the card gap; spacing doesn't read as a stepped scale, just inconsistent air.

Nothing is dishonest or truly broken at the component level — cards, header, and footer are well-built. The page-level failures are the dead zone, the missing hierarchy, and the collapsed status pill.
