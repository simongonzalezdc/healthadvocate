judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-help.png)

I can see the image. Audit follows.

## What I see

**Layout, top to bottom:** White app header — sage rounded-square logo + "HealthAdvocate" wordmark left; ochre "#1 due soon" pill, gear icon, sun icon right. Below it a full-width nav strip on cream: ~11 items (first one clipped at the left viewport edge, reading "…iments", then Discharge, 2nd Opinion, Recorder, Library, Directory, Scanner, Family, Tracks, Coverage, Help). Active "Help" is a sage-filled pill at the right end. Main area: one large cream double-bezel card, left-aligned content: eyebrow "HELP & REAL HUMANS" + two-line intro paragraph; "CRISIS SUPPORT (US)" + two bold-lead-in bullets (988, SAMHSA); "FIND HELP WITH COVERAGE AND CARE" + three bullets; "HOW HEALTHADVOCATE REPORTS ITSELF" + one dense 8-line paragraph. Hairline divider, then a centered two-line disclaimer footer.

**Palette:** Warm paper background (cream page, lighter cream card), near-black/slate body text, sage accent on logo + active nav pill only, ochre badge. Coral absent (no danger content shown). System-consistent.

**Type scale:** Compressed — letterspaced small-cap eyebrows, ~14px body, bold lead-ins. Eyebrow ≈ body size; no visible H1.

**Spacing:** Generous, calm, consistent section rhythm inside the card; card padding generous. Component quality generally clean — pills, bullets, hairlines all crisp.

## Defects

- **P0 — Nav strip, far left:** first nav item clipped to "…iments" at the viewport edge while the logo above sits at the proper page margin — the nav row is misaligned/overflowing with no scroll affordance. Broken and illegible.
- **P1 — Crisis bullets:** the two most safety-critical items on the page (988, SAMHSA) are plain body bullets, visually equal to the "coverage" list. No coral/emphasis, numbers not styled as callable actions. Wrong weight for this audience.
- **P1 — Whole view:** zero primary action, violating the "one primary action per view" rule — the obvious candidate is a sage "Call or text 988" button in the crisis block.
- **P1 — Card, top:** "HELP & REAL HUMANS" is the page title but styled identically to section eyebrows — no H1, flat hierarchy.
- **P1 — Coverage bullets:** "HealthCare.gov navigator finder," "NAIC lookup," "Patient Advocate / Patient Relations" have no link affordance (no underline/sage color); bold is doing double duty for lead-ins and inline emphasis, so nothing reads as clickable.
- **P1 — "HOW HEALTHADVOCATE REPORTS ITSELF" paragraph:** ~95-char measure, 8 dense lines of nuanced hedging — the hardest reading on the page, given to the most fatigued users, unstructured. Break into 2–3 short items.
- **P2 — Header right, "#1 due soon" pill:** ambiguous copy ("#1" reads as a ranking); ochre caution tint on an unclear meaning.
- **P2 — Nav strip overall:** 11 flat items, no grouping; already clipping — will break further at narrower widths.
- **P2 — Footer:** centered text breaks the page's left-aligned rhythm.
- **P2 — Eyebrow labels:** small tracked caps on cream are contrast-borderline; verify ≥4.5:1.
- **P2 — Header icons (gear, sun):** low-contrast hairline glyphs, small hit targets.
- **P2 — SAMHSA bullet:** stacked parentheses "(1-800-662-HELP, 24/7) (treatment referral)" — merge or restructure.

**Verdict:** Solid, on-system foundation; one P0 (clipped nav) plus a systemic problem — the page's most important content (crisis access) carries the least visual weight, and the view has no primary action.
