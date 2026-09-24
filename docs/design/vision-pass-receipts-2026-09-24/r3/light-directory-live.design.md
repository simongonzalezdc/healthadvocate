judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/light-directory-live.png)

I can see the image — auditing it now.

## What I see

**Layout (top→bottom):** White header bar — sage roundel logo + "HealthAdvocate" left; coral outline pill "+1 reminder due soon" plus two small square icon buttons (clipboard?, sun/theme) right. Below: a full-width tab row (Documents … Recorder, Library, Directory as active sage pill) with one more item clipped at the right viewport edge. Body: warm-gray page, one large double-bezel paper card centered, containing: "Directory" H1 with a "DEMO DATA" slate outline pill top-right; icon + two-line gray intro paragraph; full-width search field; filter chip row (All active-sage, Doctors, Labs, Imaging, Therapy, Pharmacy, Insurers); a two-line legend explaining provenance chips (FROM A CALL / INFERRED / YOU CONFIRMED ✓); then 4 stacked double-bezel provider cards (Dr. Maya Patel / Riverside Imaging / Aetna member services / Corner Pharmacy), each: icon + name + right caps type label, "Merged from…" source line, label-value rows (PHONE, ADDRESS, EMAIL, HOURS, APPEALS FAX) each with a provenance chip and a quiet right-aligned "Confirm" link, footer row with Call + Items in Library. Centered small-print disclaimer footer.

**Palette:** warm paper neutrals (cream page, near-white cards), sage accent (logo, active tab, All chip, YOU CONFIRMED chips), coral (reminder pill, INFERRED chips), slate (VOICEMAIL/DOCUMENT/CALL chips, DEMO DATA), dark ink + muted gray text. On-system.

**Type:** single sans; ~20px bold H1; ~13px card titles (weight-only hierarchy); 11–12px body; 9–10px letterspaced caps for row labels and chips. Scale skews very small overall.

**Spacing/components:** generous, consistent card padding (~20–24px) and even card gaps; 1px hairline double bezels; uniform pill chips and radii. Calm, restrained, no motion. Build quality is generally high.

## Defects

**P0**
- **Top nav, right edge:** last tab after "Directory" is cut mid-word at the viewport edge — clipped, illegible content, no scroll/overflow affordance.
- **Filter row, right edge:** "Insurers" chip is clipped at the card's inner edge; a reachable filter is partially unreadable/untappable.

**P1**
- **Legend vs. card chips:** legend names "FROM A CALL" but cards show "CALL"; BILL DECODE / DOCUMENT / LETTER appear in cards but not in the legend. The provenance key doesn't decode what's on screen — core to the "where it came from" promise.
- **Card 1 (Dr. Maya Patel), PHONE row:** "YOU CONFIRMED ✓" chip sits next to a "Confirm" action — contradictory/redundant affordance; Corner Pharmacy's confirmed rows correctly omit it. Inconsistent rule for identical state.
- **Header, right:** "+1 reminder due soon" is coral = danger; a due-soon reminder is caution-grade (ochre). False-alarm red dilutes real danger cues.
- **Global:** intro paragraph, "Merged from…" lines, and footer run ~11px muted gray on paper — below comfortable contrast for the stressed/sick target audience.

**P2**
- **Corner Pharmacy source line:** "Merged from one source: You confirmed every field" breaks the count+source pattern used by every other card.
- **Chip microcopy:** comma separator inside "INFERRED, PATTERN" / "INFERRED, VOICEMAIL" vs. "·" used elsewhere; pick one.
- **Header icon buttons:** clipboard icon is ambiguous (copy? paste? records?); no tooltip/label visible.
- **Card 1 ADDRESS:** "Biggs C" reads as a truncated street type ("Biggs Ct").
- **Aetna APPEALS FAX "+1-500-…"**: invalid-looking NANP area code; even for demo data it undermines the tool's credibility with phone-savvy users.
- **In-card hierarchy:** card titles only ~1px larger than metadata; hierarchy rides on weight alone at small sizes.
- **Sage used for both primary accent and YOU CONFIRMED status chips** — status borrows the action color; slight semantic crowding.

Verdict: calm, on-system, well-built surface; the two edge-clipping bugs and the legend/chip mismatch are the must-fixes before ship.
