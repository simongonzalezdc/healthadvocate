judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/light-drugs-result.png)

**DESCRIPTION**

Top-to-bottom: (1) warm-white top bar — sage rounded-square heart logo + "HealthAdvocate" wordmark left; coral-tinted pill "1 reminder due soon" + two circular ghost icon buttons (gear, moon) right. (2) Horizontal nav rail: Documents, Bills, Insurance, **Drugs** (active, sage-outlined pill), Appointments, Discharge, 2nd Opinion, Recorder, Library, Directory, plus a partially clipped item at the right viewport edge. (3) Centered white workbench card on warm paper ground: small pale-sage icon tile + "Drug Checker" H1 + one-line subtitle; uppercase micro-label "DRUG NAME"; full-width light-fill input containing "Lipitor"; sage "Check Drug" pill button (the only filled control — good, one primary action); result line "1. LIPITOR" in small slate caps; tiny italic gray parenthetical about name-matching; pale-ochre bordered callout stating the optional model is off and this is not a drug review (honest — good). (4) Hairline rule + centered gray footer disclaimer.

Palette: warm paper neutrals throughout; sage = logo/active nav/primary button; coral = reminder pill; ochre = caution callout; slate = result text. Typography scale is compressed: ~20px semibold heading, ~13px body, ~10–11px uppercase labels/captions. Spacing rhythm is generous and calm; left margins inside the card are consistent. Component quality is generally clean — consistent radii, restrained borders, no visual noise.

**DEFECTS**

- **P0 — Nav overflow:** last nav item clipped mid-glyph at the right viewport edge (~x=630, "Bi…"). Eleventh nav item with no overflow/scroll affordance — reads as broken, item unreachable.
- **P1 — Input value contrast:** "Lipitor" in the input (center-left of card) renders placeholder-gray on the light fill. A submitted value should be foreground-dark; as rendered it's ambiguous whether it's real input, and likely fails 4.5:1.
- **P1 — Coral misuse on reminder pill:** "1 reminder due soon" (top-right) uses coral, which the system reserves for danger. A scheduling nudge is ochre-level at most; coral in the masthead reads as alarm to anxious users and dilutes real danger states.
- **P1 — Result hierarchy inverted:** the entire product output — "1. LIPITOR" — is a ~12px slate caps line, visually weaker than the "DRUG NAME" label above it. The payoff of the primary action is the least prominent text in the card.
- **P2 — Result styled as link:** "LIPITOR" is slate/blue and small, pattern-matching a hyperlink though it isn't one.
- **P2 — Orphaned caption:** the italic name-matching parenthetical (below the result) floats between result and callout at ~10px light gray; illegible-adjacent and structurally unattached to either.
- **P2 — Label contrast:** "DRUG NAME" micro-label is very light gray at ~10px uppercase; borderline legibility for the exact low-vision audience this tool serves.
- **P2 — Bezel spec:** card reads as a single white surface with one hairline border; the committed double-bezel workbench treatment (inner second surface) is not visible.
- **P2 — Dead space:** content ends ~55px above the card's bottom edge, leaving an empty band that makes the sparse result feel unfinished.

**PASSES:** one primary action per view held; ochre callout used correctly and states its limits honestly; spacing rhythm and radii consistent; coral/ochre/slate otherwise used per system.
