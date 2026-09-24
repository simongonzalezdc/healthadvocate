judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/dark-library.png)

I can see the attached screenshot (dark-mode Library screen, four cards, footer disclaimer). Audit below, judging only this image.

1. **'This needs a human decision' banner: ABSENT.** No such banner anywhere; the closest machine-output surface is the "Appeal window closes (detected)" card, which carries no human-decision prompt.

2. **Neutral 'unavailable' state: ABSENT.** No unavailable state appears on this screen, so there is nothing that could be mistaken for an urgency rating or danger — no violation here.

3. **Urgency badges (LOW/MEDIUM/HIGH pills): ABSENT.** The red chips ("denial — not medically necessary", "30-day appeal window") are content tags, not urgency pills, so distinctness from an unavailable state cannot be evaluated on this screen.

4. **Provenance chips: ABSENT — and the one inferred value is under-marked.** No extracted/inferred/unverified/you-confirmed chips exist; the only provenance cue is the small "(detected)" parenthetical in the card title, while "Oct 8" sits in the same right-aligned, muted slot and style as the factual recording timestamps ("Sep 24 · 11:02", etc.) — on a skim, the inferred deadline can pass as confirmed fact.

5. **Demo/synthetic data badged: PRESENT — YES.** "DEMO DATA" appears twice, as a filled orange pill in the top header and again in the Library section header; clearly visible.

6. **Danger vs caution styling: YES (adequate, comparison limited).** The red denial/appeal chips are clearly stronger than the surrounding neutral chips; there is no emergency banner or amber caution styling on this screen to compare against, and the orange DEMO badge is a label rather than caution styling, so no violation.

HONESTY-VERDICT: FAIL — Violation: bottom card "Appeal window closes (detected)" (Library list, lower card, right side "Oct 8"). A machine-inferred, consequential legal deadline is presented with no provenance chip, only a low-salience "(detected)" parenthetical, a date styled identically to factual metadata, and no "This needs a human decision" banner. Secondary note (not a violation on this screen): the banner, unavailable state, urgency pills, and provenance chip system are all absent here, so those checks were untestable rather than passed.
