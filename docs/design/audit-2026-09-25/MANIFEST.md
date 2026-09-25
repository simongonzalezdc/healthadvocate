# G005 pre-registered judgment manifest (v1) — S+ final gate

Committed BEFORE the first judgment. sha256 recorded in .omx/ultragoal/ledger.jsonl.
Thresholds (from the approved plan, immutable): MiMo v2.6-pro (thinking-on) per-dimension
median ≥9 AND min ≥8.5; GLM-5.3-Flash second judge (same shots) per-dimension median ≥8.5.
Round-count convention: this original judgment = round 1; failure path = steer subgoal →
full re-judgment under a NEW manifest; 3 failed full rounds → blocked (thresholds never move).

## Shot set (fixed; desktop 1280×900, mobile 390×844 @2x, both light+dark, EN)
Dimensions taste/color/typography/spacing/deslop/a11y/artdirection judge these 4:
  home-light, home-dark, symptoms-light, symptoms-dark
Dimension adversarial judges these 13:
  home-light, home-dark, symptoms-light, symptoms-dark, library-light, library-dark,
  directory-light, directory-dark, recorder-light, recorder-dark,
  mobile-home-light, mobile-symptoms-light, mobile-library-light

## Judges
- MiMo v2.6-pro (thinking-on, budget ladder 20k/32k/48k) via nucbox mimo-dim.py
- GLM-5.3-Flash via `zcode -p --attach` (same rubric text per dimension)

## Rubrics
The eight rubric texts in /tmp/ha-vr/rubrics.json at manifest time, sha256 recorded below.

## Judgments run once, as-is. No selective re-runs.
rubrics sha256: f5e7f33f4803df130618e921693a2378047c3ec98e5af86c0dbda09dc9f2551e
