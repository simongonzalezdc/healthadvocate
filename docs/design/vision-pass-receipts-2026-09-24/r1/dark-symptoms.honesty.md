judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/dark-symptoms.png)

**Honesty audit — dark-symptoms.jpg (Symptoms tab, pre-assessment state)**

1. **ABSENT** — No "This needs a human decision" banner anywhere; the only human-in-loop language is the small footer line "…support, not replace, professional medical guidance," but no machine answer exists on this screen for it to compete with.

2. **ABSENT** — No 'unavailable' state is shown (the card contains only an empty textarea), so nothing could be mistaken for an urgency rating or a danger signal.

3. **ABSENT** — No LOW/MEDIUM/HIGH pills; the only badge is the orange "#1 due soon" chip in the top header, which is a task-due reminder, not a medical urgency rating, and is spatially far from the assessment card.

4. **ABSENT** — No provenance chips of any species; the screen displays no data values at all, so no inferred value could pass as confirmed.

5. **ABSENT (nothing to badge)** — No synthetic/demo data is presented as real; the textarea holds only an "e.g., I've been having chest pain…" placeholder, clearly framed as an example prompt.

6. **ABSENT (N/A)** — No danger/emergency styling is present to compare against caution; the strongest visual accents are the green "Assess Symptoms" CTA and the orange due-soon chip, both non-alarm.

Context: this is an empty intake form — no AI output, fallback, rating, or extracted data is visible, so there is nothing that could impersonate a confident answer. The footer disclaimer ("not replace, professional medical guidance") is present and legible.

**HONESTY-VERDICT: PASS** — no violations; no fallback, urgency, provenance, or synthetic-data elements exist on this screen to misrepresent (audit limited to the attached image; no files read or written).
