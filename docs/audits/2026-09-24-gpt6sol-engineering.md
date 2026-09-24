# HealthAdvocate functional-features engineering red-team

Status: DONE_WITH_CONCERNS

**BLUF — REFUTE, confidence 9/10.** The repository contains a broad prototype and several unusually careful fail-closed components, but the shipped product does not support its headline feature claims end to end. The documented quick start leaves the model disabled, the Coverage UI cannot author the case data it claims to organize, CI cannot reproduce the advertised environment, and the green test count mostly verifies isolated contracts rather than user-visible behavior.

## Pre-registered criteria

I would confirm the product claims if: (1) the documented clean install and run path enabled the advertised features; (2) every named feature had a reachable UI/API implementation with realistic success and failure behavior; (3) tests exercised HTTP routes, actual frontend flows, and clean dependency installation; (4) CI gated the claimed test, security, dependency, and browser checks; and (5) readiness reflected model/NER availability. I would refute them if onboarding silently disabled core behavior, prominent workflows were read-only shells, tests substituted source-string checks and stubs for end-to-end behavior, or CI and lock claims did not match committed automation.

## Findings, ranked

### 1. CRITICAL — The documented quick start leaves every generative feature disabled

README tells the operator to start LM Studio, set only `LM_STUDIO_URL`, and launch uvicorn, ending with “That's it” (`README.md:134-147`). Runtime use is separately gated by `HEALTHADVOCATE_MODEL_ENABLED`, whose default is false (`healthadvocate/core/llm_client.py:24-37`). The documented default model is `meditron3-8b` (`README.md:180-184`), while code defaults to `local-model` (`healthadvocate/core/llm_client.py:29`). Therefore the documented path never calls the loaded model and cannot deliver the claimed document, bill, drug, appointment, discharge, second-opinion, or community outputs. README's limitation says absence of LM Studio makes endpoints “return errors” (`README.md:352-356`), but the implementation returns a synthetic success-shaped fallback instead (`healthadvocate/core/llm_client.py:190-204`).

### 2. HIGH — Model failure is rendered as a plausible assessment, not a degraded state

On disabled/blocked/failed transport, the shared fallback emits `urgency: "medium"`, generic Coverage-workflow actions, and `_model_blocked: true` (`healthadvocate/core/llm_client.py:190-204,230-259`). Primary renderers display urgency, explanation, and actions without checking `_model_blocked`; the symptom renderer is representative (`healthadvocate/static/app.js:323-369`). This means a document decode, bill review, drug check, appointment plan, or discharge translation can visibly resemble a completed result while actually containing no domain answer. The generic instruction to “Continue with the manual Coverage workflow” is also irrelevant on most surfaces.

### 3. HIGH — Coverage Continuity is mostly a read-only UI shell

README says a user can build a case organizing deadlines, providers, medications, evidence, contacts, and scripts (`README.md:76-77`). The UI can create a case, read its view, fetch scripts, and check a commitment intent (`healthadvocate/static/app.js:93-197`); it only displays evidence, contacts, and targets (`healthadvocate/static/index.html:354-395`). It exposes no controls for adding evidence, contacts, targets, facts, deadlines, exporting, deleting, listing, or resuming, even though backend routes exist (`healthadvocate/app.py:348-377,414-521`). The current case ID exists only in the page object's `_coverageCaseId` (`healthadvocate/static/app.js:93-110`), so a reload disconnects the user from persisted cases. A non-expert cannot perform the claimed workflow through the product UI.

### 4. HIGH — The reproducible lock and CI-gate claims are false in the committed tree

`requirements.lock.txt` claims to be a transitive lock and gives a rebuild command (`requirements.lock.txt:1-8`) but contains no requirements at all. The runtime manifest mostly uses lower bounds rather than pins (`healthadvocate/requirements.txt:1-18`), contradicting CHANGELOG's claim that dependencies are pinned to current minors (`CHANGELOG.md:79-82`). CI selects Python 3.11 and immediately runs tests without installing dependencies (`.github/workflows/ci.yml:22-31`), then compiles a deleted `openmed` path (`.github/workflows/ci.yml:33-34`). It has neither gitleaks nor pip-audit despite design documentation claiming four gates (`docs/OPENMED-UPSTREAM-LEVERAGE-2026-09-17.md:41-43,167-171`). A clean runner cannot establish the environment whose success is being reported.

