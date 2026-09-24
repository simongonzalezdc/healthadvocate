judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/light-discharge.png)

I can see the attached image (the Discharge Translator empty state), so I'll judge it directly as instructed.

**Honesty audit — `r3/light-discharge.jpg`**

1. **'This needs a human decision' banner: ABSENT.** No banner exists, but there is also no machine answer anywhere in the frame — this is a pre-submit empty input state, so nothing is being passed off as a confident answer.

2. **Neutral 'unavailable' state: ABSENT.** No gray/dashed "unavailable" element appears; the only dashed-ish field is the input textarea, which reads plainly as an empty input and could not be mistaken for an urgency rating or danger.

3. **Urgency badges (LOW/MEDIUM/HIGH pills): ABSENT.** No filled urgency pills are rendered anywhere in the frame.

4. **Provenance chips (extracted/inferred/unverified/you-confirmed): ABSENT.** No chips exist, so no inferred value can pass as confirmed — but also no provenance system is exercised in this frame.

5. **Demo/synthetic data badging: ABSENT (not applicable).** No data results of any kind are shown, so there is nothing synthetic to badge; the only data-ish element is the user's own empty textarea.

6. **Danger vs. caution styling: CAUTION PRESENT, DANGER ABSENT.** The sole caution element is the amber outlined "⚠ 1 reminder due soon" pill (top right), styled appropriately mild; with no danger/emergency element shown, no inversion or weak-danger violation is visible.

**Mitigating honesty feature present:** the footer states "HealthAdvocate is here to support, not replace, professional medical guidance. Always consult a qualified healthcare provider…" — an honest scope disclaimer.

**HONESTY-VERDICT: PASS** — no honesty violations in this frame; note the audit covers only the empty input state (banner, urgency badges, provenance chips, and unavailable states are unexercised here, not verified).
