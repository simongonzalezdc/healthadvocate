# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added — 2026-09-24/25 ship
- **Appeal-letter generator** (F1a): denial + records → complete appeal letter via the
  local champion lane; INFERRED-labeled, source-cited, editable, .txt download, print
  view; entry points from insurance, bills, and the library.
- **Share-safe pack** (F1b): `POST /api/privacy/share-safe` strips names/dates/phones/IDs
  on-device (OpenMed PII deidentifier, in-process, zero network); type-labeled masks,
  per-type counts, refuse-unsafe guard; button on document decode (copy/download).
- **Four user color themes** — gold (default) / rose / moss / blue swatches in the header
  (WAI-ARIA radiogroup, arrow-key nav, persisted, light + dark each).
- **The reading-nook art direction**: painterly scene (window glow, bookshelf, pothos,
  lamp pool, the friend placing a stamped coffee-ringed denial letter, steaming tea),
  per-view scene fragments + hand-notes (EN/ES), rubber-stamp eyebrow, custom warm icons
  (stitched-heartline ECG, wax-seal letter, coffee-ring receipt), felt texture + layered
  warm shadows, frosted header.
- **i18n frame**: HA.t with authored-English fallback, data-i18n bindings, EN/ES
  catalogs (~500 keys, parity-tested), auto-cycling language toggle; adding a language
  is one file + one script tag.
- **Build stamp**: `/api/version` + footer `build <sha>` — staleness is one glance.
- Design-system gates as tests: named-color census, four-role radius census, contrast
  matrix (4 themes × light/dark), theme-layering pin, alignment probe, theme-dots probe.

### Changed
- One-measure alignment (920px everywhere; --grid-max subsumes --max-w + panel literal).
- 5-step type scale (13/15/18/28/40) with full migration map; script font ≥16px.
- AA contrast enforced across all four themes in both modes (9 violations fixed).
- Service worker: network-first static + cache v3 (stale first-paint killed).
- ax-audit: SC 4.1.3 "residual" retired (instrument bug — stale needle + snapshot race).
- Suite grew to 402 tests + 241 subtests; acceptance 35.

### Design
- S+ certification honestly BLOCKED at blind-audit median 8 (3 pre-registered two-judge
  rounds; thresholds never moved). Receipts: docs/design/audit-2026-09-24/ and -09-25/.


### Added
- **Design system: "a warm paper clinic"** (2026-09-24,
  `feat/design-system-20260924`). `docs/DESIGN-SYSTEM.md` is the committed
  source of truth: nine interview dimensions decided from the product truths,
  primitives → semantic tokens → legacy aliases in `static/styles.css` (all
  existing class contracts preserved), a type scale on a deliberate system
  stack (the Google Fonts CDN is REMOVED — a privacy-absolute, local-first
  tool makes zero third-party requests), a 4px spacing ladder, restrained
  motion tokens, and the **Honesty Lane** as the signature system:
  NEEDS_HUMAN / unavailable / urgency verdicts are mutually exclusive visual
  species; unavailable stays neutral-dashed; HIGH gains a non-color dot;
  the recording pulse is the product's only glow. Coverage risk chips moved
  off raw dark-only hexes onto tokens. Scroll-reveal no longer hides content
  without JS (pending-marker pattern + bfcache restore).
- **Call Recorder (demo mode)** + `docs/CALL-RECORDER-SPEC.md`. Consent
  screen (fail-closed start), recording state (pulse, timer, waveform,
  sticky stop bar), live transcript with speaker turns where interim text is
  visually distinct from final and `[inaudible]` is an honest gap, post-call
  summary with provenance-labeled analysis and an unverified deadline
  rendered through the NEEDS_HUMAN discipline. Clearly badged synthetic
  demo — no audio backend; the spec covers local ASR options
  (whisper.cpp/Vosk/offline SpeechRecognizer), consent law notes, and the
  privacy boundary integration.
- **Library, Directory, "What's coming up"** (demo views) +
  `docs/PROACTIVE-CATALOG-SPEC.md`: catalog with filters/search and per-matter
  timeline; self-building provider directory with field-level provenance
  (extracted / inferred / user-confirmed — confirmed is the only solid
  species and overrides inference; one-tap confirm; merge notes with source
  lists; tel:/mailto: fire on tap only); home reminder cards
  (upcoming/due-soon/overdue/done) with one-tap call actions and a due-soon
  header badge. Encrypted-at-rest storage schema, typed-decision analysis
  pipeline, merge rules, and local-notifications design specified.
