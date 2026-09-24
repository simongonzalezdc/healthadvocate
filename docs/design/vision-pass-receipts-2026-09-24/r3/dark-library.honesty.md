judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r3/dark-library.png)

I can see the attached image (HealthAdvocate "Library" screen, dark theme, demo dataset). Audit below, judged on this screenshot only.

**(1) 'This needs a human decision' banner — ABSENT.** No such banner appears anywhere on the Library screen; the closest machine-derived item ("Appeal window closes (detected)") self-labels as *detected* and cites its source, so no fallback is posing as a confident answer here.

**(2) Neutral 'unavailable' state — ABSENT.** No gray/dashed "unavailable" element is shown (all four cards have real content), so nothing on this screen could be misread as an urgency rating or danger signal.

**(3) Urgency badges (LOW/MEDIUM/HIGH pills) — ABSENT.** All chips are content tags ("denial → not medically necessary," "$1,200.00," "appeal window," etc.); no urgency pills exist, so no confusion with an unavailable state is possible.

**(4) Provenance chips (extracted / inferred / unverified / you-confirmed) — ABSENT as a system.** The four species don't appear; the only provenance signaling is ad-hoc on the last card ("Appeal window closes **(detected)**" + "★ FROM THE DENIAL LETTER"), which is honest but not the canonical species set — no inferred value is visually passing as confirmed on this screen.

**(5) Demo/synthetic data badged — PRESENT.** A clear teal-outlined "DEMO DATA" pill sits at the top right of the Library header, reinforced by the footer disclaimer ("support, not replace, professional medical guidance").

**(6) Danger styling vs caution styling — cannot be verified (no danger styling present).** The only emphatic styling is amber caution on the deadline card and its "FROM THE DENIAL LETTER" chip; no red/emergency element exists on this screen to compare, and the deadline is appropriately *not* dressed up as an emergency.

**Notes (not violations):** the machine-detected appeal deadline is the one item that would merit a human-decision affordance in an answer/analysis view — here it is mitigated by explicit "detected" labeling and source citation, but the four-species provenance system should appear once values are rendered in detail views.

HONESTY-VERDICT: PASS
