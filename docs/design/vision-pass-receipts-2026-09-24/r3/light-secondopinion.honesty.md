judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/light-secondopinion.png)

Audit of the attached light-mode "Second Opinion Brief" screenshot (judged from the image only, no files touched):

1. **'This needs a human decision' banner: ABSENT.** No banner anywhere; the only human-in-the-loop messaging is the small gray footer line "HealthAdvocate is here to support, not replace, professional medical guidance…" — but no machine answer appears on this screen, so nothing outcompetes it.

2. **Neutral 'unavailable' state: ABSENT.** The only gray element is the standard empty textarea with placeholder "Paste medical records, test results, treatment history…", which reads as an input field, not an availability status — it cannot be mistaken for an urgency rating or danger.

3. **Urgency badges: ABSENT.** No LOW/MEDIUM/HIGH filled pills exist; the only pill is the amber-outline "1 reminder due soon" chip in the header, which is a scheduler notice, not an urgency rating.

4. **Provenance chips: ABSENT.** No extracted / inferred / unverified / you-confirmed markers appear, so an inferred value cannot pass as confirmed — no values of any kind are shown.

5. **Demo/synthetic data badge: ABSENT.** The screen shows an empty form with placeholder text only, so no synthetic data is displayed and none is labeled; nothing here claims to be real data either.

6. **Danger vs. caution styling: NO.** No danger/emergency styling is present at all, so it cannot be stronger — the only alert-toned element is the soft amber reminder chip, making caution the strongest tone on screen (acceptable here since no emergency claim is being made).

**HONESTY-VERDICT: PASS** — this is an empty input screen with no machine answer, fallback, urgency rating, or data values rendered, so nothing can be mistaken for a confident answer; the "support, not replace" footer disclaimer is present. No violations found.
