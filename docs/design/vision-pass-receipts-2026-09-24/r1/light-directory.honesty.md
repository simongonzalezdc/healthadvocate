judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-directory.png)

I can see the attached image and will judge only it — no files read or written.

**Honesty audit — HealthAdvocate Directory screenshot (`r1/light-directory.jpg`)**

1. **ABSENT** — No "This needs a human decision" banner anywhere on the page; the only human-decision affordances are the small inline "Confirm" links next to inferred/decoded fields (e.g., Dr. Patel's email, Aetna's appeals fax), which is acceptable here because this is a directory with no machine answer/fallback card claiming confidence — the inferred values are explicitly labeled, so none reads as a confident answer.

2. **ABSENT (moot)** — No "unavailable" state appears; every field on all four cards is populated, so there is nothing that could be mistaken for an urgency rating or a danger signal.

3. **ABSENT** — No LOW/MEDIUM/HIGH filled pills exist; the only urgency-like element is the small amber "1 due soon" pill in the top header, and with no unavailable state present, distinctness is moot.

4. **YES distinguishable / NO it cannot pass** — Confirmed values carry green-outlined "YOU CONFIRMED ✓" chips; inferred values carry amber filled chips ("INFERRED · PATTERN", "INFERRED · VOICEMAIL", "INFERRED · LETTER"); extracted values carry neutral/blue chips ("BILL DECODE", "DOCUMENT", "VOICEMAIL", "FROM A CALL") — hue, label, and the ✓ mark all differ, so an inferred value cannot visually pass as confirmed, and the legend states "confirmed information always wins over inference."

5. **YES, PRESENT** — A blue-outlined "DEMO DATA" badge sits prominently at the top-right of the Directory header block, clearly labeling the dataset as synthetic.

6. **ABSENT (moot)** — No danger/emergency styling exists on this page (no red elements at all); only caution-amber appears ("1 due soon" pill, inferred chips), so there is no danger-vs-caution hierarchy to evaluate — and nothing dresses caution up as danger.

Overall the page behaves honestly: nothing uncertain is styled as confident, inference is chromatically and typographically separated from confirmation, and demo data is badged. The absent banner/unavailable state/urgency pills are simply out of scope for this view, not violations.

HONESTY-VERDICT: PASS
