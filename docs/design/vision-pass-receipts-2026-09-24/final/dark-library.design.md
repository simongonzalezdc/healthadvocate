judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/final/dark-library.png)

DESCRIPTION

**Layout, top-to-bottom:** Fixed top bar (logo + wordmark left; ochre "1 reminder due soon" pill and two icon-only circles right). Below it, two stacked tab rows: row 1 = Symptoms, Documents, Bills, Insurance, Drugs, Appointments, Discharge, 2nd Opinion, Recorder; row 2 = Library (active, sage outline pill), Directory, Scanner, Family, Tracks, Coverage, Help. Centered workbench panel: "Library" title + sage glyph, two-line gray subtitle, ghost "BRING DATA" pill at right. Then inset search field, filter chips (All active in sage; Calls / Appointments / Voicemails / Reminders), a one-line machine-derived disclaimer, and four list cards (title + avatar left, date right; body line; chip row; card 1 also has a "Bills" / "Delete" action row). Footer divider + centered three-line safety disclaimer.

**Palette:** Background near-black warm espresso; cards one step lighter, warm gray. Text: warm off-white headings, mid-gray body, dimmer gray meta. Sage green = logo, active tab, active chip, panel glyph, card-2 avatar. Ochre = reminder pill, "$1,200.00", "Sep 30" (filled), "appeal window", "30-day appeal window" (outlined), "COMPUTED FROM THE LETTER" badge. Coral = card-1 avatar glyph, "denial" chip, "Delete". Slate/info: absent entirely.

**Typography:** Sans throughout; scale is flat — "Library" ~18–20px bold, then almost everything else clusters at 10–13px (titles ~12px bold, body ~11px, chips/meta ~9–10px). Uppercase micro-labels ("BRING DATA", "COMPUTED FROM THE LETTER") at ~8–9px.

**Spacing rhythm:** Panel and card padding generous and consistent; card gaps even. Top zone (two tab rows) is cramped — rows nearly touching — versus the calm panel below.

**Component quality:** Radii consistent (pill chips, ~10px cards, inset search). Honesty patterns are genuinely present ("COMPUTED FROM THE LETTER" badge, per-card "Recorded with consent", stored-locally claims). No clipping, rotation, or overlap anywhere.

DEFECTS

**P0 — none.** Nothing broken, illegible, misaligned, or dishonest per se. Closest call below.

1. **P1 — Legend/UI mismatch (honesty system broken):** disclaimer under filter chips says items are "marked VERIFIED or UNVERIFIED," but no such markers exist; the actual marker is an unexplained asterisk on chips ("* Insurance", "* Appointments", "* Documents"). Users can't decode asterisk → app-inferred. Critical for this audience.
2. **P1 — Primary action fails the system:** "BRING DATA" (panel header right) is the only view-level action but is a dim ghost micro-pill, not sage, lowest-emphasis element in the panel — while five sage items (logo, Library tab, All chip, panel glyph, DR avatar) are all non-action. Accent semantics inverted.
3. **P1 — Chips read as buttons:** card 1 carries 5 outlined chips + 2 buttons (7 pill elements); chips share the exact radius/border/treatment of "BRING DATA" and nav tabs. Metadata looks tappable; for overwhelmed users this is a mis-click factory.
4. **P1 — Unlabeled money:** card 1 chip "$1,200.00" in ochre with no label (cost? disputed amount? bill?). A bare figure on a denial call is dangerous ambiguity.
5. **P1 — Contrast under spec:** dates ("Sep 24 · 11:02"), card subtitles, and especially the two disclaimers ("Machine-derived items…", footer) render dim-gray-on-dark at roughly 3:1 or below, at 9–11px. The safety legend is the least legible line on the page.
6. **P1 — Destructive action undifferentiated:** card 1 "Delete" (coral text) sits in the same ghost-button style, same row rhythm, directly beneath chips as benign "Bills"; no separation or weight step.
7. **P1 — Nav overload / two-row tabs:** 13 tabs in two stacked rows with no visual relationship between rows; core action "Recorder" is the last text item of row 1. Hierarchy of the product's information architecture is unreadable at a glance.
8. **P1 — Deadline de-emphasized:** card 4 — the loud ochre "COMPUTED FROM THE LETTER" badge dominates the title row while the actual date "Oct 8" is small, dim, and far right. The consequential fact is the quietest element on the most consequential card.
9. **P2 — Ochre encoding inconsistent:** "Sep 30" is filled ochre, "appeal window" / "30-day appeal window" outlined ochre — same deadline family, two fills, no stated meaning.
10. **P2 — Card anatomy inconsistent:** only card 1 has an action row (Bills/Delete); cards 2–4 end at chips. Reads as a missing state, not a deliberate pattern.
11. **P2 — Coral misuse:** card 1 avatar glyph is coral for a routine payer call; coral should be reserved for danger semantics, not speaker identity.
12. **P2 — Slate missing:** the committed slate=info role appears nowhere; informational items (results ready, asterisk chips) default to neutral gray. Palette is 4 of 5 roles.
13. **P2 — Type scale too flat:** no step between panel title (~18px) and 11px body; the whole list lives in a 10–13px band — dense for sick, stressed readers.
14. **P2 — Icon-only header controls:** top bar right — two unlabeled circular icons (account?, leave/export?); meaning is guesswork.
15. **P2 — Identity drift:** near-black ground abandons "warm paper" warmth (hue is warm, but the material feel is gone); sage reads as bright emerald on dark rather than muted sage. If dark mode is sanctioned it needs its own warm-neutral ramp and a desaturated sage variant.
