judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-appointments.png)

I can see the attached image, so here is the audit of that one screenshot (dark-mode Appointments / "Appointment Prep" screen).

1. **'This needs a human decision' banner: ABSENT.** No such banner anywhere; there is also no machine-generated answer on this screen for it to outrank — it's an empty input form with a green "Prepare" button.

2. **Neutral 'unavailable' state: ABSENT.** No gray/dashed/sentence-case fallback state is shown, so nothing on this screen could be mistaken for an urgency rating or a danger signal.

3. **Urgency badges (LOW/MEDIUM/HIGH pills): ABSENT.** The only pill is the amber "1 reminder due soon" chip in the header (top right), which is a reminder count, not a LOW/MEDIUM/HIGH urgency badge; distinctness from an unavailable state is moot since neither is present.

4. **Provenance chips: ABSENT.** No extracted/inferred/unverified/you-confirmed chips appear; no AI-derived values are displayed, so an inferred value cannot pass as confirmed on this screen.

5. **Demo/synthetic data badge: ABSENT — but no synthetic data is shown either.** The only placeholder text ("Describe what you want to discuss with your doctor…", "e.g., Is this medication still right for me?") is genuine empty-input placeholder copy, not fabricated data posing as real.

6. **Danger vs. caution styling: no danger styling present, so no comparison — and no violation.** The sole caution-toned element is the small amber "1 reminder due soon" pill, which is appropriately mild and doesn't crowd out or impersonate any emergency signal; the footer disclaimer ("support, not replace, professional medical guidance…") is present and legible.

Notably, this screen makes no clinical claims and shows no model output, so the product law ("a fallback must never look like a confident answer") is not stressed here — there is no fallback and no confident-looking machine answer. The one honesty affordance that does appear, the footer "not replace professional medical guidance" disclaimer, is present and readable.

**HONESTY-VERDICT: PASS** — no violation found; all honesty affordances queried (human-decision banner, unavailable state, urgency badges, provenance chips, demo badge) are absent but non-applicable on this empty input screen, and nothing present is dishonest.
