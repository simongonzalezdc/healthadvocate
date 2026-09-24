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
  National Helpline, 1-800-662-4357 / 1-800-662-HELP — pairing verified against samhsa.gov 2026-09-24; the earlier draft mislabeled the Disaster Distress number) plus link-only resources
  (HealthCare.gov navigator finder, NAIC state-insurance lookup) and the
  plain-language line "Ask the hospital for the Patient Advocate /
  Patient Relations office" — nothing scraped, nothing invented.
  Urgency value `unavailable` — which the backend now emits whenever the
  gated call made no real judgment — renders as a neutral "Model
  unavailable — no urgency assessment was made" state with no urgency
  badge and no high/red styling, defensively for either landing order.
  Browser-level checks in
  `tools/browserframe/honesty_matrix.mjs` (playwright, chromium): the
  fallback-shaped symptoms response renders the banner; `unavailable`
  renders without high-urgency styling; no rendered home/symptoms string
  claims "verified"/"confirmed" (old `Validation`/`Reliability` badge
  strings absent).
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
  score.- **Insurance denial-reason classification routes through the HA-JEV
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
- **No-judgment outputs never surface a fabricated urgency verdict**
  (verified findings, 2026-09-24): with the model runtime disabled (the
  default), a mild symptom input no longer returns `urgency: "high"`
  with a red HIGH badge next to the NEEDS_HUMAN banner — the API and
  the screen now agree that no urgency assessment was made. The
  no-judgment placeholder markers (`_model_blocked`/`_raw_text`, which
  also cover deidentification failure and transport failure) make the
  symptom surface and all eight other llm-backed surfaces
  (documents, bills, insurance, discharge, second opinion, community,
  appointments, drugs) emit the honest `urgency: "unavailable"` via the
  new `healthadvocate.core.llm_client.urgency_from_output`; real-signal
  escalations (NER/LLM urgency disagreement, fail-closed legs on actual
  model responses) still surface the conservative `high`.
- **A NEEDS_HUMAN refusal can no longer silently disappear**
  (drift hole): banner detection keys on `outcome: NEEDS_HUMAN` alone;
  a missing, empty, non-array, or string `allowed_next_steps` still
  renders the banner (defensively formatted) with the named-human
  resources — never a normal-looking answer.
- **Absence is never a MEDIUM verdict**: the UI renders an urgency
  badge only for a real low/medium/high pick; missing, null, or
  unrecognized urgency values render the neutral "No urgency assessment
  was made" notice instead of coercing to a confident MEDIUM badge.
- **The model's silence is no longer fully trusted**
  (`build_urgency_candidate`): a missing or null `urgency` key types to
  no candidate and fails closed (invalid-answer → NEEDS_HUMAN →
  conservative external urgency) instead of defaulting to a
  confidence-1.0 "medium" answer; the compliant `null` and plain key
  omission now behave identically.
- **README configuration honesty**: the Configuration table now lists
  `HEALTHADVOCATE_MODEL_ENABLED` (default `0`, opt-in master switch)
  and `HEALTHADVOCATE_MODEL_URL` (preferred; `LM_STUDIO_URL` marked
  deprecated alias), with truthful defaults
  (`http://127.0.0.1:11434/v1`, `local-model`); the Quick Start sets
  the enable switch explicitly; the Known Limitations bullet no longer
  claims endpoints error without LM Studio — they return HTTP 200
  deterministic fallback payloads with the model-unavailable state.- Incomplete `.gitignore` entry that left local artifacts unignored.

### Docs
- README docs-honesty pass (Lane C, audit C3): new
  "What works without a model" table enumerating every feature surface's
  no-model behavior from
  the real fallback shape (`unavailable_structured_fallback` in
  `healthadvocate/core/llm_client.py`) — deterministic preparation vs
  degraded generative, with urgency documented as an honest "unavailable"
  state rather than an alarm. The configuration table now documents
  `HEALTHADVOCATE_MODEL_ENABLED` (off by default — the switch that makes
  generative features live), `HEALTHADVOCATE_MODEL_URL`, `LM_STUDIO_URL`
  (deprecated alias), and the real `MEDICAL_LLM_MODEL` default
  (`local-model`, not `meditron3-8b`); the contradictory "Without it,
  feature endpoints return errors" claim is retired in favor of the actual
  silent-fallback behavior. New "Why this exists" section states the
  mission plainly (a free tool to help people have some hope against the
  medical system; free, open source, local-first; not a doctor, not a
  diagnosis, not verified medical advice), the hero and quick start are
  aligned with it, and the cross-validation confidence figure now matches
  the code (80%+, not 90%+). Pins: `tests/test_docs_honesty.py`.

### Dependencies
- `fastapi`, `uvicorn`, `pydantic`, `openai`, `openmed`, `faker`, `pysbd`,
  `transformers`, `huggingface-hub`, `accelerate`, and `tokenizers` pinned to
  current minor releases; `actions/checkout` and `actions/setup-python` bumped.

---

## 2026-05-20 — Initial changelog

### Added
- Initial changelog file so release and repository health tooling have a
  canonical change log.