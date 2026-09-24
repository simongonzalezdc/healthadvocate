judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-appointments.png)

I can see the attached screenshot clearly. It shows the Appointments tab's "Appointment Prep" screen: an empty two-field form with a green "Prepare" button, a "1 due soon" count pill in the header, and a support-not-replace disclaimer in the footer.

1. **'Human decision' banner — ABSENT.** No banner appears anywhere; acceptable here because the screen contains no machine-generated answer that would need one (only empty input placeholders).
2. **Neutral 'unavailable' state — ABSENT.** No gray/dashed unavailable element exists on this screen, so nothing can be mistaken for an urgency rating or danger.
3. **Urgency badges — ABSENT.** No LOW/MEDIUM/HIGH pills are shown; the only pill is the header's neutral amber "1 due soon" count, which doesn't impersonate an urgency rating.
4. **Provenance chips — ABSENT.** No extracted/inferred/unverified/you-confirmed chips appear, so no inferred value can pass as confirmed.
5. **Demo/synthetic data badge — ABSENT, and correctly so.** The screen holds only empty form fields with placeholder text, so there is no synthetic data presented that could masquerade as real records.
6. **Danger vs. caution styling — N/A/ABSENT.** Neither danger nor caution styling appears; the footer disclaimer is plain gray and appropriately subordinated to the form.

HONESTY-VERDICT: PASS — no violations; the screen presents no machine answers, fallbacks, or data claims that could overstate confidence, and its only decorative emphasis (the "1 due soon" header pill) is a factual count, not a simulated judgment.
