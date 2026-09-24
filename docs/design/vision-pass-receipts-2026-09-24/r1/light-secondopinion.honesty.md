judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-secondopinion.png)

I can see the attached screenshot (light-mode "2nd Opinion" intake page) and will audit it directly.

1. **'This needs a human decision' banner — ABSENT.** No banner anywhere; the only human-decision messaging is the small footer line "…not replace, professional medical guidance…" — no machine answer appears on this screen for it to outrank, so no fallback-confident-answer risk.

2. **Neutral 'unavailable' state — ABSENT.** No gray/dashed-border unavailable element exists on this screen; therefore it cannot be mistaken for an urgency rating or a danger (nothing to misread).

3. **Urgency badges — ABSENT.** No LOW/MEDIUM/HIGH pills appear; the only pill is the orange "#1 due soon" scheduling chip in the header, which is not an urgency rating. Distinctness from an unavailable state is not testable here (neither present), but no conflict exists.

4. **Provenance chips — ABSENT.** No extracted/inferred/unverified/you-confirmed chips are rendered; since none exist, an inferred value cannot pass as confirmed on this screen.

5. **Demo/synthetic data badge — ABSENT.** No demo or synthetic-data badge is visible — but this is an empty intake form (placeholder text only, no records or generated content), so there is no data present that could be mistaken for real.

6. **Danger vs. caution styling — ABSENT (danger styling).** No red/emergency styling exists on this screen; the only caution-adjacent element is the small orange "#1 due soon" chip. No danger content is shown, so there is no case where danger styling is weaker than caution.

Overall: this is an empty input state with an honest "support, not replace" disclaimer and "Your information stays on your device" note. Nothing on screen presents a fallback, machine answer, urgency rating, or unverified data, so the core product law (a fallback must never look like a confident answer) is not violated — there is simply no machine answer on this screen to be dishonest about.

**HONESTY-VERDICT: PASS** — no violations; all six checks are ABSENT/not-applicable because the screen contains only an empty intake form and a support-not-replace disclaimer, with no machine answer, fallback, badges, chips, or synthetic data rendered.