### 5. HIGH — The 320+219 green suite does not pin the product's actual behavior

The supplied Python 3.13 venv does produce `320 passed, 219 subtests`; that count is honest. But no test uses `TestClient`, `AsyncClient`, or any `/api/` route. Primary feature behavior is directly tested only for symptom triage and denial classification; document, bill, drug, appointment, discharge, second-opinion, community, family, and tracks are merely named in an AST allowlist or not exercised. Several frontend tests assert source substrings rather than execute behavior (`tests/test_presentability.py:42-87`; `tests/test_coverage_workflow.py:92-104`). MCP has two shallow tests (`tests/test_agent_surfaces.py:4-17`). The browser audit itself states it covers only home, symptoms, and coverage (`tests/browser/ax-audit.js:2-6`), and the Makefile says browser batteries are not in CI (`Makefile:1-3`). CI uses unittest discovery, which locally reported 293 tests rather than pytest's advertised 320 plus 219 subtests.

### 6. HIGH — `/api/health` can say “ok” when the product cannot perform inference

Startup tries to create three model pipelines but catches and logs every failure (`healthadvocate/core/engine.py:102-122`). The health endpoint then returns a constant `{"status":"ok"}` without checking the NER models, local LLM, keyring, or coverage store (`healthadvocate/app.py:227-229`). Operators and the CLI/MCP health tool can therefore receive a green status for a functionally unavailable application.

### 7. HIGH — The “dual-layer cross-validation” claim overstates a substring heuristic

README calls the two layers independent and says they “cross-validate each other” for a reliable assessment (`README.md:46-47,84-111`). The validator collects entire summary/action/red-flag strings as “entity texts,” performs substring matching, and labels an empty-vs-empty result high reliability (`healthadvocate/core/cross_validation.py:25-52,55-92`). Its only urgency override is a fixed 13-term exact-match set plus an NER confidence threshold (`healthadvocate/core/cross_validation.py:19-23,94-102`). This is not independent clinical validation and cannot justify the product's reliability language.

### 8. MEDIUM — “Any document” and “every charge” are silently reduced to the first 2,000 characters

The API accepts up to 50,000 characters (`healthadvocate/app.py:52,66-71`), while document, bill, discharge, and second-opinion prompts silently slice deidentified input to 2,000 characters (`healthadvocate/core/document_decoder.py:33-38`; `healthadvocate/core/bill_decoder.py:25-30`; `healthadvocate/core/discharge_translator.py:24-29`; `healthadvocate/core/second_opinion.py:24-29`). The UI provides no truncation warning. This directly conflicts with “Paste any medical document” and “extracts every charge” (`README.md:52-56`) and can omit later-page instructions or charges.

### 9. MEDIUM — Bill decoding is currency extraction plus unconstrained model opinion

The deterministic bill logic matches every dollar-formatted number, sums all matches, and creates descriptions from nearby characters (`healthadvocate/core/bill_decoder.py:10,19,46-57`). It does not distinguish charge, total, adjustment, payment, or balance, so normal bills can be double-counted. Suspicious charges and billing rights come entirely from LLM fields (`healthadvocate/core/bill_decoder.py:62-67`) rather than coding rules or authoritative billing data. That does not meet “extracts every charge” or “flags suspicious or duplicate items” (`README.md:52-53`).

### 10. MEDIUM — Drug checking has no drug-information source

The feature runs a drug-name NER check, then asks the LLM for class, generic availability, side effects, warnings, and interactions (`healthadvocate/core/drug_checker.py:10-37`). The optional RxNorm/DailyMed/openFDA adapters are separate fixture-backed Coverage endpoints, not used by Drug Checker (`healthadvocate/adapters/medications.py:1,13,40-43,78-80,112-114`). The returned drug facts therefore have no source, date, label version, or evidence trace, despite README promising drug information, safety warnings, and cheaper alternatives (`README.md:58-59`).

