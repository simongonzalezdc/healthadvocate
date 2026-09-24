judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/dark-discharge.png)

I can see the attached screenshot (dark-mode Discharge tab, empty translator form). Audit below — this frame shows only the input/empty state, which shapes every answer.

1. **'This needs a human decision' banner: ABSENT.** No such banner anywhere; the only header caution is a small amber "# 1 due soon" pill, and there is no machine answer on screen for it to outweigh.

2. **Neutral 'unavailable' state: ABSENT.** The frame shows only an empty textarea with placeholder text ("Paste your discharge summary or after-visit instructions...") — no unavailable/fallback output exists that could be mistaken for an urgency rating or danger.

3. **Urgency badges: ABSENT.** No LOW/MEDIUM/HIGH filled pills appear; the sole filled pill is the amber "1 due soon" task counter in the header, which is not an urgency badge.

4. **Provenance chips: ABSENT.** No extracted/inferred/unverified/you-confirmed chips are rendered, so there is no surface where an inferred value could pass as confirmed — nothing shown at all.

5. **Demo/synthetic data badge: ABSENT.** No demo/synthetic content is displayed (the form is empty), so no badge is needed or present; nothing on screen pretends to be real patient data.

6. **Danger/emergency styling: ABSENT (not assessable).** There is no red/danger styling and only mild caution styling (the amber "due soon" pill plus the footer disclaimer "support, not replace"), so no hierarchy violation is observable.

HONESTY-VERDICT: PASS — no violation of "a fallback must never look like a confident answer" is possible in this frame: it contains no machine answer, fallback, urgency badges, or provenance chips, only an honest empty input form with a support-not-replace disclaimer. (Note: this pass covers only the empty state; the required banner, unavailable state, badges, and chips must be verified on a frame that actually shows translated output.)
