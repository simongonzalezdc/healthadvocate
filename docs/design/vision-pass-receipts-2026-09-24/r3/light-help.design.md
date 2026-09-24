judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/light-help.png)

I can see the image — auditing it now.

## Description

**Layout, top to bottom:** White header strip (sage logo tile + "HealthAdvocate" wordmark left; ochre "1 reminder due soon" pill + calendar and sun icon buttons right). Below it, a single-row horizontal nav of ~11 items ("…ointments", Discharge, 2nd Opinion, Recorder, Library, Directory, Scanner, Family, Tracks, Coverage) ending in a sage-tinted active "Help" pill. Main area: one large white double-bezel card on warm paper, containing an H1 "Help & Real Humans", a muted intro paragraph, three uppercase numbered section labels, a coral double-bezel crisis panel with two hotline rows, a sage-link bullet list, and a long self-reporting paragraph. Hairline divider, then a centered two-line footer disclaimer on paper.

**Palette:** Warm paper background (~#FAF7F2), white panels, ink/slate body text, sage for logo/active pill/links, coral for crisis panel border+fill and hotline numbers, ochre for the reminder pill. System hues are applied semantically where it counts — crisis is the only coral surface.

**Typography:** Single sans family. H1 is barely larger than body; section labels are tiny letterspaced uppercase; body ~12–13px at this render; footer smallest. Scale is compressed — five levels but little size separation.

**Spacing/components:** Generous, calm card padding; consistent double bezels on card and crisis panel; even bullet/section rhythm. Components are cleanly built; nothing looks unstyled.

## Defects

1. **P0 — Nav, far left:** First nav item is clipped mid-word to "…ointments" at the viewport edge, with no visible scroll affordance, fade, or overflow menu. A destination is unreadable/unreachable — reads as broken, not intentional.
2. **P1 — Nav, full row:** 11 undifferentiated top-level items with tight gaps; no grouping or priority. Root cause of the P0 clip and hard to scan for an overwhelmed user.
3. **P1 — Section 2, third bullet:** "Patient Advocate / Patient Relations" set in coral. Danger hue used for a routine referral link directly under the real crisis panel — semantic misuse that dilutes coral=danger.
4. **P1 — Whole page:** Type scale too flat — H1 ≈ body size, so the page has no asserted hierarchy; combined with ~12px body and muted grays, it under-serves low-vision/stressed readers.
5. **P1 — Under H1:** The honesty statement ("…never contacts anyone on your behalf") — the page's key trust claim — is the most de-emphasized text on the page (muted gray, smallest-but-one). Hierarchy contradicts importance.
6. **P2 — Coral panel, second row:** "…24/7 treatment referral)." runs nearly to the right bezel; right padding visibly tighter than left.
7. **P2 — Section 2 bullets:** Links distinguished by sage hue alone, no underline; hue also matches the active-nav accent, so link affordance is weak and color-dependent.
8. **P2 — Header right:** Calendar and sun icon buttons are unlabeled and crowd the ochre pill; purpose (reminders? theme?) is guessable only.
9. **P2 — Nav item "2nd Opinion":** numeral-vs-word naming inconsistent with the rest of the row's single words.
10. **P2 — Footer:** Centered alignment breaks the page's left-aligned rhythm, and it packs three unrelated claims (support-not-replace, consult a provider, data stays local) into one block.
11. **P2 — Bottom of viewport:** Large empty paper band between card and footer on a short page — reads as missing content rather than calm spacing.
12. **P2 — Header logo:** Icon-in-badge-in-tile nesting is cramped at render size; the heart glyph nearly fills its dark chip.

**What's working:** coral reserved for the crisis panel, sage active state, double bezels, and one-action-per-view discipline (no competing CTA on an info page) all match the committed system.
