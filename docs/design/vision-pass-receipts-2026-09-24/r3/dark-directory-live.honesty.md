judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-directory-live.png)

I can see the attached image (dark-theme Directory screen, live data) and will audit it directly without reading or writing anything.

**Honesty audit — `dark-directory-live.jpg` (Directory, live view)**

1. **'This needs a human decision' banner: ABSENT.** No banner exists anywhere; the nearest functional equivalent is the legend "Each field shows where it came from" plus per-field `Confirm` buttons next to every INFERRED value (email, pharmacy hours, appeals fax), so no machine answer stands unflagged.

2. **Neutral 'unavailable' state: ABSENT.** Every field on this screen is populated, so there is no gray/dashed state that could be misread as an urgency rating or danger — nothing to misjudge.

3. **Urgency badges (LOW/MEDIUM/HIGH pills): ABSENT.** No filled urgency pills appear; the only similar element is the small "Reminder due soon" chip in the top bar, which is a reminder, not an urgency grade, and it cannot collide with an unavailable state that doesn't exist here.

4. **Provenance chips: PRESENT, species distinguishable — an inferred value could NOT pass as confirmed.** Blue ★ chips (CALL / VOICEMAIL / DOCUMENT / BILL DECODE), amber ● chips (INFERRED · PATTERN / · VOICEMAIL / · LETTER), and green ✓ YOU CONFIRMED ✓ chips differ in color, icon, and wording, and the legend maps them explicitly. One caveat: the amber INFERRED pills are visually *louder* (filled/bright) than the quieter outlined green confirmed chips — identity is unambiguous, but salience is inverted relative to trust.

5. **Demo/synthetic badging: PRESENT.** A "DEMO DATA" pill sits beside the Directory header, reinforced by `.example` email domains and 555-prefix phone numbers; the badge itself is low-contrast but legible.

6. **Danger vs. caution styling: ABSENT / not assessable.** No emergency or danger styling appears on this screen to compare against caution styling, so no violation is possible here (amber is the strongest accent used, for inference and the reminder chip).

**HONESTY-VERDICT: PASS** — no violation found. Advisory (non-blocking): on the Dr. Maya Patel card (email row) and Riverside Imaging (hours row), the filled amber INFERRED chips out-shout the outlined YOU CONFIRMED chips, inverting the trust hierarchy; consider quieting inference styling so confirmation, not inference, is the most salient state.
