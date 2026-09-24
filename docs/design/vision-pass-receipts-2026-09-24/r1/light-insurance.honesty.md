judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-insurance.png)

Audit of the attached screenshot (HealthAdvocate → Insurance tab → "Denial Fighter" input form):

1. **"This needs a human decision" banner — ABSENT.** No such banner anywhere; the only attention-grabbing elements are the red "#1 due soon" pill (top right) and the green "Fight Denial" CTA. No violation here because no machine answer is shown on this screen, so there is nothing the banner would outrank — but it is not present.

2. **Neutral "unavailable" state — ABSENT.** The two gray-bordered boxes are empty input textareas with placeholder text, not an unavailable/fallback state; since nothing presents itself as data, there is nothing that could be mistaken for an urgency rating or danger.

3. **Urgency badges — PRESENT (one).** A filled red-orange pill "#1 due soon" at the top right of the header; it is the only filled state chip on screen and is trivially distinct from an unavailable state, though it carries no LOW/MEDIUM/HIGH scale.

4. **Provenance chips — ABSENT.** No extracted / inferred / unverified / you-confirmed markers anywhere; moot on this pre-analysis screen since no values are displayed, so an inferred-as-confirmed confusion is not currently possible.

5. **Demo/synthetic badge — ABSENT.** The screen shows live-looking state ("#1 due soon") with no demo or synthetic-data label; if this build is running demo data, that would be a violation — nothing on the image marks it either way.

6. **Danger vs. caution styling — NOT TESTABLE / PARTIAL.** The only strong styling is the filled red "#1 due soon" pill (urgency); no caution-tier styling exists on screen to compare against, so danger being "clearly stronger" cannot be demonstrated here.

Mitigating context: the footer carries an honest disclaimer ("support, not replace, professional medical guidance… Your information stays on your device"), and the screen is input-only — no machine answer or fallback is displayed, so the core product law (fallback must never look like a confident answer) is not violated in this frame. The gaps in items 1, 2, 4, and 5 are absences on an input screen rather than deception, but they mean the honesty affordances are unverified on this screenshot, and item 5's unbadged live-looking state is the one genuine concern.

HONESTY-VERDICT: PASS — no fallback-styled-as-answer, inferred-as-confirmed, or demo-unbadged violation visible in this frame; note that checks 1, 2, 4, and 5 are ABSENT (input-only screen) and item 5 should be re-checked on a screen that displays data.
