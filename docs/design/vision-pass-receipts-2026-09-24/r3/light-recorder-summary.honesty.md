judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/light-recorder-summary.png)

I can see the attached image clearly, so here is the audit, judged on this screenshot only.

**Honesty audit — HealthAdvocate Call Recorder (r3/light-recorder-summary.jpg)**

1. **PRESENT / YES — banner is stronger.** "This needs a human decision" is the only tinted block in the region (pink fill, red accent border, bold red heading), visibly outweighing the plain-text deadline rows and small outline chips immediately above it.

2. **ABSENT in the specified style / NO — not mistakable.** The unavailable state is rendered as bold strikethrough "no date" plus a full sentence ("no date could be read reliably from the audio") with an amber UNVERIFIED chip — no gray dashed box, but also no pill shape, no red, and no gauge-like styling, so it reads as absence of data, not urgency or danger.

3. **ABSENT.** No LOW/MEDIUM/HIGH filled pills exist anywhere in this screenshot (only provenance chips: FROM TRANSCRIPT, UNVERIFIED, MODEL-INFERRED), so there is nothing that could collide with the "no date" state.

4. **YES — species distinguishable / NO — inferred can't pass as confirmed.** FROM TRANSCRIPT chips are cool blue, UNVERIFIED is yellow, MODEL-INFERRED is orange, all with explicit text labels; the one softness is that UNVERIFIED and MODEL-INFERRED sit in similar warm hues and are separated mainly by their wording, but neither resembles the confirmed-looking blue transcript chip.

5. **YES.** "DEMO MODE" pill top-right, section header "YOUR RECORDINGS (DEMO)", "(demo recording)" in the item label, plus "synthetic call script" / "Replay the demo call" controls.

6. **YES.** Danger is a fully saturated red (filled Delete pills, pink alert panel), clearly heavier than the pale amber caution tints used for the reminder pill, UNVERIFIED, and MODEL-INFERRED chips.

Minor notes (non-blocking): the second recording, "Aetna — MRI denial call — Sep 24 · 11:02", carries no per-item demo tag — it is only covered by the section-level "(DEMO)" badge; and the human-decision banner borrows pink/danger coloring, which is acceptable here since it's the escalation state, but it must never be reused for routine content.

**HONESTY-VERDICT: PASS**
