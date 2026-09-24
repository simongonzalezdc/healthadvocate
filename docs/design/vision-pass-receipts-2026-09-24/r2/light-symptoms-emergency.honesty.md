judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/light-symptoms-emergency.png)

**Note on the attachment path:** the stated path `judge-img/r2/light-symptoms-emergency.jpg` does not exist — `judge-img/r2` is a JPEG file (a different page), not a folder. The named screenshot exists exactly once in the tree, at `judge-img/r1/light-symptoms-emergency.jpg`, which is what I judged. No other screenshots were read.

**(1) Human-decision banner: PRESENT, and visually stronger.** A large filled pink/red panel headed by bold red "This needs a human decision." with "HealthAdvocate could not answer this on its own" plus 988 and SAMHSA hotline lines sits directly above every machine output, which are only thin-ruled plain text and thin-outlined pills.

**(2) Neutral unavailable state: PRESENT in substance, styling partial.** Unavailability is stated in sentence-case gray body text ("The optional local model is unavailable or blocked by the privacy boundary…") with a neutral outlined "Initial" placeholder, but no gray dashed-border component is visible; it cannot be read as a danger (no red fill, no icon), and it does not fake a severity level — though "Initial" occupying the URGENCY LEVEL slot is mildly ambiguous between "rating pending" and "unavailable."

**(3) Urgency badges: ABSENT on this screen.** No filled LOW/MEDIUM/HIGH pill appears anywhere; the only urgency badge is the outlined neutral "Initial," and the claimed "upgraded to HIGH for safety" exists only as a small red alert line at the card bottom — so filled-badge vs unavailable-state distinctness cannot be verified from this screenshot.

**(4) Provenance chips: ABSENT as species.** No extracted / inferred / unverified / you-confirmed chips are rendered; inferred values are caveated only by section labels ("POSSIBLE CONDITIONS," "NAME OVERLAP (INFORMAL)") — so nothing inferred passes as confirmed on this screen, but the four chip species themselves can't be audited here.

**(5) Demo/synthetic badge: ABSENT.** No demo/synthetic/sample badge appears in the header, the card, or the footer, while the page renders scored outputs (87%, 95%).

**(6) Danger vs caution: YES, danger clearly stronger.** Danger styling is the filled red-toned banner plus a red-text safety alert with a red left border; no amber/caution tier exists on the screen at all, so no confusion is possible — the neutral states are plain gray outlines well below the danger tier.

**Violations found (locations):**
- Confidence-style percentages "chest pain (87%)" / "shortness of breath (95%)" under POSSIBLE CONDITIONS — the closest approach to the product law, since bare numbers read as machine confidence in a declared no-answer state (scoped only by the section label; recommend dropping or annotating the percentages).
- "Urgency disagreement detected — upgraded to HIGH for safety" is carried only by a small alert line at the card bottom; the URGENCY LEVEL badge itself still shows neutral "Initial," so a badge-level scan misses the HIGH escalation.
- No demo/synthetic badge despite scored outputs being shown.
- Copy defects that undermine the fallback's credibility: unresolved token "HAVC_LOOKUP" in the "Find help near you" list, insurance-page copy ("manual Coverage workflow") and garbled text ("Submit a fallback-only remark runtime only, if you need generation drafts") in ACTION ITEMS.

The core law holds: the fallback is dominated by the human-decision banner, admits model unavailability in plain text, and never fabricates a rating or a confident answer. Secondary violations above should still be fixed.

HONESTY-VERDICT: PASS
