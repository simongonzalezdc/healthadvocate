judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/dark-directory.png)

**Judged image:** `/tmp/ha-ds-shots/judge-img/r1/dark-directory.jpg` (dark-mode Directory screen, 620×436). Disclosure: the stated attachment path `…/judge-img/r2/dark-directory.jpg` does not exist — `judge-img/r2` is a stray JPEG (byte-identical to `r2-view.jpg`, and it renders the **Coverage** page, not Directory). The only genuine `dark-directory.jpg` is the r1 file above, which matches the attachment's name and subject; I audited it and no other project content.

---

**(1) "This needs a human decision" banner** — **ABSENT.** No such banner anywhere on the screen; the page has no pending machine answer, only provenance-labeled directory rows each with a "Confirm" affordance, so absence is appropriate rather than a hidden decision.

**(2) Neutral "unavailable" state** — **ABSENT.** Every field carries a value; there is no gray/dashed/sentence-case "unavailable" field, and consequently nothing on this screen could be mistaken for an urgency rating or danger signal.

**(3) Urgency badges (LOW/MEDIUM/HIGH pills)** — **ABSENT.** No filled urgency pills exist, so there is also no collision possible with an unavailable state (which is likewise absent).

**(4) Provenance chips** — **PRESENT, species distinguishable; an inferred value could NOT pass as confirmed.** Green `YOU-CONFIRMED ✓` chips, neutral slate source chips (`BILL DECODE`, `DOCUMENT`, `CALL`, `VOICEMAIL`), and orange `INFERRED · PATTERN/VOICEMAIL/LETTER` chips differ in hue and text, reinforced by the legend "confirmed information always wins over inference"; the literal "unverified" species does not appear (all extracted values are attributed to a named source), and notably Dr. Patel's mismatched inferred email (`s.chen@drpatelho…`) is honestly flagged `INFERRED · PATTERN` rather than presented as fact.

**(5) Demo/synthetic data badged** — **YES.** A `DEMO DATA` chip sits at the top-right of the directory header card (modest but legible), backed by hygiene cues (555-xxxx numbers, `.example` email domain).

**(6) Danger/emergency styling vs caution styling** — **ABSENT/N-A.** This screen carries no danger or emergency styling; the only cautionary element is the small orange "1 reminder due soon" pill in the header, and nothing competes with or outranks it.

Caveat: judged at the file's native 620×436 resolution — chip hue classes (green/orange/neutral) were clearly separable, but 1-px stroke details carry minor uncertainty.

**HONESTY-VERDICT: PASS** — no violation found; the one product-law risk area (inferred email that pattern-matched the wrong name) is explicitly labeled `INFERRED · PATTERN` with a Confirm action rather than shown as a confident answer.
