judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r1/light-symptoms-emergency.png)

I can see the image — audit follows.

## What I see

**Layout (top→bottom):** White header band: sage logo tile + "HealthAdvocate" wordmark left; ochre-outline chip "#1 due soon", avatar button, sun/theme button right. Paper-background tab row of 10 items, "Symptoms" active as a sage-tinted pill. One centered warm-white card (double-bezel workbench) containing: eyebrow "SYMPTOM ASSESSMENT" + intro; label "WHAT ARE YOU EXPERIENCING?"; paper-tinted textarea pre-filled "chest pain and shortness of breath for the past hour"; sage primary button "Assess Symptoms"; a large coral danger panel ("This needs a human decision.", clinician-review bullets, divider, "Talk to a real person:" hotline list); "URGENCY LEVEL" with ochre "HIGH" pill; "EXPLANATION" paragraph; "POSSIBLE CONDITIONS" (chest pain 87%, shortness of breath 95%, hairline-separated rows); "ACTION ITEMS" numbered list; "NAME OVERLAP (INFORMAL)" with "Name overlap / Low" row; coral banner "Urgency disagreement detected — upgraded to HIGH for safety." Centered small footer disclaimer.

**Palette as named:** warm paper ground + near-white card; sage = logo, active tab, sole primary button; coral = danger panel + bottom banner; ochre = "HIGH" pill + header chip; slate/ink text. Semantics read correctly at a glance.

**Type:** humanist sans; ~3-step scale — letter-spaced gray caps labels (~10px eq.), ~13px body, weight-only hierarchy. No display size anywhere.

**Spacing/component quality:** calm, consistent section rhythm (~28px), uniform radii, inset panels behave as sub-bezels. Exactly one filled primary action per view — compliant.

## Defects

- **P0 — Danger panel, "Talk to a real person:" block:** Chest pain + dyspnea for an hour is a possible cardiac emergency, yet the panel never says "call 911 / go to the ER now." It routes to 988 (suicide) and SAMHSA (substance-use) — wrong crisis lines for this presentation. The single most important action is missing; this is dishonest-by-omission for the tool's core use case.
- **P0 — Coral panel, bullet 2 and Action items, item 2:** Broken generated copy — "use the stapled visitation errors" and "Submit a lowstack-only modal routine only if you need operative drafts" are meaningless strings inside safety-critical and instruction content. Broken/dishonest.
- **P1 — URGENCY LEVEL pill:** "HIGH" for this symptom set is a danger-grade signal rendered in ochre (caution). Per the committed semantics it should be coral; the current choice softens the verdict.
- **P1 — Bottom coral banner:** "Urgency disagreement detected — upgraded to HIGH for safety" — a safety correction — is the last element on the page, ~5 sections below the pill it amends. Anyone skimming the top sees only the stale urgency.
- **P1 — Coral panel, "Find help near you:" block:** Lead-in promises local help; entries are non-local and partly broken: "Your health insurance helps —" (broken English) and "NACA lookup" (unknown/wrong acronym). Crisis directory doesn't survive scrutiny.
- **P1 — EXPLANATION section:** Internal system state surfaced verbatim to sick users — "optional local model is unavailable or blocked by the privacy boundary. Deterministic preparation steps…" Jargon, not patient language.
- **P1 — NAME OVERLAP (INFORMAL) section:** Irrelevant pipeline module on a triage view ("two extraction methods" of what?). The value row "Name overlap / Low" followed by a full-width rule reads as a one-row table with its columns missing. Pure cognitive load for an overwhelmed user.
- **P2 — POSSIBLE CONDITIONS rows:** Not sorted by confidence (87% above 95%), and percents are inline parentheticals rather than right-aligned tabular figures — the row's key datum is the hardest to scan.
- **P2 — Page-wide labels:** 7+ identical gray letter-spaced caps labels at equal weight flatten the hierarchy; urgency and explanation look as important as the emergency panel.
- **P2 — Coral panel internal structure:** One undifferentiated wall of red text; the three intents (escalate to clinician / human decision / hotlines) get equal weight with a single hairline divider. Needs subgrouping before someone has to read it fast.
- **P2 — Header chip "#1 due soon":** No referent for "#1" anywhere; cryptic status token.
- **P2 — Global type scale:** ~3 steps, body ≈13px at this width, hierarchy carried by weight alone — small for the stated audience; no size step distinguishes the danger panel's headline from body copy.
- **P2 — Below primary button:** Gap to the coral panel (~16px) is tighter than the page's section rhythm, visually welding the CTA to the alert as one cluster.

**Net:** the system's surface grammar (palette semantics, single primary action, calm spacing, honest "a human decides" framing) is intact and on-brand. The failures are content-level: the emergency routing is wrong for the presenting symptoms, and generated filler text has leaked into safety-critical slots. Fix the 911 omission and the broken copy first; everything else is recoverable polish.
