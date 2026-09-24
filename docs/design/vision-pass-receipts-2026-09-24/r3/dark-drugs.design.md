judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-drugs.png)

DESCRIBE

- **Layout, top to bottom:** (1) slim top app bar — sage logo chip + "HealthAdvocate" wordmark left; ochre pill badge "1 reminder due soon" + two circular icon buttons right. (2) Full-width secondary nav with 10 items (Symptoms … Library), "Drugs" active as a sage outline pill; a faint glyph is clipped at the far-right edge. (3) Centered single-column double-bezel panel (~60% width): sage icon chip, "Drug Checker" H1, one-line subtitle, tracked-caps "DRUG NAME" label, text input with placeholder "e.g., Lipitor, Zoloft, Advair", sage "Check Drug" primary button. (4) Full-width hairline. (5) Centered two-line legal disclaimer. (6) Bottom ~40% of the viewport is empty black.
- **Palette as rendered:** page is cool neutral charcoal (near-black #111–#1a), panel a slightly lighter charcoal, dark grey hairlines; sage-green carries logo chip, active nav pill, and primary button; one ochre/amber badge; text in white/grey tints. No paper neutrals, no coral, no slate anywhere.
- **Typography:** all sans, small scale — brand ~15px bold, nav ~12px, panel title ~20px bold, subtitle/placeholder ~13px, label ~10px caps, body ~12px.
- **Spacing/components:** panel padding and label→input→button rhythm are generous and calm; consistent rounded radii; double-bezel (outer border + inset content) is present; exactly one filled primary action. Header and nav rows are comparatively tight.

DEFECTS

1. **P0 — Off-system palette, global.** The committed system is "warm paper clinic"; this renders as cool neutral charcoal. Even if a dark variant is sanctioned, it fails "warm" — no warm undertone in the blacks, no paper hue anywhere. System-breaking as shown.
2. **P0 — Clipped control, nav far-right edge (x≈615, y≈45).** A glyph is cut off at the viewport edge — a truncated overflow affordance or icon. 10 items overflow the row and the cue is a sliver.
3. **P1 — Nav scannability, full nav row.** 10 equal-weight items at ~12px in one row; the sage outline on "Drugs" is too weak a signal against 9 muted siblings. Sick, overwhelmed users need stronger wayfinding.
4. **P1 — Vertical balance, below the disclaimer.** Content ends ~60% down; the remaining viewport is dead black. The panel floats high and the page reads unfinished rather than calm.
5. **P1 — Placeholder contrast, input (panel mid).** "e.g., Lipitor, Zoloft, Advair" is low-contrast grey on a dark field (~3:1), borderline illegible for the exact audience this tool serves.
6. **P2 — Alignment conflict, footer vs panel.** Disclaimer is centered while all panel content is left-aligned — two alignment systems on one page.
7. **P2 — Header density, top bars.** App bar and nav are tight and shallow against the "generous calm spacing" commitment; the badge and icon buttons nearly touch on the right.
8. **P2 — Accent competition, header right.** The ochre badge is the highest-chroma element on screen, pulling the eye before the sage primary action — caution color outranks the task.
9. **P2 — Naming drift.** Nav says "Drugs", panel says "Drug Checker"; pick one.

Compliant: single primary action, one ochre caution state, double-bezel panel, restrained flat surfaces, consistent radii, working disclaimer with privacy line.
