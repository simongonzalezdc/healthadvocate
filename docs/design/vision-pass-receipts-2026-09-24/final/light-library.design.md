judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/final/light-library.png)

**DESCRIBE**

**Layout, top to bottom:** Fixed-feel header bar: sage shield logo + "HealthAdvocate" wordmark left; coral warning pill "1 reminder due soon" + two ghost icon buttons right. Below, two flat nav rows: 9 dark text links (Symptoms…Recenter), then 7 lighter links with "Library" as a sage filled pill. Main content is one centered white workbench card (~80% width) on warm cream paper, containing: card header (small square doc-icon chip, "Library" title, two-line muted description; lavender "DROP DATA" pill top-right), full-width search field, filter chip row ("All" active), a small-print disclaimer line ("Machine-derived items…"), then 4 stacked record cards — each: left icon chip, bold title + right-aligned gray timestamp ("Sep 24 · 11:02"), one-to-two-line summary, and a wrap of outlined tag pills (reason, "$1,200.00", provider names, "appeal window", "→ Insurance/Bills/Appointments/Documents", one filled dark "Device" chip). Centered footer disclaimer. Double-bezel: outer card reads as a single hairline border with calm interior padding — bezel layering is present but subtle.

**Palette as named hues:** warm paper cream page + white surfaces; sage green = logo, "Library" pill, provider tags; coral = reminder pill, "appeal window" tag, "Sep 30" tag, dot on Riverside icon; ochre = "denial…" tag, "COMPUTED FROM THE LETTER" badge; slate = timestamps, "→" cross-link tags; ink text. Mapping is mostly faithful to the system.

**Type scale:** one sans family; ~4 steps: card title (bold lg) → body (sm) → tags/timestamps (xs, ~2 steps below body) → fine-print disclaimers. Scale is coherent but the bottom steps run very small.

**Spacing/components:** generous, even card padding and row rhythm; chips, pills, and cards share radius and border weight. Component quality is genuinely high.

**DEFECTS**

- **P1 — "DROP DATA" pill, card header right.** Label is ambiguous and reads as destructive ("drop"). If it deletes/exports data, it's not in coral=danger; if it means drag-in import, it says so nowhere. It's also the loudest action in the view but is lavender — violates "primary = sage," and no sage primary action exists anywhere in this view.
- **P1 — Tag pills, all 4 rows.** Set ~2 steps below body size in low-contrast slate outlines with tiny hit targets — legibility/usability risk for the exact audience (sick, overwhelmed). Worse, navigational tags ("→ Insurance", "→ Bills") are visually identical to decorative metadata tags, so the useful affordance is invisible.
- **P1 — Safety disclaimer line ("Machine-derived items… confirm it before relying on it"), above list.** The most important trust text on the page is gray fine print, while decorative tags around it are larger and louder. Hierarchy inversion for a honesty-critical message.
- **P2 — "Sep 30" tag, row 2 (Dr. Patel).** Coral=danger used for a routine follow-up date; dilutes real danger signals.
- **P2 — "1 reminder due soon" pill, header right.** Coral again for a caution-level event; ochre is the system's slot for this. As-is, header screams danger alongside actual deadlines.
- **P2 — Active-state inconsistency, one screen:** "Library" nav = sage pill; "All" filter chip = dark ink fill. Two different "selected" vocabularies.
- **P2 — Row 1 tag soup.** Six tags of mixed ontologies (clinical reason, dollar amount, person, deadline, two cross-links) wrapping to a second line; the filled dark "Device" chip sits in that second line with a style unlike its outline siblings and appears on no other row — inconsistent metadata.
- **P2 — "Dr. M. Patel" (row 1) vs "Dr. Maya Patel" (row 2):** same provider, two formats.
- **P2 — Card 4 title "Appeal window closes (computed)"** duplicates the "COMPUTED FROM THE LETTER" badge beside it; pick one honesty signal.
- **P2 — Search placeholder** promises "medications, providers" but this library indexes recordings/transcripts/matters — copy mismatch.
- **P2 — Unexplained coral dot on Riverside card icon (row 3):** unlabeled status badge.
- **P2 — Nav load:** 9 + 7 flat, equal-weight links, no grouping; "Recenter" is vague. Wayfinding tax on overwhelmed users.

**No P0 found** — nothing broken, misaligned, or dishonest; the computed-item labeling is actually a model of the honesty the disclaimer promises.
