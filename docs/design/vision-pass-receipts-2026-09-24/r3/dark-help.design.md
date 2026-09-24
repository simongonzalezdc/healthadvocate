judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-help.png)

**What I see**

- **Layout, top-to-bottom:** Two stacked dark bars — app header (sage shield-heart logo + "HealthAdvocate" wordmark left; ochre "1 reminder due soon" pill and two small icon buttons right) — then a secondary nav strip (≈11 items: "…stiments" [clipped], Discharge, 2nd Opinion, Recorder, Library, Directory, Scanner, Family, Tracks, Coverage, and a sage-filled active "Help" pill far right). Below, one raised double-bezel panel holds all content: H1 "Help & Real Humans", intro paragraph, small-caps numbered sections — "1. CRISIS SUPPORT (US)" with a coral-bordered crisis card (988 + SAMHSA lines), "2. FIND HELP WITH COVERAGE AND CARE" with three sage links, "3. HOW HEALTHADVOCATE REPORTS ITSELF" with a long explanation paragraph. Centered dim footer disclaimer outside the panel.
- **Palette:** Warm near-black charcoal page; slightly lighter warm-charcoal panel; sage-green on logo, active pill, and links; coral correctly reserved for the crisis card (border, tint, phone numbers); ochre on the reminder chip; warm off-white headings, muted warm-gray secondary text. Consistent with an inverted "warm paper" ramp, though warmth is faint at these depths.
- **Type scale:** Clear four-step hierarchy — H1 ≈ 2× body, micro tracked small-caps section labels, body ~14px-equivalent, oversized coral "988" as emphasis. Sans throughout.
- **Spacing rhythm:** Generous, calm section separation inside the panel; crisis card padding generous; nav strip is the exception — cramped.
- **Component quality:** Crisis card is the single unmistakable primary element (good "one primary action"); pill/border radii consistent; hairline dividers clean; coral=danger and sage=advocate semantics respected.

**Defects**

1. **P0 — Top nav, leftmost item:** label clipped to "…stiments" at the viewport's left edge; it starts left of the logo margin, so the strip overflows and a destination is illegible.
2. **P1 — Intro paragraph (under H1):** dangling copy — "Their widely published US resources point to real people" has no antecedent ("Their" of what?). Reads like a botched sentence merge; trust-damaging on the page whose job is trust.
3. **P1 — Secondary nav strip (top):** ~11 undifferentiated items at tight spacing for sick, overwhelmed users — flat hierarchy, no grouping, and the crowding is what caused defect #1.
4. **P1 — Footer disclaimer (bottom center):** the safety line ("Always consult a qualified healthcare provider…") and privacy claim ("Your information stays on your device") are the smallest, lowest-contrast text on the page. Safety/privacy content should not have the weakest emphasis.
5. **P2 — Bulleted list, item 3 (section 2):** "Patient Advocate / Patient Relations" switches to bold-white while the two items above are sage links — inconsistent affordance; looks like a link that lost its color.
6. **P2 — Section 3 paragraph + intro:** measure runs very long (~90–100 chars) in muted gray — dense reading blocks for the target audience; narrower column or larger type needed.
7. **P2 — Header, right icon pair (keyboard, theme):** tiny hit targets, low-contrast borders, unclear affordance next to the reminder pill.
8. **P2 — Dark surfaces overall:** panels read neutral charcoal-brown; the "warm paper" warmth barely survives inversion — acceptable variant, but the tint could be nudged warmer to stay on-system.
9. **P2 — Footer:** centered alignment is the only centered block on the page, with a widowed second line.

**Verdict:** Structure and color semantics are on-system and the crisis block is exemplary; the P0 nav clipping plus the P1 copy defect and disclaimer contrast are what block sign-off.
