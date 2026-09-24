judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/final/light-symptoms-modeloff.png)

Image is visible. Audit follows.

## What I see

**Layout, top-to-bottom:** White header band on warm paper body — sage logo tile + "HealthAdvocate" wordmark left; coral pill "1 reminder due soon" + two bordered icon buttons (apps grid, theme toggle) right. Below, a two-row pill tab bar: row 1 Symptoms (active, sage outline) through Recorder; row 2 wraps Library…Help — 15 peer tabs total. Centered single card (double-bezel, white on paper) containing: icon chip + "Symptom Assessment" title + one-line subtitle; letterspaced micro-label "WHAT ARE YOU EXPERIENCING?"; borderless warm-gray textarea pre-filled "mild headache and dizziness for two days"; sage pill button "Assess Symptoms" (the only primary action). Then a large coral danger panel (left rule, dotted internal divider): "This needs a human decision." with crisis lines (988, SAMHSA) in bold coral and escalation links. Then five numbered result sections: 1 URGENCY LEVEL (muted gray pill "Model unavailable…"), 2 EXPLANATION (privacy-boundary paragraph), 3 NAME MATCHES ("headache 94%", "dizziness 90%" with hairline dividers), 4 action items rendered ghost-faint, 5 NAME OVERLAP (INFORMAL) — "Name overlap: low". Centered small-print footer disclaimer, two lines.

**Palette as named hues:** paper cream ground, white panels, sage-green on logo/active tab/primary button, coral on danger panel + reminder badge + title chip, warm-gray/ochre-ish "model unavailable" chip, slate-gray body text.

**Type scale:** ~18px semibold title, ~11px letterspaced uppercase section labels, ~13px body, ~11px captions. One size of body does almost all the work; the scale is compressed and label-heavy.

**Spacing rhythm:** calm and generous — consistent ~24–28px between card sections, safe padding throughout. Component quality is generally high: bezel card, pill buttons, hairline dividers all read as one family.

## Defects

- **P0 — Illegible ghost section.** Section "4 Action items" (card, between the dizziness divider and "5. NAME OVERLAP"): header and both bullet lines render at ~10% opacity ink on white. Content that tells the user what to do next is unreadable, and numbering visually jumps 3 → 5. Raise to body-contrast ink or a proper disabled treatment.
- **P1 — Dev jargon in safety-critical copy.** Danger panel, second bullet: "Find the conditions below using the stripped validation errors" exposes internal error plumbing inside the most important panel on the page. Same leak in section 3: "(name match, 94% string similarity)" is meaningless to a sick layperson. Rewrite in user language.
- **P1 — Hierarchy inversion on the key result.** "Model unavailable — no urgency assessment was made" (section 1 pill) is the single most consequential output and is styled as a low-contrast gray footnote chip, while decorative dictionary matches get bold terms and dividers. The "we did NOT assess urgency" state must be at least as loud as the matches.
- **P1 — Nav overload.** Header tab bar: 15 peer-level tabs wrapping to an orphaned second row (Library…Help) with no grouping or overflow affordance. For an overwhelmed user this is a wall; group into primary + "More", or an overflow menu.
- **P2 — Copy error.** Section 3 header: "NOT A DIAGNOSE" → "NOT A DIAGNOSIS".
- **P2 — Coral semantic dilution, two spots.** (a) Decorative pink/coral icon chip left of "Symptom Assessment" title; (b) header "1 reminder due soon" badge is a caution, not a danger — should be ochre per system. Coral should appear only where the danger panel does.
- **P2 — Copy repetition.** "no urgency assessment was made" appears three times within one screen (section 1 pill, section 2 paragraph, section 3 caption). Say it once, prominently (see P1 above), and cut the echoes.
- **P2 — Micro-label legibility.** The ~10px letterspaced uppercase labels ("WHAT ARE YOU EXPERIENCING?", numbered section headers) sit at the floor of comfortable reading for this audience; step up ~1–2px or darken one tint.

**Holds up well:** one primary action per view is respected (lone sage button); the danger panel is correctly the loudest element with 988/SAMHSA emphasized; double-bezel card, calm spacing, and restrained motion all match the committed system.
