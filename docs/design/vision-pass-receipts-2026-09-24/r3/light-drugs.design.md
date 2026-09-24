judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/light-drugs.png)

**DESCRIPTION**

Layout, top-to-bottom: (1) brand bar — sage rounded-square heart logomark + "HealthAdvocate" wordmark left; right cluster = ochre pill badge "🔔 1 reminder due soon", circular bell icon button, circular sun/theme button. (2) Nav bar — 10 flat text tabs (Symptoms, Documents, Bills, Insurance, **Drugs** as sage-filled pill with white text, Appointments, Discharge, 2nd Opinion, Recorder, Library) ending in a tiny right-chevron overflow glyph at the far edge. (3) One centered white double-bezel card (~66% width): header row of sage-tinted icon tile + "Drug Checker" title + one-line gray subtitle, full-bleed hairline divider, then form block — tiny letterspaced caps label "DRUG NAME", full-width flat-tint input with gray placeholder "e.g., Lipitor, Zoloft, Advil", sage filled "Check Drug" button, left-aligned. (4) Full-width hairline rule + two-line small gray centered disclaimer, then ~40% of the viewport is empty paper.

Palette: warm paper/ivory page, white panels, sage-green = brand/active/primary, ochre = reminder badge, ink-dark primary text, mid-gray secondary. No coral anywhere (correct — nothing is dangerous here). On-system.

Typography: compressed but consistent scale — title ≈18px semibold, subtitle/body ≈12px, caps micro-label ≈10px. Spacing: generous outer margins, calm card padding; internal form rhythm tighter than exterior.

**DEFECTS**

P0: none — nothing broken, illegible, or dishonest at this size.

- **P1 — Nav overflow truncation.** Far right of nav bar (~y45): the chevron `▸` sits clipped at the viewport edge; ≥1 section is hidden behind an affordance that's ~10px and near-invisible. For the target user (sick, overwhelmed), hiding destinations with no scroll cue is a wayfinding failure.
- **P1 — Nav density/legibility.** Same bar: 10 labels at ~11px with tight gaps; tap/click targets are thin text, not padded zones. Violates the "generous calm" system where it matters most.
- **P1 — Input affordance too weak.** Form block (~y165–190): the field renders as a flat tint with a barely-there border — it reads as a disabled strip, and the placeholder is low-contrast. This is the view's core task input; it should be the most obviously interactive element after the button.
- **P1 — Footer floats mid-canvas.** Rule at ~y262, disclaimer ~y285–300, then ~140px of dead paper to the fold. Reads as an unpinned footer / unfinished page, and the empty band outweighs the content. Pin to viewport bottom, or fill the calm space with an empty-state hint (example drugs, "how this works").
- **P2 — Ochre badge semantic dilution.** Header right: routine reminder dressed in the system's caution hue trains users to discount ochre for real warnings (alarm fatigue). Consider a neutral/sage info treatment; also the badge bell + adjacent bell button are redundant glyphs.
- **P2 — Primary-action weight competition.** "Drugs" pill and "Check Drug" button are both saturated sage fills of similar size; the active-tab state nearly matches the primary action's weight. Keep nav active state as tint-outline or darker sage.
- **P2 — White-on-sage contrast.** "Drugs" pill text (and to a lesser degree the button label) looks near 3:1 — risky for ~11px text; verify ≥4.5:1.
- **P2 — Icon semantics.** Card header tile uses a document/page glyph for "Drug Checker" — a pill/capsule or scan glyph matches the task.
- **P2 — Internal rhythm.** Divider→"DRUG NAME" gap (~y148–158) is tighter than header→divider; the form block feels cramped against the airy card padding. Normalize to the spacing scale.
- **P2 — Secondary text size.** Card subtitle and footer disclaimer are small mid-gray on white; confirm 4.5:1 at shipped size given the audience.

Verdict: calm, on-system, honest single-primary-action view — but fix the truncated nav, invisible input affordance, and floating footer before ship.
