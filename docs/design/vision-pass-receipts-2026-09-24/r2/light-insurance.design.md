judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/light-insurance.png)

# Audit — HealthAdvocate "Coverage Continuity" (file named *light-insurance*)

**Headline: the "light" shot renders the DARK theme.** The frame is near-black end to end, and it is byte-identical to the file tagged `dark-insurance`. Either the wrong variant was attached or the light build fell back to dark. Everything below judges the image as seen.

## What I see

- **Layout, top to bottom:** App bar (sage shield-heart logo badge + "HealthAdvocate" left; ochre outlined pill "1 reminder due soon", two circular ghost icon buttons right) → full-width nav row of 11 small links (Intake…Help) with "Coverage" as an active sage pill → content block: H1 "Coverage Continuity", one-line intro, "Case title (synthetic)" label, text input with placeholder, sage filled button "Create Coverage Case" → hairline divider → centered muted disclaimer. Content is top-anchored and left-col; the bottom ~45% of the frame is empty ground.
- **Palette as named hues:** Ground is warm near-black charcoal, *not* warm paper — the paper neutrals are inverted. Sage green is correctly used for logo icon, active nav pill, and the single filled CTA. Ochre/amber appears on the reminder pill. No coral, no slate on this view. Text is white/off-white headings, warm-gray body, dimmest warm-gray footer.
- **Typography:** One sans family; H1 ~20–22px bold, body ~13px, label/placeholder ~12px, nav ~11px, disclaimer ~10–11px. Ladder is compressed; the H1 barely out-ranks body.
- **Spacing rhythm:** Header/nav tight and tidy; heading→body gap tight (~8px); form gaps comfortable; wide calm gap before the disclaimer. Overall vertically sparse rather than composed.
- **Component quality:** Cleanly rendered — pills, ghost icon buttons, input, filled button all aligned, no visible misalignment, no motion artifacts.

## Defects

- **P0 — Whole frame:** Theme contradiction. Deliverable named "light" shows the dark theme (near-black ground everywhere). Fails the committed warm-paper neutrals at the root; the light variant was never actually shown.
- **P1 — Content area:** Committed double-bezel workbench panel is absent. The form floats bare on the ground with only a hairline divider; the system's signature container appears nowhere.
- **P1 — Label + placeholder row:** Internal seed language leaked into user copy — "Case title **(synthetic)**" and placeholder "e.g. **Synthetic** job-loss coverage case." Confusing, test-bench wording in a patient-facing tool.
- **P1 — Footer disclaimer:** The safety line ("Always consult a qualified healthcare provider…") is the dimmest, smallest text on the page; contrast looks below 4.5:1 at ~10–11px. Safety copy can't be the lowest-legibility element.
- **P1 — Header right:** "1 reminder due soon" pill is bordered and tinted like a second CTA, competing with the one-primary-action rule; it also spends ochre (caution) on a routine reminder where slate (info) is the system's fit.
- **P2 — Lower ~45% of frame:** Dead ground. Content is top-anchored and the footer ends mid-frame; reads as an unfinished render at this viewport rather than generous calm spacing.
- **P2 — Type scale globally:** Compressed ladder (~1.5 step from H1 to body); nav at ~11px is small for sick, tired users.
- **P2 — Nav row:** 11 flat links, no grouping/separators; "Reactor" and "Scanner" are opaque labels. Density undercuts the "calm" claim.
- **P2 — Input field:** Placeholder warm-gray on dark fill looks ~3:1, under placeholder-contrast guidance.
- **P2 — Heading block:** "Coverage Continuity" sits ~8px above its supporting line — visually glued, tighter than the system's generous rhythm.

**Verdict:** Fail. The P0 theme contradiction alone invalidates this as the light-variant deliverable; the missing double-bezel panel and the "(synthetic)" copy leak are the next must-fixes.
