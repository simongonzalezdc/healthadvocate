judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/dark-directory-live.png)

Viewed the screenshot (dark-mode "Coverage Continuity" screen under the Coverage nav item). Audit of exactly this image:

**Honesty audit — `dark-directory-live.jpg` (rendered from the attached JPEG)**

1. **ABSENT** — No "This needs a human decision" banner anywhere on the screen; the only prominent elements are the "Coverage Continuity" heading, an input, and a green "Create Coverage Case" button, none of which carry a human-decision callout (not applicable here, as no machine answer is displayed either).
2. **ABSENT** — No neutral unavailable state (gray box, dashed border, sentence-case "unavailable" text) appears; the only bordered element is the empty "Case title" input, which reads as a form field, not an answer, so there is nothing that could be mistaken for an urgency rating or danger.
3. **ABSENT** — No LOW/MEDIUM/HIGH filled urgency pills exist; the sole pill is the amber "⚡ 1 reminder due soon" chip in the header, which is a reminder notice, not an urgency rating.
4. **ABSENT** — No provenance chips (extracted / inferred / unverified / you-confirmed) are shown; with no chips present, no inferred value can pass as confirmed.
5. **PARTIAL** — Synthetic labeling is present but weak: "Case title (synthetic)" and the placeholder "e.g. Synthetic job-loss coverage case" disclose it, yet only as small muted gray body text, not a distinctive badge — acceptable here because the form is empty and no demo data values are displayed, but it would be insufficient if actual synthetic case content were shown.
6. **N/A (no violation)** — There is no danger/emergency styling on the screen at all, only caution-level amber (the reminder chip); with nothing styled as an emergency, no hierarchy conflict exists.

**Overall**: This is an empty case-creation form with no machine answers, fallbacks, ratings, or provenance claims, so product law ("a fallback must never look like a confident answer") is not violated — the main honesty gap is that the synthetic disclosure would need badge-strength styling once real demo content populates the screen.

HONESTY-VERDICT: PASS
