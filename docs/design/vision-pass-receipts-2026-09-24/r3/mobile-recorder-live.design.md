judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/mobile-recorder-live.png)

**DESCRIBE — what I see, top to bottom**

- **Header:** cream-paper band. Sage-green rounded-square tile with white heart + "HealthAdvocate" bold dark-slate wordmark. Right cluster: ochre outline badge "• 1", bordered home icon button, bordered sun/theme button.
- **Tab bar:** horizontally scrolling tabs — Discharge, 2nd Opinion, **Recorder** (active: sage text + sage outline pill), Library, and a clipped "D…" at the right edge. Hairline divider below.
- **Workbench panel:** proper double bezel (outer paper card, inner ivory surface), generous ~24px padding. Inside: periwinkle mic tile + narrow intro paragraph ("Record medical calls…"), dashed slate "DEMO MODE" pill floated right (with a stray "0" glyph in it); full-width pale-sage privacy strip with lock icon ("Stays on this device — never uploaded, never sent"); recording status row — coral pulsing dot, "RECORDING · DEMO" tracked caps, large tabular mono "00:18"; coral two-tone waveform pill; nested ivory transcript card with mono timestamps and caps speaker labels (YOU in sage; INSURER REP truncated).
- **Floating recorder bar:** white shadowed pill — coral dot, mono "00:18", coral filled "Stop & save" button. It sits mid-panel, overlapping the transcript card.
- **Below:** italic-aware explainer paragraph ("[inaudible]… the recorder never guesses"), panel closes, then a muted centered disclaimer footer and a large empty paper region.
- **Palette:** warm paper + ivory neutrals ✓, sage on logo/active tab/labels ✓, coral confined to recording/stop ✓, slate text ✓, ochre badge ✓, one lavender interloper (mic tile). **Type:** humanist sans, coherent scale (~12 tracked caps labels / 16 body / ~34 mono timer), tabular mono for all time values ✓. **Spacing:** calm, even vertical rhythm, consistent 12–16px radii. Overall a credible "warm paper clinic" read.

**DEFECTS**

- **P0 — Stray "0" glyph** inside the DEMO MODE badge, left of "DEMO" (intro row, right column, ~38% down). Broken copy or leaking counter — dishonest artifact.
- **P1 — Floating recorder bar occludes live transcript:** "INSURER REP" speaker label is cut mid-glyph behind the bar (panel center, ~62% down); "medically necessary." continues below it with tight, unmasked clearance. Active content hidden during recording is a usability failure, not just scroll-under.
- **P1 — Primary action in danger hue:** "Stop & save" is the view's one primary action but is coral-filled (floating bar, bottom right). System says sage = primary, coral = danger; it reads as destructive.
- **P1 — Squashed hero paragraph:** intro text locked to ~50% column → 10 short ragged lines with dead whitespace to its right, and it doesn't reflow under the DEMO badge (top-left of panel). First thing the user reads is the hardest to read.
- **P1 — Duplicate recording status:** "RECORDING · DEMO 00:18" (status row) and "● 00:18" (floating bar) both on screen, two large timers competing (upper-mid + mid panel). Pick one source of truth.
- **P1 — Heading fragment clipped mid-glyph** in the seam between tab bar and panel top edge (directly under the active Recorder tab). Sticky header isn't masking scrolled content cleanly.
- **P2 — Off-palette lavender mic tile** (intro row left): cool periwinkle inside a warm-paper system; recolor to slate-tinted paper.
- **P2 — Last tab "D…" hard-clipped** at right bezel with no fade/scroll affordance (tab row, right edge).
- **P2 — Theme (sun) button** nearly invisible — cream border on cream paper (header, right).
- **P2 — Triple-nested bezel:** transcript card inside inner panel inside outer bezel (mid panel) — heaviest nesting on the page; flatten one level.
- **P2 — Privacy message ×3 in one screen:** intro paragraph, sage strip, footer disclaimer all say "stays on this device." Keep the strip; trim the other two.
- **P2 — Redundant badge encoding:** ochre header badge shows both a dot and "1" (header, right).
- **P2 — Dead paper** below the footer disclaimer (~10% of page height, bottom): pull footer to bottom or reclaim the space.
