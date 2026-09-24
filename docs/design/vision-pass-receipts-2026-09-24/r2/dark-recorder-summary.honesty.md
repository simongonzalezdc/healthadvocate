judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/dark-recorder-summary.png)

I viewed the screenshot (620×436, dark theme). It shows HealthAdvocate's **"Coverage Continuity"** screen: a nav bar with a "1 reminder due soon" amber outline pill, a "Case title (synthetic)" input with placeholder "e.g. Synthetic job-loss coverage case", a green "Create Coverage Case" button, and a footer medical disclaimer. It is an empty create-case form — no AI answers, fallbacks, or results are rendered on it.

Honesty audit of `dark-recorder-summary.jpg`:

1. **'This needs a human decision' banner: ABSENT.** No banner anywhere on the screen; there is also no machine answer near it to be weaker or stronger than (screen is a bare create-case form).
2. **Neutral 'unavailable' state: ABSENT.** The only gray text is the standard input placeholder ("e.g. Synthetic job-loss coverage case"), a normal form affordance — nothing here could be mistaken for an urgency rating or danger.
3. **Urgency badges (LOW/MEDIUM/HIGH filled pills): ABSENT.** No filled urgency pills exist; the sole pill is the outlined amber "1 reminder due soon" header chip, which is a reminder, not a severity rating, and is distinct from the (absent) unavailable state.
4. **Provenance chips: ABSENT.** No extracted / inferred / unverified / you-confirmed chips appear; since no values are shown at all, no inferred value can pass as confirmed.
5. **Demo/synthetic data clearly badged: YES.** The field is labeled "Case title (synthetic)" and the placeholder repeats "Synthetic job-loss coverage case" — plain text labels rather than a styled badge, but unambiguous.
6. **Danger vs. caution styling: NO danger styling present.** The only caution-leaning element is the amber "1 reminder due soon" outline pill; with no emergency content on this screen there is nothing styled weaker than it, so no inversion occurs.

**Product-law check (fallback must never look like a confident answer): not violated** — this screen renders no fallback or machine answer; it makes honest claims ("Local and private", "No payments or submissions from this screen", synthetic labeling, medical disclaimer).

**HONESTY-VERDICT: PASS** — no violation; note only that this is an empty-state/create screen, so items 1–4 and 6 are not applicable rather than demonstrably compliant, and item 5's synthetic marking is text-only, not a visual badge.
