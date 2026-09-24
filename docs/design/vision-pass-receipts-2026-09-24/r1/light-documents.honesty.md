judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-documents.png)

I can see the attached screenshot (light mode, Documents tab, empty "Document Decoder" input form) and will audit it directly.

**Honesty audit — light-documents.jpg (Documents tab, empty state)**

1. **'This needs a human decision' banner — ABSENT.** No such banner appears anywhere; the only guidance is the card subtitle and the footer disclaimer ("support, not replace, professional medical guidance"). No machine answer is shown nearby, so there is nothing the banner needs to outrank in this state.

2. **Neutral 'unavailable' state — ABSENT.** The only box is the document textarea (solid light border, placeholder "Paste lab results, visit notes, referral letters…"), which reads as an input, not an unavailable marker; it cannot be mistaken for an urgency rating or danger since it carries no fill, badge, or icon.

3. **Urgency badges (LOW/MEDIUM/HIGH pills) — ABSENT.** No LOW/MEDIUM/HIGH pills exist; the only filled pill is a tan header chip reading "#1 due soon," which is a scheduler reminder, not an urgency scale, and is visually unrelated to any unavailable state.

4. **Provenance chips — ABSENT.** No extracted/inferred/unverified/you-confirmed chips appear; there are no extracted or generated values on screen at all, so nothing inferred could pass as confirmed.

5. **Demo/synthetic data badge — ABSENT (not applicable).** No data values of any kind are displayed, so nothing synthetic is masquerading as real; the empty form shows only placeholder text.

6. **Danger vs. caution styling — ABSENT / not comparable.** No danger or emergency styling is present; the strongest caution-adjacent element is the muted tan "#1 due soon" pill, and there is no danger element it could overshadow.

**Overall:** this screenshot is a clean empty input state — no machine answers, fallbacks, ratings, or data claims are rendered, so nothing violates the rule that a fallback must never look like a confident answer. The audit's target elements simply have no output state to attach to here; they would need to be verified on a screenshot showing decoded results.

HONESTY-VERDICT: PASS — no violations found; note the audit is limited because this image shows only the empty input state (no decoded output, fallback, or unavailable state is exercised).
