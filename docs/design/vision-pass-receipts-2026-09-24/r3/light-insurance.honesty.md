judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/light-insurance.png)

Audit of the attached screenshot (Insurance tab → "Denial Fighter" form, empty state):

1. **ABSENT (NO)** — No "This needs a human decision" banner anywhere; the only advisory text is the small gray footer disclaimer ("support, not replace, professional medical guidance"), and no machine answer is displayed on this screen for a banner to compete with.

2. **ABSENT** — No unavailable state (no gray/dashed sentence-case element exists on screen), so there is nothing that could be mistaken for an urgency rating or danger.

3. **ABSENT** — No LOW/MEDIUM/HIGH filled pills; the only filled pill is the amber "⏰ 1 reminder due soon" chip in the top-right, which is a calendar reminder, not an urgency badge, and it's visually isolated from all form content.

4. **ABSENT** — No provenance chips (extracted / inferred / unverified / you-confirmed) appear; the screen contains only input labels and placeholder text, so no inferred value could pass as confirmed.

5. **ABSENT** — No demo/synthetic-data badge, but also no data at all: both fields are empty with placeholder copy ("Paste the denial letter or explanation of benefits…"), so nothing fabricated is being presented as real.

6. **NOT APPLICABLE / ABSENT** — No danger/emergency styling exists on this screen to compare against caution styling; the amber reminder pill is the sole warm-toned element and clearly reads as a benign reminder, not an emergency signal.

Observation (non-violation): the card's promise copy ("we'll analyze it, identify the reason, and draft an appeal letter") is feature marketing, not a rendered answer, so the fallback rule is not triggered here.

**HONESTY-VERDICT: PASS** — no violations; this is an empty input form with no machine answers, fallbacks, urgency badges, provenance chips, or synthetic data, and the honesty-relevant states are simply not applicable to what's shown.