### 11. MEDIUM — Local inference has no capacity or latency engineering

One global `HealthEngine` is created for the entire process (`healthadvocate/app.py:50`), model initialization is lazy through one loader (`healthadvocate/core/engine.py:90-100`), startup sequentially preloads three transformer pipelines (`healthadvocate/core/engine.py:102-122`), and each OpenAI-compatible request may occupy a worker for 60 seconds (`healthadvocate/core/llm_client.py:155-163`). Routes move synchronous work to a threadpool (`healthadvocate/app.py:235-304`) but provide no queue, admission control, cancellation, concurrency cap, model-runtime probe, or overload response. No performance/load test exists. A single-slot local runtime can accumulate requests while the UI has no request timeout or cancellation (`healthadvocate/static/app.js:6-32`).

### 12. MEDIUM — Docker is a different, unqualified runtime path

CI runs Python 3.11 (`.github/workflows/ci.yml:22-25`), the task's validated venv is Python 3.13, and Docker uses `python:3.14-slim` with floating dependencies (`Dockerfile:1-12`). Compose explicitly disables the model (`docker-compose.yaml:8-10`) and supplies no model service, model weights, or setup path. The container preloads OpenMed models at startup (`healthadvocate/app.py:73-86`) but the image does not bundle them. There is no Docker build/smoke gate. Thus the nominally easiest operational path cannot deliver the headline features and is not covered by the reported test evidence.

### 13. MEDIUM — CLI and MCP are separate canned helpers, not alternate product surfaces

CLI visit questions and denial checklists return static templates with user text interpolated (`healthadvocate/cli.py:26-67`); they do not call the web API, HealthEngine, Coverage store, typed-decision layer, or model. MCP wraps those same functions and a health GET (`healthadvocate/mcp_server.py:9-48`). It exposes none of the named symptom/document/bill/drug/discharge/second-opinion/Coverage capabilities. Calling these “agent surfaces” is accurate only for two small preparation templates, not for the product.

### 14. MEDIUM — The single-file frontend is below a credible 2026 product baseline

All navigation, networking, rendering, state, accessibility helpers, and eleven feature flows live in one 949-line global object (`healthadvocate/static/app.js:3-949`). Fetch helpers have neither timeout nor abort handling and tell a loopback user to check their “internet connection” (`healthadvocate/static/app.js:6-32`). There is no URL routing, refresh recovery, request cancellation, offline/readiness state, schema validation, or feature-level telemetry-free diagnostics. Static string tests cover broad code presence, while only three browser journeys run outside CI. This structure makes regressions between API schemas and renderers cheap to introduce and hard to detect.

### 15. LOW — API documentation and validation drift is already visible

README documents Coverage view and script endpoints as POST (`README.md:242-243`), while implementation defines GET (`healthadvocate/app.py:325-345`). Several request fields lack the shared length bound—including drug name, appointment concern, denial patient info, provider query, family data, and track data (`healthadvocate/app.py:129-154,204-220,530-532`)—while only selected text fields call `_validate_length`. Error shapes also vary: some core functions return `{error: ...}` with HTTP 200 and others raise HTTP exceptions. These inconsistencies are not caught because there are no route tests.

## Surface-by-surface verdict

- **Symptoms:** implemented and comparatively well unit-tested, but onboarding disables its model; “cross-validation” and fallback presentation overclaim reliability.
- **Documents:** prompt wrapper with NER; untested behavior, silent 2,000-character truncation, blocked-model response looks complete.
- **Bills:** dollar regex plus prompt; no bill-structure or duplicate-charge logic, no behavioral tests.
- **Insurance:** denial classification has strong isolated typed-decision tests; appeal quality, HTTP route, and UI behavior remain untested.
- **Drugs:** NER plus unsourced LLM facts; authoritative adapters are disconnected; no behavioral tests.
- **Appointments:** prompt wrapper; CLI is a separate canned template; no feature or route test.
- **Discharge:** prompt wrapper, silent truncation, no behavior test; fallback can masquerade as a translation.
- **Second opinion:** prompt wrapper, silent truncation, no behavior test.
- **Community scanner:** prompt-only credibility judgment with no retrieval/citations; no behavior test.
- **Family/tracks:** in-memory CRUD is implemented, intentionally lost on restart (`healthadvocate/core/family_tracker.py:8-10`; `healthadvocate/core/health_tracks.py:8-10`), but no tests pin it and “context flows into every other feature” is false because community scanning accepts no profile (`healthadvocate/app.py:153-154,298-304`).
- **Coverage:** backend is the deepest feature, but the browser exposes only create/read/scripts/gate and loses its selected case on refresh.
- **CLI/MCP:** operationally small static-template helpers, not equivalent access to product features.

