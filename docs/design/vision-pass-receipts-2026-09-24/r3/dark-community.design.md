judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-community.png)

I can see the image. Audit follows.

## Description

**Layout (top→bottom):** Fixed header (~44px): sage rounded-square logo tile + bold "HealthAdvocate" wordmark left; coral-outlined pill "· 1 reminder due soon" + two circular icon buttons (bell, moon) right. Below, a single-row horizontal nav of 11 small text links (Documents … Directory) ending in a sage-highlighted active pill that runs off the right edge. Main stage: one centered dark workbench panel (~y 90–310) containing an orange glyph tile + "Community Health Scanner" heading, one dim description line, a small-caps field label, a large bordered textarea with placeholder, and a sage "Scan" pill. Thin divider, then a two-line centered footer disclaimer.

**Palette:** Near-black warm-umber app background, slightly lighter panel; off-white heading/wordmark; mid-gray secondary text; sage-green accent (logo, active nav, Scan — consistent); coral on the reminder pill; orange glyph in the scanner tile. Hues track the system tokens, but the field is inverted, not paper.

**Typography:** Single sans family. Wordmark ~14px bold; heading ~18px semibold; body/placeholder ~12px; nav ~11px; label ~10px caps. Scale is coherent but globally small.

**Spacing/component quality:** Left edges of icon tile, label, textarea, and Scan align cleanly; generous calm margins; consistent pill radii; restrained, motion-free. One filled action per view (Scan) — the system's "one primary action" rule is honored.

## Defects

- **P0 — Active nav pill clipped at right viewport edge** (nav row, far right, ~x 600–620): the highlighted active item is truncated mid-word, past the last visible link "Directory". Nav overflows its container with no wrap/scroll affordance — a broken interactive element on the delivered screen.
- **P1 — Theme drift from committed system**: full dark mode abandons "warm paper neutrals"; background reads neutral soot, not warm paper. If this is a sanctioned dark variant, fine — but nothing in the frame says intentional variant rather than drift.
- **P1 — Low-contrast secondary text at small sizes**: heading description line (~y 128), textarea placeholder (~y 175), and footer disclaimer (~y 352) are mid-gray on dark at 12px — likely below 4.5:1, hostile to the exact audience (sick, overwhelmed, possibly older users).
- **P1 — Coral misuse on reminder pill** (header right): coral = danger per system, but "1 reminder due soon" is routine urgency — should be ochre/caution. As-is, it teaches users to ignore the danger color.
- **P1 — Nav usability**: 11 links at ~11px with tight gaps (~x 95–560) make small, error-prone targets for trembling or low-vision users; no grouping or hierarchy among sections.
- **P2 — Stray text bullet in reminder pill**: leading "·" before "1" renders as a typed character, not a status dot — reads as a typo.
- **P2 — Semantic-hue leakage on scanner icon tile** (panel top-left): orange glyph uses a caution/danger-family hue as mere decoration, diluting the token system.
- **P2 — Double-bezel treatment invisible**: panel edge-to-background separation is barely perceptible at this contrast; the committed workbench bezel reads as a flat card.
- **P2 — Dead-zone bottom of panel** (~y 290–310) and large void between panel and footer (~y 310–350): bottom-heavy emptiness; the view feels unanchored.
- **P2 — Redundant instruction layers**: label "PASTE A HEALTH BULLETIN OR ALERT" (~y 155) repeats the placeholder's content almost verbatim.
- **P2 — Icon-button glyphs (bell, moon, ~x 515/545) nearly invisible** against their dark circles — lowest-contrast controls on the page.

**Strengths worth keeping:** sage accent discipline, single primary action, aligned left rhythm, calm spacing — the bones are on-system; the failures are the clipped nav, contrast, and coral semantics.
