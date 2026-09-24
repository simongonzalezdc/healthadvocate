judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/light-drugs-result.png)

I can see the attached screenshot (Drug Checker page, model-off fallback state). Audit below, judged on this image only.

1. **'This needs a human decision' banner: ABSENT.** No such banner exists; the nearest equivalents are "This name was recognized by name matching…" and the muted fallback note, so there is no banner-strength signal — though the fallback itself is deliberately de-emphasized, not confident.

2. **Neutral unavailable state: PRESENT (with one caveat).** The box "No drug details were generated — the optional model is off…" is gray, sentence case, and reads as a quiet note, so it cannot be mistaken for an urgency rating or danger (no red, no badge shape); caveat: its border appears solid, not dashed, at this resolution.

3. **Urgency badges: ABSENT.** There are no LOW/MEDIUM/HIGH filled pills anywhere on the page; the only filled pill is the red "#1 reminder due soon" header badge, which is a reminder count, not an urgency rating.

4. **Provenance chips: ABSENT (N/A).** No extracted/inferred/unverified/you-confirmed chips exist — provenance is conveyed only in prose ("recognized by name matching against the medical dictionary"), so there is no chip species to confuse and no inferred value that could pass as confirmed.

5. **Demo/synthetic data badge: ABSENT (N/A).** No DEMO/SYNTHETIC badge is shown, but the page discloses in plain text that the optional model is off and "Only the name match above is real; this is not a drug review" — i.e., no synthetic data is displayed to badge.

6. **Danger > caution styling: YES.** The only alarm-colored element is the saturated filled red header pill, which clearly outranks the pale gray/tan caution and fallback boxes; no danger or emergency styling is diluted or competing.

Product law check: the fallback (gray box, lower third of the card) is visually the quietest element on the page and explicitly negates itself ("this is not a drug review") — it does not look like a confident answer. The capitalized "1. LIPITOR" result line is a name match, not a review, and is immediately hedged by the adjacent disclosures.

**HONESTY-VERDICT: PASS** — no violations found; minor observations only: the unavailable-state border is solid rather than dashed, and the human-decision banner, provenance chips, and demo badge are absent because this state contains no model output, inferred values, or synthetic data to flag.
