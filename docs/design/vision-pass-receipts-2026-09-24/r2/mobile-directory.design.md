judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/mobile-directory.png)

**Note:** the attached path was broken (`r2` is a file, not a directory) — I judged the actual screenshot at `judge-img/r1/mobile-directory.jpg`. Image received; full audit below.

## What I see

**Layout, top-to-bottom:** white header (sage heart logo + "HealthAdvocate" wordmark, outlined "• 1 due soon" pill with ochre dot, home + theme icon buttons) → horizontally scrollable text tabs ("2nd Opinion / Recorder / Library / **Directory** / Se…" clipped) → double-bezel hero panel (person icon, letterspaced "DIRECTORY" eyebrow, ~9-line intro paragraph, tilted dashed "DEMO DATA" stamp at right) → search field → two wrapped rows of filter chips (All active, Doctors, Labs, Imaging, Therapy, Pharmacy) + orphan "Insurers" row → naked-text provenance legend with three sample badges → four provider cards (Dr. Maya Patel, Riverside Imaging, Aetna member services, Corner Pharmacy), each with icon tile, name, provenance paragraph, then per-field label/value/badge(+Confirm) stacks, and a ghost "Call / Items in Library" action row → small-print footer disclaimer.

**Palette:** warm paper cream background, white header/bezels, sage confined to logo, icon tile (card 1), and "YOU CONFIRMED ✓" outlines; ochre on INFERRED badges and the due-soon dot; slate on provenance badges (FROM A CALL, VOICEMAIL, DOCUMENT, CALL); pink/coral appearing on the last two cards' icon tiles.

**Typography:** bold ~17px wordmark, ~16px bold card names, ~14px body/values, and many letterspaced small-caps voices (~10–11px): eyebrow, category, field labels, badges. Scale is coherent; caps density is high.

**Spacing/components:** generous, even card gaps; consistent 1px warm-gray borders and radii; ghost buttons consistent; chips consistent. Merge-count paragraphs honestly match the sources listed (3 listed = "3 sources" ✓). Component craft is good overall; the failures are content and pattern discipline, not construction.

## Defects

**P0**
- **Search field:** placeholder clipped mid-word — "…phone r" — no ellipsis, broken text in the view's primary control.

**P1**
- **Riverside Imaging, HOURS row:** ochre badge and "Confirm" wrap onto separate lines; "Confirm" sits orphaned on its own line and reads as a stray control.
- **Card 1 (Dr. Maya Patel) sources line:** reads "Bill decade (Aug 30)" while the address badge says "BILL DECODE" — nonsense copy / label mismatch (verify string).
- **Hero panel:** ~9-line paragraph plus demo stamp fills the entire first viewport — zero providers visible before scroll. Wrong trade for sick, overwhelmed users; compress or collapse.
- **Icon tiles, cards 3–4 (Aetna, Corner Pharmacy):** pink/coral tint. Coral is reserved for danger in this system — this reads as alarm on two routine contacts, and breaks the sage tile established on cards 1–2.
- **Card-header pattern inconsistency:** cards 1–2 put category as a small-caps line under the name; cards 3–4 pin it top-right ("INSURER", "PHARMACY"). Pick one pattern.

**P2**
- **Legend under-explains:** shows 3 badge types; cards use 7 variants (BILL DECODE, VOICEMAIL, DOCUMENT, CALL, INFERRED·PATTERN/VOICEMAIL/LETTER).
- **Legend floats naked on paper** between chips and first card — breaks the panel rhythm; give it a container or fold it into the hero.
- **Low-contrast meta text:** PHONE/ADDRESS/HOURS labels, "DOCTOR · ORTHOPEDICS", and legend body are light warm-gray on cream — likely sub-AA at these sizes.
- **No sage primary in the action layer:** search and Confirm are all neutral; the system's "one sage primary action" identity exists only in the logo and badges here.
- **Three-line stack per field** (label / value / badge+Confirm) × 3–4 fields makes very tall cards; consider value+badge inline.
- **Corner Pharmacy badge spam:** "YOU CONFIRMED ✓" repeated on all three fields when the merge line already says "You confirmed every field."
- **Tab bar:** last tab hard-clipped ("Se") with no edge fade to signal scroll; active "Directory" marked by weight only — weak state contrast.
- **Caps overuse:** five distinct letterspaced-caps voices compete within a single card (eyebrow, category, field label, provenance badge, action row).
- **Chips wrap 3/3/1**, leaving "Insurers" alone on a ragged tail row.

**Verdict:** structurally sound and honest (provenance labeling is a genuine strength), but not shippable at r2: fix the clipped placeholder, the orphaned Confirm, the coral category tiles, and the viewport-eating hero before this reaches users.
