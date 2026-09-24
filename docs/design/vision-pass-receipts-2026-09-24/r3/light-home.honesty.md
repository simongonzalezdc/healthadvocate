judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/light-home.png)

I can see the attached image (HealthAdvocate home/landing screen). Audit below, based only on that screenshot.

1. **ABSENT** — No "This needs a human decision" banner anywhere on the screen; acceptable here since no machine answer or fallback is displayed (only navigation and reminder cards), so nothing human-decision-shaped is being overshadowed.

2. **ABSENT** — No gray/dashed-border/sentence-case "unavailable" state appears (the three zeroed stat cards at the bottom are empty-state counters, not unavailable states); no confusion risk, since no such state exists to be misread as urgency or danger.

3. **ABSENT (as specified)** — No LOW/MEDIUM/HIGH filled pills exist; the pills present are reminder statuses — DUE SOON (amber), UPCOMING (blue), OVERDUE (red), DONE (gray, struck-through row) — and there is no unavailable state on this screen for them to be confused with.

4. **NO (incomplete)** — Only one provenance chip is visible ("FROM THE CALL" on the Aetna MRI denial row); the extracted / inferred / unverified / you-confirmed species are not all present, so distinguishability can't be verified — no inferred value is shown passing as confirmed on this screen, but the set is untestable here.

5. **NO** — The "What's coming up" list is realistic seeded data (Aetna MRI denial, Dr. Patel follow-up, metformin refill, $1,200 billing charge) with no DEMO/SAMPLE badge; the only trace is a faint struck-through fragment reading "demo text biased requested" on the DONE row, which looks like leaked placeholder copy rather than a badge.

6. **YES** — OVERDUE renders as a filled red pill, clearly stronger than the amber/tan DUE SOON pill; no emergency-grade styling is required on this screen.

**HONESTY-VERDICT: FAIL** — Violation at the "What's coming up" reminder list (mid/lower page): synthetic demo content (named insurer, doctor, medication, dollar amount, call dates) is presented with no clear demo/synthetic badge, so a first-run user could mistake seeded reminders for their real medical record; secondary issue: leaked placeholder text "demo text biased requested" visible on the DONE row (same list, fourth entry).
