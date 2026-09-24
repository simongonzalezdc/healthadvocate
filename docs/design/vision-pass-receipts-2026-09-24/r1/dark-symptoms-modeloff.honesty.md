judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/dark-symptoms-modeloff.png)

I can see the image (dark-mode Symptoms view, model-off fallback state). Audit against the six questions:

1. **YES — banner present and dominant.** "This needs a human decision." leads a red-tinted panel with a solid accent bar and bold heading, visually outweighing the dim gray "headache (98%) / dizziness (97%)" lines and all other machine output near it.

2. **PRESENT (mostly) / NO — not mistakable for danger.** Gray sentence-case chip "Model unavailable — no urgency assessment was made." sits under URGENCY LEVEL; it carries no red/orange so it can't read as danger, though being badge-shaped in the urgency slot gives a small skim-risk of "a rating exists" — its explicit text negates that. Border is not clearly dashed at this resolution.

3. **ABSENT.** No LOW/MEDIUM/HIGH filled pills appear anywhere; the only urgency-slot element is the gray unavailable chip, which would be clearly distinct from colored pills.

4. **ABSENT — and this is where it breaks.** None of the four species (extracted / inferred / unverified / you-confirmed) appear anywhere; the bare "(98%)" and "(97%)" confidences on headache/dizziness carry no provenance mark at all, so an inferred/unverified value passes as a confirmed finding.

5. **ABSENT.** No demo/synthetic badge is visible, and nothing on screen labels the percentage scores' origin (the symptom text reads as user-typed, but the scores are unattributed).

6. **YES.** The danger-grade panel (red tint, fill, accent bar, containing the 988/SAMHSA emergency lines) is clearly stronger than the only caution element, the small amber "● 1 due soon" pill in the header.

Secondary note (not one of the six, but honesty-relevant): the fallback copy appears leaked from a different module — "Let the counterparty answer using the stripped validation errors," "manual Coverage workflow," "generated drafts" — incoherent for a symptom flow and undermines the trustworthiness of the fallback.

**HONESTY-VERDICT: FAIL** — Violation: in the model-unavailable fallback, the POSSIBLE CONDITIONS section (lower-middle of the results card) still shows confident-looking machine answers "headache (98%)" and "dizziness (97%)" with no provenance chip or demo/unverified marking; a fallback that disclaims urgency judgment while retaining high-confidence condition percentages looks like a confident answer, breaching the product law.
