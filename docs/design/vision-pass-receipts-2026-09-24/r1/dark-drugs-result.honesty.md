judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/dark-drugs-result.png)

Judging only the attached screenshot (dark-mode HealthAdvocate "Drugs" page, Drug Checker card with input "Lipior", a green Check Drug button, and a result line beneath).

1. **'This needs a human decision' banner: ABSENT.** No banner anywhere on the page; the only text near the result is the machine's own claim "This name was recognized by name matching against the medical dictionary," which is the strongest element in the card.

2. **Neutral 'unavailable' state: ABSENT.** No gray/dashed/sentence-case unavailable state appears; nothing exists that could be mistaken for an urgency rating or danger (N/A on that sub-check).

3. **Urgency badges (LOW/MEDIUM/HIGH pills): ABSENT.** No filled pills of any color are rendered, so distinctness from an unavailable state cannot be evaluated (N/A).

4. **Provenance chips: ABSENT — species not distinguishable.** The name-matched result "LIPIOR" (a fuzzy match on the likely typo of "Lipitor") carries no extracted/inferred/unverified/you-confirmed chip, so an inferred recognition is displayed as a bare, confident fact — it passes as confirmed.

5. **Demo/synthetic badge: ABSENT.** No "demo"/"synthetic"/"sample" badge appears; the form content (typed "Lipior") looks like live data with no synthetic-data marking.

6. **Danger/emergency styling vs caution styling: ABSENT (no comparison possible).** Neither danger nor caution styling is present; the only accent color is the green header icon and Check Drug button.

**HONESTY-VERDICT: FAIL** — Violation: the result block below the Check Drug button ("LIPIOR — This name was recognized by name matching against the medical dictionary") presents a fuzzy name-match fallback as a confident answer, with no 'needs a human decision' banner, no unverified/inferred provenance chip, and no uncertainty styling — directly breaching "a fallback must NEVER look like a confident answer."
