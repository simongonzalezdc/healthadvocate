judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-symptoms.png)

## WHAT I SEE

**Layout, top→bottom:** (1) White header bar — sage rounded-square logo + "HealthAdvocate" wordmark left; ochre-outlined pill badge "#1 due soon", then two hairline circle buttons ("?", sun) right. (2) Tab strip on paper ground — 10 flat tabs (Symptoms…Library); active "Symptoms" is a white pill with sage text. (3) Centered white card (~2/3 viewport width): coral-on-pink icon tile → tracked-caps title "SYMPTOM ASSESSMENT" → two-line muted intro → tracked-caps field label "WHAT ARE YOU EXPERIENCING?" → large rounded textarea with example placeholder → sage pill button "Assess Symptoms", left-aligned. (4) Full-bleed hairline. (5) Centered muted disclaimer, "HealthAdvocate" bolded; empty paper below.

**Palette:** warm-paper cream ground, white surfaces, sage = logo/active tab/primary button, coral/pink = icon tile, ochre = due badge, dark-slate primary text, muted gray secondary. Matches the committed system — except the coral tile (see below).

**Type:** three tiers — semibold wordmark (~15px), micro-caps tracked labels (~10–11px), body/placeholder (~13px), small disclaimer (~11–12px). Coherent but compressed; micro-caps carry 2 of 5 text roles.

**Spacing/components:** calm 8px-family rhythm, generous card padding, consistent pill radius on badge/tab/button, 1px hairlines, single soft card shadow. Left edges of logo, tab strip, and card align. One primary action per view ✓. No P0 observed.

## DEFECTS

- **P1 — Icon tile (card top-left):** coral/pink on a routine entry point. Coral = danger is committed semantics; it fires an alarm cue exactly where sick users are asked to type symptoms, and competes with the sage primary in the same card. Use sage or slate.
- **P1 — Header right, badge:** "#1 due soon" is opaque copy (≈"#1" of what?) and the highest-salience chrome element — it out-pulls the page's actual primary action.
- **P1 — Textarea/button zone:** the placeholder's own example is "chest pain… past hour," yet no emergency/urgent-care signpost exists near the input; safety guidance is demoted to a passive footer line. For this audience that's a hierarchy failure — surface a quiet "if this is an emergency…" affordance adjacent to the button.
- **P2 — Primary button:** small and left-aligned beneath a full-width input; weak terminus of the form's axis and a small target. Full-width (or markedly larger) sage button fits the audience.
- **P2 — Active tab "Symptoms":** white pill on cream — figure/ground contrast is near nil; active state rides on text hue alone. Needs border/weight or sage fill.
- **P2 — Tab strip:** 10 equal-weight destinations, no grouping (records vs. care-team vs. reference). Heavy working memory for overwhelmed users.
- **P2 — Textarea bottom-right:** visible resize grip; invites layout breakage and is chrome against "restrained/calm."
- **P2 — Header far right:** exposed sun/theme toggle on a committed single light theme invites off-system rendering; sits at equal weight with help "?".
- **P2 — Card edges:** reads as single bezel + shadow; committed double-bezel workbench treatment isn't visible (verify at full res).
- **P2 — Footer:** small muted text on tinted paper — verify ≥4.5:1; placeholder uses straight apostrophes.
- **P2 — Below hairline:** bottom ~30% of viewport is empty paper; consider vertical centering or one supportive element (recent assessment, "what happens next"). On-brand calm, but currently reads as unfinished.
- **Verify (P0-if-false):** "Your information stays on your device" must be literally true for a tool that processes symptom text; can't be confirmed from the image.
