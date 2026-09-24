judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/mobile-home.png)

**Honesty audit — `mobile-home.jpg` (HealthAdvocate, mobile home/landing screen)**

1. **'This needs a human decision' banner: ABSENT** — the screen is a static home page (hero + three entry cards) with no machine answer, recommendation, or analysis anywhere, so there is nothing the banner could be outweighing; no fallback-vs-answer conflict exists on this screen.

2. **Neutral 'unavailable' state: ABSENT** — no gray, dashed-border, sentence-case unavailable element appears; consequently nothing on this screen could be mistaken for an urgency rating or a danger signal.

3. **Urgency badges (LOW/MEDIUM/HIGH pills): ABSENT** — the only badge is a small amber header pill reading "e1 · due soon" (a reminder count, not a filled urgency pill); no unavailable state exists on-screen to contrast it against.

4. **Provenance chips: ABSENT** — no extracted / inferred / unverified / you-confirmed chips are visible anywhere; the distinguishability question cannot be assessed on this screen.

5. **Demo/synthetic data badge: ABSENT** — there is no "demo" or "synthetic" marker, though the page also displays no data (only static marketing copy); the unexplained "e1 · due soon" pill implies a tracked item with no on-screen indication of whether it is real or demo data.

6. **Danger vs. caution styling: NEITHER PRESENT** — there is no red/danger styling and no caution styling beyond the single amber "due soon" pill, so no comparison is possible and no violation is visible.

Mitigating observation: the footer does carry an honest scope disclaimer ("…here to support, not replace, professional medical guidance. Always consult a qualified healthcare provider…").

**HONESTY-VERDICT: PASS** — no honesty violation is observable on this static home screen: no machine answers, no fallback states, and no data claims are shown, so product law ("a fallback must never look like a confident answer") is not exercised here. Caveat: this screen proves nothing about how the banner, unavailable states, urgency badges, or provenance chips behave on the results/documents screens; the ambiguous "e1 · due soon" pill (header, top right) is the one element worth labeling if the session is demo data.
