judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-home.png)

Auditing the attached dark-home screenshot only (no files touched).

1. **ABSENT.** No "This needs a human decision" banner appears anywhere; there is also no machine answer on this screen for a banner to outrank — the strongest visual weight sits on the green "Start a symptom check" CTA.

2. **ABSENT.** No gray/dashed/sentence-case "unavailable" state is rendered, so there is nothing here that could be misread as an urgency rating or a danger signal.

3. **ABSENT (as LOW/MEDIUM/HIGH filled pills).** The only status badges are schedule states — DUE SOON (amber outline), UPCOMING (gray outline), OVERDUE (red outline), DEMO (dim outline) — all hollow pills, so no filled urgency pill competes with or mimics an unavailable state.

4. **ABSENT.** No extracted/inferred/unverified/you-confirmed chips; the closest element is a "FROM THE CALL" source pill on the Aetna MRI denial row, which states origin rather than claiming confirmation — no value on screen can pass as "confirmed."

5. **PRESENT, but faint.** The synthetic row "Ask billing about the $1,200 charge" carries a "DEMO" outline pill at the right edge and the entire row is dimmed to reduced opacity, so it is distinguishable — though the badge's low contrast on the dark theme is the weakest part of the design.

6. **NO.** Danger styling is not clearly stronger than caution: OVERDUE (red) and DUE SOON (amber) are identical-size outline pills differing only by hue, and no emergency treatment (filled red pill, banner, alert icon) exists to dominate the caution tier.

Context for the verdict: this is the home screen — no answer, fallback, or urgency rating is displayed, so the product law ("a fallback must never look like a confident answer") is not tripped; demo data is badged, provenance is stated honestly ("from the call," "detected in the call"), and a clear "support, not replace professional medical guidance" disclaimer sits in the footer. The two watch items — the faint DEMO badge and the hue-only urgency hierarchy — should be fixed before the answer/screens with real fallbacks ship, but neither is a violation on this screen.

HONESTY-VERDICT: PASS — no product-law violation found; watch items: faint "DEMO" badge (What's coming up, 4th row, right edge) and OVERDUE vs DUE SOON differentiated by hue only.
