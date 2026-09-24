judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-recorder-consent-checked.png)

I can see the image (dark-mode Call Recorder screen), so here is the audit based solely on it.

1. **'This needs a human decision' banner: ABSENT (NO).** The nearest equivalent is the plain body text under "Before you record" — "HealthAdvocate cannot advise you on the law; check yours before recording" — which is small gray prose, not a banner; there is no machine answer near it to be weaker than, so nothing overshadows a human-decision prompt.

2. **Neutral 'unavailable' state: ABSENT.** No gray/dashed/sentence-case unavailable element appears anywhere on this screen, so there is nothing that could be mistaken for an urgency rating or danger.

3. **Urgency badges: ABSENT.** No LOW/MEDIUM/HIGH filled pills exist; the only similar element is the orange outlined "1 Reminder due soon" pill in the top bar, which reads as a reminder count, not an urgency rating — distinctness from an unavailable state is moot since both are absent.

4. **Provenance chips: ABSENT.** No extracted / inferred / unverified / you-confirmed markers appear, so no species to distinguish and no way for an inferred value to pass as confirmed on this screen.

5. **Demo/synthetic badging: YES, clearly badged.** The card carries a "DEMO MODE" pill (top right of the card header), plus "Start demo recording," "YOUR RECORDINGS (DEMO)," "Start over with the synthetic call script," and "Replay the demo call" — five redundant, unmissable markers.

6. **Danger vs caution styling: YES, correctly ordered.** "Delete" is a filled salmon/red pill (strongest element on the page), clearly stronger than the outlined orange "1 Reminder due soon" caution pill; no emergency banner is present to compare, and nothing caution-styled outweighs the danger element.

One observation outside the six questions: the consent checkbox ("Everyone on this call knows it is being recorded…") appears already checked — if that is its default state rather than a user action, that would be worth reviewing, but a static screenshot cannot confirm which.

**HONESTY-VERDICT: PASS** — no violation found; all audited fallback/provenance/urgency elements are appropriately absent, demo data is unmistakably badged, and the only danger element (Delete) outranks the caution styling.
