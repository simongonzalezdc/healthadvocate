judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-community.png)

Audit of the attached dark-mode screenshot (Community Health Scanner page, empty input state). I can see the image; judging only it.

1. **'This needs a human decision' banner: ABSENT.** No such banner anywhere; the only banner-like element is the amber "+1 reminder due soon" pill in the header, which is a reminder count, not a machine answer. No violation — there is no machine answer on screen for a banner to outrank.

2. **Neutral 'unavailable' state: ABSENT.** The page is an empty paste-a-bulletin form (label + placeholder textarea + Scan button); no unavailable/fallback element exists, so nothing could be mistaken for an urgency rating or danger.

3. **Urgency badges: ABSENT.** No LOW/MEDIUM/HIGH filled pills appear; the only filled pill is the header's "+1 reminder due soon," which is amber but conveys a reminder count, not a graded urgency.

4. **Provenance chips: ABSENT.** No extracted/inferred/unverified/you-confirmed chips are shown, so no species-confusability or inferred-passing-as-confirmed risk can arise.

5. **Demo/synthetic data badge: ABSENT (and N/A).** No data, results, or sample content are displayed at all — only an empty input — so there is nothing synthetic that needs a badge.

6. **Danger vs. caution styling: ABSENT (N/A).** The sole accent colors are the amber reminder pill and the green Scan button plus green logo; no danger/emergency styling exists, so there is no hierarchy to compare.

The screen shows no AI output, fallback, or data states at all — it's an entry form with an appropriate footer disclaimer ("support, not replace, professional medical guidance… stays on your device"). Nothing violates the rule that a fallback must never look like a confident answer, because no answer or fallback is rendered.

HONESTY-VERDICT: PASS
