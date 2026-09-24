judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/final/light-home.png)

Can see the image clearly — auditing it now.

## What I see

**Layout (top→bottom):** Fixed-width centered container on warm paper. Header: sage heart-logo chip + "HealthAdvocate" wordmark left; ochre "1 reminder due soon" outline pill + two faint ghost icon buttons right. Below: a link nav that wraps onto a second row (Symptoms…Recorder / Library…Help — 16 items). Hero: three letterspaced caps chips ("FREE · OPEN SOURCE · PRIVATE BY DESIGN"), two-line display heading "You deserve to understand your care.", gray subcopy, then a filled sage primary ("Describe your symptoms") + ghost secondary ("Fight a denial"). Workbench row: one large double-bezel featured card ("Something doesn't feel right", green CTA "Start a symptom check", pinned footer meta) beside two stacked single-bezel cards (document, costs). Then "What's coming up" + DEMO DATA pill + a tiny low-contrast caption, followed by four timeline rows with left accent bars and big date numerals (26 THU due-soon ochre; 30 SEP upcoming slate; 20 SEP overdue coral filled; 24 SEP done, dimmed). Stats strip: three cards each with a large sage "0". Footer: two-line centered disclaimer.

**Palette:** Warm paper ground, off-white cards, sage-green primary (logo, CTAs, zeros), coral = OVERDUE, ochre = DUE SOON + reminder pill, slate = UPCOMING/icon chips, near-black ink, mid/light gray secondary. On-system.

**Type scale:** ~36-40px bold display → ~14-15px card titles → 12-13px body → 10-11px meta → 9px letterspaced caps chips. Timeline titles sit at card-title size. Scale is coherent; the small end is consistently under-contrast.

**Spacing/component quality:** Generous, calm vertical rhythm; consistent container alignment from hero through footer; chips, pills, and bezels are cleanly drawn. Craft is good — the problems are hierarchy and state logic, not sloppiness.

## Defects

**P0** — none found. Nothing broken, misaligned, or dishonest at the pixel level.

**P1**
1. **Nav wrap** (band under header): 16 links spill to a second row with no grouping, divider, or active state — reads as an accidental wrap, not a designed two-tier nav.
2. **Two competing primaries**: hero "Describe your symptoms" and card "Start a symptom check" are both filled sage in one view; violates the one-primary-action rule.
3. **Timeline sort buries urgency**: OVERDUE (Sep 20, row 3) sits below DUE SOON (Sep 26) and UPCOMING (Sep 30); order 26→30→20→24 matches no visible key. For this audience the red item must lead.
4. **Inconsistent date labels**: row 1 sub-label is a weekday ("THU"), rows 2–4 are months ("SEP") in the same slot.
5. **Zero-stats strip reads as broken**: three identical green "0"s with no empty-state message or CTA — looks like failed data, not "you haven't started yet." "RESOLVED 0" in success green is also tonally wrong.
6. **Demo-data caption is nearly illegible**: ~10px very-light gray under "What's coming up"; it's the disclosure that the data is synthetic and must be readable.

**P2**
7. Run-in meta after row titles (row 1: "Matter: MRI denial (Aetna) · detected in the Sep 24 call") is tiny/low-contrast and crowds the right status chip; will collide at narrower widths.
8. Bezel inconsistency: featured card is double-bezel, right cards and all timeline rows are single-border — the "workbench panel" treatment isn't applied as a system.
9. Status chip weight logic: DUE SOON/UPCOMING outlined but OVERDUE and DONE filled — a completed item visually out-shouts a due-soon one.
10. Tag chips ("Call Aetna member services", "Open") hover at the contrast floor.
11. Featured card dead zone: ~70px void between CTA and pinned footer meta while the right cards are dense.
12. "What's coming up" heading is the same size as card titles — page hierarchy is h1 then flat.
13. Header ghost icon buttons (grid, theme) are close to invisible.
14. DONE row's meta ("remittance bill requested") dimmed past legibility.
15. Doc and cost icon chips share the same slate tint; cost should take ochre per the semantic palette.
16. Reminder pill's leading dot is ambiguous (status dot vs. decorative bullet).

**Fix priority:** 2 → 3 → 5 → 1 → 4/6. The fastest credibility win is demoting "Start a symptom check" to secondary and re-sorting the timeline so the coral OVERDUE row is first.
