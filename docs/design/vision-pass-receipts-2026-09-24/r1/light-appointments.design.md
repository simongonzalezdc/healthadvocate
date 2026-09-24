judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-appointments.png)

Audit of `r1/light-appointments.jpg` — overall a clean, on-system screen: calm paper canvas, single card, one sage CTA, honest disclaimer. No P0s; a handful of P1 usability issues and P2 polish.

## What I see

**Layout, top-to-bottom:** (1) Cream app bar — sage rounded-square logo mark + "HealthAdvocate" wordmark left; right cluster: ochre-outlined pill "# 1 due soon", two hairline circular icon buttons (help "?", sun/theme). (2) Ten-item tab nav (Symptoms, Documents, Bills, Insurance, Drugs, Appointments, Discharge, 2nd Opinion, Recorder, Library); "Appointments" active as sage text on a pale sage pill. (3) One centered white workbench card (~640px, soft shadow, generous padding): calendar icon chip + "APPOINTMENT PREP" eyebrow + one-line description → uppercase label "YOUR SYMPTOMS OR REASON FOR VISIT" → tall textarea with placeholder → uppercase label "SPECIFIC CONCERN OR QUESTION (OPTIONAL)" → single-line input → sage "Prepare" button, left-aligned. (4) Hairline rule + centered two-line footer disclaimer, product name bolded.

**Palette:** warm paper cream canvas; white surfaces; sage accent confined to logo, active tab, CTA (one primary action ✓); ochre on the due-soon badge; warm-gray text tiers; coral/slate correctly unused.

**Type:** one sans family; ~10–11px letterspaced uppercase labels/eyebrow, ~13–14px body/placeholder, ~16px semibold wordmark. Modest scale, calm.

**Spacing/component quality:** consistent generous rhythm inside the card; airy margins; components clean and aligned (button left edge tracks the fields, right header cluster is even).

## Defects

- **P1 — Field affordance nearly invisible.** Textarea and input hairline borders (card center) all but disappear against the white card, and both placeholders are light gray on white — borderline contrast. For a sick/low-vision audience the input boundaries don't read. Darken borders one step; check placeholder ≥4.5:1 intent.
- **P1 — No appointment context.** The badge says "1 due soon" but the prep card names no appointment — no date, doctor, or clinic. The user can't confirm what they're prepping for; the two elements don't connect. Surface the due appointment in the card header.
- **P1 — Weak active-tab signal + flat nav.** Active "Appointments" pill is low-chroma sage on cream, near-identical weight to 9 siblings at ~12px. Scanning cost is high for overwhelmed users. Strengthen the active state (heavier weight or underline) and consider grouping/overflow for 10 tabs.
- **P2 — Badge copy.** "# 1 due soon" (top-right pill): stray space after "#", and the "#" reads as a ranking ("#1 due soon"). Use "1 due soon" or "1 appointment due soon".
- **P2 — Native textarea resize grip.** Default browser grip visible at the textarea's bottom-right corner, sitting on the rounded corner. Unstyled raw control breaks the workbench component quality; disable resize or restyle.
- **P2 — Label size.** Eyebrow and field labels at ~10px uppercase with wide tracking are at the legibility floor for this audience. Bump to 11–12px or reduce tracking.
- **P2 — Ochre badge competes with the CTA.** The only saturated element besides the CTA sits top-right, pulling the eye away from "Prepare". Acceptable semantic use of caution, but consider muting until relevant.
- **P2 — Dead band under the card.** ~80–100px of empty paper between card bottom and footer rule makes the view feel unfinished at this viewport; either more content or tighter vertical balance.

No broken, misaligned, or dishonest elements found — nothing at P0.
