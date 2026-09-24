judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/light-bills.png)

I can see the image. Auditing it as rendered.

## What I see

**Layout, top to bottom:** White masthead — sage rounded-square heart logo + "HealthAdvocate" wordmark left; ochre filled chip "⏰ 1 reminder due soon" plus two outlined circular icon buttons (bell, sun) right. Below, a single-row tab nav: Symptoms, Documents, **Bills** (active — sage-outlined pill, tinted fill), Insurance, Drugs, Appointments, Discharge, 2nd Opinion, Recorder, Library, then a clipped chevron at the far right edge. Main area: one large centered double-bezel white panel on warm paper, containing a "$" icon in an outlined circle, bold "Bill Decoder" title, two-line description, letterspaced caps label "PASTE YOUR BILL TEXT", a tall cream textarea with placeholder, and a sage "Analyze Bill" pill button. Hairline rule, then centered two-line disclaimer footer.

**Palette:** Warm paper page ground, white panels, sage-green on logo / active tab / primary button, ochre reminder chip, slate-gray body text, hairline warm-gray borders. Coral unused (correct — no danger state present).

**Type & spacing:** Sans throughout; scale is flat — title only ~1.25× body, nav/label/body near-identical. Spacing is genuinely calm: generous panel padding, big air between panel and footer. Component quality is consistent (uniform radii, one button style); the reminder chip is the most saturated object on the page.

## Defects

1. **P0 — Clipped nav control.** Far-right chevron after "Library" (~x 528, y 44) is cut in half by the header edge — a broken, half-rendered affordance. Fix overflow or hide it cleanly.
2. **P1 — Reminder chip outshouts the primary action.** The filled ochre "1 reminder due soon" (masthead right) is the highest-salience element on a view whose one primary action is the sage "Analyze Bill." Demote the chip (outline/tint, no fill) or relocate it.
3. **P1 — Flat, undersized type scale.** "Bill Decoder" (~x 150, y 113) barely clears body size; nav, caps label, and description all sit in the same ~10–11px band. Weak hierarchy is a real cost for overwhelmed, possibly unwell users. Establish 3 clear steps: title ≫ body ≫ label.
4. **P2 — Two left edges in the panel.** Title + description align to ~x 150 (indented past the "$" icon); label, textarea, and button align to ~x 122. Pick one content edge for the panel.
5. **P2 — Inverted emphasis in the field.** The caps label "PASTE YOUR BILL TEXT" (y ~163) is fainter and smaller than the placeholder inside the field it names; the label should be the stronger of the pair.
6. **P2 — Placeholder contrast.** "Paste your medical bill or explanation of benefits…" is very low-contrast warm-gray on cream — borderline at a glance; lift one step.
7. **P2 — Widow.** Description's second line is the lone word "upcoding." (y ~139) — rewrap or tighten the line.
8. **P2 — Nav density.** Ten equal-weight tabs with no grouping is a lot of scanning for this audience; group related tabs or add a break before lower-frequency items.

Overall: composition, palette discipline, and one-primary-action intent are largely intact; the clipped chevron and the ochre chip stealing focus are the two things I'd fix before shipping.
