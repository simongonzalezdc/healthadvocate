judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/light-directory.png)

I can see the image — here is the audit of `light-directory.jpg` (Directory screen, Dr. Maya Patel / Riverside Imaging / Aetna / Corner Pharmacy cards).

1. **"This needs a human decision" banner: ABSENT.** No banner exists; the only human-decision affordances are per-field "Confirm" links next to inferred values, which is consistent since every field already carries a provenance chip (N/A on banner strength).

2. **Neutral 'unavailable' state: ABSENT.** Every field on the page has a value, so no gray/dashed "unavailable" state appears and nothing could be mistaken for an urgency or danger signal.

3. **Urgency badges (LOW/MEDIUM/HIGH pills): ABSENT.** No urgency pills exist on this screen; nothing to compare against an unavailable state (the only pill-like elements are filter chips and provenance chips, which don't read as urgency).

4. **Provenance chips: PRESENT and species distinguishable.** Three visibly distinct species — teal with checkmark for "YOU CONFIRMED ✓", blue-gray for extracted sources ("FROM A CALL", "BILL DECODE", "VOICEMAIL", "DOCUMENT"), and peach for "INFERRED · PATTERN/VOICEMAIL/LETTER" — and the inferred chips cannot pass as confirmed because they lack the checkmark, carry the explicit "INFERRED ·" label, and use a different hue (e.g., Dr. Patel's inferred email, Aetna's inferred fax).

5. **Demo/synthetic data badged: PRESENT.** A dashed-border "DEMO DATA" badge sits at the top-right of the Directory card, clearly visible, and all phone numbers use the 555 convention.

6. **Danger vs. caution styling: ABSENT (nothing to compare).** There is no danger/emergency styling anywhere on this screen; the strongest alert tone is the mild peach "1 reminder due soon" pill, which is appropriately low-key for a directory page and doesn't impersonate emergency severity.

**HONESTY-VERDICT: PASS** — no violations found; all displayed values carry distinguishable provenance labels, demo data is badged, and the absent elements (banner, unavailable state, urgency badges, danger styling) are absent because this screen contains no such content, not because honesty cues were omitted or disguised.
