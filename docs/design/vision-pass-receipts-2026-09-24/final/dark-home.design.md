judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/final/dark-home.png)

The image loaded fine — full audit below.

## DESCRIPTION

**Layout, top-to-bottom.** Dark header band: sage shield logo + "HealthAdvocate" left; ochre pill "1 reminder due soon" + two circular icon buttons right. Below it, a 16-item nav wrapped over two rows (Symptoms … Recorder / Library … Help). Hero: sage micro-badge "FREE · OPEN SOURCE · PRIVATE BY DESIGN", two-line display heading "You deserve to understand your care.", three-line muted sub, sage-filled "Describe your symptoms" + outlined "Fight a denial". Card cluster: one featured card (sage top rail, icon chip, "Start a symptom check" CTA, footer chips "Private by design / No account needed") plus two stacked quiet cards ("I have a document to understand", "I need help with costs"). "What's coming up" section: heading + DEMO DATA pill, two-line dim explainer, four timeline rows each with big date numeral (26/30/20/24 SEP), title + inline meta, action chips, right-aligned status pill (DUE SOON ochre, UPCOMING slate, OVERDUE coral, DONE gray), colored left rails per status. Then three stat cards (ACTIVE TRACKS / FAMILY MEMBERS / RESOLVED, each a big sage "0" over a caption) and a centered two-line footer disclaimer.

**Palette.** Page and cards are cool neutral graphite (near-black page, ~#1a–1c raised cards). Accent semantics are on-system: sage = primary CTAs, badge text, zeros, featured rail; ochre = caution (DUE SOON, header pill); slate = info (UPCOMING, DEMO DATA); coral = danger (OVERDUE, overdue date numeral). The neutrals are off-system — this is not warm paper; it's a blue-cast dark theme.

**Type.** Display ~44–48 light; section headings ~16–17 semibold; card titles ~15 semibold; body 13–14; micro 10–11 used everywhere (nav, chips, meta, captions, badge). Coherent hierarchy, compressed at the bottom.

**Spacing/components.** Generous, calm, consistent rhythm; left margin aligns from logo through hero to cards. Buttons/chips/cards share disciplined pill/rounded radii. All panels are single-surface — no double bezel anywhere.

## DEFECTS

**P0**
- Stat-card captions (three cards, bottom row) are illegible — ~10px gray at roughly 2.5–3:1 on charcoal; even allowing for JPEG softness, unreadable at true size.

**P1**
- Two sage-filled primaries in one view: hero "Describe your symptoms" and featured-card "Start a symptom check" (both lead to the same journey). Violates one-primary-per-view — keep the hero CTA, quiet the card button.
- Timeline order is 26 → 30 → 20 → 24 SEP: the coral OVERDUE metformin refill — the most urgent item on the page — sits third, and the DONE (24 SEP) row mixes into active items with no divider. Sort overdue-first/by-date or split "Upcoming / History."
- Contrast band on micro-text: nav links, DEMO-DATA explainer, inline row meta, and the footer disclaimer all sit ≈3–4:1 on near-black. The footer is a medical safety disclaimer — it must clear 4.5:1.
- Nav is 16 undifferentiated ~11px links over two wrapped rows, no grouping, no active state — a wall of jargon for sick, overwhelmed users. Group into journeys or demote to a menu.
- Palette deviation: surfaces are cool graphite, not warm paper neutrals. If dark mode is a sanctioned variant, warm-shift the grays; the accent roles themselves hold.

**P2**
- Featured card has a dead zone: large empty gap between "Start a symptom check" and the "Private by design / No account needed" chips (card stretched to match the right column). Anchor the chips to the card foot or cap height.
- Three big sage zeros read as a data bug, and green gives no-information numbers primary weight. Quiet the numerals and add empty-state framing.
- Header pill says "1 reminder due soon" while the list shows one due-soon AND one overdue — the badge undercounts urgency.
- Double-bezel workbench treatment is absent from every panel — confirm home is exempt from that system rule.
- Micro-type inflation: nav, chips, meta, captions, and badge all sit at 10–11px; consolidate to one micro style with adequate contrast.
- The DEMO-DATA explainer ("local notifications fire only while the app is open…") reads as release notes on the home page — move to an info popover.
- Top-right icon buttons: faint gray glyphs, small hit targets.

**Net:** accent semantics and spacing discipline are genuinely good; the page fails on the neutrals (cool vs. warm paper), micro-text contrast, urgency ordering in the timeline, and a duplicated primary CTA.
