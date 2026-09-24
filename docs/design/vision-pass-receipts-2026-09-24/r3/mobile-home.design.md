judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/mobile-home.png)

I can see the image — auditing it now.

## DESCRIBE

**Layout, top to bottom:** Fixed-feeling header (dark-sage logo tile with heart + "HealthAdvocate" wordmark; right side: amber "• 1" count pill, bell button, gear). Horizontally scrollable tab row (Symptoms active, Documents, Bills, Insurance, "Dru…" clipped). Tracked-uppercase trust chip ("FREE · OPEN SOURCE · PRIVATE BY DESIGN" — wraps to two lines). Hero: 2-line headline + 2-line subcopy + filled sage primary "Describe your symptoms" + ghost "Fight a denial". Three task cards (pulse icon card with its own filled sage CTA + trust footer row; document card; cost card — last two CTA-less). "What's coming up" section: muted privacy disclaimer + four reminder cards, each with left date rail (day/weekday/month), status pill at right (ochre DUE SOON, slate UPCOMING, coral OVERDUE, muted DONE), a "call" bubble, and a ghost "Open" chip; colored left accent edges match status. Stats: three uppercase-labeled zero-count cards in a 2+1 grid. Footer disclaimer.

**Palette:** Warm paper ground throughout; dark sage for logo/primary fills; sage tint on chip + icon wells; ochre, coral, slate used correctly and semantically on status pills and card accent edges. Nothing off-palette.

**Type:** System sans. Hero ~30/34 bold; card titles ~17 semibold; body ~15; muted meta ~13–14; tracked uppercase micro-labels ~11. Scale is coherent; section header "What's coming up" is the weakest voice — barely larger than card titles.

**Spacing/component quality:** Generous, calm vertical rhythm (~20–24px card gaps, roomy card padding). Card 1 shows the committed double-bezel; siblings don't. Zeros in stats are honest, not faked. Overall it genuinely reads "warm paper clinic."

## DEFECTS

**P1**
- **Two filled sage primaries in one view** — hero "Describe your symptoms" and card-1 "Start a symptom check" are the same task, both filled, both in the first viewport. Violates the one-primary rule; keep the hero button, demote card 1's to ghost or remove the card.
- **Reminders unsorted** — order runs 26 → 30 → 20 → 24 Sep; the coral OVERDUE item (20 Sep, "Refill metformin") sits third behind two future items. The most urgent card for an overwhelmed user is buried; sort by urgency (overdue → due soon → upcoming), park DONE last.
- **Reminder card grid collapsed** — in all four cards ("Appeal deadline", "Appointment with Dr. Patel", "Refill metformin", "Ask billing…"), the title spans the full card *above* the date rail, so the status pill floats mid-card at the right, aligned to the date row instead of the title line. Intended rail-beside-content anatomy broke; it also inflates each card's height.
- **Cards 2 & 3 have no affordance** — "I have a document to understand" and "I need help with costs" are big cards with no CTA, chevron, or pressed style while sibling card 1 has a button; tappability is guesswork.
- **Zero-state dead end** — stats row shows three large 0s (ACTIVE TRACKS / FAMILY MEMBERS / RESOLVED) with captions but no "add your first…" affordance anywhere; new users hit a wall of empties.

**P2**
- **Trust chip wraps** — "FREE · OPEN SOURCE · PRIVATE BY / DESIGN" breaks mid-phrase in the hero chip; shorten copy or drop the tracking so it fits one line.
- **Privacy claim said ~5×** — chip, hero subcopy, card-1 footer, reminders disclaimer, footer. Consolidate to one header chip + one footer line; the repetition starts to sound anxious.
- **Tab row clips "Dru…"** with no fade or partial-next-tab peek; scrollability isn't signalled.
- **Date-rail anatomy inconsistent** — first reminder shows weekday ("26 FRI"); the other three show day+month only.
- **Card anatomy drift** — card A's call bubble carries a "• FROM THE CALL" header, cards B/C bubbles are bare; card B stuffs schedule detail ("9:40 AM - bring the imaging CD") into the bold title line while C/D use muted meta lines.
- **Double bezel applied to card 1 only**; cards 2–3 are single hairline — panel system drifts within one group.
- **Stats grid orphan** — third card ("RESOLVED") sits half-width with an empty right cell; go 3-up, 2+full, or full-width.
- **Badge detached** — the "• 1" count pill floats left of the bell instead of anchoring to it.
- **"Open" ghost chips** are the only per-reminder action — very small target and low affordance for the primary thing to do with a reminder.

**P0: none** — nothing illegible, dishonest, or overlapping; the zeros are honest and status colors map truthfully to state. The worst offenders are the collapsed reminder grid and the double primary.
