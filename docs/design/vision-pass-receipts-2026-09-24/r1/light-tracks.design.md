judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-tracks.png)

Can see the image. Audit follows.

## Description (top to bottom)

- **Header bar** (white): sage rounded-square heart logo + bold slate "HealthAdvocate" wordmark left; right side an ochre pill "# 1 due soon" plus two circular ghost icon buttons (bell, sun/theme toggle).
- **Nav row** below header: 11 items in one strip — `tients` (clipped), Discharge, 2nd Opinion, Recorder, Library, Directory, Scanner, Family, Tracks (active, sage tint pill), Coverage, Help.
- **Body** (warm paper background): one centered white panel, hairline border + soft shadow (double-bezel reads correctly). Inside: small sage icon tile, letterspaced caps eyebrow "HEALTH TRACKS", gray subtitle, then the task row — text input (placeholder "What are you tracking?"), a "General" select, dark-sage "Start Track" button. Centered empty state: circled "!" glyph + gray caption. Large empty region below.
- **Footer**: hairline rule, two-line centered gray disclaimer with bold "HealthAdvocate".
- **Palette adherence**: warm neutrals + sage for identity/primary, ochre for the due-badge, slate ink text, no coral (no danger state present). One primary action per view: satisfied.
- **Type**: compressed scale — wordmark ~14px bold; nav, eyebrow, subtitle, placeholder, caption, footer all cluster ~10–11px.
- **Spacing**: header/nav tight (~14px gaps); card padding generous top, excessive bottom.

## Defects

- **P0 — Nav row, leftmost item**: renders as mid-word fragment "tients" (presumably "Patients"). Primary navigation illegible at rest — clipped with no scroll affordance.
- **P1 — Nav row, overall**: 11 destinations crammed into one horizontally overflowing strip; left edge already cut, "Help" abuts the right viewport edge. Wayfinding is unusable at this width.
- **P1 — Header right badge**: "# 1 due soon" — stray gap between "#" and "1", cryptic phrasing; user can't tell what is due or why ochre/caution applies.
- **P1 — Form row**: placeholder-only input plus an unlabeled "General" select — no persistent labels on the view's single task; a11y and first-run clarity fail.
- **P2 — Card interior**: empty state floats mid-card with ~80px dead space beneath; bottom padding ≈3× top — vertical rhythm unbalanced.
- **P2 — Card body text**: subtitle, empty-state caption, and footer disclaimer are small low-contrast gray on white/paper — near or below WCAG floor at this size.
- **P2 — Form row select**: native OS chrome (raw field, black chevron) next to custom-styled input and button — component-quality mismatch in the primary row.
- **P2 — Empty-state icon**: exclamation-in-circle glyph reads as an error alert on a neutral, expected state — off-tone for the calm system.
- **P2 — Type scale**: eyebrow, subtitle, caption, and footer all sit within ~1–2px of each other; subtitle vs. caption hierarchy barely distinguishable.
- **P2 — Footer**: rule and disclaimer run wider than the card column above — two competing container widths on one page.

System conformance is otherwise solid: paper neutrals, sage reserved for primary action + active state, honest empty state, single primary button.
