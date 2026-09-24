I can see the image — dark-mode Appointments view, 2000×~1400. Audit follows.

## What I see

**Layout, top to bottom:** Header bar — sage heart-logo tile + "HealthAdvocate" wordmark left; right cluster: ochre-dot pill "1 due soon", home icon button, moon (theme) button. Below: 10-item text nav (Symptoms → Library) with hairline under; "Appointments" active in sage with faint green pill. Main: one full-width rounded panel — calendar icon tile, sage letterspaced eyebrow "APPOINTMENT PREP", two-line gray description, then a form: caps label + tall textarea, caps label + single-line input, sage pill button "Prepare" (only primary on the page ✓). Hairline divider, then centered two-line disclaimer with bolded "HealthAdvocate".

**Palette (named hues):** near-black neutral-gray canvas; slightly elevated dark-gray panel; off-white foreground, mid-gray secondary; sage green on logo tile, active nav, eyebrow, icon, and Prepare (sage correctly reserved for primary ✓); ochre on the due-soon dot/text ✓; no coral or slate present. Dark surfaces read cool-neutral, not warm.

**Type scale:** ~20px bold wordmark; ~16px nav; ~13px letterspaced caps eyebrow and field labels; ~16–17px body/placeholders; ~17px semibold button; ~15px footer. Scale is quiet and consistent; caps+tracking used consistently for microcopy.

**Spacing rhythm:** generous and calm throughout — large nav→card gap, ~95px card padding, consistent label→field gaps. Component quality: pill radii consistent with logo tile; fields have subtle borders and matching radii; button is a proper 56px touch target with dark-on-sage text.

## Defects

- **P1 — Header right, "1 due soon" badge:** the page's only urgent signal. The Appointments view shows no appointment list, date, or link target — the promised due item has no visible destination or content. Users can't act on the one time-critical thing.
- **P1 — Card body, symptoms textarea:** spans full panel width (~1150px ≈ 140+ chars/line). Measure far past readable range on the primary typing surface; constrain to ~65–75ch, left-align with breathing room.
- **P1 — Page hierarchy:** no H1. The strongest on-page title is a 13px eyebrow; 16px nav items out-rank the page's own heading. Flat hierarchy hurts orientation for overwhelmed users.
- **P2 — Footer divider:** spans wider than the card and content column (~50px past each edge) — inconsistent gutters; should match content width.
- **P2 — Header right, icon buttons:** home button duplicates the nav and is ambiguous (first tab is Symptoms, not "home"); moon toggle doesn't communicate current vs. target theme state.
- **P2 — Header right, badge grouping:** "1 due soon" chip sits at the same 12px gap as the icon buttons — a status reads as a button; separate by role (larger gap or divider).
- **P2 — Card bottom:** ~80px dead space below Prepare vs. ~95px above the icon block — panel reads slightly unfinished; tighten bottom or balance padding.
- **P2 — Palette fidelity:** dark surfaces are cool gray with no warm undertone — "warm paper" survives only via accents; the identity thins out in dark mode.
- **P2 — Primary button copy:** "Prepare" is vague about the outcome (prepare *what*?); e.g. "Prepare my visit" suits anxious users scanning for consequences.

No P0s: nothing illegible, dishonest, or broken; alignment of icon/labels/fields/button on a single left edge is clean.
