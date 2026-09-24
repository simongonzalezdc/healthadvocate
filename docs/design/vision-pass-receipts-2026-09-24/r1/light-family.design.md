judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-family.png)

I can see the image. Audit follows.

## Description (top → bottom)

1. **Header bar** — white surface, hairline bottom edge. Left: sage-green rounded-square logo (white heart glyph) + "HealthAdvocate" wordmark in dark warm gray. Right cluster: coral outlined pill badge reading "# 1 due soon", a gear icon button, a sun (theme) icon button in a circled bezel.
2. **Nav bar** — same white surface, 11 small gray text items: Bills, Insurance, Drugs, Appointments, Discharge, 2nd Opinion, Recorder, Library, Directory, Scanner, and an active item rendered as "Fami" in a pale sage pill.
3. **Page canvas** — warm paper cream. One centered white card (~80% width, rounded corners, hairline border, soft shadow) containing: an icon chip + letterspaced caps micro-label "FAMILY HEALTH TRACKER" with a one-line description; a form row of text input ("Family member name" placeholder), a native select ("Self"), and a sage-green "Add Member" button; below, a centered empty state (small circled glyph + gray caption "No family members added yet. Add someone above.").
4. **Footer** — full-width hairline, then two lines of centered small-print disclaimer in mid-gray.

**Palette as named hues:** warm paper canvas, white surfaces, sage green (logo, primary button, active nav), coral (status badge), slate/gray text, warm hairlines. No ochre present.
**Type scale:** flat and small — one letterspaced caps micro-label, everything else 12–14px-equivalent gray sans; no visible H1 or section heading.
**Spacing rhythm:** generous card padding, consistent ~12px form-row gaps, large calm (arguably too empty) page field.
**Component quality:** buttons, pill badge, and input are clean; the select betrays native browser chrome; panel reads single-bezel.

## Defects

- **P0 — Nav, far right:** active tab label truncated to "**Fami**" (mid-word clip, presumably "Family"). Broken, visible text in the highest-attention nav slot.
- **P1 — Nav bar overall:** 11 items crammed at this width with no overflow strategy — the truncation above is the symptom. Horizontal nav needs scroll, overflow menu, or responsive collapse.
- **P1 — Header right badge:** "**# 1** due soon" has a stray space ("# 1") and is semantically opaque; worse, it's rendered in **coral = danger** for a non-danger status. Per system this is ochre/caution at most. It's also the only coral on the page, giving a false alarm accent that competes with the single primary action.
- **P1 — Typography scale:** the page has no real heading — the card title is a 10px caps micro-label, so the view reads as all-caption. Hierarchy is carried entirely by the nav pill.
- **P2 — Form row, select:** native OS dropdown chevron/chrome on "Self" — breaks from the styled input beside it; restyle or custom control.
- **P2 — Card panel:** single border + shadow; doesn't express the committed **double-bezel workbench** panel language.
- **P2 — Card bottom → divider:** ~2× card-padding of dead paper between card, divider, and footer; vertical balance is top-heavy for a single-card view.
- **P2 — Empty-state glyph:** circled icon is ambiguous at size (reads as "(!)") — an alert glyph for an empty state signals error; use a people/family glyph with clearer weight.
- **P2 — Header right cluster:** badge, gear, and sun buttons sit tight against the viewport edge with uneven gaps between the three elements vs. the logo's left margin.