- **PWA (CEO amendment)**: web app manifest (standalone, token theme colors,
  PNG/SVG icons generated with stdlib python — no new dependencies), service
  worker at `/sw.js` (scope `/` via header) caching STATIC ASSETS ONLY —
  `/api/*` is never cached or intercepted (no patient data in the SW cache;
  no push, no network), installability meta (theme-color per scheme,
  apple-touch-icon), guarded SW registration. Mobile-first: 40–48px touch
  floors, coarse-pointer bumps, sticky recorder bar in the thumb arc.

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
- **Model-off urgency is honest, not an alarm** (adversarial-audit
  findings 1/2/4, 2026-09-24): with the model runtime off (the
  default), `unavailable_structured_fallback` now carries
  `urgency: "unavailable"` instead of a guessed `"medium"` — the
  previous value surfaced a fabricated MEDIUM on 8 of 9 generative
  endpoints. On the symptom surface the typed decision layer gained a
  deliberate exception to the conservative escalation:
  `external_urgency(..., no_judgment=True)` maps the
  `_model_blocked` no-judgment leg (no candidate answer exists) to
  the honest `UNAVAILABLE_URGENCY` instead of
  `CONSERVATIVE_URGENCY` ("high"), which had made "model off"
  indistinguishable from a real emergency. The safety guarantee is
  otherwise unchanged and pinned: every NEEDS_HUMAN leg that involves
  a real or unrejected judgment — unparseable `_raw_text` model
  output, deidentification failure, invalid receipt, out-of-rubric
  pick — and every NER/LLM urgency disagreement still escalates to
  conservative "high", and disagreement dominates the no-judgment
  waiver. The frontend passes `"unavailable"` through `safeUrgency`
  (previously collapsed to a guessed MEDIUM badge), renders it with a
  deliberately neutral `.urgency-unavailable` badge (no coral alarm),
  and renders the `NEEDS_HUMAN` wrapper (`urgency_decision`) that the
  backend already ships — reason, gate state, allowed next steps, and
  an emergency-services line — instead of silently dropping it.
  Pins: `tests/test_model_off_honesty.py`,
  `tests/test_symptom_triage_jev.py` (contract updated),
  `tests/test_docs_honesty.py` (README claim now pinned to code, not
  prose), `tests/test_frontend_model_off_honesty.js`.
- **Insurance denial-reason classification routes through the HA-JEV>>>>>>> ed14a17 (fix(honesty): model-off urgency is an honest 'unavailable', not an alarm; NEEDS_HUMAN wrapper rendered; 2 XSS escapes; docs complete)
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

### Security
- **Two markup-injection escapes in the frontend** (adversarial-audit
  findings, 2026-09-24): `renderCommunity` interpolated
  `data.credibility.toUpperCase()` into `innerHTML` unescaped
  (app.js) — raw model output, so a crafted credibility value parsed
  as live markup — now escaped (uppercased before escaping; entities
  are case-sensitive); `renderTrackDashboard` interpolated the
  `active`/`monitoring`/`resolved` counters unescaped — now escaped as
  defense-in-depth like every sibling field. Synthetic-payload render
  proofs: `tests/test_frontend_model_off_honesty.js`.

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
  the code (80%+, not 90%+). The configuration table now documents every
  environment variable the package reads (9, was 5): the four missing
  ones are `HEALTHADVOCATE_BIND_HOST` (the loopback-only bind that the
  fail-closed startup check enforces), `HEALTHADVOCATE_CASE_DIR`
  (encrypted Coverage Case storage), `HEALTHADVOCATE_CMS_TIC_ENABLED`,
  and `HEALTHADVOCATE_POLICYENGINE_ENABLED` (both off-by-default
  adapter feature flags) — pinned by a test that cross-checks the table
  against every env read in the code. Pins: `tests/test_docs_honesty.py`.

### Dependencies
- `fastapi`, `uvicorn`, `pydantic`, `openai`, `openmed`, `faker`, `pysbd`,
  `transformers`, `huggingface-hub`, `accelerate`, and `tokenizers` pinned to
  current minor releases; `actions/checkout` and `actions/setup-python` bumped.

---

## 2026-05-20 — Initial changelog

### Added
- Initial changelog file so release and repository health tooling have a
  canonical change log.