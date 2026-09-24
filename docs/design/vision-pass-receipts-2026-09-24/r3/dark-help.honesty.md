judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-help.png)

Auditing the attached dark-mode "Help & Real Humans" screenshot only.

**Honesty audit — `/tmp/ha-ds-shots/judge-img/r3/dark-help.jpg`**

1. **ABSENT** (as a rendered banner) — "This needs a human decision" appears only as quoted copy inside the section-3 explanation paragraph; there is no banner component, and no machine answer near it to compare against.
2. **ABSENT** — no unavailable state is rendered anywhere; the "Model unavailable … it is not a rating" concept exists only as prose, so there is nothing on this page that could be misread as a rating or a danger.
3. **ABSENT** — no LOW/MEDIUM/HIGH pills exist; the only filled pill is the small salmon "1 reminder due soon" header nudge, which is a reminder badge, not an urgency rating.
4. **ABSENT** — no provenance chips are rendered; the three species are named in copy only ("quoted from the transcript, inferred by a model, or unverified"), so no inferred value can pass as confirmed because no values are shown at all.
5. **ABSENT** — no demo/synthetic data or badge is present; the resources shown are real published US hotlines (988, SAMHSA 1-800-662-4357, HealthCare.gov), so nothing needed badging.
6. **YES** — the crisis block is a bordered container with red-accented, bolded 988 and 1-800 numbers, clearly the strongest styling on the page and stronger than the small salmon reminder pill (the only caution-like element).

**Caveat:** this is a static transparency/help page with zero machine outputs, so the audit can only confirm no dishonest fallback is displayed here — it cannot verify that the banner, unavailable state, urgency badges, or provenance chips render honestly on results views. Those need auditing on a screenshot that actually shows a model result.

HONESTY-VERDICT: PASS
