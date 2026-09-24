judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-directory.png)

I can see the attached image and will audit it directly.

**(1) 'This needs a human decision' banner** — ABSENT. No such banner anywhere on the screen; the only human-decision cues are per-field "Confirm" ghost buttons beside each unconfirmed value, so there is no banner to compare against machine answers.

**(2) Neutral 'unavailable' state** — ABSENT. Every field is populated (phone/address/hours/fax all have values with provenance chips); no gray/dashed "unavailable" element exists, so nothing here could be misread as an urgency rating or danger.

**(3) Urgency badges (LOW/MEDIUM/HIGH pills)** — ABSENT. No filled LOW/MEDIUM/HIGH pills; the only filled amber pill is "● REMINDER DUE SOON" in the top bar, which is a scheduling reminder, not an urgency rating.

**(4) Provenance chips distinguishable?** — YES, distinguishable; NO, inferred cannot easily pass as confirmed. Green "YOU CONFIRMED ✓", amber "INFERRED · PATTERN / VOICEMAIL / LETTER" (with the inferred value text itself amber), and neutral white source chips ("BILL DECODE", "DOCUMENT", "VOICEMAIL", "CALL"), differentiated by hue *and* literal text labels/✓ glyph — though all chips share the identical pill shape, so differentiation rests on color plus wording, a mild colorblind risk. The legend sentence ("confirmed information always wins over inference") reinforces the hierarchy.

**(5) Demo/synthetic data badged** — YES. A "DEMO DATA" badge sits at the top-right of the Directory panel; it is clearly labeled but low-contrast gray, easy to overlook on first glance.

**(6) Danger/emergency vs caution styling** — ABSENT (danger). No red/danger styling exists anywhere on this screen; caution styling is present (amber REMINDER DUE SOON pill, amber INFERRED chips), so the required danger>caution strength hierarchy cannot be demonstrated on this view — nothing violates it here, but the screen offers no evidence of it.

**Summary of product-law compliance:** the governing rule — a fallback must never look like a confident answer — is not violated: there are no fallback states, and every machine-inferred value is visibly demoted (amber, "INFERRED ·" label, adjacent "Confirm" action) rather than presented confidently. The absences in (1), (2), and (6) are contextual gaps on a fully-populated directory screen, not confident-looking fallbacks.

HONESTY-VERDICT: PASS — no violation found; noted gaps: no "needs a human decision" banner (human decision is delegated to per-field Confirm buttons), no unavailable state or danger styling exercisable on this screen, and the DEMO DATA badge is subtle.
