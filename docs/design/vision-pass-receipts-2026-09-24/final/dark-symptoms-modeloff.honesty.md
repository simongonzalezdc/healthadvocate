judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/final/dark-symptoms-modeloff.png)

Audit of the attached screenshot (`dark-symptoms-modeloff.jpg`, dark mode, Symptom Assessment with the local model off):

1. **YES — banner present and dominant.** "This needs a human decision." renders as a filled salmon/red callout with bold crisis lines (988, SAMHSA) directly above the machine output; the nearest machine content (the gray "Model unavailable" pill and muted explanation text) is far weaker.

2. **PRESENT and clearly neutral.** Section 1 shows a gray, sentence-case pill reading "Model unavailable — no urgency assessment was made."; a dashed border isn't discernible at this resolution, but nothing about it (no red/amber, no filled urgency pill shape, explicit "no urgency assessment was made") could be mistaken for a rating or a danger.

3. **ABSENT (correct for this state), and distinct.** No LOW/MEDIUM/HIGH filled pills appear anywhere; the gray unavailable pill uses no urgency color, so it cannot be conflated with one.

4. **ABSENT — no extracted/inferred/unverified/you-confirmed chips in this view.** The nearest analogs are distinguishable: "headache (exact match, 94% string similarity)" vs "dizziness (fuzzy match, 86% string similarity)" in muted text, and no inferred value is offered at all, so nothing could pass as confirmed.

5. **ABSENT — no demo/synthetic badge.** No "demo"/"synthetic" badge is visible, but nothing on screen is labeled demo data — the input is a plain user-typed symptom string, so no badge is owed here.

6. **YES — danger clearly outranks caution.** The large salmon "human decision" block with red hotline text is far heavier than the only caution element (the small amber outline pill "1 reminder due soon" in the header).

Product law holds: the fallback says plainly that no urgency assessment was made, the name-match list is capped with "NOT A DIAGNOSIS," and the strongest visual weight sits on the human-decision banner, not on any machine answer.

**HONESTY-VERDICT: PASS**
