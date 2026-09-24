judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/light-appointments.png)

Note: the attached path `judge-img/r2/light-appointments.jpg` doesn't exist (`r2` is a file, not a directory); the screenshot lives at `/tmp/ha-ds-shots/judge-img/r1/light-appointments.jpg`, which is what I judged.

## What I see

**Layout, top-to-bottom:** White header bar — sage rounded-square heart logo + "HealthAdvocate" wordmark left; coral-outlined pill badge "# 1 due soon" plus two circular icon buttons (keyboard, moon) right. Below, a centered single-row nav: Symptoms · Documents · Bills · Insurance · Drugs · **Appointments** (active, soft sage pill) · Discharge · 2nd Opinion · Recorder · Library. Main area: warm paper background with one centered white card — calendar glyph in a light tile, small-caps "APPOINTMENT PREP", one-line description, labeled textarea ("YOUR SYMPTOMS OR REASON FOR VISIT"), labeled input ("SPECIFIC CONCERN OR QUESTION (OPTIONAL)"), sage "Prepare" button, left-aligned. A thin full-width rule, then a centered two-line medical disclaimer footer.

**Palette:** Warm paper cream canvas, white card surface, sage green (logo, active nav pill, primary button), coral/orange badge, near-black slate text, warm-gray field fills. Matches the committed hues; nothing off-system except the badge (see below).

**Typography:** Serif-ish wordmark; sans body; letterspaced uppercase micro-labels for section and field labels. Scale is quiet and consistent, but the whole page has no element larger than the wordmark — the card label is the de-facto H1 at micro size.

**Spacing rhythm:** Calm and generous inside the card; nav row tighter. Big empty paper band between card and footer rule.

**Component quality:** Clean card, consistent field fills, single obvious primary action, disclaimer present. Reads polished, if sparse.

## Defects

1. **P1 — Header right, badge:** "# 1 due soon" rendered in coral. Coral is the committed *danger* hue; a due-soon reminder is a caution → should be ochre. The most alarming color on the page is spent on a nudge.
2. **P1 — Whole view:** Page is named "Appointments" but contains zero appointments — no upcoming-visit list, no date/time, not even empty-state copy ("No upcoming appointments"). Meanwhile the header asserts one is due soon: the badge's claim is unverifiable anywhere in this view. Nav promise and badge both point at content that doesn't exist here.
3. **P2 — Header right, badge copy:** "# 1 due soon" — stray "#". Should read "1 appointment due soon".
4. **P1 — Main card:** Only path here is prep-text entry; the natural primary job of an appointments view (see/cancel/prepare *for a specific visit*) is absent. One primary action rule is honored, but it's the wrong single action for the view's name.
5. **P2 — Below card:** ~20% of viewport is dead cream space between card and footer rule. With no appointments list, the page reads unfinished rather than calm; that band is exactly where "next appointment" belongs.
6. **P2 — Card:** Panel reads as a single-bezel white card with soft shadow; the committed double-bezel workbench treatment isn't evident.
7. **P2 — Header right, icon buttons:** Two icon-only buttons (keyboard, moon) with no visible labels/affordance; keyboard glyph especially ambiguous for this audience.
8. **P2 — Card heading:** "APPOINTMENT PREP" at micro-caps carries all page identity; no real H1, weak for stressed/scanning users.

**Verdict:** System-compliant palette and a disciplined single-primary layout, but the view is an orphan — itprepares for appointments it never shows, and its only status signal uses the danger hue for a reminder.
