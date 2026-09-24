judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/mobile-recorder.png)

Judging only the attached screenshot (Call Recorder page, demo mode).

1. **'This needs a human decision' banner: ABSENT.** No such banner exists; the closest analog is the consent checkbox "Everyone on this call knows it is being recorded…" plus "HealthAdvocate cannot advise you on the law" — but the comparison is moot because no machine answer appears anywhere on this screen.

2. **Neutral 'unavailable' state: ABSENT.** There is no gray/dashed-border "unavailable" element; the only dashed-border item is the "DEMO MODE" badge, which is a mode label, not a data state, so nothing risks being read as an urgency rating or danger.

3. **Urgency badges: ABSENT.** No LOW/MEDIUM/HIGH pills appear anywhere; with no unavailable state either, there is no collision risk on this screen.

4. **Provenance chips: ABSENT.** No extracted/inferred/unverified/you-confirmed chips are shown, so the species can't be distinguished here — but no value can pass as confirmed because no values are displayed at all.

5. **Demo/synthetic data badged: YES, prominently and redundantly.** Dashed-border "DEMO MODE" badge at the card's top right, "Start demo recording" button, section header "YOUR RECORDINGS (DEMO)", and "Start over with the synthetic call script" — a user cannot mistake this for a live recording session.

6. **Danger vs caution styling: YES, correctly ordered.** The only danger element is the filled red "Delete" pill, which is visibly stronger than the muted beige "Before you record" caution card; no emergency styling exists to compare, and nothing inverts the hierarchy.

Minor observation (non-blocking): the "Start demo recording" button renders as a fully filled green pill even though the consent checkbox is unchecked — worth verifying it's actually gated in code, since the static styling doesn't advertise the gate.

HONESTY-VERDICT: PASS — no fallback or machine answer is present to masquerade as confident, demo/synthetic status is unmistakably badged, and the absent elements (Q1–Q4) are inapplicable to this recorder screen rather than missing where required.
