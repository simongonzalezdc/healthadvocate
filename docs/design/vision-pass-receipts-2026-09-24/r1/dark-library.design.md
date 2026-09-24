judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/dark-library.png)

**IMAGE RECEIVED** — dark-variant Library view, 620px-wide capture. Audit follows.

## Description (what's actually there)

**Layout, top-to-bottom:** Fixed header (sage shield-cross logo + "HealthAdvocate" wordmark left; sage "+ 1 due soon" pill, bookmark and history icon buttons right) → single-row nav of 10 tabs (Symptoms…Recorder, "Library" active as sage pill) → one large rounded workbench panel containing: eyebrow "LIBRARY" + description + outlined "DEMO DATA" pill right-aligned → full-width search field → filter chip row ("All" active in sage, then Calls/Appointments/Voicemails/Reminders) → 4 stacked record cards, each with icon tile, bold title, right-aligned timestamp, 1–2 line description, wrapped chip rows; card 1 adds a footer meta row → centered muted disclaimer footer.

**Palette as named hues:** Surfaces are near-black charcoal with a faint olive cast (dark variant of warm paper, reading cool); card titles off-white; body text mid-gray. Sage appears on logo, active nav pill, "+ 1 due soon", active filter chip. Coral on denial icon/chips/"Denies"/deadline card. Ochre on money chip, provider/org chips, "Sep 30". Slate on "physical therapy", "screening results", "+ Entity" outline chips. Accents land in the right semantic lanes overall.

**Typography scale:** Letter-spaced caps eyebrow; semibold card titles; two muted body sizes; ~9–10px chip labels. Scale steps exist but body/chip sizes sit at the small end.

**Spacing rhythm:** Consistent card gaps (~12px) and generous panel padding; calm, nothing cramped inside the panel.

**Component quality:** Cards, chips, pills and search are cleanly drawn, uniform radius, no rendering artifacts.

## Defects

- **P0 — Card 1 body, line 2:** copy is broken/garbled — "Rep confirmed the appeal address and said a call is expected within the reference number." Reads clipped mid-thought, no ellipsis. Broken copy in a trust-critical advocacy tool is dishonest content.
- **P1 — Card 1 chip row vs Card 2 chip row:** same entity type, inconsistent color — "Dr. M. Patel" is neutral gray while "Dr. Maya Patel" is ochre. Entity coloring is arbitrary; users will read meaning that isn't there.
- **P1 — Card 1 footer row:** bare coral word "Denies" floating next to the "+ Bills" link with no chip/affordance — reads as a leaked status label, unclear if text or control.
- **P1 — View level:** no single primary action. Panel's most button-like control is the outlined slate "DEMO DATA" pill (top-right of panel), which competes with the sage "+ 1 due soon" header pill; "DEMO DATA" also has ambiguous affordance (badge vs button). Violates one-primary-action rule.
- **P1 — Card headers, timestamps:** date format inconsistent — "Sep 24 · 11:02" / "Sep 30 · 07:48" vs bare "Oct 8" (card 4). Also card 2 chip "Sep 30" duplicates its own header timestamp.
- **P2 — Whole surface:** dark surfaces read cool/neutral, not warm-paper; tint drift from the committed system (verify warm undertone on bg and panels).
- **P2 — Main panel + cards:** double-bezel workbench construction not visible — everything reads single-bezel; system fidelity gap.
- **P2 — Card 1 chip "denial - not medically necessary":** spaced hyphen vs the em dash used everywhere else; punctuation inconsistency.
- **P2 — Card 4 title:** "(detected)" leaks internal detection jargon into a patient-facing title.
- **P2 — Card descriptions/chip labels:** low-contrast gray on dark panel; chip text especially small — verify ≥4.5:1 and chip tap targets.
- **P2 — Nav row:** 10 tabs in one row; gaps around "Discharge / 2nd Opinion / Recorder" visibly tighter than the rest — density uneven.
- **P2 — Header right:** bookmark and history icon buttons unlabeled (a11y/affordance).
- **P2 — Card anatomy:** card 1 has an extra footer meta row the other three lack; card heights/anatomy don't share one pattern.
- **P2 — Search field:** placeholder ends "..." (three dots) rather than ellipsis character; minor but visible at this scale.

**Net:** structure and accent semantics are largely on-system; the P0 garbled sentence and the entity-color inconsistency are the two fixes I'd make before this ships.
