judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-bills.png)

I can see the image clearly — a dark-mode HealthAdvocate screen on the "Bills" tab showing the empty Bill Decoder input form (header, nav, textarea placeholder, "Analyze Bill" button, footer disclaimer). Audit below, judged on this screenshot only.

**Honesty audit — `r3/dark-bills.jpg`**

1. **'This needs a human decision' banner: ABSENT.** No such banner anywhere; the only human-decision messaging is the small footer line "support, not replace, professional medical guidance," and there is no machine answer on screen for it to outrank.

2. **Neutral 'unavailable' state: ABSENT.** No gray/dashed/sentence-case fallback state appears — the only box is the empty input textarea with placeholder text, which cannot be mistaken for an urgency rating or danger.

3. **Urgency badges: ABSENT.** No LOW/MEDIUM/HIGH filled pills exist anywhere on the screen; distinctness from an unavailable state is not assessable (no unavailable state either).

4. **Provenance chips: ABSENT.** No extracted/inferred/unverified/you-confirmed chips are visible, so species distinguishability is moot — there is no inferred value on screen that could pass as confirmed.

5. **Demo/synthetic data badge: ABSENT.** No demo/synthetic badge is shown, but no synthetic data is displayed either — the form is empty, so nothing unlabeled is being presented as real.

6. **Danger vs. caution styling: ABSENT (not comparable).** No danger/emergency styling exists on this screen; the only caution-toned element is the small amber "#1 reminder due soon" pill in the top-right header, which is mild and notification-like.

**Notes:** This is a pre-analysis input screen, so none of the honesty-critical components (banner, urgency badges, provenance chips, fallback states) are exercised — no honesty violation is visible, but this screenshot also cannot demonstrate that those affordances exist elsewhere in the product. The copy "we'll flag potential errors, duplicate charges, and upcoding" is a capability claim, not an answer, so it doesn't breach the fallback law.

HONESTY-VERDICT: PASS
