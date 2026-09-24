judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/light-discharge.png)

I viewed the screenshot (620×436, dark-theme "Coverage Continuity" screen). Audit follows.

**Honesty audit — `r2/light-discharge.jpg` (Coverage Continuity screen)**

1. **'This needs a human decision' banner: ABSENT.** No such banner anywhere; the only advisory text is the bottom disclaimer ("HealthAdvocate is here to support, not replace, professional medical guidance…"), and there is no machine answer on screen for it to outrank.
2. **Neutral 'unavailable' state: ABSENT.** The only bordered control is a standard solid-gray rounded input ("e.g. Synthetic job-loss coverage case") — no gray/dashed "unavailable" element exists, so nothing can be mistaken for urgency or danger.
3. **Urgency badges: ABSENT.** No filled LOW/MEDIUM/HIGH pills; the single pill is an amber-outlined "+1 reminder due soon" (top right), which is a reminder, not an urgency rating.
4. **Provenance chips: ABSENT.** No extracted/inferred/unverified/you-confirmed chips appear; no data values are rendered at all, so an inferred value cannot pass as confirmed because none are shown.
5. **Demo/synthetic data badged: YES.** The form label reads "Case title (synthetic)" and the placeholder says "e.g. Synthetic job-loss coverage case" — labeled in two places, though only in small gray sentence-case text.
6. **Danger vs. caution styling: ABSENT (danger side).** There is no danger/emergency styling on screen at all (no red anywhere); the only caution-tone element is the amber reminder pill, so the required dominance can't be judged — nothing unsafe is being under-signaled.

**Overall:** This screen renders no machine answers, no fallbacks, no urgency or provenance-bearing values — so the missing banner/badges/chips are appropriate absences, not concealment. The honesty-bearing elements that do apply (synthetic-data label, "not replace professional medical guidance" disclaimer, "local and private" claim) are present and honest. Nothing looks like a confident answer that isn't one.

**HONESTY-VERDICT: PASS** — no violation; note for future screens: when machine answers do appear here, items 1–4 and 6 become mandatory, and the synthetic badge (item 5) could be made more prominent than a small gray label.
