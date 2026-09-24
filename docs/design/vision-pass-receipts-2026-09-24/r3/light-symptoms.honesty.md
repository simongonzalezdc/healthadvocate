judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/light-symptoms.png)

Judging the attached screenshot only (HealthAdvocate "Symptom Assessment" screen, light mode, empty input state).

1. **'This needs a human decision' banner: ABSENT.** No such banner exists anywhere on the screen — only the Symptom Assessment card, an empty textarea, and an "Assess Symptoms" button; there is also no machine answer near it, so nothing outranks anything.

2. **Neutral 'unavailable' state: ABSENT.** No gray/dashed-border/sentence-case fallback element is rendered; since none exists, it cannot be mistaken for an urgency rating or danger (NO risk).

3. **Urgency badges: ABSENT.** No LOW/MEDIUM/HIGH filled pills appear — this is the pre-assessment input state, so there is nothing to distinguish from an unavailable state.

4. **Provenance chips: ABSENT.** No extracted/inferred/unverified/you-confirmed chips are visible; no species to compare, and no inferred value exists that could pass as confirmed.

5. **Demo/synthetic data badge: ABSENT — but nothing to badge.** The screen displays no data at all (empty textarea, placeholder only), so no synthetic content is being passed off as real; the only disclaimer is the footer's scope-of-support note.

6. **Danger vs caution styling: ABSENT (both).** The strongest accent on the page is the solid green "Assess Symptoms" button plus a soft amber-outlined "1 reminder due soon" chip; there is no red/emergency styling and no caution panel, so no hierarchy conflict is visible.

**HONESTY-VERDICT: PASS** — no dishonest pattern is visible: no fallback styled as a confident answer, no urgency badge, no provenance chip, and no data presented without attribution. Caveat: this is the empty input screen, so all audited honesty elements are absent rather than validated; the result/post-assessment screen is where questions 1–4 and 6 can actually be confirmed.
