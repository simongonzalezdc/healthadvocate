judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-symptoms-emergency.png)

I can see the image — auditing it directly, no files touched.

**Honesty audit — r1/light-symptoms-emergency.jpg**

1. **YES — banner present and dominant.** "This needs a human decision." sits in a full-width pink panel with bold dark-red crisis-line entries (988, SAMHSA), outweighing every machine element near it (small HIGH pill, plain gray condition list).

2. **PRESENT (text only) — but not to spec.** Unavailability is disclosed in sentence-case gray text under EXPLANATION ("The optional local model is unavailable or blocked by the privacy boundary"), but there is no gray/dashed-border state treatment; it is not mistakable for an urgency rating or danger.

3. **YES — present and distinct.** URGENCY LEVEL shows a filled dark-red "HIGH" pill, clearly a different visual species from the plain-text unavailable disclosure.

4. **ABSENT — and that's a failure.** No extracted/inferred/unverified/you-confirmed chips appear anywhere; "chest pain (87%)" and "shortness of breath (95%)" carry zero provenance marking, so an inferred keyword match reads as a confirmed clinical finding. (The "not a check of clinical accuracy" note covers only the name-overlap check.)

5. **ABSENT.** No demo/synthetic badge anywhere on the screen, yet percentage-scored conditions are displayed during an explicit model-unavailable fallback — they read as real model output.

6. **YES.** Danger styling (dark-red filled HIGH pill, bold crisis numbers, large banner) clearly outranks the small light-pink "Urgency disagreement detected" caution note.

**HONESTY-VERDICT: FAIL** — Violation: confident-looking fallback output. The EXPLANATION states the model is unavailable, yet directly below it, POSSIBLE CONDITIONS renders "chest pain (87%)" and "shortness of breath (95%)" as precise, unqualified confidence percentages with no provenance chips and no demo/synthetic badge (middle of the Symptom Assessment card). This directly breaches the product law — a fallback must never look like a confident answer — and the banner's own claim ("HealthAdvocate would not answer this on its own") is contradicted ~200px below it. Secondary violations at the same location: missing provenance species (Q4) and missing synthetic-data badging (Q5).
