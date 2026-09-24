# Vision-pass receipts — 2026-09-24 (design-system mission, feat/design-system-20260924)

**Judge:** GLM-5.3-Flash (`zai/glm-5.3-flash`), reached through the org's sanctioned
flash-home zcode lane (`HOME=~/.zcode/flash-home`, config model pin fail-closed verified
before every sweep; images attached straight from local disk — no CDN detours, per the
vision-pass law and CEO amendments 4–5 of this mission). Every receipt file carries a
`judged-by:` header line.

**Method:** each screenshot in each audit round gets two targeted GLM-5.3-Flash passes —
a design pass (describe, then P0/P1/P2 defects with locations) and a HONESTY pass (six
fixed questions: needs-human prominence, unavailable neutrality, urgency distinctness,
provenance species, demo badging, emergency strength — ending in `HONESTY-VERDICT`).
Judgment runs on a 620px JPEG copy for latency; the full-resolution original named in the
receipt header is archived in `docs/design/screenshots/<round>/`.

**Corrections of record (CEO amendment 5):** an early probe batch of six screenshots was
judged through the maas/ufileos CDN detour (non-GLM-5.3-Flash endpoint) before the
precision landed. Those judgments were DISCARDED and every screenshot was re-judged
through GLM-5.3-Flash from scratch in round 1 — no CDN-era judgment informs any fix.
A lane-test probe also ran once on the default session model (not Flash) to verify the
attach mechanism; it produced no design judgment and is not cited anywhere.

**Rounds:**
- `r1/` — baseline (pre-fix implementation), full sweep: 56 screenshots, 112 passes.
  Drove the P0/P1 fix batch (home composition, honesty species, dark warmth).
- `r2/` — intermediate state. Shot mid-rebuild; the judge rig lost its image
  directory (`judge-img/r2` was never created — a path component bug), so GLM-5.3-Flash
  **correctly refused to judge 40/56 honesty passes and 27/56 design passes**
  ("I can see no pixels … fabricating an honesty audit without seeing the image would
  itself be the exact failure mode the audit exists to catch"). Those refusals are kept
  as evidence the honesty gate holds; the ~17 partial verdicts that did land were all
  PASS except one stale-capture artifact. Superseded by r3.
- `r3/` — the deciding round, on the interview-derived rebuild (dark-first lamp
  material, serif letter-voice display, vitals green, tightened radii, numbered
  findings). Full sweep, both themes + mobile + interaction states. Per-view verdicts
  for the ship gate come from this round.
- `final/` — reserved for the ship-gate verdict set (same lane, both passes).

Findings that drove code changes are quoted verbatim in the mission report with their
receipt path.
