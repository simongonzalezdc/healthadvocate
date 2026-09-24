judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/light-documents.png)

**Note:** the path in the prompt (`judge-img/r2/light-documents.jpg`) doesn't exist — `r2` is a stray file, not a folder. The actual image is `judge-img/r1/light-documents.jpg`; that's what I judged.

## DESCRIPTION

**Layout (top→bottom):** White app bar — sage heart-in-shield mark + bold "HealthAdvocate" wordmark at left; right cluster: coral pill badge reading "#1 due soon", two ghost circular icon buttons (person, theme toggle). Below, a second white nav row of 10 text items (Symptoms, Documents … Library) with "Documents" in a pale sage active pill. Body sits on warm paper: one centered white card containing a document-icon chip, micro-caps title "DOCUMENT DECODER", two-line gray subtitle, a micro-caps field label "PASTE YOUR MEDICAL DOCUMENT TEXT", a tall bordered textarea (placeholder "Paste lab results, visit notes, referral letters…"), and a single sage pill button "Decode Document". Below the card: full-width hairline, then a centered two-line disclaimer with bolded product name. Nothing else on the page.

**Palette (as named):** warm paper cream canvas, white surfaces; sage-green accent on mark, active nav, card title, primary button; coral on the header badge (the only danger hue); warm near-black primary text, mid-gray secondary. Ochre and slate absent from this view.

**Type:** single sans family throughout; scale is compressed — roughly wordmark 14px, nav/body ~11px, micro-caps labels ~9–10px with wide tracking. No display-size heading anywhere.

**Spacing/components:** generous card padding, calm vertical rhythm, one primary action, double-bezel present (card bezel + inner textarea bezel). Radii consistent (pills, rounded-squares). Quality is clean; nothing broken, clipped, or misaligned.

## DEFECTS

1. **P1 — Coral badge "#1 due soon", app bar top-right.** Coral = danger, but "due soon" is a deadline nudge = caution → should be ochre. Danger hue spent on a non-emergency trains users to ignore the danger color.
2. **P1 — Same badge, copy.** "#1 due soon" is cryptic — #1 of what? Unparseable without context; label the noun ("1 bill due soon").
3. **P1 — Card header, left ~upper card.** Hierarchy is inverted/compressed: the view's only title ("DOCUMENT DECODER") is a 9–10px micro-caps line, visually equal to the form label below it (same size, same caps, similar tone). Two competing micro-caps styles, no page-level heading; the eye lands on the textarea, not the title.
4. **P2 — Card upper-right half.** Header text block wraps at ~55% card width; entire right half of the card header is dead white, and the card floats in a large empty paper field below. Calm, but under-filled — composition reads unfinished at this aspect ratio.
5. **P2 — Nav row.** All 10 items set at ~10–11px — smallest type on the page carrying primary wayfinding. Tight but not touching; increase nav size before any other type.
6. **P2 — Active nav pill "Documents".** Pale-sage pill on white row is barely separable at a glance; needs a hairline border or deeper fill to read as selected state.
7. **P2 — App bar ghost icon buttons (right).** Person and theme icons are extremely light gray on white — near-invisible affordances.
8. **P2 — Badge legibility.** White-on-coral at ~9px is below comfortable legibility; if the badge stays, bump size/weight.
9. **P2 — Nav label "2nd Opinion."** Only numeral-led, abbreviated item among spelled-out words ("Appointments", "Insurance"); inconsistent naming pattern.

No P0s: nothing illegible, misaligned, or dishonest; the single-primary-action and double-bezel rules are honored.
