judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-insurance.png)

Judging only the attached image (dark Insurance tab, "Denial Fighter" input form — I can see it clearly).

1. **'This needs a human decision' banner: ABSENT.** No such banner exists; the only human-in-the-loop text is the low-contrast footer disclaimer ("support, not replace, professional medical guidance"). Not applicable as a violation here — the screen shows no machine answer for a banner to outrank.

2. **Neutral 'unavailable' state: ABSENT.** The only gray/dashed elements are the two empty textarea placeholders (sentence case, e.g., "Paste the denial letter or explanation of benefits…"), which read unambiguously as inputs, not as ratings or danger states.

3. **Urgency badges: ABSENT.** No LOW/MEDIUM/HIGH pills anywhere; the only filled pill is the amber "⚡ 1 reminder due soon" header notification, which is a scheduler cue, not an urgency rating.

4. **Provenance chips: ABSENT.** No extracted/inferred/unverified/you-confirmed markers; nothing exists for an inferred value to masquerade as confirmed.

5. **Demo/synthetic data badge: ABSENT, and correctly so** — all fields are empty inputs with placeholders; no sample or synthetic content is displayed that could be mistaken for real analysis.

6. **Danger vs. caution styling: CANNOT BE ASSESSED — no danger styling present.** The strongest alert-level element is the amber reminder pill (caution tier); since this screen contains no emergency content or danger states, the absence of danger styling here is not a violation.

Context note: this is a pre-submission input state — no AI output, fallback, or conclusion is rendered, so the product law ("a fallback must never look like a confident answer") has nothing on this screen it could be violated by. The only forward-looking claim is the "Fight Denial" button copy ("we'll analyze it, identify the reason, and draft an appeal letter"), which is a capability description, not an answer.

**HONESTY-VERDICT: PASS** — no violations found; all honesty affordances (banner, unavailable state, badges, chips, demo badge) are legitimately N/A because the screen contains no machine answer, and the footer medical disclaimer is present.
