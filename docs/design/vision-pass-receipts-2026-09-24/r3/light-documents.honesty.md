judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/light-documents.png)

I can see the image (an empty-state "Document Decoder" input screen), so here is the audit.

1. **ABSENT** — No "This needs a human decision" banner anywhere; the screen shows only the empty Document Decoder form and footer disclaimer, and no machine answer exists near it to be upstaged.

2. **ABSENT** — No unavailable state is shown; the gray rounded box is a standard text-input with border and placeholder "Paste lab results, visit notes, referral letters…", which reads as a form field, not an urgency rating or danger.

3. **ABSENT** — No LOW/MEDIUM/HIGH filled pills exist; the only pills are the amber "1 reminder due soon" chip and the active "Documents" nav pill, so no confusion with an unavailable state is possible.

4. **ABSENT** — No provenance chips (extracted / inferred / unverified / you-confirmed) of any species appear, so an inferred value cannot pass as confirmed on this screen.

5. **ABSENT** — No demo/synthetic data appears (input area is empty), so there is nothing presented as data that lacks a badge; no "demo" marker is shown because none is needed here.

6. **NOT EVALUABLE / ABSENT** — The only caution-toned element is the amber "1 reminder due soon" pill in the header; there is no danger/emergency styling on screen, so no inverted hierarchy violation is visible.

Overall: this is an empty input state — no decoded output, no fallback answer, no urgency or provenance elements are rendered, so the product law ("a fallback must never look like a confident answer") is not exercised, and the footer honestly scopes the tool ("support, not replace, professional medical guidance"). The strongest visual accent is the green "Decode Document" CTA, which is the user's own action, not a machine claim.

HONESTY-VERDICT: PASS — no violations; caveat: this screenshot is an empty-state form, so all audited elements are unexercised rather than proven correct — output states must be audited separately.
