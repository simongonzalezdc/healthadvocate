# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Glass honesty: the safety truth reaches the screen** (lane B, audits
  E1/E2/D5/D3/B3, 2026-09-24). When a response payload carries a typed
  decision wrapper whose outcome is `NEEDS_HUMAN` (e.g. the symptom
  assessor's `urgency_decision`), `static/app.js` renders a visible
  banner — "This needs a human decision." with the wrapper's
  `allowed_next_steps` list — above any results; the detection helper is
  generic (any payload key shaped `outcome` + `allowed_next_steps`), so
  other surfaces can adopt it without new plumbing. The banner and a new
  Help view name real humans (E2), exactly two widely published US
  crisis lines (988 Suicide & Crisis Lifeline, call/text 988; SAMHSA
  National Helpline, 1-800-985-5990) plus link-only resources
  (HealthCare.gov navigator finder, NAIC state-insurance lookup) and the
  plain-language line "Ask the hospital for the Patient Advocate /
  Patient Relations office" — nothing scraped, nothing invented.
  Urgency value `unavailable` (pairs with the backend honesty lane)
  renders as a neutral "Model unavailable — no urgency assessment was
  made" state with no urgency badge and no high/red styling, defensively
  for either landing order. Browser-level checks in
  `tools/browserframe/honesty_matrix.mjs` (playwright, chromium): the
  fallback-shaped symptoms response renders the banner; `unavailable`
  renders without high-urgency styling; no rendered home/symptoms string
  claims "verified"/"confirmed" (old `Validation`/`Reliability` badge
  strings absent).

### Changed
- `healthadvocate/decisions/` — the HA-JEV typed, calibrated decision layer
  (J1; design `docs/HA-JEV-TYPED-DECISIONS-DESIGN-2026-09-22.md`):
  Choice/Score/Noul question and answer schemas with strict real-float
  probabilities (numpy dtypes accepted; str/bytes/bool/int never coerced),
  the identification-receipt gate (receipt required; missing, invalid,
  canary-bearing, or failed-deidentification inputs fail closed into a
  NEEDS_HUMAN wrapper that carries the numbers), surface-linked measured
  threshold provenance (cross-surface application fails closed; no
  production threshold defaults), and a runner registry (`code` default,
  `local-ml`, and an inert CEO-gated `hosted-jev` stub with no gate flag
  in code). Contract tests in `tests/test_ha_jev_decisions.py`, including
  the canary PHI-free tripwire and the AST-derived assessor-allowlist pin.
- CLI surfaces for appointment prep, denial checklists, and server health
  (`python -m healthadvocate.cli`).
- MCP server surface (`python -m healthadvocate.mcp_server`) with uplifted tool
  descriptions and cache hints.
- `llms.txt` machine-readable project summary for AI tooling and GEO discovery.
- Lightweight CI workflow (test + compile gates on pull requests and `master`).
- Renovate dependency automation configuration.

### Changed
- **Flag honesty (audit B3)**: payload flags no longer overstate what
  happened. Every core surface that reported `pii_scrubbed` now also
  reports `pii_found_and_masked` with honest semantics — true only when
  PII was found and masked; false/absent means none was found, never a
  guarantee that none slipped through (`pii_scrubbed` is kept one
  release with a deprecation comment, then removed). The drug checker's
  `ner_verified` (a dictionary name match presented as verification) is
  joined by `ner_name_match`, and its prompt note now says "recognized
  by name matching". UI copy follows the flags: the document decoder
  states what was found and masked (or that the automated scan found
  nothing, not a guarantee), the drug view says "recognized by name
  matching", and the symptoms cross-check badge is relabeled "Name
  overlap (informal)" — never presented as validation or a Reliability
  score.
- **Insurance denial-reason classification routes through the HA-JEV
  typed-decision layer** (J2-b; design
  `docs/HA-JEV-TYPED-DECISIONS-DESIGN-2026-09-22.md` §5). The free-text
  `denial_reason` the structured model returns is normalized by a
  deterministic `code`-runner rule onto a canonical seven-option set
  (not medically necessary, prior authorization required, experimental
  or investigational, out-of-network, not a covered benefit, formulary
  exclusion, insufficient documentation), then adjudicated by
  `healthadvocate.decisions.assess` on surface `denial-classifier` behind
  the identification-receipt contract: the receipt is built from the
  call's real NER identify stage and states the real privacy-boundary
  deidentification status; thresholds are measured, surface-linked, and
  conservative (1.0 — the deterministic rule's degenerate confidence
  distribution; the provenance records the frozen synthetic measurement
  corpus). Every fail-closed leg — invalid receipt, failed or unknown
  deidentification, unknown or ambiguous pick, below-threshold — maps to
  the surface's pre-existing safe fallback (empty `denial_reason`), with
  the NEEDS_HUMAN wrapper and consumed receipt attached as additive
  audit (`denial_reason_decision`, `denial_reason_receipt`; canary-free
  by construction and pinned so). The public `fight_denial` signature
  and every existing result key are unchanged; the
  deidentify-before-reasoning order is untouched. Contract tests:
  `tests/test_denial_classifier_jev.py`.
- **OpenMed vendoring retired** — the repo-root `openmed/` fork (upstream
  v1.4.0 + 3 local patches, 67 files) is deleted; the runtime is the
  PyPI-pinned package (`openmed[hf]==2.5.0`, exact pin; Renovate offers
  bumps). The `engine.py` sys.path insert that let the vendored copy shadow
  the pip pin is removed. Version-agnostic contract tests
  (`tests/test_openmed_contract.py`) gate the surface HA consumes.
  Rationale + full upstream update list:
  `docs/OPENMED-UPSTREAM-LEVERAGE-2026-09-17.md`,
  `docs/OPENMED-UPSTREAM-CHANGELOG-2026-09-22.md`. Our offset-safe
  `reidentify` patch is superseded upstream (occurrence-aware); the config
  thread-lock patch is dropped (HA never touches OpenMed global config).
- Public repo hygiene hardening; tracked agent session state removed.
- Docker Python base image tag updated to `3.14`.
- README restored to full pre-wave2b content with S+ SEO/GEO public-face pass and
  sibling-repo cross-links.
- `.gitignore` completed (was missing its trailing entry).
- README documents the live Coverage Continuity Track (Features entry,
  project-structure lines for `coverage/`, `privacy/`, `governance/`,
  `adapters/`, the 16 `/api/coverage/*` endpoints in the All Endpoints
  table, and the encrypted-case + Commitment-Gate privacy bullets).

### Fixed
- Incomplete `.gitignore` entry that left local artifacts unignored.

### Dependencies
- `fastapi`, `uvicorn`, `pydantic`, `openai`, `openmed`, `faker`, `pysbd`,
  `transformers`, `huggingface-hub`, `accelerate`, and `tokenizers` pinned to
  current minor releases; `actions/checkout` and `actions/setup-python` bumped.

---

## 2026-05-20 — Initial changelog

### Added
- Initial changelog file so release and repository health tooling have a
  canonical change log.