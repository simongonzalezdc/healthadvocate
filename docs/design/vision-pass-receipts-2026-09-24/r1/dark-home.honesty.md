judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/dark-home.png)

I can see the attached image (dark-mode HealthAdvocate home/landing screen), so the audit proceeds. Judging only what is visible in it:

1. **'This needs a human decision' banner: ABSENT.** No such banner anywhere on the screen, and no machine-generated answer appears either — the closest thing is static hero copy ("we'll help you understand what might be happening"), which makes no confident claim.

2. **Neutral 'unavailable' state: ABSENT.** There is no gray/dashed/sentence-case unavailable element; nothing on screen could be misread as an urgency or danger signal because the only colored element is the amber "1 due soon" header chip, which reads as scheduling, not a fallback.

3. **Urgency badges (LOW/MEDIUM/HIGH pills): ABSENT.** No filled urgency pills exist; the amber "1 due soon" chip is a due-date indicator, and since no unavailable state exists either, there is no confusability between the two.

4. **Provenance chips (extracted / inferred / unverified / you-confirmed): ABSENT.** No provenance labeling of any kind is shown, but no data values are shown either, so no inferred value could pass as confirmed.

5. **Demo/synthetic data badge: ABSENT (and no synthetic data present).** The screen contains only static navigation and three feature cards with generic copy — no sample records, bills, or triage output — so nothing unlabeled synthetic is being displayed.

6. **Danger/emergency styling vs caution styling: ABSENT (no danger styling exists).** There are no red/emergency elements at all; the strongest accent is the amber caution-level "1 due soon" chip, so there is no danger styling that could be under-powered relative to caution.

**HONESTY-VERDICT: PASS** — no violation. This is a data-free landing/home surface: no machine answers, fallbacks, urgency ratings, provenance labels, or synthetic data appear, so nothing impersonates a confident answer. Note the pass is narrow: the screen's only honesty signal is the footer disclaimer ("support, not replace, professional medical guidance"), so the audited mechanisms simply aren't exercised here and would need to be checked on a results/document screen where they actually render.
