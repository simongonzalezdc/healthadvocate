judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-symptoms-modeloff.png)

Can see the image clearly — auditing the dark-mode Symptoms view in its "model off" state.

## What I see

**Layout, top to bottom:** Header bar — sage logo tile + "HealthAdvocate" wordmark left; right cluster: pill "● 1 reminder due soon" (coral dot), two ghost icon buttons (clipboard, theme/moon). Below, a full-width tab strip: "Symptoms" active as a sage pill, then Documents, Bills, Insurance, Drugs, Appointments, Discharge, 2nd Opinion, Recorder, Library — and a 12th tab clipped at the right edge. Main stage: one double-bezel dark workbench panel, centered ~70% width, containing H1 "Symptom Assessment" (with a mauve icon tile), 2-line subcopy, overline "WHAT ARE YOU EXPERIENCING?", a tall single-line textarea, sage pill button "Assess Symptoms", then the results stack: a coral-outlined danger panel ("This needs a human decision." → dev bullets → dashed rule → "Talk to a real person:" crisis/advocate links), then five numbered caps sections (Urgency, Explanation, Name Matches, Action Items, Name Overlap) separated by hairlines. Footer: 2-line centered disclaimer.

**Palette:** Espresso/near-black warm ground, slightly lifted warm-dark panel; sage = logo, active tab, primary button, text links; coral = danger panel border/title/988 line + reminder dot; slate = muted pill and secondary text; ochre absent. This is a dark variant — the committed "warm paper" light identity is not present.

**Type:** One sans family; H1 ~15–16px semibold; overlines and section headers ~9px letterspaced caps; body ~11px; micro-captions (similarity %, footer) ~8–9px. Compressed scale overall.

**Spacing/quality:** Panel padding is calm; the results stack beneath is noticeably denser. Pills, dividers, and radii are consistent; the danger panel construction (border + tinted fill) is good. Honesty is excellent — "NOT A DIAGNOSIS", "Model unavailable — no urgency assessment was made", "not a check of clinical accuracy" all present.

## Defects

**P0**
- Danger panel, bullet 2 reads "Decide: on or Human" — garbled/truncated string (presumably "AI or Human") in the safety-critical escalation panel. Verify the source string.
- Section 3 intro line appears to end mid-sentence: "…no urgency assessment was made after" — truncated copy. Verify.
- Nav bar, far right edge: a 12th tab is clipped mid-pill with no scroll affordance or fade — broken overflow; target unknown/unreachable.

**P1**
- Danger panel body copy (dark-red text on maroon fill: "HealthAdvocate would not answer this on its own…", both bullets, the 988 line) sits at/near the contrast threshold at ~10–11px. Safety copy must clear WCAG AA comfortably; this is the weakest text on the page.
- Sage-green links inside the coral danger panel — green-on-red adjacency is colorblind-hostile, and reusing the primary/advocate hue as inline links blurs the one-sage-primary rule.
- Danger panel speaks developer, not patient: "stripped validation errors", "candidate answer", "loopback-only model runtime", "privacy boundary", "generative drafts". Section 4's action items are engineer instructions. Rewrite for a sick, overwhelmed reader.
- Crisis resources (988 line) are same-weight inline links buried below two dev bullets — escalation block needs priority by size/weight/order, not equal list items.
- Hierarchy collapse: H1, overlines, and the five numbered section headers are all within ~5px of each other; the results half reads as a flat undifferentiated list.
- Base type too small for the stated audience (body ~11px, captions ~8–9px); contradicts "generous, calm".

**P2**
- Icon tile left of the H1 is a muted mauve/brown — off-token (not sage/coral/ochre/slate); reads arbitrary.
- Reminder pill dot appears coral; "due soon" is caution → should be ochre per system. Verify token.
- Whole view ships dark against a committed warm-paper system — if dark mode is sanctioned, this ramp needs its own warm-neutral review; currently it's espresso-black, not paper.
- Textarea ~50px tall for one line, with a visible resize grip bottom-right — oversized, and the grip invites broken layouts; reclaim the space for the results stack.
- Ghost icon buttons (clipboard, theme) top-right are very low contrast on near-black.
- Footer disclaimer is the dimmest, smallest text on the page while carrying the legal/safety line.
- Dashed + solid divider mix inside the danger panel reads dev-console; pick one style.
- Nested numbering collision: section "4. ACTION ITEMS" contains its own "1./2." items in the same style as the page-level numbering.

Net: the honesty layer is genuinely good, but the safety panel — the most important block on the page — is where the contrast, copy-integrity, and jargon problems concentrate; fix that panel and the clipped nav first.
