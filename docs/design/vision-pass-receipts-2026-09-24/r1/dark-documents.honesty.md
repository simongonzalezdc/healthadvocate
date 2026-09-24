judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/dark-documents.png)

The image is visible, so here is the audit of this single screenshot (a dark-mode "Documents / Document Decoder" input screen).

1. **'This needs a human decision' banner: ABSENT.** No such banner exists anywhere on this screen — though no machine answer is shown either, so nothing currently demands one.
2. **Neutral 'unavailable' state: ABSENT.** The only boxes are the solid-bordered textarea and card; no gray/dashed/sentence-case unavailable state appears, and nothing here could be misread as urgency or danger.
3. **Urgency badges (LOW/MEDIUM/HIGH pills): ABSENT.** The only alert-like element is the small amber "⚠ 1 due soon" pill in the top bar, which is a count, not a filled urgency rating.
4. **Provenance chips: ABSENT.** No extracted/inferred/unverified/you-confirmed markers appear, so there is no risk of an inferred value passing as confirmed — but also no provenance labeling once results do render.
5. **Demo/synthetic data badge: ABSENT (not applicable).** No sample or synthetic data is displayed, and nothing indicates this is a demo environment; the amber "due soon" pill looks like real user state.
6. **Danger vs. caution hierarchy: NOT EVALUABLE.** Only caution styling exists (soft amber "1 due soon" pill); no danger/emergency styling is present, so no incorrect ranking is visible — but the hierarchy is untested on this screen.

Context that supports the verdict: the footer states "HealthAdvocate is here to support, not replace, professional medical guidance. Always consult a qualified healthcare provider…" and "Your information stays on your device," which is an honest-support framing. The one mild tension is the marketing copy "we'll extract and explain all the medical terms" above a confident green "Decode Document" button — confident phrasing, but it's a call-to-action on an empty form, not a fallback posing as an answer.

**HONESTY-VERDICT: PASS** — no violation: this screen contains no machine answers, fallbacks, urgency ratings, or provenance states to misuse; the only caution element (amber "1 due soon", top-right) is correctly sub-danger in tone. Note the audit is limited: most honesty affordances (1–5) are absent because the screen is a pure input form, so they must be verified on a results screen.
