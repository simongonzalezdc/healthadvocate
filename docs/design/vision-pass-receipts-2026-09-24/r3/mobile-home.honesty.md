judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/mobile-home.png)

Audit of the attached mobile home screenshot (judged from the image only — no files read or written):

**(1) "This needs a human decision" banner — ABSENT.** No such banner anywhere on the screen; note this is a home/landing screen with no machine answers at all, so no fallback content exists to be outcompeted.

**(2) Neutral 'unavailable' state — ABSENT.** No gray/dashed/sentence-case unavailable card appears; consequently nothing here could be misread as an urgency rating or danger.

**(3) LOW/MEDIUM/HIGH urgency pills — ABSENT (as such).** The badges present are scheduling-status pills — DUE SOON (amber), UPCOMING (blue-gray), OVERDUE (red), DONE (gray) — and since no unavailable state exists, no confusion between the two is possible on this screen.

**(4) Provenance chips — PARTIAL.** Only one species appears, a "FROM THE CALL" chip on the Aetna MRI-denial card (with matching body text "detected in the Sep 24 call"); with a single species visible no inferred-value could pass as confirmed, but the extract/inferred/unverified/you-confirmed set can't be assessed here.

**(5) Demo/synthetic data badged — NO.** The "What's coming up" cards carry realistic, PHI-looking seeded content (Aetna MRI denial, Dr. Patel, metformin, $1,200 charge) with no DEMO/SAMPLE marker anywhere, while the stat cards directly below read 0 active tracks / 0 family members / 0 resolved — i.e., no real user data exists, so these entries read as synthetic yet are presented identically to real reminders.

**(6) Danger vs caution styling — WEAK-PASS.** OVERDUE (red pill) and DUE SOON (amber pill) are differentiated by hue only, at identical pill size, weight, and placement — danger is not *clearly* stronger than caution, though no emergency-level content exists on this screen to be misranked.

**HONESTY-VERDICT: FAIL** — Violation at check (5): the "What's coming up" reminder cards (mid/lower screen — "Appeal deadline — Aetna MRI denial", "Appointment with Dr. Patel", "Refill metformin", "Ask billing about the $1,200 charge") present synthetic/demo entries with no demo/synthetic badge, contradicted by the zeroed ACTIVE TRACKS / FAMILY MEMBERS / RESOLVED cards immediately below; a viewer could take the seeded data as real case history. Secondary weakness at (6): OVERDUE vs DUE SOON differ by hue only, not visual strength.
