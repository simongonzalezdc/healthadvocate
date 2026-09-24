judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/dark-coverage.png)

Auditing the attached dark-mode "Coverage Continuity" screenshot only.

1. **'This needs a human decision' banner — ABSENT.** No such banner anywhere; the only prominent elements are the "Coverage Continuity" heading, an input, and a green "Create Coverage Case" button, and no machine answer appears that would require the banner.

2. **Neutral 'unavailable' state — ABSENT.** There is no gray/dashed sentence-case unavailable state on screen, so there is nothing that could be mistaken for an urgency rating or danger signal.

3. **Urgency badges (LOW/MEDIUM/HIGH pills) — ABSENT.** No filled urgency pills exist; the only pill-like items are the "# 1 due soon" nav chip (small amber outline) and the "Coverage" nav tab, neither an urgency rating.

4. **Provenance chips — ABSENT.** No extracted/inferred/unverified/you-confirmed chips are visible; since no values carry provenance at all, an inferred value cannot pass as confirmed — but nothing is provenance-labeled either.

5. **Demo/synthetic data badging — PRESENT.** The input is labeled "Case title (synthetic)" with placeholder "e.g. Synthetic job-loss coverage case," though the badge is low-emphasis small gray text rather than a distinct chip.

6. **Danger vs. caution styling — ABSENT (not exercised).** No danger/emergency styling appears on this screen; the strongest accents are the green CTA and the amber "due soon" chip, so no hierarchy violation is observable.

HONESTY-VERDICT: PASS — no violation found. This screen is a synthetic-data entry form with no machine answers, fallbacks, urgency ratings, or provenance-bearing values, so the product-law rule ("a fallback must never look like a confident answer") is not violated; minor note only: the "synthetic" badge at the input is subtle and could be made a distinct chip.
