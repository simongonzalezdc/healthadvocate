judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-recorder-summary.png)

I can see the image — a full-page capture of the Recorder summary view rendered in a dark theme. Audit follows.

## What I see

**Layout, top to bottom:** (1) A "Call Recorder" hero — mic badge, title, two-line privacy description, "DEMO MODE" pill at right, then a dark-sage privacy banner ("Stays on this device…"). (2) A full-bleed sticky nav band floating mid-capture: HealthAdvocate logo + wordmark left; "1 reminder due soon" ochre pill, bell, and moon/theme icons right; a horizontally scrolling nav row (Symptoms → Recorder [active, sage pill] → Library, clipped at the edge). (3) A double-bezel dark panel containing numbered sections in this visible order: **2** Commitments (two quotes + "FROM TRANSCRIPT" chips), **3** Deadlines ("Oct 8" row + "no date" row + "UNVERIFIED" chip), a coral callout ("This needs a human decision"), **4** Suggested Actions (two rows + ochre "MODEL-INFERRED" chips), **5** Use This Call (three equal ghost buttons), then **1** Your Recordings (two rows with Library + coral Delete pills, plus a replay row). (4) Dim centered disclaimer footer.

**Palette:** deep warm umber/near-black page and panel (inverted paper), warm cream text, sage only in the logo tile + active "Recorder" pill + privacy banner, coral on the two Delete pills and the danger callout, ochre on the reminder pill and MODEL-INFERRED chips, slate on FROM TRANSCRIPT chips and the action/Library buttons. Hue semantics are applied correctly.

**Type:** hero title barely outranks body; body ~1 step down from that; section labels and provenance chips are very small tracked caps; footer smallest. **Spacing:** genuinely calm — even generous section gaps, consistent row rhythm, hairline separators; this is the strongest quality. **Components:** pills, chips, and buttons are consistently radiused and cleanly built; the coral callout is well-formed.

## Defects

**P0**
- **Section order is broken:** visible sequence reads 2 → 3 → 4 → 5 → **1**; "1. Your recordings" renders at the bottom, below "5. Use this call." For the target user this is a broken summary. (main panel, lower third)
- **Sticky nav slices the page mid-content:** the full-bleed nav band + hard shadow seam cuts between the hero and section 2, so the capture reads hero → nav → mid-document. If it's a full-page-capture artifact, still wrong in the artifact; if real, it's an overlay bug. (band at ~1/3 page height)

**P1**
- **No primary action — inverted emphasis:** the forward path ("Prepare for the callback" / "Decode as document" / "Open in Library") is three equal ghost buttons, while the most saturated fills on the page are destructive coral Deletes. Violates "one primary action per view" at exactly the moment a sick user needs a next step. (Use This Call; Recordings rows)
- **Nav clipped mid-word:** "Library" cut at the right viewport edge with no fade or scroll affordance. (nav row, right edge)
- **Dark theme strays from the committed system:** "warm paper clinic" is a light-paper identity; this is a full dark inversion where sage — the advocate accent — survives only in two small elements. If dark is an official variant it needs its own audited token set; as committed, this reads off-brand. (global)
- **Type scale too small overall:** section labels, provenance chips, and footer sit well below comfortable reading size relative to the canvas, and the hero title barely outranks body — hostile to overwhelmed, possibly unwell readers. (worst: chips, section labels, footer)
- **Mic glyph nearly invisible:** dark icon on dark-sage badge in the hero. (top-left hero)

**P2**
- **Two right gutters in one panel:** provenance chips right-align noticeably further right than the Library/Delete/Replay buttons below — compare "FROM TRANSCRIPT" edge to "Delete" edge. 
- **"UNVERIFIED" chip is uncolored:** siblings are slate/ochre-coded; this one reads as disabled rather than caution, weakening the honesty signal it exists to give. (deadlines, row 2)
- **Solid coral Delete pills are the loudest element, twice:** downgrade to outline/ghost with coral text so danger stays available but not dominant. (recordings rows)
- **Reminder/bell/theme cluster crowds the nav's right edge** with three small low-contrast targets. (nav, right)

**Honesty check — pass:** "no date," "UNVERIFIED," "MODEL-INFERRED," the confirm-in-writing callout, and the privacy banner are exactly the right integrity moves; keep all of them. The fixes needed are order, emphasis, and scale, not truthfulness.
