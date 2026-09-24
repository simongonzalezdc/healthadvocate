judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-bills.png)

I can see the image. Audit follows.

## DESCRIPTION

**Layout, top-to-bottom:**
1. Header bar (white): sage logo tile w/ heart + bold "HealthAdvocate" wordmark left; right cluster = coral-outlined pill badge "# 1 due soon", two ghost circle icon buttons (account, sun/theme toggle).
2. Nav bar (white): 10 text tabs — Symptoms, Documents, Bills, Insurance, Drugs, Appointments, Discharge, 2nd Opinion, Recorder, Library. "Bills" active in a sage pill.
3. Body (warm paper): one large white card, centered, ~77% viewport width. Card contains: ochre-tinted icon tile + "BILL DECODER" tracked-caps eyebrow, 2-line slate helper sentence; "PASTE YOUR BILL TEXT" caps field label; tall textarea w/ placeholder and native resize grip; sage "Analyze Bill" pill button, left-aligned.
4. Footer: full-width hairline, centered small slate disclaimer, "HealthAdvocate" bolded inline.

**Palette:** paper/ecru body; white card surfaces w/ warm-gray hairlines; sage = logo, active pill, primary button; coral = badge only; ochre = decoder icon tile; slate = nav/help/placeholder text; near-black ink for wordmark. System mapping reads correctly at a glance — except the badge (see defects).

**Type scale:** flat and small — wordmark ~15px semibold, everything else 10–13px. Eyebrow caps are the largest "heading" on the page. No display size exists in this view.

**Spacing rhythm:** genuinely calm — generous card padding, consistent ~16/24px group gaps, single soft shadow, consistent radii (8px fields, full-round pills/buttons). Double-bezel reads: card → inset field.

**Component quality:** buttons, pills, and fields are cleanly built; one primary action per view is respected; nothing looks broken.

## DEFECTS

- **P1 — No page heading / flat hierarchy.** Card top: "BILL DECODER" is an 11px eyebrow doing H1 duty. The entire view sits in one 10–13px type range; sick, overwhelmed users get no anchor. Add a real heading (~20–24px) above or promote the eyebrow.
- **P1 — Broken-looking badge copy.** Header right: "# 1 due soon" — the literal `#` reads as an unresolved icon glyph or ticket ID; "1" of what? Reword ("1 bill due soon") or fix the icon ligature.
- **P1 — Coral (danger) misused for a caution-level message.** Same badge: "due soon" is a heads-up, not a crisis; coral inflates urgency at the exact anxious users this tool serves. System says ochre=caution — recolor to ochre.
- **P1 — Active nav pill contrast risk.** "Bills" pill appears to be white text on mid sage-green; at ~13px that's likely below WCAG AA (~3:1). Verify or darken the sage/ink the label.
- **P2 — Native textarea resize grip** (field, bottom-right corner): raw browser chrome breaks the calm double-bezel finish. Disable resize or restyle.
- **P2 — Ochre icon tile next to BILL DECODER:** decorative use of the caution hue makes the tool's intro read as a warning chip. Use sage or neutral.
- **P2 — No field meta.** Beside "PASTE YOUR BILL TEXT": no format hint, size limit, or "runs on your device" reassurance near the point of input — privacy claim lives only in the footer. Small slate line under the label would help.
- **P2 — Empty right half of card** on wide viewports: single-column content in a full-width card leaves dead space right of the helper text/eyebrow block; cap the card ~640–720px or add a supporting rail.

**No P0s** — nothing is illegible, overlapping, or misaligned. The two semantic-color issues (badge hue, `#` glyph) are the closest thing to dishonest UI and are the first things I'd fix.
