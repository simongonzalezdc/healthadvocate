judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/mobile-help.png)

Image retrieved (the attachment path pointed at the file `/tmp/ha-ds-shots/judge-img/r2` directly — `r2` is the JPEG, not a folder; I viewed its byte-identical copy `r2-view.jpg`, MD5 match). The screenshot shows the HealthAdvocate "Coverage Continuity" creation screen: dark theme, nav with Coverage active, a case-title field, a green "Create Coverage Case" button, and a medical disclaimer footer.

**Honesty audit — mobile-help.jpg (620×436, Coverage Continuity create-form state):**

1. **'This needs a human decision' banner: ABSENT** — no banner anywhere on the screen, and no machine answer is rendered near it to compare strength against (the screen shows only an input form, no AI output).
2. **Neutral 'unavailable' state: ABSENT** — no gray/dashed sentence-case unavailable element exists; the only field is a solid-bordered input with a placeholder, so nothing could be mistaken for an urgency or danger signal.
3. **Urgency badges: ABSENT** — no LOW/MEDIUM/HIGH filled pills; the sole alert-grade element is the amber *outline* chip "1 reminder due soon" in the header, which is a reminder notice and reads as neither an urgency rating nor a danger.
4. **Provenance chips: ABSENT** — none of extracted/inferred/unverified/you-confirmed appear; the only provenance marker is "(synthetic)" on the case-title label, and no inferred value exists that could pass as confirmed.
5. **Demo/synthetic data badging: PRESENT** — the field is labeled "Case title (synthetic)" and the placeholder reads "e.g. Synthetic job-loss coverage case"; it is styled as quiet gray helper text rather than a loud badge, but it is unambiguous at the only data-entry point.
6. **Danger vs caution styling: NOT EXERCISABLE** — no danger/emergency styling appears on this screen at all; with only the restrained amber outline chip present, there is no hierarchy to violate, but also no verified emergency hierarchy.

**HONESTY-VERDICT: PASS** — no violations found: no fallback is presented as a confident answer (no answers are presented at all), synthetic data is labeled, and the one caution element is appropriately restrained. Caveat: this is an empty creation-form state, so checks 1–4 and 6 are absent rather than verified-good — the banner, unavailable state, urgency badges, and provenance chips must be re-audited on screens that actually render machine answers or fallbacks.
