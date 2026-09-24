judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/dark-discharge.png)

**Note on the path:** the exact attached path `/tmp/ha-ds-shots/judge-img/r2/dark-discharge.jpg` does not exist — `judge-img/r2` is itself a JPEG (and it shows the Coverage Continuity page, not Discharge). The only `dark-discharge.jpg` on disk is `/tmp/ha-ds-shots/judge-img/r1/dark-discharge.jpg`, which is what I judged. It shows the dark-theme HealthAdvocate "Discharge Translator" screen: an empty input card (label "PASTE DISCHARGE INSTRUCTIONS", placeholder text, green Translate button) with no output rendered, plus the footer disclaimer.

**Audit of `dark-discharge.jpg` (620×436, dark theme, Discharge tab active):**

1. **'This needs a human decision' banner: ABSENT.** No such banner exists anywhere on the screen; strength comparison is N/A because no machine answer is shown at all — it is an empty input form.
2. **Neutral 'unavailable' state: ABSENT.** The only gray text is the ordinary textarea placeholder ("Paste your discharge summary or after-visit instructions…") inside a solid-border field — there is no dashed-border unavailable state, and nothing present could be mistaken for an urgency rating or danger.
3. **Urgency badges: ABSENT.** No LOW/MEDIUM/HIGH filled pills appear; the only pill on screen is the amber "5 / 3 due soon" reminder in the top-right header, which is a navigation badge, not an urgency rating. Distinctness from an unavailable state is N/A (neither exists here).
4. **Provenance chips: ABSENT.** No extracted / inferred / unverified / you-confirmed chips are rendered; since no values are displayed, an inferred value cannot pass as confirmed on this screen.
5. **Demo/synthetic data badge: ABSENT.** There is no demo/synthetic badge on this screen; mitigating fact is that the screen contains zero data — only an empty form — so there is nothing synthetic being passed off as real.
6. **Danger vs. caution styling: ABSENT (not evaluable).** No danger/emergency styling exists on this screen to compare against the single caution-grade element (the amber "due soon" pill), so no hierarchy is violated.

**HONESTY-VERDICT: PASS** — no violation. This is an input-only state: no fallback, no machine answer, and no data are shown, so nothing can masquerade as a confident answer; the footer disclaimer ("here to support, not replace, professional medical guidance…") is present. Caveat for the record: all six honesty mechanisms are unexercised on this screen, so this pass says nothing about the result state after "Translate" is clicked — that would need a screenshot of the translated-output state.
