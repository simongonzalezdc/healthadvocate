judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/mobile-help.png)

I can see the image — full audit below.

## Description

**Layout, top-to-bottom (mobile, ~375–412pt, light mode):**
1. **App bar** (white): sage rounded-square heart logo tile → bold "HealthAdvocate" wordmark → ochre stadium status badge ("• 1 due soon", wrapped to two lines) → circular home button → circular sun/theme button.
2. **Tab row**: Scanner / Family / Tracks / Coverage / Help; "Help" active as a sage-tint pill with sage text; hairline rule beneath.
3. **Body** on warm paper ground: one large white rounded card containing — sage caps kicker "HELP & REAL HUMANS" + intro paragraph; caps label "CRISIS SUPPORT (US)" + two bullets (988 Lifeline, SAMHSA Helpline, bold names/numbers); caps label "FIND HELP WITH COVERAGE AND CARE" + two sage link bullets + one plain-bold bullet; caps label "HOW HEALTHADVOCATE REPORTS ITSELF" + long honesty paragraph.
4. **Footer** below a full-width hairline: small gray disclaimer paragraph with inline bold "HealthAdvocate", center-aligned.

**Palette as named hues:** paper/ivory ground, white card, sage accent (logo, active tab, links, kicker), ochre caution on the "due soon" badge, near-black ink. No coral present (nothing danger-semantic on screen), no slate info treatment.

**Typography scale:** ~3 restrained steps — bold ~21px wordmark; ~15px letter-spaced caps section labels; ~17px/1.6 body; ~14–15px footer gray. Consistent.

**Spacing rhythm:** calm and generous; ~40–48px between sections, roomy card padding, even rhythm.

**Component quality:** pills/circles/card cleanly rounded, bullet hanging indents correct, hairline borders subtle — high craft overall, except one broken component (the badge).

## Defects

1. **P0 — Header status badge (top center):** "due soon" wraps to a second line ("• 1 due" / "soon"), inflating the stadium into a tall egg that overpowers the wordmark and breaks the bar's baseline alignment. Force one line (nowrap + truncation or shorter copy).
2. **P1 — "CRISIS SUPPORT (US)", bullet 2:** the SAMHSA number breaks mid-figure across lines — "1-800-662-" / "4357" — and "1-800-662-HELP" also splits. The page's most safety-critical string must never break; non-breaking hyphens / nowrap on numbers.
3. **P1 — Same section:** crisis numbers (988, 1-800-…) render as plain bold body while the two coverage resources are sage links — no tappable affordance on phone numbers on the one screen whose job is reaching humans. Make them `tel:`/`sms:` links in the accent style; this is also the view's missing primary action.
4. **P2 — Card section labels:** kicker "HELP & REAL HUMANS" is sage; the other three labels are charcoal at identical size/weight/tracking. Reads as inconsistency, not hierarchy — unify color or add a second differentiator.
5. **P2 — Links under "FIND HELP…":** color-only affordance (no underline), and sage-on-white at body size is likely near the AA floor — verify ≥4.5:1 and add an underline cue for a low-vision, stressed audience.
6. **P2 — Footer disclaimer:** center-aligned while every other paragraph is left-aligned; inline bold makes staggered ragged edges. Set left.
7. **P2 — Left gutters disagree:** header logo (~28px), tab row (~18px), card (~36px). Pick one page gutter.
8. **P2 — Card bottom:** ~2 lines of trailing dead space after the last paragraph; trim to balance the block.
9. **P2 — System conformance:** the card reads as a single hairline bezel — the committed double-bezel treatment isn't discernible at this size; confirm the inner stroke isn't being lost. Ochre badge text on cream also warrants a contrast check.

**Held well:** honest "how it reports itself" disclosure (real trust content for this audience), ochre=caution used correctly for "due soon", one-accent discipline, restrained scale, calm spacing.
