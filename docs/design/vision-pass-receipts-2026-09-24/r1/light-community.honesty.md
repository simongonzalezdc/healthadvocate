judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-community.png)

I can see the attached image (HealthAdvocate "Community Health Scanner" input screen). Audit below, judging only what's visible.

1. **ABSENT** — No "This needs a human decision" banner anywhere; this is a pre-scan input screen with no machine answer present to compare against.
2. **ABSENT** — The only "empty" element is a plain white textarea with a gray sentence-case placeholder ("Paste a news article, CDC alert, FDA recall, or health advisory…"); it reads as an input prompt, not an unavailable state, and could not be mistaken for an urgency rating or danger.
3. **ABSENT** — No LOW/MEDIUM/HIGH filled pills in the scanner area; the only filled pill on screen is an unrelated amber "#1 due soon" reminder in the global header, so no distinction to evaluate.
4. **ABSENT** — No provenance chips (extracted / inferred / unverified / you-confirmed) of any species; an inferred value cannot pass as confirmed here only because no values are shown at all.
5. **ABSENT** — No demo/synthetic badge, but also no data whatsoever is displayed (empty form), so nothing synthetic is shown unlabeled — the check is vacuous rather than satisfied.
6. **ABSENT** — No danger/emergency styling appears anywhere on screen; the strongest styling is the caution-level amber "#1 due soon" pill, so no danger-vs-caution hierarchy violation is visible, but danger styling also cannot be verified from this screen.

**HONESTY-VERDICT: PASS** — No violation visible: this is an empty pre-scan input state with no machine answers, fallbacks, urgency ratings, or data claims, so nothing masquerades as a confident answer. Caveat: all honesty-critical result-state elements (human-decision banner, unavailable state, urgency badges, provenance chips, demo badge) could not be assessed because no scan output appears in this screenshot; this verdict covers only what is shown.
