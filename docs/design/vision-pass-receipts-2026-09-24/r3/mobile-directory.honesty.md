judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/mobile-directory.png)

Judging only the attached Directory screenshot (mobile, r3).

1. **"This needs a human decision" banner: ABSENT.** No such banner anywhere on the screen; the closest analog is per-field "Confirm" buttons on inferred fields, which are low-key and attached to the labeled inferred chips rather than competing with a confident answer.

2. **Neutral 'unavailable' state: ABSENT.** Every field shows a value (phone, address, email, hours) with a provenance chip, so there is no gray/dashed "unavailable" state that could be misread as urgency or danger.

3. **Urgency badges: ABSENT.** No LOW/MEDIUM/HIGH pills exist; the only pills are provenance chips, the dashed "DEMO DATA" badge, and a header notification dot showing "1" — none rating urgency.

4. **Provenance chips: PRESENT, species distinguishable — an inferred value could NOT pass as confirmed.** Confirmed fields use filled teal "YOU CONFIRMED ✓" pills, inferred fields use amber dashed outlines explicitly labeled "INFERRED · PATTERN / VOICEMAIL / LETTER", and machine-source decodes use blue outlines ("BILL DECODE", "VOICEMAIL", "DOCUMENT", "CALL"); e.g. Dr. Patel's inferred email sits visibly apart from her confirmed phone. (Minor nit: the legend renders "YOU CONFIRMED" as an outline chip while cards render it filled — same color and ✓, low confusion risk.)

5. **Demo/synthetic data badged: PRESENT.** A dashed "DEMO DATA" pill sits at the top-right of the Directory intro card, and the data itself is unmistakably synthetic (555 numbers, `.example` domain), backed by a footer disclaimer.

6. **Danger vs caution styling: ABSENT (danger styling) — no violation visible.** There is no red/emergency styling on this frame at all; the strongest alert tone is the amber dashed INFERRED chips, so caution is the ceiling here, but the danger>caution hierarchy simply cannot be verified from this screen.

**HONESTY-VERDICT: PASS** — no honesty violation found in this frame; note that the human-decision banner, unavailable state, urgency badges, and danger styling are all absent (nothing in-frame masquerades as a confident answer, so nothing violates the fallback law), and the danger-vs-caution comparison is untestable on this screen.
