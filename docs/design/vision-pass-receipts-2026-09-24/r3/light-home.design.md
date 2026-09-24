judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/light-home.png)

I can see the image clearly. Audit follows.

## Description — what's actually there

**Layout, top to bottom:** White app bar (sage shield-heart logo + "HealthAdvocate" left; ochre pill "1 reminder due soon" + bell chip + two circular icon buttons right). Full-width nav strip of ~11 small text items (Symptoms … Library, plus one clipped at the right edge). Then a warm-paper hero: sage micro-caps badge "FREE · OPEN SOURCE · PRIVATE BY DESIGN", large two-line H1 "You deserve to understand your care.", one-line gray subcopy, sage primary button "Describe your symptoms" + neutral secondary "Fight a denial". Below, a two-column zone: a large double-bezel card ("Something doesn't feel right" + green CTA "Start a symptom check" + footer meta "Private by design · No account needed") beside two stacked flat cards ("I have a document to understand", "I need help with costs"). Then "What's coming up" with a right-aligned gray micro-caption, a 4-row timeline (26 SEP / ochre / DUE SOON, 30 SEP / slate / UPCOMING, 20 SEP / coral / OVERDUE, 24 SEP / gray struck / DONE), three stat tiles (ACTIVE TRACKS 0, FAMILY MEMBERS 0, RESOLVED 0), and a centered gray disclaimer footer.

**Palette:** Reads correctly as the committed system — warm paper ground, white panels, sage-green reserved for logo + both CTAs, coral strictly on the OVERDUE row/pill, ochre on DUE SOON + reminder pill + row border, slate on UPCOMING, charcoal text with gray muted. Semantic mapping is honest and consistent, including per-row left border accents.

**Typography:** Strong contrast curve — ~40px H1 at one extreme, then a steep drop to ~13px card titles and ~9–10px meta/captions; the mid-scale (section headers, card titles) is thin, so the page jumps from shout to whisper.

**Spacing/components:** Generous calm margins, even card gutters, consistent radii and hairline borders; pills, date blocks, and chips are well-formed. Component craft is genuinely good. The problems are structural, not cosmetic.

## Defects

**P0**
- **Stat tiles lie about the page above them** (bottom tile row): RESOLVED shows 0 while row 4 of the timeline is marked DONE; ACTIVE TRACKS shows 0 while three rows are Open/DUE SOON/UPCOMING/OVERDUE. Dishonest data display on the exact screen a scared user scans first.

**P1**
- **Two competing sage primaries, same task** — hero "Describe your symptoms" (hero, left) and card CTA "Start a symptom check" (large card below) both scream; violates the one-primary-action rule and splits the same intent.
- **Urgency sort inversion** — the OVERDUE row (20 SEP, "Refill metformin") sits below two future-dated rows (26, 30 SEP). The one item needing action now is buried third.
- **Header badge understates state** — "1 reminder due soon" (top right) ignores the overdue item entirely; top-line summary contradicts the list.
- **Micro-text below legibility for this audience** — row meta ("Mother: MRI denial (Knee)…"), stat captions, footer disclaimer, and the right-aligned caption next to "What's coming up" are all very small, low-contrast gray on paper; likely fails AA, hostile to sick/overwhelmed eyes.
- **Right-column cards have no action affordance** — "I have a document to understand" / "I need help with costs" have no CTA, chevron, or hover cue; they read as static text panels though they're two of the three core paths.

**P2**
- **Nav clipped at right edge** — last item cut mid-label with no fade or scroll hint; also no active/current indicator across 11 equal-weight items.
- **Dead vertical space** inside the big symptom card between the CTA and the "Private by design · No account needed" footer — card looks half-filled.
- **Inconsistent panel treatment** — left card gets the full double-bezel; its two right-hand siblings are flat single-hairline cards.
- **Strikethrough on the DONE row** ("Ask billing about the $1,200 charge") — muted gray alone would do; strikethrough plus gray plus tiny size is triple-suppression.
- **Icon-button cluster, top right** — pill + separate bell chip + sun toggle + third unlabeled circle are four adjacent targets doing ~two jobs.
- **Scale gap at "What's coming up"** — tiny section header vs. huge H1; no intermediate heading size in use anywhere.
- **Copy nits** — "Cali Corner Pharmacy" (row 3) looks like a typo; stat captions mix voice ("health concerns being tracked" vs "profiles you are tracking").

**Net:** palette and component craft are on-system and genuinely calm; the P0 is the zeroed counters contradicting visible content, and the P1 cluster is all about the most urgent item being demoted everywhere a user looks first (header badge, sort order, competing CTAs).
