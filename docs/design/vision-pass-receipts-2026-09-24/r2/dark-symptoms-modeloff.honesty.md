judged-by: GLM-5.3-Flash (zai/glm-5.3-flash, flash-home zcode lane; full-res original: screenshots/r2/dark-symptoms-modeloff.png)

**Honesty audit — `r2` (dark, "model off" shot, 620×436).** Visible content: HealthAdvocate dark header, nav with "Coverage" tab active, a "Coverage Continuity" page containing one empty form (label "Case title (synthetic)", placeholder "e.g. Synthetic job-loss coverage case", green "Create Coverage Case" button), a muted amber "● 1+ reminder due soon" pill top-right, and a footer medical disclaimer. Note: the filename says "symptoms" but the rendered page is the Coverage screen — I judged only what is visible. (I viewed the attached image via temp crops of that same file only; no project files were read or written.)

1. **'This needs a human decision' banner: ABSENT.** No such banner anywhere; there is also no machine answer on this screen (only an empty create-case form), so nothing masquerades as a confident decision — the fallback complies with the product law by showing no answer at all.

2. **Neutral 'unavailable' state: ABSENT.** No gray/dashed "unavailable" element exists, so there is nothing that could be mistaken for an urgency rating or danger.

3. **Urgency badges (LOW/MEDIUM/HIGH pills): ABSENT.** The only filled pills are the nav "Coverage" active tab (muted sage) and the top-bar "● 1+ reminder due soon" (muted amber text on dark, strongest pixel ≈ RGB(107,95,81) — no red fill), neither an urgency rating.

4. **Provenance chips: ABSENT.** No extracted/inferred/unverified/you-confirmed chips appear, and no machine-derived value is displayed, so an inferred value cannot pass as confirmed on this screen.

5. **Demo/synthetic data badged: PRESENT.** "Case title (synthetic)" label and the placeholder "e.g. Synthetic job-loss coverage case" flag the demo data twice in unambiguous sentence case, though styling is quiet (gray parenthetical).

6. **Danger/emergency styling: ABSENT (nothing to compare).** There is no danger or emergency element on the screen; the loudest styling is the sage-green primary button, and the sole attention cue ("1+ reminder due soon") is understated amber — no overstated danger and nothing that outshouts a caution state.

**HONESTY-VERDICT: PASS** — no violation found in this image: the model-off fallback presents no confident machine answer, synthetic data is badged, and no fake urgency/danger/provenance styling exists. Caveat: because this screen contains no AI output, the banner, unavailable state, urgency badges, and provenance chips are untested here rather than demonstrated — a symptoms/results screen would be needed to certify those species.
