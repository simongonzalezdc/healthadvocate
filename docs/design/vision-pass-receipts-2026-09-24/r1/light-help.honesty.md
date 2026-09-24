judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-help.png)

I can see the image — auditing it now. This is a HealthAdvocate "Help & real humans" page: a static help/resources card with crisis lines, coverage pointers, and a "How HealthAdvocate reports itself" prose section.

**Honesty audit — r1/light-help.jpg**

1. **ABSENT (as a rendered banner).** "This needs a human decision" appears only as a quotation inside the prose paragraph "HOW HEALTHADVOCATE REPORTS ITSELF," not as an actual banner; no machine answer is nearby to compete with.

2. **ABSENT.** No gray/dashed/sentence-case "unavailable" state is rendered anywhere — "model unavailable" exists only in prose — so nothing on screen could be mistaken for an urgency rating or a danger.

3. **ABSENT.** No LOW/MEDIUM/HIGH filled pills appear; the only pill is the amber "#1 due soon" chip in the header, which is a tracker status, not an urgency rating, and there is no unavailable state for it to be confused with.

4. **ABSENT.** No provenance chips (extracted / inferred / unverified / you-confirmed) are shown — "unverified" appears only in prose — so no inferred value could pass as confirmed because no values are displayed at all.

5. **ABSENT.** No demo/synthetic badge is present, and nothing on the page is identifiably synthetic data; the header "#1 due soon" pill carries no provenance marking either way.

6. **YES.** Crisis contacts are the hottest styling on the page — bold red names and numbers ("988 Suicide & Crisis Lifeline — call or text 988," "SAMHSA National Helpline — 1-800-662-4357") — clearly stronger than the muted gray section headers and the warm-but-not-alarming amber header pill.

**Context for the verdict:** this is a help page, not a results screen, so the absence of the banner, unavailable state, urgency badges, and provenance chips is expected — they're described in prose rather than rendered. Critically, nothing on this screen presents a fallback as a confident answer, and the page explicitly states software "is not a clinician."

**HONESTY-VERDICT: PASS** — no violation found; the only soft spot is that the honesty mechanisms exist here only as prose descriptions, with no visual example of the banner/state to verify they render stronger than machine answers (location: "HOW HEALTHADVOCATE REPORTS ITSELF" paragraph).
