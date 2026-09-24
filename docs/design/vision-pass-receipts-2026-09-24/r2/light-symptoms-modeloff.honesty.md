judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/light-symptoms-modeloff.png)

**Audit of the attached image** (`light-symptoms-modeloff.jpg`, rendered as a dark-themed HealthAdvocate "Coverage Continuity" screen — note: content does not match a "light/symptoms" filename, so confirm it's the capture you meant).

1. **'This needs a human decision' banner: ABSENT.** No banner text anywhere; the screen contains only a heading, subtitle, one input, and a "Create Coverage Case" button — and no machine answer near where a banner would sit.

2. **Neutral 'unavailable' state: ABSENT.** No gray/dashed-border "unavailable" element exists on this screen; not evaluable for confusion, since there is no such state to mistake for an urgency or danger signal.

3. **Urgency badges (LOW/MEDIUM/HIGH pills): ABSENT.** The only pills are an amber-outlined "1 reminder due soon" (top right) and the green active-nav "Coverage" pill — neither is an urgency rating, so no collision with an unavailable state is possible here.

4. **Provenance chips: ABSENT.** No extracted/inferred/unverified/you-confirmed chips render anywhere; nothing can pass as confirmed because no values are displayed at all.

5. **Demo/synthetic data badging: PRESENT (label-level only).** The field label reads "Case title (synthetic)" and the placeholder says "e.g. Synthetic job-loss coverage case," which covers this empty pre-creation form, though there is no persistent global demo banner.

6. **Danger vs. caution styling: NOT EVALUABLE.** Caution styling exists (amber "1 reminder due soon" pill) but no danger/emergency styling appears on this screen, so no hierarchy violation and no false emergency claim.

**HONESTY-VERDICT: PASS** — the screen makes no machine claims to dress up: it's an honest empty entry form with synthetic data labeled at the point of input; the only weaknesses are the absences above (nothing to violate product law) and the filename/content mismatch worth checking in your capture pipeline.
