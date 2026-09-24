judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-appointments.png)

I can see the image. Audit follows.

## Description

**Layout, top-to-bottom:** (1) Header bar — sage logo tile + "HealthAdvocate" wordmark left; coral "● 1 reminder due soon" pill plus two circular icon buttons (help, dark-mode moon) right. (2) Tab nav row — Symptoms → Library, with "Appointments" active as a sage-outlined pill; a partial element is clipped at the right viewport edge. (3) Content card "Appointment Prep" — icon tile + heading + subtext, two labeled fields (textarea, then single input), one filled sage "Prepare" button. (4) Hairline divider, then centered two-line disclaimer footer. Full page visible, header to footer.

**Palette as named hues:** warm near-black brown page ground; umber panel; sage green on logo, active tab, icon tile; **mint** (not sage) on the button; coral on the reminder badge; muted warm-gray labels/placeholders; off-white headings/body. Dark-mode execution of the paper system — coherent warm cast, sanctioned by the moon toggle.

**Typography:** wordmark ~14 bold; heading ~17 semibold; body ~13; nav ~12; uppercase micro-labels ~10–11 tracked; footer ~11. Compressed scale, muted labels are the smallest text on the page.

**Spacing:** calm and generous — ~24px card padding, clear grouping between label/field pairs, large page margins. Best-in-view attribute.

**Component quality:** inputs clean 1px-border rounded rects; single primary action (✓ one-per-view); restrained chrome. Radio silence on motion, appropriately.

## Defects

**P0**
- **Nav row, far right:** last tab/chevron after "Library" is clipped by the viewport edge — unreachable control, no scroll affordance. Header content above ends ~90px short of the edge, so this is real container overflow, not a crop.

**P1**
- **Header top-right, badge:** "1 reminder due soon" is coral — a caution-grade message on the danger channel. System says ochre=caution; this erodes coral's meaning.
- **Card, both field labels:** inverted hierarchy — labels ("YOUR SYMPTOMS…", "SPECIFIC CONCERN…") are the smallest, dimdest text on the page while their placeholders render brighter. Borderline contrast on dark ground for a fatigued/low-vision audience.
- **Card, whole view:** "Appointments" tab shows a prep form with zero appointment context — no date, provider, or which-visit indicator. Users can't tell what they're prepping for.
- **Card, "Prepare" button:** hue drift — bright mint, not the committed sage; reads techy against the warm-brown field and doesn't match the logo/active-tab green. Two greens in one view.

**P2**
- **Content card:** single bezel only — the committed double-bezel workbench construction is absent.
- **Page columns:** nav row, card, and footer divider each terminate at different x-positions (card inset ~10px inside the divider; nav overshooting both) — reads unaligned down the left edge.
- **Header, two circular icon buttons:** fill/border barely above background — near-invisible affordance.
- **Radius scale:** pill button and nav pill vs ~8px inputs vs ~12px card — three radii, no system.
- **Type floor:** 10–11px micro-labels and ~11px footer are below a comfortable floor for this audience; scale overall is compressed.

Verdict: strong calm structure and spacing; blocked on the clipped nav item (P0), and the label hierarchy + mint-button hue are the two fixes with the most perceptible payoff.
