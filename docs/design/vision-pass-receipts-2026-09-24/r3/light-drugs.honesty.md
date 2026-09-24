judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/light-drugs.png)

I can see the image clearly (the empty-state Drug Checker screen of HealthAdvocate), so here is the audit of that screenshot only.

1. **'This needs a human decision' banner: ABSENT.** No such banner exists on the screen; the only human-decision messaging is the small gray footer line "…to support, not replace, professional medical guidance," which is low-emphasis — but there is also no machine answer on this screen for it to compete with.

2. **Neutral 'unavailable' state: ABSENT.** The screen is a bare input form (label, text field, "Check Drug" button); there is no unavailable state rendered, and nothing on screen could be mistaken for an urgency rating or a danger.

3. **Urgency badges (LOW/MEDIUM/HIGH filled pills): ABSENT.** No urgency pills appear; the only pill-shaped element is the orange outlined "+1 reminder due soon" chip in the header, which reads as a reminder notice, not an urgency rating.

4. **Provenance chips: ABSENT.** No extracted/inferred/unverified/you-confirmed chips are visible anywhere, so no species comparison is possible — and no inferred value can pass as confirmed because no values are shown at all.

5. **Demo/synthetic data badge: ABSENT (and no demo data present).** Everything on screen is UI chrome and a placeholder example ("e.g., Lipitor, Zoloft, Advair" inside an empty input), which is correctly rendered as placeholder text, not presented as data.

6. **Danger vs. caution styling: NEITHER PRESENT / not evaluable.** There is no danger/emergency styling on this screen at all; the strongest accent is the mild orange reminder chip, so no violation, but also no hierarchy to verify.

**Context note:** this screenshot is the pre-search entry state — no answer, fallback, or result content is displayed, so the "fallback must never look like a confident answer" law is not exercised here. The footer disclaimer is present and honest ("not replace, professional medical guidance… Your information stays on your device").

**HONESTY-VERDICT: PASS** — no violation found; all audited elements are absent because this screen shows only the empty input form, with no machine answer, urgency badges, provenance chips, unavailable states, or synthetic data displayed.
