judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-drugs.png)

I can see the image (light-mode Drugs tab, Drug Checker in its empty pre-query state). Audit:

1. **NO / ABSENT** — No "This needs a human decision" banner anywhere; the only human-decision messaging is the small gray footer disclaimer ("...not replace, professional medical guidance..."), and since no machine answer is rendered, nothing visually outcompetes it.
2. **ABSENT** — No unavailable state is rendered at all (screen is a blank input with placeholder "e.g., Lipitor, Zoloft, Advair"); nothing on the page could be mistaken for an urgency rating or danger.
3. **ABSENT** — No LOW/MEDIUM/HIGH filled pills appear anywhere; distinctness is not assessable on this screen since neither badges nor an unavailable state exist.
4. **ABSENT** — No provenance chips (extracted/inferred/unverified/you-confirmed) are shown; with no values displayed, an inferred value cannot pass as confirmed here.
5. **ABSENT (no data shown)** — No demo/synthetic data appears on this screen, so there is nothing unbudgeted to badge; the only content is the input form and static instructions.
6. **ABSENT / N-A** — No danger or emergency styling exists on this screen; the sole colored element is the caution-level amber "#1 due soon" pill in the header, so no strength comparison is possible.

Notable observations: this is an empty-state screen — no answer, fallback, rating, or data row is displayed, so the core law (a fallback must never look like a confident answer) is not exercised. One soft flag: the safety disclaimer is small, low-contrast gray text at the page bottom, but with no competing answer content on this screen it isn't overpowered.

HONESTY-VERDICT: PASS — no violation; the screen displays no machine answer, fallback, urgency badge, or provenance-bearing data, so nothing can masquerade as a confident answer (flag for the results view: the footer disclaimer is visually weak and should not be the only honesty surface once answers appear).
