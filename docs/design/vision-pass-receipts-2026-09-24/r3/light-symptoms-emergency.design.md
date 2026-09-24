judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/light-symptoms-emergency.png)

I can see the image — full audit follows.

## Description

**Layout, top-to-bottom:** Cream page. Top bar: sage logo tile + "HealthAdvocate" wordmark left; ochre "1 reminder due soon" chip + two ghost circular icon buttons right. Below: single-row nav of ~10 text tabs, "Symptoms" active in a sage pill; a partial element is clipped at the far right edge. Center: one large white double-bezel card containing — header row (sage icon tile, "Symptom Assessment" title, two-line subtitle); eyebrow "WHAT ARE YOU EXPERIENCING?"; large warm-gray textarea with typed text and a resize grip; sage pill button "Assess Symptoms"; then a full-width pale-coral alert panel (title "This needs a human decision.", bullets, dashed rule, "Talk to a real person:" with three hotline bullets, then three more referral bullets); then five result sections with numbered uppercase eyebrows: 1. URGENCY LEVEL (small coral outline "● HIGH" pill), 2. EXPLANATION, 3. NAME MATCHES — NOT A DIAGNOSIS (two rows: "chest pain" 97%, "shortness of breath" 95%, hairline rules), 4. ACTION ITEMS (numbered 1–2), 5. NAME OVERLAP (INFORMAL) with a stray "low" tag and a rule; then a pale-coral rounded banner "Urgency disagreement detected — upgraded to HIGH for safety." Footer: centered three-line disclaimer.

**Palette as named hues:** Warm paper neutrals for page/card/textarea fill; sage = logo tile, active tab, icon tile, primary button (used correctly as the single primary); coral = alert panel, HIGH badge, disagreement banner, all alert text; ochre = reminder chip; slate = eyebrows, secondary text, footer.

**Typography scale:** Humanist sans throughout. Compressed scale: title ~18px, section titles ~15px, body ~13px, eyebrows/annotations ~10–11px uppercase letterspaced. No large display size anywhere.

**Spacing rhythm:** Generous and calm in the input half (card margins, header, field); noticeably denser in the results half (tight eyebrow→content stacking, hairline dividers).

**Component quality:** Double bezel reads consistently (card → inner panels). Pills, radii, and hairlines are consistent; buttons and badges are cleanly drawn. Build quality is good; the failures are semantic and copy-level.

## Defects

**P0**
1. **Coral panel body + all six hotline numbers** (card, just below primary button): coral text on pale-coral fill at ~12px fails AA contrast — on the most safety-critical copy in the product. Crisis numbers should be near-black, larger, bold.
2. **Coral panel, first bullet:** "For the candidate answer using the stripped validation errors" — garbled/truncated sentence (missing verb) plus leaked internals, inside the safety panel.
3. **Coral panel, last bullet:** "Ask the hospital's the Patient Advocate" — doubled article; broken copy in the same panel.
4. **Nav bar far right (~y 8%):** last nav element clipped mid-shape at the container edge, no fade/scroll affordance — broken render.

**P1**
5. **Inverted hierarchy (whole card):** the refusal/disclaimer panel is the loudest object on the page; the actual clinical output ("● HIGH") is a small outline pill and results §1–5 are a uniform wall of small text. The assessment should outrank the meta-messaging.
6. **Coral semantic overuse:** coral simultaneously carries a refusal notice, the urgency badge, and a procedural status banner (card bottom, ~85%). Danger channel diluted; the disagreement banner is status, not danger — ochre or slate.
7. **Dislocated explanation:** "Urgency disagreement detected — upgraded to HIGH" sits at the card bottom, far from the HIGH badge it explains (§1, ~48%). Co-locate.
8. **Internal jargon in patient-facing copy:** "stripped validation errors" (alert), "privacy boundary" (§2), "laptop-only model runtime" (§4), "two extraction methods" (§5). Wrong register for sick, overwhelmed users.
9. **Hotlines not actionable:** 988 / 1-800-662-4357 / "FindHelp Now" are plain mixed-format text — no link or tap-to-call styling. On mobile these must be one-tap buttons.
10. **Nav crowding:** 10 tabs plus clipped overflow; no affordance for the overflowed items.
11. **Compressed type scale / scanability:** three near-identical sizes (~18/13/10px); results §1–5 undifferentiated — no size or weight steps to guide a distressed reader.

**P2**
12. **Stray "low" tag** right of "Name overlap" (§5, ~78%): bare lowercase text, no badge treatment — reads as a stray word.
13. **Double numbering:** numbered eyebrows (1.–5.) with a second 1–2 list inside §4 — two competing numbering systems.
14. **Textarea resize grip** (bottom-right of field, ~26%): off-system for a calm workbench; pin the height.
15. **"(name match, 97% string similarity)"** annotations: tiny, low-contrast, and string-similarity percentages are noise to patients even with the disclaimer.
16. **Rhythm split:** airy input half vs. dense results half — inconsistent vertical beat within one card.
17. **Ochre reminder chip** uses caution-level color for a routine reminder; neutral chip + ochre dot would reserve ochre.
18. **"Coverage workflow"** in §4 references another tab with no link or cross-reference affordance.

**Strengths worth keeping:** single sage primary action respected, consistent double bezel, restrained palette usage in the chrome, calm footer. The system is intact — the failures are contrast, copy integrity, and danger-channel discipline.
