judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/light-directory-live.png)

I can see the attached screenshot (HealthAdvocate "Directory" page, light theme) and judged it directly.

**Honesty audit — r3/light-directory-live.jpg**

1. **'This needs a human decision' banner: ABSENT.** No such banner anywhere in the frame; the only directive UI is the legend "Confirmed information always wins over inference" plus per-field "Confirm" links next to inferred values, which is proportionate since nothing in this view is escalated as unresolved.

2. **Neutral 'unavailable' state: ABSENT.** Every field on all four provider cards carries a real value and a provenance chip — there is no gray/dashed empty state to evaluate, and nothing in the frame could be mistaken for urgency or danger styling.

3. **Urgency badges (LOW/MEDIUM/HIGH pills): ABSENT.** No filled urgency pills exist in this screenshot; distinctness from an unavailable state is untestable in this frame (nothing to collide with).

4. **Provenance chips: PRESENT — species distinguishable; an inferred value could NOT pass as confirmed.** Confirmed is a filled teal pill with a checkmark ("YOU CONFIRMED ✓"), extraction chips are blue/lavender outline ("• FROM A CALL", "• BILL DECODE", "• VOICEMAIL", "• DOCUMENT", "• CALL"), and inference chips are amber with explicit "INFERRED" text ("• INFERRED · PATTERN", "• INFERRED · VOICEMAIL", "• INFERRED · LETTER") — differing hue, fill, icon, and label, reinforced by the legend.

5. **Demo/synthetic data badged: PRESENT.** A clear "DEMO DATA" badge (database icon, blue outline pill) sits at the top right of the Directory header.

6. **Danger vs. caution styling: ABSENT (nothing to compare).** There is no red/danger or emergency styling in this frame at all; the strongest caution signals are the amber inferred chips and the amber "+1 reminder due soon" pill, so no hierarchy violation is observable.

No fallback, unavailable, or urgency state appears in this view, and every machine-derived value is honestly labeled with its provenance — nothing presented here masquerades as more certain than it is.

**HONESTY-VERDICT: PASS**
