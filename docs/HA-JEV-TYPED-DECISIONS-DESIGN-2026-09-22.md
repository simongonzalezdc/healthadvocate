# HA-JEV — typed, calibrated decisions for HealthAdvocate — design — 2026-09-22

Owner: PM-HEALTHADVOCATE (session 3, CEO order: "is openmed doing anything to
incorporate that type of model? if not, we should for us. on HA."). Status:
DESIGN STAGED — not implemented; lands as PRs after the Wave-1 push decision.

## 1. What Jev is (org dossier, 2026-09-16 — TYPESAFE-JEV-RLCD-DOSSIER)

Jev = TypeSafe AI's first "System One Model" (launched 2026-09-15, early access):
non-autoregressive, input = unstructured state + typed questions, output =
**typed structured values with calibrated probabilities** — never prose. Three
primitives: **Choice** (pick from ≤255 options), **Score** (ordered rubric,
per-level probability + confidence), **Noul** (yes/no claim, calibrated
probability). Named for Jevons; the class name borrows Kahneman's fast System 1.
Vendor-reported 70–500ms latency, ~$0.042/M input tokens; accuracy BELOW frontier
LLMs on their own benchmarks — the value is speed × cost × **calibration** (a
model that knows when it doesn't know), not raw judgment quality.

The Prose→Code program's gloss — "identification owed before assessment" — is
the org's reading of the class: classify/identify with calibrated confidence
BEFORE any pipeline assesses, judges, or acts.

## 2. Does openmed incorporate that type of model? — NO (verified at 2.5.0)

Evidence (reference clone @ `b161a18f`, searched 2026-09-22):
- Zero hits for typesafe / system-one / typed-question / decision-primitive /
  noul across the entire 2.5.0 tree (code + docs).
- No non-autoregressive typed-decision primitive exists; openmed remains
  classic transformers NER/PII + policy pipeline.
- Two Jev-ADJACENT fragments (pattern-level, not model-class):
  1. `openmed/clinical/routing.py` — "Classify a note locally and resolve its
     extraction profile" + `note_router.py::route_note_sections`: an
     identify-then-extract ordering at the pipeline level.
  2. `calibration_thresholds_path` threaded through deidentify paths
     (`core/pii.py`, `aio.py`, `core/document_stream.py`): calibration as a
     tuning input, not as a typed output contract.

Conclusion: the TYPE is not incorporated upstream — we build it for us, as the
CEO ordered.

## 3. HA's fit — the DNA already points here

- HA's Commitment Gate already IS Jev-shaped in spirit: classify intent →
  act-class intents fail closed → "blocked: … requires a human decision outside
  this application." Identification before action, calibrated by policy, not
  prose.
- HA's PrivacyBoundary + fail-closed release gate are the same discipline at
  the data layer.
- The Prose→Code program's Typesafe-AI watch row says it directly: typed
  outputs make products code-consumable/verifiable by construction.

## 4. Design — the HA-JEV typed-decision layer

**Module:** `healthadvocate/decisions/` (new; no change to existing surfaces
until each converts).

**Consensus amendments (RALPLAN-class Critic requirements, applied 2026-09-22
before J1 code — the loop's apply step; round receipts in the workflow run):**
(a) the receipt is a REQUIRED pydantic argument of the public assess API, and a
static gate tripwire test (the TestNoVendoredShadow pattern,
tests/test_openmed_contract.py:178) pins that no assess entry point exists
without it; (b) NEEDS_HUMAN is a WRAPPER outcome carrying the numbers — never
a sentinel inside ChoiceAnswer.value or ScoreAnswer.level — and J1 tests pin
all four fail-closed legs: below-threshold, threshold-data-missing-or-malformed,
unknown-runner, invalid-receipt; (c) cross-field validation at the schema layer:
value ∈ options, options non-empty/unique/≤255, level indexes the rubric,
per_level_probabilities length == rubric length and sums ≈ 1, probabilities
and confidences ∈ [0,1], answers reference their question ids; (d) a
score_source (raw|calibrated) honesty field on local-ml answers; (e) the
hosted-jev stub is INERT — no URL, no HTTP client, no env read — and J3 is an
ADDITIVE CEO-gated policy tier that leaves assert_loopback_model_url
(healthadvocate/adapters/endpoint_policy.py:87-118) and
PrivacyBoundary.assert_model_allowed (healthadvocate/privacy/boundary.py:162-179)
untouched; (f) no parallel vocabulary — reference the existing Intent/GateState
types (healthadvocate/coverage/commitment_gate.py:10-36); (g) every NEEDS_HUMAN
outcome carries the numbers plus deterministic allowed_next_steps
(commitment_gate.py:192-196 pattern).

**Round-2 amendment (Architect review of the landed design, applied 2026-09-22;
the threshold-provenance half of the same round is written into the calibration
honesty rule below and the J1/J2 stages in §5):**
(h) the assessor allowlist is pinned by DERIVATION, not by name list: a second
static gate tripwire AST-walks `healthadvocate/core/` collecting module-level
public functions whose first positional parameter is `engine`, and asserts
`derived == ALLOWLIST` as set equality. The frozen ALLOWLIST is the nine entry
points that walk finds in this tree (AST-verified 2026-09-22):
`assess_symptoms` (core/symptom_assessor.py:10), `fight_denial`
(core/insurance_fighter.py:10), `decode_bill` (core/bill_decoder.py:13),
`decode_document` (core/document_decoder.py:10), `prepare_appointment`
(core/appointment_prep.py:10), `scan_bulletin` (core/community_health.py:10),
`translate_discharge` (core/discharge_translator.py:10), `check_drug`
(core/drug_checker.py:10), `create_brief` (core/second_opinion.py:10). The
assertion fails on ANY addition — a new engine-consuming assessor cannot
appear in `healthadvocate/core/` without an explicit design decision — and
J2+ conversions REMOVE entries as surfaces move behind the receipt contract,
so the ALLOWLIST only ever shrinks. Exclusion is by scope, never by exemption:
`structured_model_call` (healthadvocate/privacy/gated_model.py:16) also takes
the engine first but is model plumbing, not an assessment surface — the
walk's scope (`healthadvocate/core/` only) excludes it; `evaluate_intent`
(healthadvocate/coverage/commitment_gate.py:175) takes `raw_intent`, not an
engine, so it never enters the derived set and needs no exemption. A
name-based grep is not an acceptable derivation for this tripwire: only one
of the nine names contains "assess", so a grep satisfies the letter while
exempting nothing that matters — the prose-only-tripwire failure mode the
mechanical-derivation requirement exists to close.

**Question schemas (pydantic, typed, no prose):**
- `ChoiceQuestion(id, options: list[str] (≤255), context_ref)` →
  `ChoiceAnswer(value: str, probability: float, confidence: float)`
- `ScoreQuestion(id, rubric: list[ScoreLevel])` →
  `ScoreAnswer(level: int, per_level_probabilities, confidence)`
- `NoulQuestion(id, claim: str)` → `NoulAnswer(probability_true, confidence)`

**Identification-before-assessment contract (the load-bearing rule):**
every assessment surface (symptom triage, denial classification, bill
category, coverage intent) must carry an **identification receipt** — entity
classes found, coverage notes, model used, confidences — produced by the
identify stage (openmed NER + rules). No receipt → no assessment → the
fail-closed sentence. This generalizes the Commitment Gate to every decision
point.

**Calibration honesty rule:** an answer below its confidence threshold is not
a best guess — it is `NEEDS_HUMAN` with the calibrated numbers attached
(audit trail, not silence). Thresholds per question class, stored as data
(upstream's `calibration_thresholds_path` mechanism is the natural carrier
post-2.5.0-bump). Threshold provenance is a shipping condition: per-question-
class thresholds must be derived from MEASURED confidence distributions on
each converted surface before that surface's below-threshold leg goes live —
a threshold invented from defaults is not a threshold. Until measured data
exists for a surface, `threshold-data-missing-or-malformed` fails closed
(structural leg (b)) and the surface answers `NEEDS_HUMAN` — never a default
threshold. J1 accordingly ships NO production threshold defaults; thresholds
exist only in synthetic test fixtures.

**Runners (pluggable behind the existing model gate pattern):**
1. `code` — deterministic rules where the four-question test says code wins
   (default; most current decision points).
2. `local-ml` — openmed NER/PII confidences + calibrated thresholds feeding
   typed decisions (no new models required).
3. `hosted-jev` — the actual Jev API. OFF by default and **CEO-gated forever**:
   hosted = cloud call = external act + likely spend; permitted only on
   DEIDENTIFIED text, behind the PrivacyBoundary model-destination gate, with
   the waitlist/early-access status and non-OpenAI client shape noted in the
   dossier. Zero active code path until the CEO's dated word.

**Prose→code receipts:** contract tests pinning schema round-trips, calibration
field presence and ranges, fail-closed-below-threshold, receipt-required, and
no-hosted-runner-without-gate-flag. These are the tripwire class proven this
session (19 contract tests, both-legs method).

**Canary PHI-free tripwire (Critic requirement, J1-blocking):** the J1 test
suite must build an IdentificationReceipt and a NEEDS_HUMAN outcome from
canary-bearing synthetic input — CANARY = "CANARY_PATIENT_ALPHA_9f3c",
CANARY_MEMBER = "MEMBER-ID-SYNTH-42" (tests/test_privacy_boundary.py:33-34) —
and then assert the SERIALIZED receipt/answer/wrapper JSON contains neither
canary nor raw entity text. Grounds: `_extract_entities` stores raw entity
text plus offsets in EntityMatch (healthadvocate/core/engine.py:59-66), so a
naive receipt would leak exactly what the privacy boundary exists to strip.

## 5. Staged implementation (right-sized waves; HoP scope call per the plan)

- **J0 (this doc):** design staged; RALPLAN addendum recorded (CEO-ordered;
  gets its own Architect/Critic pass before code lands).
- **J1:** schema + gate skeleton + contract tests (one small PR, synthetic
  fixtures only — and explicitly NO production threshold defaults: thresholds
  appear in synthetic test fixtures and nowhere else), INCLUDING the canary
  PHI-free tripwire, the assessor-allowlist pin (h), and the four fail-closed
  legs above; the revised design doc lands on the branch with it.
- **J2:** convert surfaces in (frequency × failure-cost × token-cost) order —
  first candidates: coverage Commitment Gate intents (already classified),
  denial-reason Choice, symptom-triage Score. Each conversion pays for its
  below-threshold leg with measured data, never defaults: per-question-class
  thresholds are derived from measured confidence distributions on that
  surface BEFORE the leg goes live; a surface without measured data answers
  NEEDS_HUMAN. Converting a surface removes it from the (h) ALLOWLIST.
- **J3 (optional, CEO-gated):** hosted-jev runner behind the destination gate.

## 6. Guardrails

Synthetic-only inputs; fail-closed posture unchanged; local-first default;
nothing leaves the workspace; no spend; no medical-claim surface authored;
hosted runner = CEO gate (money/keys/external). Health-data class law governs
every word of this design.
