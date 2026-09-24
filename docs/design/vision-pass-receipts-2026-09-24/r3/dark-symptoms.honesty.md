judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-symptoms.png)

I can see the attached screenshot (HealthAdvocate, dark mode, Symptom Assessment intake screen). Audit of that image only:

1. **'This needs a human decision' banner: ABSENT** — the screen shows only an empty intake form ("Describe your symptoms and we'll identify possible conditions…") with no machine answer rendered anywhere, so there is no banner and nothing for it to outrank.

2. **Neutral 'unavailable' state: ABSENT** — no gray/dashed/sentence-case unavailable element appears; since no result or fallback is shown at all, there is nothing that could be misread as urgency or danger.

3. **Urgency badges: ABSENT** — no LOW/MEDIUM/HIGH pills exist; the only filled pill is the amber "+1 reminder due soon" chip in the header, which is a reminder notification, not an urgency rating, and nothing shares its style.

4. **Provenance chips: ABSENT** — no extracted / inferred / unverified / you-confirmed markers are visible; no risk of inferred passing as confirmed because no values are displayed.

5. **Demo/synthetic data badge: ABSENT** — no demo or synthetic-data label is present; the screen displays no data whatsoever (only a placeholder text field), so nothing synthetic is being shown unlabeled.

6. **Danger vs. caution styling: NEITHER PRESENT** — the only color signals are the green brand logo, green "Assess Symptoms" CTA, and the amber header reminder chip; no danger/emergency or caution styling exists to compare, though it's worth noting the placeholder invites typing "chest pain and shortness of breath" with no emergency-call affordance on this screen (the footer disclaimer is the only safety text).

HONESTY-VERDICT: PASS — no honesty violation is visible on this screenshot; it is a pre-result intake screen, so none of the honesty-critical states (fallback answers, urgency badges, provenance chips, unavailable states) are exercised. Note the audit is necessarily shallow: this image cannot prove those states behave honestly once results render.
