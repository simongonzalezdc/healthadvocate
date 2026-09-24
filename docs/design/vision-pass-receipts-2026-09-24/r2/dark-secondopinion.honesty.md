judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/dark-secondopinion.png)

The image rendered (via its byte-identical copy — the attachment path `.../r2/dark-secondopinion.jpg` was broken because `r2` is itself the JPEG file; MD5-verified identical). One note: although the filename says "secondopinion," the screenshot actually shows the **Coverage Continuity** screen in dark mode (nav "Coverage" active), containing a title, a subtitle, a "Case title (synthetic)" input with green "Create Coverage Case" button, and a footer disclaimer. Judging that visible content:

**Honesty audit — Coverage Continuity (dark), 620×436**

1. **ABSENT** — No "This needs a human decision" banner; no machine answer appears anywhere on the screen (it's an empty-state creation form), so there is nothing the banner would be subordinate to.
2. **ABSENT** — No unavailable/fallback state (no gray box, dashed border, or "unavailable" text); nothing present that could be misread as urgency or danger.
3. **ABSENT** — No LOW/MEDIUM/HIGH urgency pills; the only pill is the amber "⏰ 1 reminder due soon" notification in the header, which is clearly a reminder count, not an urgency rating.
4. **ABSENT** — No provenance chips (no extracted/inferred/unverified/you-confirmed tokens); the only labeling is "Case title (synthetic)" above the input, and no inferred value could pass as confirmed because no values are shown.
5. **PRESENT** — Synthetic data is clearly badged at the point of entry: the field label reads "Case title (synthetic)" and the placeholder reads "e.g. Synthetic job-loss coverage case," both in quiet sentence case.
6. **NOT VERIFIABLE / no violation** — There is no danger or emergency styling on this screen to compare; the sole caution-toned element (amber reminder pill) is visually modest and does not masquerade as a danger or as an answer.

This screen contains no machine answers, fallbacks, urgency badges, or provenance-bearing values — so the "fallback must never look like a confident answer" law is not tested here, and nothing on-screen misrepresents machine output as human-grade advice. The one honesty-relevant element (synthetic data) is labeled correctly.

**HONESTY-VERDICT: PASS**
