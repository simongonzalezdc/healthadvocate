judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-recorder-summary.png)

I can see the attached screenshot (dark-mode HealthAdvocate "Call Recorder" summary) — auditing it directly, no files touched.

**(1) 'This needs a human decision' banner — PRESENT, and yes, visually stronger.** It's a salmon-tinted, red-bordered filled card with a bold lead line ("This needs a human decision.") plus instruction text; the machine answers near it (deadline rows, "MODEL-INFERRED" suggestions) are plain text with small outline chips, so the banner dominates.

**(2) Neutral 'unavailable' state — PRESENT; not mistakable for urgency or danger.** The deadline row renders "no date" in dim gray sentence-case text with a gray "• UNVERIFIED" chip, clearly de-emphasized; no dashed border is discernible at this resolution, but the treatment is unmistakably neutral (gray/dim), not red or filled, so it can't be read as an urgency level or a danger.

**(3) Urgency badges (LOW/MEDIUM/HIGH filled pills) — ABSENT.** No LOW/MEDIUM/HIGH pills appear anywhere on the screen; the only filled pills are the red "Delete" buttons and the pink "1 reminder due soon" notice, neither an urgency badge — distinctness from the gray unavailable state is therefore moot but trivially satisfied.

**(4) Provenance chips — PRESENT and species distinguishable; inferred cannot pass as confirmed.** Blue-outline "• FROM TRANSCRIPT" (extracted), gray "• UNVERIFIED", and amber-outline "• MODEL-INFERRED" are textually explicit and color-separated; the inferred values carry a labeled amber chip rather than the blue confirmed-extracted treatment, so no inferred value reads as confirmed ("you-confirmed" chip itself doesn't appear, which is acceptable since nothing on screen is user-verified).

**(5) Demo/synthetic data badged — PRESENT, clearly.** "DEMO MODE" pill at top right, section header "1. YOUR RECORDINGS (DEMO)", row labeled "Aetna — appeal call (demo recording)", plus "Start over with the synthetic call script." / "Replay the demo call" controls.

**(6) Danger styling stronger than caution — YES.** Danger uses filled/tinted treatments (the salmon human-decision panel, solid red Delete pills, pink reminder pill), while caution ("MODEL-INFERRED") is only a thin amber outline chip — a clear hierarchy.

**HONESTY-VERDICT: PASS** — the product law holds: the one fallback on screen ("no date" / UNVERIFIED) is rendered as an explicitly uncertain gray state and immediately escalates to the human-decision banner instead of faking confidence. Minor nit only: the unavailable state lacks the ideal dashed border (still clearly neutral).
