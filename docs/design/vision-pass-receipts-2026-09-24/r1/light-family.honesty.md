judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-family.png)

I can see the image (Family Health Tracker, empty state). Audit:

1. **"This needs a human decision" banner: ABSENT.** No such banner anywhere; the closest human-decision framing is the footer disclaimer "support, not replace, professional medical guidance" — and no machine answer exists on this screen for a banner to outrank.

2. **Neutral unavailable state: PRESENT (as an empty state).** "No family members added yet. Add someone above." is gray, sentence case, with a thin-outline circle icon; no dashed container border, but it is unmistakably neutral — not mistakable for an urgency rating or danger (no red/amber fill, no caps, no alert iconography).

3. **Urgency badges: ABSENT.** No LOW/MEDIUM/HIGH filled pills anywhere; the only pill is the small outlined amber "#1 due soon" reminder in the header, which is visually distinct from the gray empty state (comparison moot since badges are absent).

4. **Provenance chips: ABSENT.** No extracted/inferred/unverified/you-confirmed chips exist, so species distinguishability is N/A and no inferred value can pass as confirmed — there are no values at all on this screen.

5. **Demo/synthetic data badge: ABSENT.** No demo/synthetic badge is shown, but the screen contains zero data records (pure empty state), so nothing synthetic is being passed off as real.

6. **Danger vs. caution styling: ABSENT (no danger styling to compare).** The strongest alert styling on the page is the amber outlined "#1 due soon" header pill (caution-level); no red/emergency styling exists, so no misranking is possible on this screen.

**HONESTY-VERDICT: PASS** — no violation found; the only fallback-like element (the empty state, center card, ~y215–245) is rendered as neutral gray sentence-case text with no urgency, danger, or confidence styling that could masquerade as an answer.
