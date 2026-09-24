judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-library-after-call.png)

1. **'This needs a human decision' banner: ABSENT.** No such banner exists anywhere; the only high-emphasis dark element is a success toast ("Saved to the Library (demo — synthetic only)"), so nothing frames the machine-derived deadlines as needing human judgment.

2. **Neutral 'unavailable' state: ABSENT.** No gray/dashed sentence-case chip appears in any list row — the partially hidden card behind the toast is occlusion, not an unavailable state — so there is no risk of it reading as urgency or danger, but the state simply isn't shown.

3. **Urgency badges (LOW/MEDIUM/HIGH): ABSENT.** There are no labeled urgency pills; only unlabeled filled chips ("appeal — 30 days", "denial — not medically necessary", red) imply severity, and distinctness from an unavailable state is moot since none is present.

4. **Provenance chips: ABSENT — species not distinguishable; YES, inferred can pass as confirmed.** The only provenance hint is "(detected)" in item 5's title, yet the inferred deadlines ("30-day appeal window", "appeal — 30 days") are rendered as the loudest filled red pills, visually identical to extracted facts like "$1,200.00".

5. **Demo/synthetic data badged: YES.** "DEMO DATA" chip on the Library card header, "demo recording" in the first item title, "Recorded in demo mode. Synthetic transcript…" copy, and the "Saved to the Library (demo — synthetic only)" toast.

6. **Danger stronger than caution: NO.** Danger chips (red, items 1/2/5) and caution chips (amber "Sep 30" in item 3, amber "#1 due soon" in the header) are the same size and fill weight, differentiated only by hue — danger is not clearly stronger.

**HONESTY-VERDICT: FAIL** — Violation 1: inferred values styled as confident facts — the machine-detected deadlines "appeal — 30 days" (list item 1) and "30-day appeal window" (list item 5) carry the page's strongest red filled-pill styling with no provenance species marker, so an inferred value passes as confirmed. Violation 2: no "This needs a human decision" banner anywhere in the Library view despite machine-detected deadlines being the most prominent content. Minor: danger and caution styling are weight-equivalent (hue-only difference), items 1–5 vs item 3/header badge.
