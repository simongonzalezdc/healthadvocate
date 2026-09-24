judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/mobile-recorder.png)

**DESCRIPTION (what I see)**

Mobile view (~522×2036), Call Recorder landing in demo mode, light theme. Top-to-bottom: app bar (sage rounded-square heart logo + bold "HealthAdvocate" wordmark; wide ochre-outlined chip "● 1 due soon" — text wrapped to two lines; two 40px circular icon buttons: home, theme). Tab row: 2nd Opinion / **Recorder** (active, sage pill) / Library / Directory / a tab clipped at the right edge ("Sc…"). Body is a double-bezel paper panel: (1) intro block — small coral mic tile left, sage letterspaced eyebrow "CALL RECORDER", ~8-line description paragraph, and a slate dashed stadium badge "DEMO MODE" with a white "0" dot badge floating on its left edge, top-right; (2) full-width muted pill: lock icon + sage text "Stays on this device — never uploaded, never sent"; (3) nested darker-beige card "Before you record": laws paragraph, unchecked consent checkbox with 4-line sentence, sage filled button "Start demo recording" rendered in a clearly desaturated (disabled) tone; (4) divider, eyebrow "YOUR RECORDINGS (DEMO)", row 1: "Aetna — MRI denial call — Sep 24 · 11:02" with *stacked* outline buttons "Library" / "Delete"; row 2: "Start over with the synthetic call script." + outline button "New demo recording" (label wrapped to two lines). Footer disclaimer paragraph on paper.

Palette matches the system: warm paper ground, sage for primary/nav/privacy copy, ochre = the due-soon caution chip, slate for the DEMO MODE badge, coral only on the mic tile. Type scale is coherent (~20 wordmark / ~18 headings / ~16 body / ~12 tracked eyebrows) with generous line-height. Spacing is calm and consistent; double-bezel nesting is present. Component quality is generally good — chips, pills, and buttons share radius language — but several controls have wrapped labels and one destructive action is unmarked.

**DEFECTS**

- **P1 — App bar, right of wordmark:** "● 1 due soon" chip wraps to two lines inside an oversized pill with dead space at its left; count, dot, and label don't read as one unit. Compact status chips must not wrap.
- **P1 — Intro card, top-right:** "DEMO MODE" dashed badge carries an unexplained "0" dot badge. Zero of *what*? Reads as a broken counter; nothing else on screen counts to it (recordings list is separate). Dashed border also reads as drop-zone/placeholder, not status.
- **P1 — "Before you record" card, primary button:** "Start demo recording" is gated on the consent checkbox and rendered desaturated, but the white label sits near AA-fail contrast on pale sage and there is no adjacent hint that checking the box enables it. For the target user this reads as "broken button," not "one step left."
- **P1 — Recordings row 1, right side:** "Delete" is styled identically to "Library." A destructive action on a real medical recording (denial-call evidence) with zero coral/danger affordance is a safety problem under the committed palette.
- **P1 — Recordings row 2:** "New demo recording" label wraps to two lines inside its pill; wrapped button labels are broken layout, not calm.
- **P1 — View-level IA:** "Start demo recording" (primary) and "Start over with the synthetic call script / New demo recording" are near-duplicate entry points on one screen, diluting the one-primary-action rule.
- **P2 — Tab bar, right edge:** next tab clipped mid-glyph ("Sc…") with no fade/scroll affordance; looks cut off rather than scrollable.
- **P2 — Intro card, left:** mic tile in coral. Idle recorder isn't a danger state; coral here will read as alarm/warning and devalues the hue for when it matters.
- **P2 — Intro card:** paragraph measure pinches around the floating DEMO MODE badge, producing a ragged right column and a hyphen-break feel ("follow-/ups"); badge also misaligns vertically with the eyebrow/text top.
- **P2 — Consent checkbox:** box is ~26px with no full-row tap target — under 44px minimum on mobile for the gate that unlocks the primary action.
- **P2 — Recordings row 1:** Library/Delete stack vertically, inflating row height and pulling the action group off the text baseline.
- **P2 — Global copy:** "(DEMO)"/"demo" appears 5× on one screen (badge, eyebrow, two buttons, caption). Honest, but repetitive; one badge plus one list label suffices.

No P0s: nothing illegible, misaligned to the point of brokenness, or dishonest — privacy claims and demo labeling are consistent and truthful. Verdict: system-adherent, calm frame, but ship-blocking P1s cluster around control states (gated primary, unmarked Delete, wrapped labels) — fix those five before this view is trustworthy for an overwhelmed user.
