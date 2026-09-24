judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/final/light-symptoms-modeloff.png)

I can see the image clearly — auditing it now against the six questions. No files read or written.

**Honesty audit — `light-symptoms-modeloff.jpg` (Symptom Assessment, model-off fallback)**

1. **PRESENT / YES — stronger than anything near it.** The pink-tinted card headed in bold red "This needs a human decision." dominates the results area; no machine urgency answer exists beside it, and every other block (gray chip, faint name-match notes, ghosted action items) is visually weaker.

2. **PRESENT — could not be mistaken.** Section 1 shows a gray, sentence-case chip reading "Model unavailable — no urgency assessment was made."; it is achromatic (no red/amber), carries explicit negation text, and takes no LOW/MED/HIGH pill form, so it reads as neutral, not as a rating or a danger. (Caveat: at this resolution the chip's border reads solid rather than dashed, if a dashed border is part of the spec.)

3. **ABSENT.** No LOW/MEDIUM/HIGH filled pills appear anywhere — consistent with an honest model-off state; with no urgency pills on screen there is nothing the gray chip could be confused with.

4. **ABSENT — nothing passes as confirmed.** No extracted/inferred/unverified/you-confirmed chips exist; the closest annotations are "(rare match; 94% string similarity)" under the explicit header "NAME MATCHES — NOT A DIAGNOSIS" and "Name overlap" labeled "(INFORMAL)" with "not a check of clinical accuracy" beneath it, so no inferred value is dressed as a confirmed one.

5. **NO badge, and none appears required.** Nothing on screen is identifiable as demo/synthetic data — the symptom text is the user's own typed input and all sections derive from it; there is no demo/synthetic content left unbadged.

6. **YES — danger clearly outranks caution.** The red-on-pink card with bold red "Talk to a real person," 988, and SAMHSA 1-800-662-4357 is far heavier than the gray unavailable chip and the ~30%-opacity ghosted action items, giving an unambiguous severity hierarchy.

**Non-gating quality note (not an honesty violation):** several strings read as garbled template output — "Free, confidential support using the stepped validation entries," "Your hospital's department arm — NACR hotline," and "Schedule a follow-up once the attribute…" in section 4. They make the page look broken rather than confident, and the real hotline numbers remain bold and correct, but they should be fixed.

HONESTY-VERDICT: PASS — the fallback explicitly disclaims machine judgment ("no urgency assessment was made," "NOT A DIAGNOSIS") and the human-decision banner is the strongest element on the page; no violation of the stated law found.
