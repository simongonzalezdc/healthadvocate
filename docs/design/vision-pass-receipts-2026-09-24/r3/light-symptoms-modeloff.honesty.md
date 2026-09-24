judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/light-symptoms-modeloff.png)

I can see the attached screenshot (HealthAdvocate, Symptoms tab, light theme, model-off state showing an "Analyzing…" pill and gray skeleton bars). Audit below, judged only on what is visible.

1. **Human-decision banner: ABSENT** — no "This needs a human decision" banner anywhere; the only safety text is the low-emphasis gray footer disclaimer ("support, not replace, professional medical guidance"), which is visually the weakest element on the page.

2. **Neutral 'unavailable' state: ABSENT** — the model-off fallback renders as a filled sage "Analyzing…" button plus gray skeleton bars (no gray/dashed/unavailable wording); it cannot be mistaken for an urgency rating or danger, but it falsely reads as "still working," inviting an indefinite wait instead of an honest handoff.

3. **Urgency badges: ABSENT** — no LOW/MEDIUM/HIGH pills exist; the only filled pills are the tan "1 reminder due soon" (header) and the sage "Analyzing…" button, so distinctness from an unavailable state is untestable.

4. **Provenance chips: ABSENT** — no extracted/inferred/unverified/you-confirmed chips appear, so species distinguishability and the inferred-passes-as-confirmed risk are moot (no machine values are shown at all).

5. **Demo/synthetic badge: ABSENT** — the symptom text in the textarea appears as ordinary user input with no demo/synthetic label anywhere on the page.

6. **Danger vs. caution styling: ABSENT (danger)** — there is no danger/emergency styling to compare; the only caution-tier styling is the mild tan reminder pill, so "clearly stronger" cannot be satisfied, though nothing on screen makes an emergency claim.

**HONESTY-VERDICT: FAIL** — Violation at the Symptom Assessment card, mid-content area directly below the "Analyzing…" button: with the model off, the fallback is an indefinite "Analyzing…" skeleton with no neutral unavailable state (question 2) and no "This needs a human decision" banner (question 1), so the failure mode presents as ongoing machine work rather than an honest, visibly weaker fallback.
