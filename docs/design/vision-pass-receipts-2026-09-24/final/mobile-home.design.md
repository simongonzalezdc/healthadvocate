judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/final/mobile-home.png)

NO-IMAGE refusal not applicable — image is visible and legible. Audit below.

## What I see

**Layout, top-to-bottom:** sticky header (sage heart logo + wordmark left; coral-count pill, bell, theme toggle right) → scrollable section tabs (Symptoms / Documents / Bills / Insurance / Dri… clipped) → hero on paper bg (letterspaced eyebrow pill "FREE · OPEN SOURCE · PRIVATE BY DESIGN", 2-line display headline, body para, solid-green primary CTA + ghost secondary) → three stacked "intent" cards (symptom check / document / costs), first with its own green CTA and trust micro-row → "What's coming up" section with DEMO DATA chip + small explainer → four vertical timeline cards, each with big date numeral left, title, body, status chip (DUE SOON / UPCOMING / OVERDUE / DONE), call-pill, ghost "Open" → stat tile row (2-up + 1 orphan) → centered legal-ish footer.

**Palette:** warm paper ground, near-black ink, warm-grey body text, white card surfaces with hairline warm borders. Sage/forest green = logo + primary CTAs + stat zeros. Coral = count pill, OVERDUE chip + card edge. Ochre = DUE SOON chip. Slate = UPCOMING + DEMO DATA chips. Semantics mostly hold.

**Type scale:** coherent ladder — letterspaced micro-caps (eyebrow, tile labels, chips) → ~34px bold display → ~19px card titles → 15px body → 12px captions; ~30px bold date numerals. No rogue sizes.

**Spacing/components:** generous section rhythm (~40–48px), consistent 16px gutters, uniform pill chips, tinted icon tiles, consistent radii, calm motion cues. Cards read as single hairline bezel + soft shadow; double-bezel only faintly suggested on the featured card. DONE card correctly de-emphasized; honest DEMO DATA disclosure is good practice.

## Defects

**P0**
- **Timeline card 1 body:** "…MRI denial (Aetna) · detected in" — sentence dies mid-clause, object missing. Broken copy in the page's most important reminder.
- **Stat tiles (bottom):** entire group renders washed-out, ~40% opacity; caps labels + captions ("health concerns being monitored"…) are near-illegible on paper. Reads as disabled; fails contrast.

**P1**
- **Two solid-green primaries in one viewport** — hero "Describe your symptoms" and featured card "Start a symptom check" compete; violates the one-primary-action-per-view commitment and doubles decision load for the exact (overwhelmed) user this serves.
- **Nav tab clipped mid-word** ("Dri…") at right viewport edge with no fade/scroll affordance — content visually broken.
- **Timeline order scrambles urgency:** 26 → 30 → 20 → 24. The coral OVERDUE item ranks third, below two future items; danger should lead (or the sort must be visibly deliberate).
- **Orphan stat tile:** 3 tiles wrap 2-up + 1 left-aligned — grid breaks, ragged bottom edge.

**P2**
- Same funnel, two names: "Describe your symptoms" vs "Start a symptom check."
- Mixed date-block units in one timeline: "26 / FRI" vs "30 / SEP", "20 / SEP", "24 / SEP."
- "Appointment with Dr. Patel Follow-up" — run-on title; needs separator before "Follow-up."
- Appeal card redundancy: "Aetna MRI denial" in title, "MRI denial (Aetna)" repeated in body.
- "FROM THE CALL" chip — cryptic jargon, crowds the chip row beside the date.
- Accent system inconsistent: OVERDUE card gets coral edge + chip; DUE SOON card gets a chip but no matching ochre edge.
- Header count pill "• 1" in coral dilutes coral=danger for a mere count; ambiguous affordance sitting next to the bell.
- Four vague ghost "Open" buttons — open what?
- Demo disclosure paragraph is the smallest, lightest text on the page despite being the honesty load-bearing line.
- Two greens in one view: CTA green reads darker forest than the sage logo tile; system names sage as the accent.
- Double-bezel workbench treatment absent on timeline/stat cards — fidelity gap vs the committed system.
- Demo date math off: "expired 4 days ago" but dated 20 SEP when "today" ≈ 26 SEP.

**Verdict:** strong bones — palette semantics, type ladder, and calm rhythm largely deliver "warm paper clinic." Ship-blockers are the truncated reminder copy, the illegible stat tiles, and the dual primary CTA; fix those plus timeline ordering before this faces a sick, overwhelmed user.
