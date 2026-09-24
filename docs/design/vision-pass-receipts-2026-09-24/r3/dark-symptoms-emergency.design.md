judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-symptoms-emergency.png)

I can see the image — full audit below.

## What I see

**Layout, top to bottom:** near-black app frame; header row (sage logo tile + "HealthAdvocate" wordmark left; coral-outlined "🔔 Reminder due soon" pill + two circular icon buttons right); full-width tab nav of 11 items with "Symptoms" active as an outlined sage pill, search icon far right; then a centered ~640px double-bezel workbench panel containing: module header (small coral icon tile, H1 "Symptom Assessment", two-line gray sub-copy), small-caps field label "WHAT YOU'RE EXPERIENCING:", a near-black pre-filled textarea with resize grip, a sage pill primary "Assess Symptoms", a full-width coral danger panel ("This needs a human decision" + crisis phone list), five numbered small-caps sections (urgency chip "● HIGH", explanation, "NAME MATCHES – NOT A DIAGNOSIS" with two matches + similarity %, action items, "NAME OVERLAP (INFORMAL)"), a coral disagreement banner, then a centered muted footer disclaimer.

**Palette:** graphite/near-black backgrounds with only a faint brown cast; warm-gray-green muted body text; sage appears only in logo, active tab, primary button; coral dominates — module icon, header reminder, entire result panel, urgency chip, banner; ochre and slate absent entirely.

**Type:** one humanist sans, ~22/14/12/11 scale; letterspaced small-caps section labels; weight contrast in the wordmark; crisis phone numbers set at caption size.

**Spacing/components:** calm, generous hero region; tighter 12–16px rhythm between result sections; consistent pill radii and 12px panel corners; double bezel respected (page → panel → inner cards). Component quality is consistent; the content inside it is not.

## Defects

**P0**
1. **Wrong crisis digits** — danger panel, "Talk to a real person," bullet 2: renders "1-800-652-4357 (1-800-662-HELP, US)". 662-HELP is 662-4357; the numeric and the mnemonic disagree. A mismatched digit in a rendered emergency number is dishonest content.
2. **Engineering jargon in the patient emergency panel** — same panel, top: "Allowed next steps: Fix the candidate answer using the stripped validation errors / Decide as a human." Recurs at §2 ("Deterministic preparation steps"), §4 ("Enable a duckling-only model runtime… generative drafts"), §5 ("interval overlap check between two extraction methods"). This is a debug status dump sitting where triage guidance belongs, shown to sick, overwhelmed users.

**P1**
3. **Coral alarm fatigue** — five separate danger-hued surfaces on one screen (module icon tile, header reminder pill, entire result panel, urgency chip, bottom banner). Danger stops signaling; also buries the sage primary action the system reserves hierarchy for.
4. **Verdict under-weighted** — the actual result, "● HIGH" (below the panel), is the smallest element in the section while jargon paragraphs get the hero space. Invert: verdict first and large, internals cut.
5. **Crisis list order/content** — 988 Suicide Lifeline listed above 911 for a chest-pain presentation; bullet 2 also conflates 911 with a substance-use helpline as one item.
6. **Crisis numbers not actionable** — caption-size, muted salmon, no tel-link affordance. For this audience: large, high-contrast, tappable.
7. **Low-contrast pass needed** — user's typed symptom text in the textarea reads placeholder-gray on near-black; also the field label, "87% string similarity" captions, and italic footnotes sit at or below ~4.5:1.
8. **Nav typo** — "Recarder" (between "2nd Opinion" and "Library") is almost certainly "Recorder."
9. **Safety banner at the bottom** — "Urgency disagreement detected — upgraded to HIGH for safety" sits after the "(INFORMAL)" section, last thing before the footer. Safety-critical; belongs at top of results.
10. **System drift** — committed identity is "warm paper clinic"; this screen contains no paper and no warmth beyond sage/coral. If dark mode is sanctioned (moon toggle suggests it is), it still needs a warm-tinted dark ramp, not neutral graphite.

**P2**
11. Coral icon tile on a neutral intake module header — danger semantics misapplied.
12. Filled textarea styled exactly like an empty/placeholder state; content color should shift once filled. Resize grip is a dev affordance on a symptom field.
13. Label punctuation inconsistent: "NAME MATCHES – NOT A DIAGNOSIS" (en dash) vs. plain labels; "(INFORMAL)", "(US)" parentheticals leak system vocabulary.
14. Double numbering on one screen — sections numbered 1–5, then action items restart 1–2 inside §4.
15. After results render, "Assess Symptoms" remains fully enabled and identical — no success/state change on the primary.

**TL;DR:** structure and component craft are solid, but this screen fails its users and its system: a wrong digit on a crisis line and dev-jargon where triage guidance should be are P0s; coral overuse and a buried urgency verdict are the top P1s.
