judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/mobile-help.png)

I can see the image clearly. Audit below.

## Describe

**Layout (top-to-bottom):** Fixed header — sage rounded-square heart logo + "HealthAdvocate" wordmark left; ochre-dot notification pill "• 1", house icon button, sun/theme button right. Below: 5-tab nav (Scanner, Family, Tracks, Coverage, Help) with "Help" as an active sage-tinted pill. Body: one large white paper card on cream — H1 "Help & Real Humans", intro paragraph, small-caps section label, coral crisis callout card (988 + SAMHSA entries), second label + 3-item bullet list (two sage links, one bold non-link), third label + ~15-line paragraph, then a darker-cream footer band with small disclaimer text.

**Palette as named hues:** Warm paper neutrals (cream canvas, white card, darker cream footer band) ✓. Sage = logo, active tab, section labels, links ✓. Coral = crisis callout border/tint and phone numerals — semantically correct danger usage ✓. Ochre = notification badge dot/pill ✓. Slate = absent on this view (fine).

**Typography scale:** ~26px bold H1 → 17px/1.6 body → 12–13px letterspaced sage small caps → ~24px bold coral numerals inline → 13px footer. Coherent ramp; oversized crisis numbers are a good emphasis pattern.

**Spacing rhythm:** Generous, even — ~24–28px card padding, ~60–80px section gaps, calm vertical flow. Matches "warm paper clinic."

**Component quality:** Double-bezel reads correctly on crisis card (outer coral ring + inner offset) and active tab pill. Header buttons consistent rounded squares. Build quality generally high — the failures are in content rendering, not chrome.

## Defects

- **P0 — Ordered-list counters broken: all three section labels render "1."** ("1. CRISIS SUPPORT (US)", "1. FIND HELP WITH COVERAGE AND CARE", "1. HOW HEALTHADVOCATE REPORTS ITSELF"). Markdown `1.` headings rendered literally / counter never increments. Also a double-wide gap after "1." in each. Most visible bug on the page.
- **P0 — SAMHSA vanity number split mid-number across lines:** "(1-800-" orphaned at line end, "662-HELP;" wraps — crisis callout card, SAMHSA block, mid-page. Critical actionable info breaking across a line wrap; needs `white-space: nowrap` / non-breaking hyphens.
- **P1 — Crisis numbers have no tap-to-call affordance.** "988" and "1-800-662-4357" are styled as bold text, not links (compare: the two coverage links are visibly sage/interactive). On mobile, dialing is the entire point — make them `tel:` links.
- **P1 — 15-line unbroken wall of text** in "How HealthAdvocate reports itself" (lower half of card). Densest, most important honesty content is the least scannable surface for the product's stated audience (sick, overwhelmed people). Break into 3–4 bullets.
- **P2 — Bullet list has no hanging indent:** wrapped lines ("HealthCare.gov navigator finder", "lookup", "Patient Advocate / Patient Relations office.") return flush to the bullet-marker column instead of the text edge — coverage list, mid-page.
- **P2 — Unexplained ochre "• 1" badge** (header right). Caution-hued alert count with no label or destination cue — anxiety-inducing for this audience; label it or tie it to a named alert.
- **P2 — Sage doubles as decorative (section labels) and interactive (links)** with no underline on links — color-only affordance, and it dilutes sage's "primary action" meaning. Underline links or reserve label tint.
- **P2 — Sage small-caps labels on cream look sub-4.5:1** at 12–13px letterspaced caps — check contrast (three labels down the left column).

**Verdict:** Structure and palette are on-system and calm; ship-blockers are the broken list numbering and the split phone number — both are content-rendering bugs, fixable in the markdown/typography layer, not the design.
