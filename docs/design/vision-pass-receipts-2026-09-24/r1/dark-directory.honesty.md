judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/dark-directory.png)

I can see the attached image (HealthAdvocate Directory screen, dark mode). Audit follows, judging only this screenshot.

1. **'This needs a human decision' banner: ABSENT.** No such banner anywhere on the screen; the only human-decision affordances are per-field "Confirm" buttons and the legend line "YOU CONFIRMED ✓ — confirmed information always wins over inference," so no banner exists to be stronger or weaker than the machine answers.

2. **Neutral 'unavailable' state: ABSENT.** Every field row shows a filled value with a provenance chip (e.g., Dr. Patel's email, Riverside's hours); no gray/dashed "unavailable" placeholder appears, so there is nothing that could be mistaken for an urgency rating or danger — not applicable on this screen.

3. **Urgency badges (LOW/MEDIUM/HIGH pills): ABSENT.** No urgency pills appear; the only pill inventory is provenance chips (★ FROM A CALL, ★ INFERRED ★ PATTERN, YOU CONFIRMED, etc.), so distinctness from an unavailable state cannot be evaluated.

4. **Provenance chips: PRESENT, species distinguishable; an inferred value should NOT pass as confirmed.** Inferred values carry an explicit orange "★ INFERRED" chip plus source ("★ PATTERN" on Patel's email, "★ VOICEMAIL" on Riverside's hours, "★ LETTER" on Aetna's fax), visually contrasted with teal "YOU CONFIRMED ✓" chips; caveat: the value text itself (e.g., "schneider@pa.example") is rendered at full strength identical to confirmed values, so the chip is the only discriminator at a glance.

5. **Demo/synthetic data badged: YES.** A "DEMO DATA" pill sits at the top right of the Directory panel header, and the data itself is synthetic (".example" email domain, 800-855-xxxx numbers).

6. **Danger/emergency styling: ABSENT (nothing to compare).** No danger/emergency element appears on this screen; the strongest caution-level styling is the orange INFERRED chips (plus the small red "1 due soon" header pill), so the required danger > caution hierarchy cannot be demonstrated here — no violation since no emergency content is shown.

HONESTY-VERDICT: PASS — no dishonest presentation found: all inferred fallbacks are explicitly labeled "★ INFERRED" and never masquerade as confirmed, and demo data is badged. Non-blocking observations: the "This needs a human decision" banner is absent despite three inferred values on screen (relying on per-field Confirm buttons), and if a danger state is ever rendered it must clearly out-rank the orange INFERRED styling seen here.
