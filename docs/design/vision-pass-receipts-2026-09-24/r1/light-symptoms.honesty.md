judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-symptoms.png)

I can see the image clearly (HealthAdvocate "Symptoms" tab showing an empty Symptom Assessment intake form). Audit below — no files read or written.

1. **'This needs a human decision' banner: ABSENT.** No such banner exists anywhere on the page; the only guidance text is the footer disclaimer "…support, not replace, professional medical guidance," so there is no machine answer it needs to outrank.

2. **Neutral 'unavailable' state: ABSENT.** Nothing on the page uses a gray/dashed "unavailable" treatment (the only dashed-bordered element is the empty input textarea, which is a normal form affordance); since no unavailable state exists, it cannot be mistaken for an urgency rating or danger — no risk.

3. **Urgency badges (LOW/MEDIUM/HIGH filled pills): ABSENT.** No LOW/MEDIUM/HIGH pills appear; the only filled pill is the orange "#1 due soon" chip in the header, which is a task reminder, not an urgency rating — no confusion risk since no unavailable state coexists with it.

4. **Provenance chips: ABSENT.** No extracted/inferred/unverified/you-confirmed chips are shown, so the species-distinguishability question doesn't arise; with zero provenance chips present, no inferred value can pass as confirmed — but if assessment results render later, this page gives no evidence they will be labeled.

5. **Demo/synthetic data badge: ABSENT (and no demo data is visible).** The page contains only a blank form with placeholder text, so there is no synthetic content on screen; nothing is mislabeled, though there is also no standing "demo data" badge in the header.

6. **Danger/emergency styling vs caution styling: ABSENT (no danger or emergency styling at all).** The strongest visual emphasis on the page is the small orange "#1 due soon" pill and the solid green "Assess Symptoms" button; since no danger state is displayed, there is no hierarchy violation to flag — but this page also demonstrates no emergency affordance (e.g., no "call 911" path) for a symptom tool.

**Overall:** this is an empty intake screen with no machine answers, so no fallback can masquerade as a confident answer — the product's core honesty law is not violated here. Note the caveat that this screenshot cannot verify how honesty UI behaves once an assessment is rendered.

HONESTY-VERDICT: PASS — no violation found; all six audited honesty elements are ABSENT because the screenshot shows only a blank input form, and nothing present looks like a confident machine answer.
