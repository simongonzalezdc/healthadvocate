judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-drugs-result.png)

The screenshot is visible, so here is the audit of the Drug Checker result screen (dark theme, "Lipitor" queried, model-off fallback shown).

1. **Human-decision banner: ABSENT.** No "This needs a human decision" banner appears anywhere; nothing on this screen presents itself as a machine answer needing sign-off, so no banner is being overpowered either.
2. **Neutral unavailable state: PRESENT (mostly).** A low-contrast gray box reads "No drug details were generated — the optional model is off. Only the name match above is real; this is not a drug review" in sentence case; the border reads as solid rather than dashed, and its gray styling cannot be mistaken for an urgency rating or danger.
3. **Urgency badges: ABSENT.** No LOW/MEDIUM/HIGH pills exist on this screen (the only pill is the amber "+1 reminder due soon" chip in the header, unrelated to the result), so no confusion with the unavailable state is possible.
4. **Provenance chips: ABSENT.** There are no extracted/inferred/unverified/you-confirmed chips; provenance is carried instead by the small gray note "This name was recognized by name matching against the medicine dictionary," and since no inferred values are displayed, none could pass as confirmed.
5. **Demo/synthetic badge: ABSENT (and appropriately so).** No synthetic drug details are shown — the disclaimer explicitly states no details were generated and only the name match is real, so nothing fake is on display to badge.
6. **Danger vs. caution styling: ABSENT (no danger styling on this screen).** The only caution-toned element is the amber reminder chip in the header; with no emergency or warning content in the result area, there is no hierarchy to violate.

The core product law holds: the fallback is muted, gray, and self-disclaiming ("this is not a drug review"), while the only confident element ("1. LIPITOR") is a real dictionary match explicitly labeled as such.

HONESTY-VERDICT: PASS
