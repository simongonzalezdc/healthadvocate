judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-symptoms-modeloff.png)

I can see the image — auditing it directly, no files touched.

**Honesty audit — `dark-symptoms-modeloff.jpg` (fallback state, model off)**

1. **YES** — "This needs a human decision." banner is present as the first element of the results area in a tinted, bordered panel with bold red heading, clearly stronger than the plain-text machine output near it (gray unavailable pill, unstyled name-match lines below).

2. **PRESENT / NO** — Under "1. URGENCY LEVEL" sits a muted gray pill, sentence case: "Model unavailable — no urgency assessment was made." (a dashed border isn't discernible at this resolution, but the state reads neutral). It cannot be mistaken for an urgency rating or danger: it explicitly negates any rating, uses no red/amber, and carries no LOW/MEDIUM/HIGH token.

3. **ABSENT** — No LOW/MEDIUM/HIGH filled pills exist anywhere in this state, which is correct for a fallback; nothing competes with the gray unavailable pill, so no confusion is possible in this screenshot (cross-state distinctness can't be judged from this one image).

4. **ABSENT / NO** — No extracted/inferred/unverified/you-confirmed chips appear; the only annotations are "(name match, 94% string similarity)" and "(name match, 80% string similarity)" under a header that says "NOT A DIAGNOSIS," so no inferred value could pass as confirmed.

5. **ABSENT (N/A)** — No demo/synthetic badge is visible, but nothing on screen is presented as demo or synthetic data — the symptom text reads as ordinary user input; note that if this is a scripted fixture, nothing on-screen flags it as such.

6. **YES** — Danger styling (red-tinted human-decision panel; bold red 988 and 1-800-662-4357 crisis lines) is clearly stronger than the only caution-toned element, the small amber "1 reminder due soon" chip in the header.

The fallback behaves per product law: it names the failure ("Model unavailable"), refuses to produce an urgency judgment, explains why, and routes to human help and crisis resources — nowhere does it dress itself up as a confident answer.

HONESTY-VERDICT: PASS (no violations; minor note only: the unavailable pill's border is solid rather than visibly dashed, and no demo-data badge exists should this content be synthetic)
