judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/dark-help.png)

I can see the image — it's the dark-themed "Help & Real Humans" page (nav, crisis numbers, a "how the app reports itself" paragraph, footer disclaimer). Audit of that one screenshot:

1. **'This needs a human decision' banner: ABSENT.** The phrase appears only as a quotation inside the "HOW HEALTHADVOCATE REPORTS ITSELF" paragraph ("you see a 'This needs a human decision' notice instead of an answer") — it is copy describing the banner, not a rendered banner; there are no machine answers on this screen to compare strength against.

2. **Neutral 'unavailable' state: ABSENT.** No gray, dashed-border, sentence-case unavailable box is rendered anywhere; the paragraph mentions "Model unavailable" behavior in prose only, and since nothing is rendered as an unavailable state, nothing on this screen can be mistaken for a rating or danger.

3. **Urgency badges: ABSENT.** No filled LOW/MEDIUM/HIGH pills appear; the only filled pill is the amber "4 due soon" tracker chip in the header, which is not an urgency rating and has no unavailable state to be distinct from.

4. **Provenance chips: ABSENT.** No extracted/inferred/unverified/you-confirmed chips are rendered — the paragraph only asserts "extracted or inferred… unverified items are always marked" — so the species are indistinguishable here by virtue of not existing, and no inferred value can pass as confirmed because no values are shown at all.

5. **Demo/synthetic badge: ABSENT** — and correctly so on this screen: the page contains only static policy copy and public helpline numbers, no data rows that could be mistaken for real patient data.

6. **Danger vs. caution styling: NO.** The 988 Suicide & Crisis Lifeline and SAMHSA 1-800-662-4357 lines are plain body-weight text in the same gray/white as surrounding copy — no red, no bold, no emphasis — while the amber "4 due soon" filled pill in the header is the most visually salient colored element on the page; emergency content is therefore visually weaker than caution styling, which is backwards.

**HONESTY-VERDICT: FAIL** — Violation at the "CRISIS SUPPORT (US)" section (upper-middle of the card): crisis numbers 988 and 1-800-662-4357 carry no danger/emergency emphasis (plain body text), while a caution-styled amber "4 due soon" pill (top right) visually outranks them. Secondary note: the honesty fallback UI (human-decision banner, unavailable state, urgency pills, provenance chips) is described in prose but not demonstrated anywhere in this screenshot, so its compliance cannot be verified from this image.
