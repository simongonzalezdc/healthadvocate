judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-directory-live.png)

## What I see

**Layout, top to bottom:** (1) Header bar: sage logo tile + "HealthAdvocate" wordmark with a micro-subtitle underneath; right side has an ochre-dot "≈ 1 due soon" pill plus two small icon buttons (case, moon). (2) Nav row of 10 links, "Directory" active as a sage pill, plus a clipped item at the far right edge. (3) One centered double-bezel workbench panel: "DIRECTORY" eyebrow + icon, two-line description, "DEMO DATA" badge right; full-width search field; filter chip row (All active, sage); a two-line badge legend ("FROM A CALL", "INFERRED", "YOU CONFIRMED ✓"); four provider cards (Dr. Maya Patel, Riverside Imaging, Aetna member services, Corner Pharmacy), each with icon tile, title, uppercase right meta (e.g. "DOCTOR · ORTHOPEDICS"), a "Merged from N sources…" provenance line, label/value rows (PHONE / ADDRESS / EMAIL / HOURS / APPEALS FAX) with source badges and gray "Confirm" links, and Call / Items-in-Library footer actions. A dark toast ("Saved to the Library (demo — synthetic only).") floats over card 2's title row. (4) Centered three-line disclaimer footer.

**Palette:** warm paper cream ground and panel fills, charcoal-warm text; sage = active nav, confirmed/call badges, logo; ochre = inferred badges, provenance source names, "due soon" dot; slate = BILL DECODE / DOCUMENT badges; coral barely present (Aetna icon tile reads faintly warm-red). System-conformant.

**Type scale:** everything small — ~9–10px eyebrow/badge microcaps, ~11px nav/body, ~13–14px card titles, wordmark ~13px, and a ~7px subtitle under the wordmark. No H1 anywhere; the eyebrow "DIRECTORY" is the de facto page title.

**Spacing rhythm:** genuinely calm — wide page margins, generous panel padding (~24px+), even card gaps, aligned uppercase label column inside cards. Best-in-screenshot aspect.

**Component quality:** chips, badges, and rows are consistent (radii, strokes); demo-honesty is excellent (DEMO DATA badge, `.example` email, "synthetic only" toast). Outliers: the toast placement and the clipped nav item.

## Defects

- **P0 — Toast occludes content.** Dark toast sits directly on card 2's title row, hiding part of "Riverside Imaging" and crowding the provenance line. Toasts belong in a corner, never over the data they reference — on a "trust the record" screen this reads as broken.
- **P0 — Clipped nav item, top-right of nav bar.** A lone "S" is cut mid-glyph at the viewport edge with no right margin. Overflow 10-item nav; looks broken at this width.
- **P1 — Illegible wordmark subtitle, header left.** ~7px gray underlined text under "HealthAdvocate"; unreadable, and underline implies a link of unknown purpose.
- **P1 — Type scale too small for the audience.** Body/legend/meta at ~9–12px low-contrast gray on cream; sick, overwhelmed, possibly low-vision users are the stated users. Titles and labels need +2–4px and darker values.
- **P1 — "Confirm" links have no affordance.** Plain light-gray text repeated ~10× across cards; reads as a label, not the view's key corrective action. Needs icon/underline/link styling and better contrast.
- **P1 — No primary action in the view.** System commits to one primary action per view; here every action (Call, Confirm, Library) is tertiary-weight. If browsing is primary, say so visually; currently nothing leads.
- **P2 — Provenance ochre inline text.** Card 1–2 "Merged from…" source names set in ochre read as warnings/links; provenance is informational, not caution-state.
- **P2 — "Confirm" links ragged.** They flow inline after badges, so their positions jitter row-to-row within each card; no shared column.
- **P2 — Coral dilution.** Aetna card icon tile appears coral-tinted; coral should stay reserved for danger, not insurer category tint.
- **P2 — Date outlier.** Card 2 provenance cites "(Dec 3)" among Aug/Sep dates — implausible next to "Sep 24" merges; undermines the honesty story even in demo data.
- **P2 — Toast styling off-palette.** Near-black charcoal pill is the harshest object on the page; a warm-dark paper tone would match the system.
- **P2 — Nav crowding.** 10 equal-weight items + truncated 11th; consider overflow menu before the edge, not a glyph cut.

**Strengths to keep:** badge semantics (sage confirmed / ochre inferred / slate decoded) are legible and consistently applied; "YOU CONFIRMED always wins" legend is exactly the right trust pattern; DEMO DATA labeling and `.example` contacts are honest.
