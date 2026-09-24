judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-symptoms.png)

I can see the image (620×430 screenshot of the Symptoms view in a dark rendering). Audit below.

## What I see, top to bottom

- **App bar (y 0–32):** sage rounded-square logo chip + white "HealthAdvocate" wordmark left; right side an ochre pill "🔔 1 reminder due soon" plus two dark circular icon buttons (bell, profile).
- **Nav row (y 32–58):** ten text tabs — Symptoms (active, sage pill + underline), Documents, Bills, Insurance, Drugs, Appointments, Discharge, 2nd Opinion, Recorder, Library — and an eleventh item clipped at the right viewport edge.
- **Workbench panel (y ~60–300, ~70% width, centered):** dark card with thin hairline bezel; sage icon chip (pulse glyph); H1 "Symptom Assessment"; two-line muted subtitle; letterspaced caps eyebrow "WHAT ARE YOU EXPERIENCING?"; large single-bezel textarea with an example placeholder ("chest pain…"); sage pill button "Assess Symptoms" at the textarea's left edge.
- **Footer (y ~335–360):** two-line centered, very small, low-contrast disclaimer ("support, not replace… Your information stays on your device"). Dead dark band below it to the bottom edge.

**Palette as named hues:** background is warm near-black charcoal, not warm paper cream — the paper is inverted. Sage is present (logo, active tab, icon chip, CTA), ochre on the reminder badge; coral and slate absent (no occasion for them). Text is off-white + mid-gray. Warmth survives; the "paper" does not.

**Type:** one sans family; steps are caps-eyebrow (~8px) → title (~14px semibold) → body (~9–10px) → footer (~8px). Hierarchy exists but the range is compressed — nav and body sit close in size.

**Spacing:** generous outer margins and panel padding, consistent left alignment of label/textarea/CTA; bottom third of the page is loosely composed.

**Component quality:** pills, chip, and bezel radii are consistent; CTA uses dark-on-sage with good contrast; no broken controls other than the nav clip.

## Defects

- **P0 — Nav, far-right edge (x≈520–528, y≈45):** eleventh nav item is clipped mid-glyph by the viewport edge. Overflow unhandled; broken.
- **P1 — Global:** entire view renders as dark charcoal despite the committed "warm paper neutrals" light system. Either this theme is off-system or dark tokens were never derived — none of the paper/coral/slate hierarchy is visible. This is the headline deviation.
- **P1 — Nav row (y 40–52):** ten ~9px tabs with tight gutters, no grouping or overflow menu. For sick, overwhelmed users this is a scanning wall; the clipped 11th item is the symptom.
- **P1 — Footer (y 338–358):** the medical disclaimer — the most safety-critical text on the page — is the smallest, lowest-contrast text on the page. Contrast looks below ~4.5:1 at this size.
- **P2 — Active tab "Symptoms" (y 38–54):** double active indicator — sage pill *and* underline. Pick one.
- **P2 — Accent budget:** sage fills four roles (logo, active pill, icon chip, primary CTA). The icon chip and active pill compete with the single sanctioned primary action; neutralize one.
- **P2 — Workbench panel (y 60–300):** the committed double bezel is not discernible — reads as one hairline; inner/outer bezel contrast is too low in this theme.
- **P2 — Page bottom (y 360–430):** footer floats mid-air above a dead band; anchor to viewport bottom or let the panel breathe into the space.
- **P2 — Header right (y 10–25):** ochre "reminder due soon" pill is the highest-salience element in the chrome; defensible as caution, but it has no visible resolve affordance and tugs against the one-primary-action rule.

One genuine positive worth keeping: exactly one filled sage CTA in the workbench, correctly aligned to the textarea's left edge — the one-primary-action rule holds inside the panel.
