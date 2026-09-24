judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/light-recorder-summary.png)

Judged from `judge-img/r1/light-recorder-summary.jpg` (the stated `r2/` path doesn't exist on disk — `judge-img/r2` is a file, not a directory; flagged in case the wrong image was attached).

## What I see

Full-page light-mode capture of the Call Recorder **summary** view. Top-to-bottom: warm paper background; a centered double-bezel white panel opening with a coral-tinted mic chip + "CALL RECORDER" small-caps label + intro paragraph + "DEMO MODE" outlined pill (right); a sage-tinted privacy strip ("Stays on this device — never uploaded, never sent"). Then — anomalous — a full-bleed white app header (sage shield logo, "HealthAdvocate", ochre "1 due soon" pill, bell, theme icon) with the 10-item nav row (Recorder active, sage, underlined) cutting across the viewport mid-page, slicing the panel. Below it: "COMMITMENTS PEOPLE MADE" (two gray-italic quotes, each with sage "● FROM TRANSCRIPT" chip); "DEADLINES DETECTED" ("Oct 8" row with FROM TRANSCRIPT chip; a "?" row with "UNVERIFIED" chip; a coral callout "This needs a human decision."); "SUGGESTED ACTIONS" (two rows with ochre "● MODEL-INFERRED" chips); "USE THIS CALL" (sage-tinted "Prepare for the callback" chip + two plain chips) with a near-black toast "Saved to the Library (demo — synthetic only)" sitting over the row; "YOUR RECORDINGS (DEMO)" (two rows with Library/Delete outline buttons, one "New demo recording" row). Centered footer disclaimer. Type is one small monotone scale (~12–13px) with letter-spaced caps section labels carrying all hierarchy. Spacing rhythm is generous and consistent; chips and rows align cleanly.

## Defects

**P0**
- **Global header floats mid-page (~y 205–265, full bleed)** — logo bar + nav band renders *over* the panel between the privacy strip and "Commitments," slicing the card in two. Chrome mispositioned over content (sticky-header scroll artifact or broken stacking); the panel intro is orphaned above the app nav.

**P1**
- **Toast occludes action row (center, ~y 610)** — the dark "Saved to the Library" pill sits on top of the "Use this call" chips, partially covering interactive targets; its near-black fill is also off the warm-paper palette.
- **No single primary action** — "Prepare for the callback" (sage tint) competes with 2 sibling chips + Library ×2, Delete ×2, New demo recording. One-primary-per-view violated.
- **"Delete" adjacent and visually equal to "Library"** (recordings rows, right edge) — destructive action undifferentiated (not coral, no separation) in a medical-records list.

**P2**
- **Copy references a nonexistent affordance** — coral callout says "The *underlined* deadline…" but nothing is underlined in the "?" row above it.
- **"DEMO MODE" pill hue (panel top-right) reads lavender-blue** — outside the named sage/coral/ochre/slate set.
- **Coral mic chip used decoratively** in the panel header — coral=danger semantics diluted on a non-danger, idle summary view.
- **Monotone type scale; evidence de-emphasized** — the commitments quotes (the payload of this view) are smaller gray italic than their section labels.
- **Stray white strip/seam across the very top (~y 0–25)** above the paper background.
- **Redundant copy** — row says "(demo recording)" inside a section already labeled "(DEMO)".
- **Footer disclaimer low contrast** (bottom center, small gray).

Honesty is otherwise good (provenance chips, "no date could be read," demo labels); palette, section rhythm, and chip alignment are largely on-system — the mid-page nav band is the one must-fix.
