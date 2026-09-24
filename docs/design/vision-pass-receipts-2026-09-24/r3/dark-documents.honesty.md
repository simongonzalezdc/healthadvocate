judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-documents.png)

I can see the attached image clearly — it's the HealthAdvocate "Document Decoder" screen in dark mode, an empty input form (nav bar, reminder pill, textarea, green "Decode Document" button, footer disclaimer). Auditing only what's visible:

**Honesty audit — r3/dark-documents.jpg (empty Document Decoder input state)**

1. **ABSENT** — No "This needs a human decision" banner appears anywhere; no machine answer exists on this screen for it to outrank, so nothing is being passed off as a confident answer.

2. **ABSENT** — No unavailable state (gray, dashed border, sentence case) is shown; the only dashed/outline element is the empty input textarea, which reads unambiguously as an input, not a result — it cannot be mistaken for an urgency rating or danger.

3. **ABSENT** — No LOW/MEDIUM/HIGH filled pills are present; the only filled pill is the orange "1 reminder due soon" in the top bar, which reads as a reminder count, not a clinical urgency rating.

4. **ABSENT** — No provenance chips (extracted / inferred / unverified / you-confirmed) of any species are visible; nothing is shown that could pass inferred data off as confirmed.

5. **ABSENT (vacuously OK)** — No demo/synthetic data is displayed at all (empty form, placeholder text only), so there is nothing that needed a demo badge.

6. **NO VIOLATION** — The only caution-toned element is the small orange "1 reminder due soon" pill; no danger/emergency styling exists on this screen, so caution styling is not competing with or overpowering anything.

The screen is honest as shown: it's a pre-submission input form, the copy makes a plain capability claim ("we'll extract and explain…"), and the footer carries the "support, not replace, professional medical guidance" disclaimer.

**HONESTY-VERDICT: PASS** — no violation; all audit-relevant components are absent because this screen renders no machine answer, fallback, urgency, provenance, or data — only an input form with a disclaimer.
