judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/final/dark-library.png)

I can see the image (dark-theme Library screen), so here is the audit, judged from the screenshot only.

1. **Banner: ABSENT.** No "This needs a human decision" banner exists; the nearest analog is the small dim caption "Machine-derived items: … confirm it before relying on it," which is visually weaker than the gold "★ COMPUTED FROM THE LETTER" badge — though that badge is itself a warning label, not a confident machine answer, and the card body says "Confirm the exact date with the insurer."

2. **Unavailable state: ABSENT.** Every card is populated; no gray/dashed-border "unavailable" element appears, so there is nothing on this screen that could be mistaken for an urgency rating or a danger.

3. **Urgency badges: ABSENT.** No LOW/MEDIUM/HIGH pills exist; the only filled pills are amber ("Sep 30", "★ COMPUTED FROM THE LETTER", "DEMO DATA") and carry no urgency taxonomy, so distinctness from an unavailable state is untestable here.

4. **Provenance chips: PARTIAL — species NOT distinguishable.** Chips use a single asterisk convention ("* Insurance", "* Appointments", "* Documents") with no distinct extracted/inferred/unverified/you-confirmed styles; however, the sole inferred value (the Oct 8 appeal-window close) cannot pass as confirmed because it is labeled three times — "(computed)" in the title, the gold "COMPUTED FROM THE LETTER" badge, and the body text "the app computed Oct 8."

5. **Demo badge: PRESENT.** An amber "DEMO DATA" pill sits at the top-right of the Library panel and is clearly visible.

6. **Danger vs caution: NOT EXERCISED.** No danger/emergency (red) styling appears anywhere; amber caution is the strongest alert level shown, so there is no case where caution visually outweighs danger — but the hierarchy is untested on this screen.

**HONESTY-VERDICT: PASS** — no violation: the only machine-computed value is prominently marked as computed (not confident), demo data is badged, and machine-derived items carry an upfront disclaimer. Notable gaps (absences, not violations): no explicit human-decision banner, no unavailable state, no urgency badges, and provenance species collapse into a single indistinguishable asterisk mark on the "* Insurance / * Appointments / * Documents" chips.
