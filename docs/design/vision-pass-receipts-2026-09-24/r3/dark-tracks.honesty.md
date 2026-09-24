judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-tracks.png)

Auditing the attached screenshot (Health Tracks page, dark theme, empty state).

1. **'This needs a human decision' banner — ABSENT.** No such banner anywhere; the only callout-style elements are the header's amber "⚡ 1 reminder due soon" pill and the footer disclaimer. N/A-strength since no machine answer exists on this screen.

2. **Neutral 'unavailable' state — ABSENT** (an *empty state* is present instead: clock icon + gray "No health tracks yet. Start tracking a concern above." in sentence case, no dashed border). It could not be mistaken for urgency or danger — it's muted gray text with a neutral clock glyph, no red/amber accent.

3. **Urgency badges — ABSENT.** No LOW/MEDIUM/HIGH pills anywhere; nothing to contrast with the empty state.

4. **Provenance chips — ABSENT.** No extracted/inferred/unverified/you-confirmed chips render, so no risk of inferred passing as confirmed on this screen — but the species are untestable here.

5. **Demo/synthetic data badge — ABSENT.** No synthetic-data badge; no data content at all to badge, so no misrepresentation, though a demo build would want one once data appears.

6. **Danger/emergency styling — ABSENT.** The only alert-toned element is the amber "1 reminder due soon" header pill (caution level); no danger styling exists, so there is no hierarchy violation — nothing red competing with or understating amber.

HONESTY-VERDICT: PASS — no violation on this screen; the only fallback shown is a genuine, plainly-worded empty state, and the footer carries a correct "support, not replace" disclaimer. Flag for later screens: provenance chips and urgency badges were unverifiable here, so their honesty can't be certified by this image.
