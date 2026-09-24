judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/dark-symptoms-emergency.png)

Judged from the attached image only (`dark-symptoms-emergency.jpg`, viewed directly; no other files read or written).

**(1) "This needs a human decision" banner — PRESENT, and YES, visually stronger.** Red-filled panel with bold red heading directly under the "Assess Symptoms" CTA, dwarfing the muted gray EXPLANATION / POSSIBLE CONDITIONS machine output below it.

**(2) Neutral 'unavailable' state — ABSENT, and YES it can be mistaken for danger.** There is no gray/dashed sentence-case "unavailable" component; the unavailability notice ("Handoff/decode mode not available on this tier") is set in emergency-red inside the danger banner, conflating system failure with clinical danger.

**(3) Urgency badges — PRESENT, but not adequately distinct.** A filled red "● HIGH" pill appears under URGENCY LEVEL, but it uses the exact same emergency red as the unavailable/fallback banner above it, so fallback-state and urgency share one visual language.

**(4) Provenance chips — ABSENT, and YES an inferred value could pass as confirmed.** No extracted / inferred / unverified / you-confirmed markers appear anywhere; values like "chest pain (0%)" and "Name overlap · low" render bare, with "(0%)" even ambiguous between "0% likely" and "0% confidence."

**(5) Demo/synthetic data badged — ABSENT.** No DEMO/SYNTHETIC/SAMPLE badge exists despite clearly synthetic content ("Schedule a laptop-only media capture…", "skipped validation errors", conditions at 0%).

**(6) Danger vs caution styling — YES.** The full-width red panel, red HIGH pill, and red "Urgency disagreement" bar clearly outweigh the only caution element, the small amber "★ 1 due soon" pill in the header.

**HONESTY-VERDICT: FAIL**
- **Primary violation:** fallback urgency rendered as a confident answer — the "● HIGH" pill (URGENCY LEVEL section) is a deterministic fallback ("upgraded to HIGH for safety", per the bottom alert) yet is styled identically to a real machine assessment, with no on-pill fallback/unverified marking; this breaks the product law that a fallback must never look like a confident answer.
- Unavailability notice danger-styled in red inside the "This needs a human decision" banner — no neutral unavailable state exists (banner, mid-screen).
- Provenance species entirely missing; bare "(0%)" condition values are ambiguous and presentation-ready to be misread (POSSIBLE CONDITIONS section).
- Synthetic content carries no demo/synthetic badge (whole screen, incl. ACTION ITEMS filler).

Credit where due: the human-decision banner itself, the disclosure captions ("not a check of clinical accuracy"), and the crisis hotlines are genuinely honest elements — the failure is in the fallback urgency styling and the missing neutral/provenance/badge layers around it.
