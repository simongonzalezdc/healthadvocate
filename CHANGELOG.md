# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
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
- **Symptom-triage honesty on model-unavailable outputs (audit D2,
  CRITICAL)** — the documented default build runs with the optional
  local model off, and that build no longer labels every symptom
  HIGH. The triage surface (`healthadvocate/decisions/symptom_triage.py`
  + `healthadvocate/core/symptom_assessor.py` wiring) now distinguishes
  MODEL-UNAVAILABLE outputs (`unavailable_structured_fallback` shape,
  `_model_blocked` marker — model disabled, blocked, or transport
  failure: no structured judgment exists) from
  GENUINELY-ANSWERED-BELOW-THRESHOLD picks. External behavior: the
  model-unavailable leg surfaces urgency `"unavailable"` (a new
  external value, deliberately not a rubric level, so no high badge
  can render) with the deterministic explanation that the optional
  local model is off while deterministic preparation steps remain.
  The safety escalations are untouched and pinned in both directions:
  a genuinely answered below-threshold pick still escalates to
  `"high"`, and every `urgency_disagreement` still dominates the
  carve-out — including SEVERE model-off inputs (see the round-2 Fixed
  entry below). Unparseable model answers (`_raw_text` — the model ran)
  and the deidentification-failed leg keep their conservative
  escalation; the audit wrapper still records below-threshold with
  the zero-measurement numbers. Regression tests:
  `tests/test_symptom_triage_jev.py` (`ModelUnavailableHonestyTests`,
  `BelowThresholdDirectionTests`).
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
- **Severe inputs escalate to HIGH on the model-off default build
  (audit D2 round 2)** — the D2 carve-out had made the README:111
  NER-safety override unreachable with the model off: the fallback
  placeholder urgency is "medium", and the disagreement rule fired
  only on "low", so all 13 NER high-urgency terms (chest pain, stroke,
  …) at ≥0.80 confidence surfaced "unavailable" instead of the
  parent-commit HIGH. `cross_validate` now treats a placeholder
  urgency (`_model_blocked`/`_raw_text` markers) as NO rating — the
  fallback's hardcoded "medium" is never consulted — so the NER
  high-urgency trigger fires as an urgency_disagreement and the
  surface externalizes conservative HIGH with the payload
  self-explaining the escalation. Mild inputs without an NER trigger
  keep the honest "unavailable"; the 0.80 trigger bar and the genuine
  low/medium model ratings are unchanged. Regression tests:
  `tests/test_symptom_triage_jev.py` (`SevereModelOffSafetyTests` —
  all 13 terms, sub-threshold confidence, benign entity, `_raw_text`,
  genuine-medium pins).
- **The symptom glass renders the NEEDS_HUMAN decision wrapper** —
  `renderSymptoms` dropped the entire `urgency_decision` subtree, so
  the wrapper's human-decision reason and deterministic
  `allowed_next_steps` never reached the patient. A
  `needs-human-banner` (`role="alert"`, escaped) now leads the result
  with the wrapper reason and steps, and `safeUrgency` passes the
  backend's `unavailable` value through instead of laundering it to a
  MEDIUM badge — a neutral `.urgency-unavailable` style (no high/danger
  styling) renders the no-judgment state as itself. Pins in
  `tests/test_presentability.py`; browser-frame checks: `tools/browserframe/honesty_matrix.mjs` (glass lane).
- **README honesty (docs audit)** — the Configuration table now
  documents the generative-path environment variables; the full set the code reads (incl. HEALTHADVOCATE_BIND_HOST, HEALTHADVOCATE_CMS_TIC_ENABLED, HEALTHADVOCATE_POLICYENGINE_ENABLED) lands with the docs lane
  (`HEALTHADVOCATE_MODEL_ENABLED` opt-in switch, preferred
  `HEALTHADVOCATE_MODEL_URL`, deprecated `LM_STUDIO_URL` alias,
  `HEALTHADVOCATE_CASE_DIR`, and the corrected defaults:
  `MEDICAL_LLM_MODEL`=`local-model`, loopback default
  `http://127.0.0.1:11434/v1`); the quick start no longer implies the
  LLM runs after exporting only `LM_STUDIO_URL` — it runs fully
  deterministic and points at a new explicit "Enable the optional
  model runtime" section; the Known Limitations "Without it, feature
  endpoints return errors" falsehood is replaced with the real
  fallback behavior; and a "What works with the model runtime off"
  table now exists in the honest-boundaries section.
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