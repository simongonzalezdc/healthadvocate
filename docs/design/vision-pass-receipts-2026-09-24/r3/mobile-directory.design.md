judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/mobile-directory.png)

I can see the image clearly. Audit below.

## DESCRIPTION

**Layout, top-to-bottom:** Warm cream app bar (heart logo lockup left; alert pill "1", home icon, theme toggle right) → scrollable tab strip (2nd Opinion / Recorder / Library / **Directory** active in sage pill / fifth tab clipped at right edge) → double-bezel hero panel: "Directory" H1 over a narrow intro paragraph, flanked by a floating avatar icon (left) and dashed DEMO DATA badge (right) → search input → filter chips wrapping to 3 rows (All · Doctors · Labs / Imaging · Therapy · Pharmacy / Insurers) → legend block ("The app fills these for you…" + chips FROM A CALL, INFERRED, YOU CONFIRMED ✓) → four double-bezel provider cards (Dr. Maya Patel, Riverside Imaging, Aetna member services, Corner Pharmacy), each with icon + name + category label, "Merged from N sources" provenance line, labeled field rows (smallcaps label / value / source chip, some with quiet "Confirm"), footer pill-buttons [Call] [Items in Library] → small-print disclaimer.

**Palette:** Paper-cream ground and warmer off-white panels; sage-green = brand, active tab/chip, confirmed chips; slate-blue = directly captured sources (BILL DECODE, VOICEMAIL, DOCUMENT, CALL); ochre dashed = inferred; coral appears only as the header alert dot; near-black ink text. System-faithful.

**Typography:** Humanist sans throughout. H1 ~20 semibold; card titles ~16 semibold; body ~14; field labels ~10–11 uppercase letterspaced. Two-level label system reads cleanly.

**Spacing/components:** Generous, mostly regular section rhythm; consistent card padding and pill radii; double bezel visible on every workbench panel. Component quality is good except the hero composition and intra-card chip alignment.

## DEFECTS

1. **P0 — Dr. Maya Patel card, chip rows:** three different left edges for the same element class — YOU CONFIRMED flush left, BILL DECODE + Confirm indented ~20px, INFERRED · PATTERN indented further with Confirm wrapping to a second line. Progressive drift, no alignment parent.
2. **P1 — Hero panel:** intro paragraph squeezed to ~55% width by the floating avatar icon and DEMO DATA badge; wraps 2–4 words/line over ~13 lines. Worst composition on the screen.
3. **P1 — Hero copy typos:** "pharmacys," "insures." Trust-breaking in a medical tool for vulnerable users.
4. **P1 — Search field:** placeholder clipped mid-word at right edge ("…phone n"), no ellipsis.
5. **P1 — Category label placement inconsistent across cards:** under-name left ("DOCTOR · ORTHOPEDICS", "IMAGING CENTER") vs top-right ("INSURER", "PHARMACY"). Same element, two positions.
6. **P2 — Header:** coral dot used for a generic "1" notification; coral is reserved for danger in this system.
7. **P2 — Legend vs cards:** legend teaches generic chips ("FROM A CALL") that never appear in the cards; actual chips are VOICEMAIL / BILL DECODE / DOCUMENT / LETTER variants. Vocabulary mismatch hurts learnability.
8. **P2 — Legend sentence:** trailing sentence starts lowercase inline after the YOU CONFIRMED chip, reading as chip continuation ("…YOU CONFIRMED ✓ confirmed information always wins…").
9. **P2 — Tab strip:** fifth tab clipped to a letter sliver ("S") with no fade or scroll affordance.
10. **P2 — DEMO DATA badge:** dashed border is the established "inferred/unverified" tell; using it for demo mode collides with chip semantics.
11. **P2 — Card naming:** "Aetna member services" sentence-case vs Title Case siblings; also the only real brand amid fictionalized data (.example emails).
12. **P2 — Confirm affordance:** bare text, no border, yet it's the corrective action the hero copy leans on ("Nothing to type unless you're correcting something"). Borderline-intentional per calm system, but it's the quietest element doing the most important job.
13. **P2 — Riverside hours:** 24-hour format ("7:00–19:00") inside otherwise US-context data (Portland OR, US phone format).

Net: strong system adherence in palette, chips, and panel construction; the hero block is the failure zone (measure, copy, ornament placement), plus one real alignment bug in the Patel card.