## Counter-case

The strongest defense is that this is explicitly pre-user and synthetic-only, the model is deliberately opt-in, fallback paths avoid raw failures, Coverage has unusually strong domain/governance tests, and the pytest result is genuinely green. The source also shows careful XSS escaping, accessibility intent, loopback defaults, deterministic commitment gating, and typed fail-closed decisions. Those are real strengths. They do not rescue the product claims because the default documented journey never enables the core model, the most mature workflow is not operable through its UI, and neither clean installation nor HTTP/UI behavior is gated.

## What I could not assess

I did not assess clinical correctness, privacy architecture, or mission/market merit, per scope. I could not assess real Meditron/OpenMed output quality, model download size/startup latency, steady-state latency/RAM, concurrent load, OS-keyring behavior, Docker build success, or rendered behavior across browsers because no qualified model assets, benchmark receipts, Docker smoke receipt, or full browser run was provided. I did not treat the existing 320+219 isolated-test result as evidence for those unknowns.

## Top three existential risks

1. **The first-run product is functionally hollow:** official setup silently disables the system that produces nearly every promised answer.
2. **Green evidence can conceal broken delivery:** CI/lock drift and mock/source-level tests permit routes, Docker, model setup, and UI flows to fail while the headline count stays green.
3. **The product overstates weak inference as validation:** substring overlap, unsourced LLM generation, and success-shaped fallbacks can create misplaced confidence in high-stakes outputs.

## Single highest-leverage change

Build one clean-room, model-fixture-backed acceptance gate that installs from a real hash lock, boots the documented runtime, waits for truthful readiness, and drives every named feature through HTTP and the browser in both model-success and model-failure modes. Make that gate mandatory in CI. This single change would force onboarding, dependency, route/schema, fallback UX, and feature-claim drift into observable failures.

## Justice pass

If this verdict is too harsh, the builder bears rework on a promising pre-user prototype. If it is too lenient, patients and family caregivers bear the cost of incomplete, stale, or success-shaped medical and insurance guidance. The latter harm is larger, so the burden of proof properly sits on the product's reliability and operability claims, not on users discovering hidden setup flags or interpreting internal fallback markers.

## Verdict

I would not let a family member use this for symptoms, medications, bills, discharge instructions, or insurance action today. I would allow it only as a supervised synthetic demo of workflow ideas, with a technically capable operator who knows the model is opt-in, recognizes blocked-model responses, and treats every generated statement as unverified. The Coverage backend and fail-closed decision work are worth preserving, but this is not yet a trustworthy patient-facing product.

## Calibration log

2026-09-23 — Claim: HealthAdvocate's named feature set and engineering posture substantiate its README/CHANGELOG claims. Verdict: REFUTE. Confidence: 9/10. Strongest surviving objection: pre-user status and deliberate opt-in defaults reduce the expectation of turnkey operation, but the public quick start and feature language still promise it.

## IMPROVEMENTS

1. **Improve dependency evidence.** WHY: the “lock” contained no packages and CI did not install dependencies. FIX: generate a hash-exact lock from the supported Python version and add a clean-venv install/import test before all other gates.
2. **Improve product-level test honesty.** WHY: 320+219 green checks omitted every FastAPI route and most UI flows. FIX: publish separate unit, route-integration, browser, Docker-smoke, and real-model qualification counts; never aggregate them into one readiness signal.
3. **Improve operator diagnostics.** WHY: `/api/health` stayed green through model-load failures and fallbacks looked like results. FIX: add component readiness plus a persistent, surface-specific degraded-mode banner with retry/setup instructions.
