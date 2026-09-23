"""HA-JEV typed-decision layer contract tests (J1, design 2026-09-22 §4-5).

Prose-to-code receipts for docs/HA-JEV-TYPED-DECISIONS-DESIGN-2026-09-22.md:
schema round-trips, calibration honesty, the four fail-closed legs
(below-threshold, threshold-data-missing-or-malformed, unknown-runner,
invalid-receipt), receipt-required, hosted-runner refusal, the canary
PHI-free tripwire, the AST-derived assessor allowlist (h), and the
stripped-errors rule for every wrapper field sourced from a pydantic
ValidationError. Synthetic fixtures only; J1 ships no production
threshold defaults — thresholds appear here and nowhere else.
"""

from __future__ import annotations

import ast
import inspect
import json
import unittest
from pathlib import Path
from typing import get_type_hints

from pydantic import ValidationError

from healthadvocate.coverage.commitment_gate import GateState, evaluate_intent
from healthadvocate.privacy.boundary import DeidentificationStatus
from healthadvocate.decisions import (
    FAIL_CLOSED_SENTENCE,
    HOSTED_JEV_GATE_MESSAGE,
    ClassThreshold,
    ChoiceAnswer,
    ChoiceQuestion,
    DecisionOutcome,
    HostedJevGateError,
    IdentificationReceipt,
    NoulAnswer,
    NoulQuestion,
    ScoreAnswer,
    ScoreLevel,
    ScoreQuestion,
    ScoreSource,
    ThresholdData,
    ThresholdProvenance,
    assess,
    hosted_jev_call,
    question_class,
    receipt_from_analysis,
    runner_names,
    stripped_validation_errors,
)

ROOT = Path(__file__).resolve().parents[1]

CANARY = "CANARY_PATIENT_ALPHA_9f3c"
CANARY_MEMBER = "MEMBER-ID-SYNTH-42"
RAW_ENTITY_TEXTS = (CANARY, CANARY_MEMBER, "Synthetic Patient Name")

# Synthetic threshold fixtures — the ONLY thresholds J1 knows (design §4:
# no production defaults; provenance must be measured, surface-linked).
SURFACE = "symptom-triage-synthetic"
MEASURED_PROVENANCE = {
    "source": "measured",
    "surface": SURFACE,
    "measured_on": "2026-09-22",
    "sample_size": 200,
}


def measured_thresholds(surface: str = SURFACE, **overrides: object) -> ThresholdData:
    """Build a valid measured ThresholdData for all three question classes."""
    entries = {}
    for qclass, min_conf in (
        ("choice", 0.80),
        ("score", 0.75),
        ("noul", 0.70),
    ):
        entry = {
            "question_class": qclass,
            "min_confidence": min_conf,
            "provenance": {**MEASURED_PROVENANCE, "surface": surface},
        }
        entry.update(overrides)
        entries[qclass] = entry
    return ThresholdData.model_validate(
        {"surface": surface, "thresholds": entries}
    )


def synthetic_receipt() -> IdentificationReceipt:
    """A valid receipt built WITHOUT raw entity text (identify-stage output)."""
    return IdentificationReceipt(
        model_used="synthetic-ner-fixture",
        entity_classes=[
            {"label": "Disease", "category": "condition", "count": 2,
             "max_confidence": 0.92},
            {"label": "MemberID", "category": "pii", "count": 1,
             "max_confidence": 0.99},
        ],
        coverage_notes=["synthetic identify stage; no raw text retained"],
        deidentification_status=DeidentificationStatus.SUCCESS,
    )


def choice_question() -> ChoiceQuestion:
    return ChoiceQuestion(
        id="q-urgency",
        options=["self-care", "clinician-visit", "emergency"],
        context_ref="receipt:synthetic-1",
    )


def choice_answer(confidence: float = 0.9) -> ChoiceAnswer:
    return ChoiceAnswer(
        question_id="q-urgency",
        value="clinician-visit",
        probability=0.62,
        confidence=confidence,
    )


class SyntheticEntity:
    """AnalysisResult-entity stand-in carrying RAW text (engine.py:59-66
    shape) — exactly what the receipt must NOT copy."""

    def __init__(self, text: str, label: str, confidence: float) -> None:
        self.text = text
        self.label = label
        self.category = "pii"
        self.confidence = confidence


class SyntheticAnalysis:
    def __init__(self) -> None:
        self.model_used = "synthetic-ner-fixture"
        self.entities = [
            SyntheticEntity(CANARY, "PatientName", 0.91),
            SyntheticEntity(CANARY_MEMBER, "MemberID", 0.99),
            SyntheticEntity("Synthetic Patient Name", "PatientName", 0.84),
        ]


# ---------------------------------------------------------------------------
# Schema round-trips + schema-layer cross-validation (amendment c)
# ---------------------------------------------------------------------------


class SchemaRoundTripTests(unittest.TestCase):
    def test_choice_round_trip(self):
        q = choice_question()
        a = choice_answer()
        dumped = q.model_dump()
        assert ChoiceQuestion.model_validate(dumped) == q
        assert ChoiceAnswer.model_validate(a.model_dump()) == a
        assert question_class(q) == "choice"

    def test_score_round_trip(self):
        q = ScoreQuestion(
            id="q-triage",
            rubric=[ScoreLevel(label="low"), ScoreLevel(label="moderate"),
                    ScoreLevel(label="high")],
        )
        a = ScoreAnswer(
            question_id="q-triage",
            level=1,
            per_level_probabilities=[0.1, 0.7, 0.2],
            confidence=0.88,
        )
        assert ScoreQuestion.model_validate(q.model_dump()) == q
        assert ScoreAnswer.model_validate(a.model_dump()) == a
        assert question_class(q) == "score"

    def test_noul_round_trip(self):
        q = NoulQuestion(id="q-claim", claim="The denial cites medical necessity.")
        a = NoulAnswer(question_id="q-claim", probability_true=0.31,
                       confidence=0.66)
        assert NoulQuestion.model_validate(q.model_dump()) == q
        assert NoulAnswer.model_validate(a.model_dump()) == a
        assert question_class(q) == "noul"

    def test_choice_options_constraints(self):
        with self.assertRaises(ValidationError):
            ChoiceQuestion(id="q", options=[], context_ref="c")  # empty
        with self.assertRaises(ValidationError):
            ChoiceQuestion(id="q", options=["a", "a"], context_ref="c")  # dup
        with self.assertRaises(ValidationError):
            ChoiceQuestion(  # >255 options
                id="q", options=[f"o{i}" for i in range(256)], context_ref="c",
            )
        with self.assertRaises(ValidationError):
            ChoiceQuestion(id="q", options=["a", ""], context_ref="c")  # blank

    def test_probability_and_confidence_ranges(self):
        for bad in (-0.01, 1.01):
            with self.assertRaises(ValidationError):
                ChoiceAnswer(question_id="q", value="a", probability=bad,
                             confidence=0.9)
            with self.assertRaises(ValidationError):
                ChoiceAnswer(question_id="q", value="a", probability=0.5,
                             confidence=bad)
            with self.assertRaises(ValidationError):
                NoulAnswer(question_id="q", probability_true=bad, confidence=0.9)

    def test_answers_reference_question_ids(self):
        with self.assertRaises(ValidationError):
            ChoiceAnswer(question_id="", value="a", probability=0.5,
                         confidence=0.9)


# ---------------------------------------------------------------------------
# Pair-level validation: value ∈ options, level indexes rubric, sums ≈ 1
# ---------------------------------------------------------------------------


class PairValidationTests(unittest.TestCase):
    def test_answer_for_other_question_fails_closed(self):
        outcome = assess(
            choice_question(),
            receipt=synthetic_receipt(),
            candidate=ChoiceAnswer(question_id="q-other", value="self-care",
                                   probability=0.9, confidence=0.95),
            surface=SURFACE, runner="code",
            thresholds=measured_thresholds(),
        )
        self.assertEqual(outcome.outcome, "NEEDS_HUMAN")
        self.assertTrue(outcome.validation_errors)

    def test_choice_value_must_be_an_option(self):
        outcome = assess(
            choice_question(),
            receipt=synthetic_receipt(),
            candidate=ChoiceAnswer(question_id="q-urgency", value="teleport",
                                   probability=0.9, confidence=0.95),
            surface=SURFACE, runner="code",
            thresholds=measured_thresholds(),
        )
        self.assertEqual(outcome.outcome, "NEEDS_HUMAN")
        types = {e.type for e in outcome.validation_errors}
        self.assertIn("value_not_in_options", types)

    def test_score_level_must_index_rubric(self):
        q = ScoreQuestion(id="q-triage",
                          rubric=[ScoreLevel(label="low"), ScoreLevel(label="high")])
        outcome = assess(
            q, receipt=synthetic_receipt(),
            candidate=ScoreAnswer(question_id="q-triage", level=2,
                                  per_level_probabilities=[0.5, 0.5],
                                  confidence=0.9),
            surface=SURFACE, runner="code", thresholds=measured_thresholds(),
        )
        self.assertEqual(outcome.outcome, "NEEDS_HUMAN")
        types = {e.type for e in outcome.validation_errors}
        self.assertIn("level_not_in_rubric", types)

    def test_score_probabilities_length_and_sum(self):
        q = ScoreQuestion(id="q-triage",
                          rubric=[ScoreLevel(label="low"), ScoreLevel(label="high")])
        bad_len = ScoreAnswer(question_id="q-triage", level=0,
                              per_level_probabilities=[1.0], confidence=0.9)
        bad_sum = ScoreAnswer(question_id="q-triage", level=0,
                              per_level_probabilities=[0.5, 0.4], confidence=0.9)
        for candidate in (bad_len, bad_sum):
            outcome = assess(q, receipt=synthetic_receipt(), candidate=candidate,
                             surface=SURFACE, runner="code", thresholds=measured_thresholds())
            self.assertEqual(outcome.outcome, "NEEDS_HUMAN")
            self.assertTrue(outcome.validation_errors)


# ---------------------------------------------------------------------------
# Calibration honesty + the four fail-closed legs (amendment b)
# ---------------------------------------------------------------------------


class CalibrationHonestyTests(unittest.TestCase):
    def test_at_or_above_threshold_answers(self):
        outcome = assess(
            choice_question(), receipt=synthetic_receipt(),
            candidate=choice_answer(confidence=0.9),
            surface=SURFACE, runner="code", thresholds=measured_thresholds(),
        )
        self.assertEqual(outcome.outcome, "ANSWERED")
        self.assertEqual(outcome.answer, choice_answer(confidence=0.9))
        self.assertEqual(outcome.threshold_applied, 0.80)
        self.assertEqual(outcome.gate_state, GateState.ALLOWED)

    def test_below_threshold_is_needs_human_with_numbers_attached(self):
        candidate = choice_answer(confidence=0.55)
        outcome = assess(
            choice_question(), receipt=synthetic_receipt(), candidate=candidate,
            surface=SURFACE, runner="code", thresholds=measured_thresholds(),
        )
        self.assertEqual(outcome.outcome, "NEEDS_HUMAN")
        # The numbers ride IN the wrapper — never a sentinel in value/level.
        self.assertEqual(outcome.answer, candidate)
        self.assertEqual(outcome.answer.value, "clinician-visit")
        self.assertEqual(outcome.threshold_applied, 0.80)
        self.assertTrue(outcome.reason)
        self.assertTrue(outcome.allowed_next_steps)
        self.assertEqual(outcome.gate_state, GateState.REVIEW_REQUIRED)

    def test_needs_human_steps_are_deterministic(self):
        args = (choice_question(),)
        kw = dict(receipt=synthetic_receipt(),
                  candidate=choice_answer(confidence=0.55),
                  surface=SURFACE, runner="code", thresholds=measured_thresholds())
        first = assess(*args, **kw)
        second = assess(*args, **kw)
        self.assertEqual(first.allowed_next_steps, second.allowed_next_steps)
        self.assertEqual(first.reason, second.reason)

    def test_threshold_missing_fails_closed_never_defaults(self):
        outcome = assess(
            choice_question(), receipt=synthetic_receipt(),
            candidate=choice_answer(confidence=0.99),  # would pass any default
            surface=SURFACE, runner="code", thresholds=None,
        )
        self.assertEqual(outcome.outcome, "NEEDS_HUMAN")
        self.assertEqual(outcome.reason_kind, "threshold-data-missing")
        # No threshold was invented to let the 0.99 through.
        self.assertIsNone(outcome.threshold_applied)

    def test_threshold_missing_for_one_class_fails_closed(self):
        data = measured_thresholds()
        data.thresholds.pop("choice")
        outcome = assess(
            choice_question(), receipt=synthetic_receipt(),
            candidate=choice_answer(confidence=0.99),
            surface=SURFACE, runner="code", thresholds=data,
        )
        self.assertEqual(outcome.outcome, "NEEDS_HUMAN")
        self.assertEqual(outcome.reason_kind, "threshold-data-missing")

    def test_threshold_without_measured_provenance_is_malformed(self):
        with self.assertRaises(ValidationError):
            # No provenance at all — a default threshold shape must not validate.
            ClassThreshold.model_validate(
                {"question_class": "choice", "min_confidence": 0.8}
            )
        with self.assertRaises(ValidationError):
            # "default" is not a measured source.
            ClassThreshold.model_validate({
                "question_class": "choice", "min_confidence": 0.8,
                "provenance": {**MEASURED_PROVENANCE, "source": "default"},
            })

    def test_unknown_runner_fails_closed(self):
        outcome = assess(
            choice_question(), receipt=synthetic_receipt(),
            candidate=choice_answer(), surface=SURFACE, runner="gpt-9-magic",
            thresholds=measured_thresholds(),
        )
        self.assertEqual(outcome.outcome, "NEEDS_HUMAN")
        self.assertEqual(outcome.reason_kind, "unknown-runner")
        self.assertIsNone(outcome.answer)

    def test_invalid_receipt_fails_closed_with_the_gate_sentence(self):
        outcome = assess(
            choice_question(),
            receipt={"model_used": 42},  # malformed receipt payload
            candidate=choice_answer(),
            surface=SURFACE, runner="code", thresholds=measured_thresholds(),
        )
        self.assertEqual(outcome.outcome, "NEEDS_HUMAN")
        self.assertEqual(outcome.reason_kind, "invalid-receipt")
        self.assertEqual(outcome.reason, FAIL_CLOSED_SENTENCE)
        self.assertIsNone(outcome.answer)
        self.assertTrue(outcome.validation_errors)

    def test_fail_closed_sentence_is_the_existing_gate_sentence(self):
        # (ask) "the existing fail-closed sentence" — pinned verbatim against
        # the Commitment Gate's BLOCKED reason so the two cannot diverge.
        self.assertEqual(FAIL_CLOSED_SENTENCE, evaluate_intent("payment").reason)


# ---------------------------------------------------------------------------
# score_source honesty (amendment d) — raw|calibrated on local-ml answers
# ---------------------------------------------------------------------------


class ScoreSourceHonestyTests(unittest.TestCase):
    def test_local_ml_requires_score_source(self):
        outcome = assess(
            choice_question(), receipt=synthetic_receipt(),
            candidate=choice_answer(confidence=0.95),  # no score_source
            surface=SURFACE, runner="local-ml", thresholds=measured_thresholds(),
        )
        self.assertEqual(outcome.outcome, "NEEDS_HUMAN")
        types = {e.type for e in outcome.validation_errors}
        self.assertIn("score_source_required_for_local_ml", types)

    def test_local_ml_raw_answer_is_honest(self):
        candidate = ChoiceAnswer(question_id="q-urgency",
                                 value="clinician-visit", probability=0.62,
                                 confidence=0.95, score_source=ScoreSource.RAW)
        outcome = assess(
            choice_question(), receipt=synthetic_receipt(), candidate=candidate,
            surface=SURFACE, runner="local-ml", thresholds=measured_thresholds(),
        )
        self.assertEqual(outcome.outcome, "ANSWERED")
        self.assertEqual(outcome.answer.score_source, ScoreSource.RAW)

    def test_score_source_is_raw_or_calibrated_only(self):
        with self.assertRaises(ValidationError):
            ChoiceAnswer(question_id="q", value="a", probability=0.5,
                         confidence=0.9, score_source="guessed")


# ---------------------------------------------------------------------------
# Receipt-required contract + static tripwire (amendment a)
# ---------------------------------------------------------------------------


class ReceiptRequiredTests(unittest.TestCase):
    def test_receipt_is_a_required_keyword_argument(self):
        import healthadvocate.decisions as decisions_pkg

        assess_functions = [
            obj for name, obj in vars(decisions_pkg).items()
            if callable(obj) and name.startswith("assess")
        ]
        self.assertTrue(assess_functions)
        for fn in assess_functions:
            sig = inspect.signature(fn)
            self.assertIn("receipt", sig.parameters, fn.__name__)
            param = sig.parameters["receipt"]
            self.assertIs(param.default, inspect.Parameter.empty, fn.__name__)
            hints = get_type_hints(fn)
            self.assertIs(hints.get("receipt"), IdentificationReceipt)

    def test_calling_without_receipt_is_a_type_error(self):
        # "No receipt → no assessment" holds at the API boundary itself:
        # the call cannot even be made.
        with self.assertRaises(TypeError):
            assess(choice_question(), candidate=choice_answer(),
                   surface=SURFACE, runner="code", thresholds=measured_thresholds())

    def test_receipt_never_stores_raw_entity_text(self):
        result = receipt_from_analysis(
            SyntheticAnalysis(),
            coverage_notes=["synthetic identify stage"],
            deidentification_status=DeidentificationStatus.SUCCESS,
        )
        self.assertEqual(result.errors, [])
        assert result.receipt is not None
        receipt = result.receipt
        self.assertEqual(receipt.model_used, "synthetic-ner-fixture")
        labels = {e.label for e in receipt.entity_classes}
        self.assertEqual(labels, {"PatientName", "MemberID"})
        serialized = json.dumps(receipt.model_dump())
        for text in RAW_ENTITY_TEXTS:
            self.assertNotIn(text, serialized)

    def test_receipt_reuses_privacy_boundary_status_vocabulary(self):
        receipt = synthetic_receipt()
        self.assertIs(receipt.deidentification_status.__class__,
                      DeidentificationStatus)


# ---------------------------------------------------------------------------
# Hosted-runner refusal (amendment e) — structurally OFF, flag does not exist
# ---------------------------------------------------------------------------


class HostedRunnerRefusalTests(unittest.TestCase):
    def test_stub_raises(self):
        with self.assertRaises(HostedJevGateError) as ctx:
            hosted_jev_call(question=choice_question(), receipt=synthetic_receipt())
        self.assertEqual(str(ctx.exception), HOSTED_JEV_GATE_MESSAGE)

    def test_assess_with_hosted_runner_raises(self):
        with self.assertRaises(HostedJevGateError):
            assess(
                choice_question(), receipt=synthetic_receipt(),
                candidate=choice_answer(), surface=SURFACE, runner="hosted-jev",
                thresholds=measured_thresholds(),
            )

    def test_registry_is_code_default_local_ml_hosted_stub(self):
        self.assertEqual(runner_names(), ("code", "local-ml", "hosted-jev"))

    def test_stub_is_inert_no_url_no_http_no_env_read(self):
        # (e) INERT: no URL, no HTTP client, no env read anywhere in the
        # package source — the gate is structural, not a runtime check.
        forbidden = ("http://", "https://", "urllib", "requests", "httpx",
                     "environ", "getenv", "socket")
        for py in sorted((ROOT / "healthadvocate" / "decisions").glob("*.py")):
            source = py.read_text()
            for token in forbidden:
                self.assertNotIn(token, source, f"{token} in {py.name}")


# ---------------------------------------------------------------------------
# Stripped-errors rule (consensus amendment, round 3): every wrapper field
# sourced from ANY pydantic ValidationError carries loc/msg/type/url only —
# never str(exc) or raw errors().
# ---------------------------------------------------------------------------


class StrippedErrorsTests(unittest.TestCase):
    def _receipt_payload_with_canary_in_rejected_field(self) -> dict:
        return {
            "model_used": "synthetic-ner-fixture",
            "entity_classes": [],
            "coverage_notes": [],
            # Rejected literal → raw ValidationError carries it under `input`.
            "deidentification_status": CANARY,
        }

    def _threshold_payload_with_canary_in_rejected_field(self) -> dict:
        data = measured_thresholds().model_dump()
        data["thresholds"]["choice"]["min_confidence"] = CANARY_MEMBER
        return data

    def test_reflex_path_would_leak_but_wrapper_does_not_invalid_receipt(self):
        payload = self._receipt_payload_with_canary_in_rejected_field()
        with self.assertRaises(ValidationError) as ctx:
            IdentificationReceipt.model_validate(payload)
        # The reflex path (str(exc) / raw errors()) WOULD leak the canary —
        # this is the vector the stripping rule exists to close.
        self.assertIn(CANARY, str(ctx.exception))
        self.assertIn(CANARY, str(ctx.exception.errors()))

        outcome = assess(
            choice_question(), receipt=payload, candidate=choice_answer(),
            surface=SURFACE, runner="code", thresholds=measured_thresholds(),
        )
        self.assertEqual(outcome.reason_kind, "invalid-receipt")
        wrapper_json = json.dumps(outcome.model_dump())
        self.assertNotIn(CANARY, wrapper_json)
        self.assertTrue(outcome.validation_errors)
        for err in outcome.validation_errors:
            self.assertEqual(
                set(err.model_dump()),
                {"loc", "msg", "type", "url"},
            )

    def test_stripping_covers_malformed_threshold_wrapper_too(self):
        payload = self._threshold_payload_with_canary_in_rejected_field()
        with self.assertRaises(ValidationError) as ctx:
            ThresholdData.model_validate(payload)
        self.assertIn(CANARY_MEMBER, str(ctx.exception))

        outcome = assess(
            choice_question(), receipt=synthetic_receipt(),
            candidate=choice_answer(confidence=0.95),
            surface=SURFACE, runner="code", thresholds=payload,
        )
        self.assertEqual(outcome.reason_kind, "threshold-data-malformed")
        wrapper_json = json.dumps(outcome.model_dump())
        self.assertNotIn(CANARY_MEMBER, wrapper_json)
        self.assertNotIn(CANARY, wrapper_json)
        self.assertTrue(outcome.validation_errors)

    def test_stripped_validation_errors_helper_never_carries_input(self):
        with self.assertRaises(ValidationError) as ctx:
            IdentificationReceipt.model_validate(
                self._receipt_payload_with_canary_in_rejected_field()
            )
        stripped = stripped_validation_errors(ctx.exception)
        self.assertTrue(stripped)
        dumped = json.dumps([s.model_dump() for s in stripped])
        self.assertNotIn(CANARY, dumped)
        for err in stripped:
            self.assertEqual(set(err.model_dump()), {"loc", "msg", "type", "url"})


# ---------------------------------------------------------------------------
# Canary PHI-free tripwire (J1-blocking): build a receipt AND a NEEDS_HUMAN
# outcome from canary-bearing synthetic input; serialized JSON stays clean.
# ---------------------------------------------------------------------------


class CanaryPhiFreeTripwireTests(unittest.TestCase):
    def test_receipt_and_needs_human_wrapper_are_canary_free(self):
        built = receipt_from_analysis(
            SyntheticAnalysis(),
            coverage_notes=["synthetic identify stage"],
            deidentification_status=DeidentificationStatus.SUCCESS,
        )
        self.assertEqual(built.errors, [])
        assert built.receipt is not None
        outcome = assess(
            choice_question(), receipt=built.receipt,
            candidate=choice_answer(confidence=0.55),  # below threshold
            surface=SURFACE, runner="code",
            thresholds=measured_thresholds(),
        )
        self.assertEqual(outcome.outcome, "NEEDS_HUMAN")
        self.assertEqual(outcome.answer.value, "clinician-visit")

        receipt_json = json.dumps(built.receipt.model_dump())
        wrapper_json = json.dumps(outcome.model_dump())
        for text in RAW_ENTITY_TEXTS:
            self.assertNotIn(text, receipt_json)
            self.assertNotIn(text, wrapper_json)

    def test_malformed_threshold_wrapper_from_canary_input_is_clean(self):
        # The tripwire covers the malformed-threshold-data wrapper too
        # (consensus amendment round 3), not just invalid-receipt.
        payload = self._canary_threshold_payload()
        outcome = assess(
            choice_question(), receipt=synthetic_receipt(),
            candidate=choice_answer(confidence=0.55),
            surface=SURFACE, runner="code", thresholds=payload,
        )
        self.assertEqual(outcome.reason_kind, "threshold-data-malformed")
        wrapper_json = json.dumps(outcome.model_dump())
        for text in RAW_ENTITY_TEXTS:
            self.assertNotIn(text, wrapper_json)

    def _canary_threshold_payload(self) -> dict:
        data = measured_thresholds().model_dump()
        data["thresholds"]["score"]["min_confidence"] = CANARY
        return data


# ---------------------------------------------------------------------------
# Assessor allowlist pin (amendment h) — derivation, not name list
# ---------------------------------------------------------------------------


ASSESSOR_ALLOWLIST = frozenset({
    # J2-c (2026-09-22): assess_symptoms is CONVERTED behind the receipt
    # contract (urgency is a typed ScoreQuestion; see
    # decisions/symptom_triage.py) but its engine-first signature is
    # deliberately stable for callers, so the AST derivation still finds
    # it and the entry stays. The shrink-only expectation applies when a
    # surface's signature itself moves behind the receipt contract.
    "assess_symptoms",       # core/symptom_assessor.py:10
    "fight_denial",          # core/insurance_fighter.py:10
    "decode_bill",           # core/bill_decoder.py:13
    "decode_document",       # core/document_decoder.py:10
    "prepare_appointment",   # core/appointment_prep.py:10
    "scan_bulletin",         # core/community_health.py:10
    "translate_discharge",   # core/discharge_translator.py:10
    "check_drug",            # core/drug_checker.py:10
    "create_brief",          # core/second_opinion.py:10
})


def derive_engine_first_assessors(core: Path) -> set[str]:
    """The (h) derivation: every engine-first public function in
    healthadvocate/core/, including `async def` and nested/conditional
    definitions (ast.walk, not just tree.body + FunctionDef — an async or
    nested engine-first def must not evade the pin)."""
    derived: set[str] = set()
    for py in sorted(core.glob("*.py")):
        tree = ast.parse(py.read_text())
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if node.name.startswith("_"):
                continue
            positional = node.args.posonlyargs + node.args.args
            if positional and positional[0].arg == "engine":
                derived.add(node.name)
    return derived


class AssessorAllowlistTests(unittest.TestCase):
    def test_derived_engine_first_assessors_equal_allowlist(self):
        """AST-derive the engine-first public functions in healthadvocate/
        core/ and require set equality with the frozen nine-entry allowlist.
        Fails on ANY addition; J2+ conversions shrink it (design §4 (h))."""
        core = ROOT / "healthadvocate" / "core"
        self.assertEqual(derive_engine_first_assessors(core),
                         set(ASSESSOR_ALLOWLIST))

    def test_derivation_collects_async_and_nested_defs(self):
        # Pins the walk itself: an async or nested engine-first def is
        # collected, so none can slip past the allowlist pin.
        snippet = (
            "async def sneak(engine):\n    pass\n"
            "def outer():\n"
            "    def hidden(engine):\n        pass\n"
            "    return hidden\n"
        )
        tree = ast.parse(snippet)
        found = {
            node.name for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and not node.name.startswith("_")
            and (node.args.posonlyargs + node.args.args)
            and (node.args.posonlyargs + node.args.args)[0].arg == "engine"
        }
        self.assertEqual(found, {"sneak", "hidden"})

    def test_no_async_def_exists_in_core_today(self):
        # Documents the latent-gap ground truth the reviewer verified.
        core = ROOT / "healthadvocate" / "core"
        for py in sorted(core.glob("*.py")):
            tree = ast.parse(py.read_text())
            async_defs = [
                node.name for node in ast.walk(tree)
                if isinstance(node, ast.AsyncFunctionDef)
            ]
            self.assertEqual(async_defs, [], py.name)

    def test_allowlist_is_the_nine_pinned_entries(self):
        self.assertEqual(len(ASSESSOR_ALLOWLIST), 9)


# ---------------------------------------------------------------------------
# ADV-004: hostile (non-Question) first arguments must fail closed into the
# NEEDS_HUMAN wrapper — never an unhandled ValueError/AttributeError.
# ---------------------------------------------------------------------------


class Adv004InvalidQuestionTests(unittest.TestCase):
    HOSTILE_QUESTIONS = ({"id": "q-urgency", "claim": "c"}, "raw string",
                         None, 42)

    def test_valid_runner_hostile_question_fails_closed(self):
        for hostile in self.HOSTILE_QUESTIONS:
            with self.subTest(question=hostile):
                outcome = assess(
                    hostile, receipt=synthetic_receipt(),
                    candidate=choice_answer(), surface=SURFACE, runner="code",
                    thresholds=measured_thresholds(),
                )
                self.assertEqual(outcome.outcome, "NEEDS_HUMAN")
                self.assertEqual(outcome.reason_kind, "invalid-question")
                self.assertIsNone(outcome.answer)
                self.assertIsNone(outcome.threshold_applied)
                self.assertEqual(outcome.gate_state, GateState.REVIEW_REQUIRED)
                self.assertTrue(outcome.allowed_next_steps)

    def test_unknown_runner_hostile_question_fails_closed(self):
        for hostile in self.HOSTILE_QUESTIONS:
            with self.subTest(question=hostile):
                outcome = assess(
                    hostile, receipt=synthetic_receipt(), candidate=None,
                    surface=SURFACE, runner="nope", thresholds=measured_thresholds(),
                )
                self.assertEqual(outcome.outcome, "NEEDS_HUMAN")
                self.assertEqual(outcome.reason_kind, "invalid-question")

    def test_hostile_question_with_valid_control_still_works(self):
        outcome = assess(
            choice_question(), receipt=synthetic_receipt(),
            candidate=choice_answer(confidence=0.9), surface=SURFACE, runner="code",
            thresholds=measured_thresholds(),
        )
        self.assertEqual(outcome.outcome, "ANSWERED")

    def test_hosted_runner_refusal_dominates_invalid_question(self):
        # The CEO gate raise is the loudest refusal; it is not weakened by
        # input-validation ordering.
        with self.assertRaises(HostedJevGateError):
            assess({"id": "q-urgency"}, receipt=synthetic_receipt(),
                   candidate=None, surface=SURFACE, runner="hosted-jev",
                   thresholds=measured_thresholds())

    def test_invalid_question_wrapper_never_echoes_hostile_input(self):
        outcome = assess(
            {"id": CANARY}, receipt=synthetic_receipt(),
            candidate=choice_answer(), surface=SURFACE, runner="code",
            thresholds=measured_thresholds(),
        )
        wrapper_json = json.dumps(outcome.model_dump())
        self.assertNotIn(CANARY, wrapper_json)
        self.assertNotIn(CANARY_MEMBER, wrapper_json)


# ---------------------------------------------------------------------------
# ADV-001: the typed gate must not accept coerced confidence/probability
# values (str/bytes/bool/int) or coerced option strings — pydantic lax
# coercion drove ANSWERED outcomes. Strict models + exact-float validators.
# ---------------------------------------------------------------------------


class Adv001StrictTypingTests(unittest.TestCase):
    COERCED_VALUES = ("0.95", b"0.95", True, 1, None)

    def test_answer_confidence_rejects_coerced_types(self):
        for bad in self.COERCED_VALUES:
            with self.subTest(value=bad):
                with self.assertRaises(ValidationError):
                    ChoiceAnswer(question_id="q", value="a", probability=0.5,
                                 confidence=bad)
                with self.assertRaises(ValidationError):
                    ChoiceAnswer(question_id="q", value="a", probability=bad,
                                 confidence=0.5)
                with self.assertRaises(ValidationError):
                    NoulAnswer(question_id="q", probability_true=bad,
                               confidence=0.5)
                with self.assertRaises(ValidationError):
                    ScoreAnswer(question_id="q", level=0,
                                per_level_probabilities=[bad], confidence=0.5)

    def test_threshold_min_confidence_rejects_coerced_types(self):
        for bad in ("0.9", b"0.9", True, 1, None):
            with self.subTest(value=bad):
                with self.assertRaises(ValidationError):
                    ClassThreshold.model_validate({
                        "question_class": "choice", "min_confidence": bad,
                        "provenance": MEASURED_PROVENANCE,
                    })

    def test_receipt_max_confidence_rejects_coerced_types(self):
        for bad in ("0.9", b"0.9", True, 1, None):
            with self.subTest(value=bad):
                with self.assertRaises(ValidationError):
                    IdentificationReceipt(
                        model_used="m",
                        entity_classes=[{"label": "L", "category": "c",
                                         "count": 1, "max_confidence": bad}],
                        coverage_notes=[],
                        deidentification_status=DeidentificationStatus.SUCCESS,
                    )

    def test_bytes_option_rejected(self):
        with self.assertRaises(ValidationError):
            ChoiceQuestion(id="q", options=[b"clinician-visit"],
                           context_ref="c")

    def test_coerced_confidence_drives_fail_closed_not_answered(self):
        # The exact ADV-001 scenario: each coerced value used to reach the
        # comparison and drive ANSWERED; it must now fail closed.
        for bad in self.COERCED_VALUES:
            with self.subTest(value=bad):
                outcome = assess(
                    choice_question(), receipt=synthetic_receipt(),
                    candidate={"question_id": "q-urgency",
                               "value": "clinician-visit",
                               "probability": 0.5, "confidence": bad},
                    surface=SURFACE, runner="code", thresholds=measured_thresholds(),
                )
                self.assertEqual(outcome.outcome, "NEEDS_HUMAN")
                self.assertEqual(outcome.reason_kind, "invalid-answer")
                self.assertIsNone(outcome.answer)

    def test_honest_float_confidence_still_answers(self):
        # Guard against over-strictness: plain floats keep flowing.
        outcome = assess(
            choice_question(), receipt=synthetic_receipt(),
            candidate=choice_answer(confidence=0.95), surface=SURFACE, runner="code",
            thresholds=measured_thresholds(),
        )
        self.assertEqual(outcome.outcome, "ANSWERED")
        self.assertEqual(outcome.answer.confidence, 0.95)


# ---------------------------------------------------------------------------
# ADV-004 round 2: the cycle-1 gate accepted subclasses (isinstance) but
# _ANSWER_TYPES keyed on exact type() — KeyError on both threshold legs —
# and a __class__-faking proxy WITH an .id attribute sailed through the
# gate (the .id probe never covered that; type-based subclass checks do).
# ---------------------------------------------------------------------------


class Adv004Round2Tests(unittest.TestCase):
    @staticmethod
    def _subclasses():
        class SubChoice(ChoiceQuestion):
            pass

        class SubScore(ScoreQuestion):
            pass

        class SubNoul(NoulQuestion):
            pass

        return (
            (SubChoice(id="q-urgency",
                       options=["clinician-visit"], context_ref="c"),
             lambda: ChoiceAnswer(question_id="q-urgency",
                                  value="clinician-visit", probability=0.5,
                                  confidence=0.9), "choice"),
            (SubScore(id="q-triage",
                      rubric=[ScoreLevel(label="low"), ScoreLevel(label="high")]),
             lambda: ScoreAnswer(question_id="q-triage", level=0,
                                 per_level_probabilities=[0.5, 0.5],
                                 confidence=0.9), "score"),
            (SubNoul(id="q-claim", claim="c"),
             lambda: NoulAnswer(question_id="q-claim", probability_true=0.4,
                                confidence=0.9), "noul"),
        )

    def test_question_subclasses_assess_end_to_end(self):
        # A legitimate pydantic extension pattern: subclasses are real
        # questions and must flow through the full contract.
        for question, answer, qclass in self._subclasses():
            with self.subTest(question_class=qclass):
                outcome = assess(
                    question, receipt=synthetic_receipt(),
                    candidate=answer(), surface=SURFACE, runner="code",
                    thresholds=measured_thresholds(),
                )
                self.assertEqual(outcome.outcome, "ANSWERED")
                self.assertEqual(outcome.question_class, qclass)
                self.assertIsNotNone(outcome.answer)

    def test_question_subclasses_threshold_missing_leg_wraps(self):
        # The leg that crashed with KeyError via _ANSWER_TYPES[type(...)].
        for question, answer, qclass in self._subclasses():
            with self.subTest(question_class=qclass):
                outcome = assess(
                    question, receipt=synthetic_receipt(),
                    candidate=answer(), surface=SURFACE, runner="code", thresholds=None,
                )
                self.assertEqual(outcome.outcome, "NEEDS_HUMAN")
                self.assertEqual(outcome.reason_kind, "threshold-data-missing")
                self.assertIsNotNone(outcome.answer)

    def test_class_faking_proxy_with_id_fails_closed(self):
        # __class__ shadow fools isinstance (asserted below — this is the
        # vector), carries .id so the cycle-1 probe passed it; the
        # type-based subclass check must reject it on every leg.
        class ProxyWithId:
            __class__ = ChoiceQuestion

            def __init__(self):
                self.id = "q-urgency"

        proxy = ProxyWithId()
        self.assertTrue(isinstance(proxy, ChoiceQuestion))  # documented vector
        for thresholds in (measured_thresholds(), None):
            with self.subTest(thresholds_present=thresholds is not None):
                outcome = assess(
                    proxy, receipt=synthetic_receipt(),
                    candidate=choice_answer(), surface=SURFACE, runner="code",
                    thresholds=thresholds,
                )
                self.assertEqual(outcome.outcome, "NEEDS_HUMAN")
                self.assertEqual(outcome.reason_kind, "invalid-question")
                self.assertIsNone(outcome.answer)

    def test_proxy_below_threshold_comparison_never_runs(self):
        # A proxy must be rejected before any leg could compare a
        # fabricated confidence against a threshold.
        class ProxyWithId:
            __class__ = NoulQuestion

            def __init__(self):
                self.id = "q-claim"

        outcome = assess(
            ProxyWithId(), receipt=synthetic_receipt(),
            candidate=NoulAnswer(question_id="q-claim", probability_true=0.1,
                                 confidence=0.99),
            surface=SURFACE, runner="code", thresholds=measured_thresholds(),
        )
        self.assertEqual(outcome.reason_kind, "invalid-question")
        self.assertIsNone(outcome.threshold_applied)


# ---------------------------------------------------------------------------
# Review round 3: threshold-provenance linkage (F1), hostile runner values
# (F2), total receipt builder (F3), deidentification gate (F4), receipt
# free-text canary screen (F7), numpy float dtypes (F8).
# ---------------------------------------------------------------------------


class ThresholdProvenanceLinkageTests(unittest.TestCase):
    def test_junk_provenance_shape_is_malformed(self):
        with self.assertRaises(ValidationError):
            ThresholdData.model_validate({"surface": "s", "thresholds": {
                "noul": {"question_class": "noul", "min_confidence": 0.0,
                         "provenance": {"source": "measured", "surface": "???",
                                        "measured_on": "not-a-date",
                                        "sample_size": 1}}}})


class PolicyProvenanceTierTests(unittest.TestCase):
    """J2-c amendment: an additive, honestly-labeled `policy` provenance
    tier for surfaces converting before measured confidence distributions
    exist (first consumer: symptom-triage). The tier exists so a policy
    threshold can say what it is; it can never borrow the measured
    tier's fields, and the measured tier stays exactly as strict."""

    POLICY_PROVENANCE = {
        "source": "policy",
        "surface": "symptom-triage",
        "adopted_on": "2026-09-22",
        "rationale": (
            "Conservative bridge until measured confidence distributions "
            "exist for this surface."
        ),
    }

    def test_policy_provenance_validates(self):
        entry = ClassThreshold.model_validate({
            "question_class": "score", "min_confidence": 0.5,
            "provenance": self.POLICY_PROVENANCE,
        })
        self.assertEqual(entry.provenance.source, "policy")
        self.assertIsNone(entry.provenance.sample_size)

    def test_measured_tier_still_requires_its_fields(self):
        for missing in ("measured_on", "sample_size"):
            with self.subTest(missing=missing):
                payload = {**MEASURED_PROVENANCE, "surface": "symptom-triage"}
                payload.pop(missing)
                with self.assertRaises(ValidationError):
                    ThresholdProvenance.model_validate(payload)

    def test_policy_tier_cannot_claim_measurement_fields(self):
        for extra in ({"sample_size": 200}, {"measured_on": "2026-09-22"},
                      {"sample_size": 1, "measured_on": "2026-01-01"}):
            with self.subTest(extra=extra):
                with self.assertRaises(ValidationError):
                    ThresholdProvenance.model_validate(
                        {**self.POLICY_PROVENANCE, **extra}
                    )

    def test_measured_tier_cannot_carry_policy_fields(self):
        for extra in ({"rationale": "r"}, {"adopted_on": "2026-09-22"}):
            with self.subTest(extra=extra):
                with self.assertRaises(ValidationError):
                    ThresholdProvenance.model_validate(
                        {**MEASURED_PROVENANCE, "surface": "symptom-triage",
                         **extra}
                    )

    def test_policy_tier_requires_dated_non_blank_rationale(self):
        for bad in (
            {k: v for k, v in self.POLICY_PROVENANCE.items() if k != "adopted_on"},
            {**self.POLICY_PROVENANCE, "adopted_on": "09/22/2026"},
            {**self.POLICY_PROVENANCE, "rationale": "   "},
            {k: v for k, v in self.POLICY_PROVENANCE.items() if k != "rationale"},
        ):
            with self.subTest(bad=sorted(bad)):
                with self.assertRaises(ValidationError):
                    ThresholdProvenance.model_validate(bad)

    def test_policy_threshold_gates_through_assess_like_any_other(self):
        # A policy-tier ThresholdData flows through the same assess()
        # fail-closed flow — same surface-linkage rule, same legs.
        data = ThresholdData.model_validate({
            "surface": "symptom-triage",
            "thresholds": {"score": {
                "question_class": "score", "min_confidence": 0.5,
                "provenance": self.POLICY_PROVENANCE,
            }},
        })
        low = assess(
            ScoreQuestion(id="symptom-triage-urgency",
                          rubric=[ScoreLevel(label="low"),
                                  ScoreLevel(label="medium"),
                                  ScoreLevel(label="high")]),
            receipt=synthetic_receipt(),
            candidate=ScoreAnswer(question_id="symptom-triage-urgency",
                                  level=0, per_level_probabilities=[1.0, 0.0, 0.0],
                                  confidence=0.0),
            surface="symptom-triage", runner="code", thresholds=data,
        )
        self.assertEqual(low.outcome, "NEEDS_HUMAN")
        self.assertEqual(low.reason_kind, "below-threshold")
        self.assertEqual(low.threshold_applied, 0.5)
        high = assess(
            ScoreQuestion(id="symptom-triage-urgency",
                          rubric=[ScoreLevel(label="low"),
                                  ScoreLevel(label="medium"),
                                  ScoreLevel(label="high")]),
            receipt=synthetic_receipt(),
            candidate=ScoreAnswer(question_id="symptom-triage-urgency",
                                  level=0, per_level_probabilities=[1.0, 0.0, 0.0],
                                  confidence=1.0),
            surface="symptom-triage", runner="code", thresholds=data,
        )
        self.assertEqual(high.outcome, "ANSWERED")
        self.assertEqual(high.threshold_applied, 0.5)


class ThresholdSurfaceLinkageTests(unittest.TestCase):

    def test_threshold_data_requires_a_surface(self):
        payload = measured_thresholds().model_dump()
        del payload["surface"]
        with self.assertRaises(ValidationError):
            ThresholdData.model_validate(payload)

    def test_entry_provenance_surface_must_match_data_surface(self):
        payload = measured_thresholds().model_dump()
        payload["thresholds"]["choice"]["provenance"]["surface"] = "other"
        with self.assertRaises(ValidationError):
            ThresholdData.model_validate(payload)

    def test_cross_surface_threshold_fails_closed(self):
        # A threshold file measured on denial-classifier must not gate a
        # symptom-triage question — the design's shipping condition,
        # enforced loudly instead of cross-applied silently.
        outcome = assess(
            choice_question(), receipt=synthetic_receipt(),
            candidate=choice_answer(confidence=0.95),
            surface="symptom-triage",
            runner="code",
            thresholds=measured_thresholds(surface="denial-classifier"),
        )
        self.assertEqual(outcome.outcome, "NEEDS_HUMAN")
        self.assertEqual(outcome.reason_kind, "threshold-surface-mismatch")
        self.assertIsNone(outcome.threshold_applied)
        self.assertEqual(outcome.gate_state, GateState.REVIEW_REQUIRED)

    def test_matching_surface_still_answers(self):
        outcome = assess(
            choice_question(), receipt=synthetic_receipt(),
            candidate=choice_answer(confidence=0.95),
            surface=SURFACE, runner="code", thresholds=measured_thresholds(),
        )
        self.assertEqual(outcome.outcome, "ANSWERED")

    def test_measured_on_must_be_iso_date(self):
        with self.assertRaises(ValidationError):
            ThresholdData.model_validate({
                "surface": SURFACE, "thresholds": {"noul": {
                    "question_class": "noul", "min_confidence": 0.5,
                    "provenance": {**MEASURED_PROVENANCE,
                                   "measured_on": "09/22/2026"}}}})


class HostileRunnerValueTests(unittest.TestCase):
    def test_unhashable_runner_fails_closed(self):
        outcome = assess(
            choice_question(), receipt=synthetic_receipt(),
            candidate=choice_answer(),
            surface=SURFACE, runner=["code"], thresholds=measured_thresholds(),
        )
        self.assertEqual(outcome.outcome, "NEEDS_HUMAN")
        self.assertEqual(outcome.reason_kind, "unknown-runner")
        # The hostile value is never echoed into the wrapper.
        self.assertEqual(outcome.runner, "")
        self.assertNotIn('["code"]', json.dumps(outcome.model_dump()))

    def test_non_string_runner_values_fail_closed(self):
        for bad in (None, 42, {"name": "code"}, ("code",)):
            with self.subTest(runner=bad):
                outcome = assess(
                    choice_question(), receipt=synthetic_receipt(),
                    candidate=choice_answer(),
                    surface=SURFACE, runner=bad,
                    thresholds=measured_thresholds(),
                )
                self.assertEqual(outcome.reason_kind, "unknown-runner")
                self.assertEqual(outcome.runner, "")

    def test_non_string_runner_with_hostile_question_no_crash(self):
        outcome = assess(
            {"id": "q"}, receipt=synthetic_receipt(), candidate=None,
            surface=SURFACE, runner=["code"], thresholds=None,
        )
        self.assertEqual(outcome.reason_kind, "invalid-question")


class ReceiptBuilderTotalityTests(unittest.TestCase):
    @staticmethod
    def _analysis(entities, model_used="m"):
        class Analysis:
            pass

        analysis = Analysis()
        analysis.model_used = model_used
        analysis.entities = entities
        return analysis

    @staticmethod
    def _entity(confidence, label="L", category="pii"):
        class Entity:
            pass

        entity = Entity()
        entity.label = label
        entity.category = category
        entity.confidence = confidence
        return entity

    def test_valid_analysis_builds_receipt_with_no_errors(self):
        result = receipt_from_analysis(
            self._analysis([self._entity(0.9)]),
            deidentification_status=DeidentificationStatus.SUCCESS,
        )
        self.assertEqual(result.errors, [])
        assert result.receipt is not None

    def test_coerced_confidences_are_rejected_not_coerced(self):
        # str/bool/int confidences must NOT become max_confidence floats —
        # the answer path's exact-float stance, applied to the builder too.
        for bad in ("0.99", b"0.99", True, 1, None):
            with self.subTest(confidence=bad):
                result = receipt_from_analysis(
                    self._analysis([self._entity(bad)]),
                    deidentification_status=DeidentificationStatus.SUCCESS,
                )
                self.assertIsNone(result.receipt)
                self.assertTrue(result.errors)
                errors_json = json.dumps(
                    [e.model_dump() for e in result.errors])
                self.assertNotIn("0.99", errors_json)

    def test_unparseable_nan_and_degenerate_inputs_fail_closed(self):
        for entities, model_used in (
            ([self._entity(float("nan"))], "m"),      # NaN confidence
            ([self._entity(float("inf"))], "m"),      # out of range
            ([self._entity(0.5, label="")], "m"),     # blank label
            ([], ""),                                 # empty model_used
            ([], 42),                                 # non-str model_used
        ):
            with self.subTest(model_used=model_used):
                result = receipt_from_analysis(
                    self._analysis(entities, model_used=model_used),
                    deidentification_status=DeidentificationStatus.SUCCESS,
                )
                self.assertIsNone(result.receipt)
                self.assertTrue(result.errors)

    def test_non_string_deidentification_status_fails_closed(self):
        result = receipt_from_analysis(
            self._analysis([]),
            deidentification_status="success",  # type: ignore[arg-type]
        )
        self.assertIsNone(result.receipt)
        self.assertTrue(result.errors)


class DeidentificationGateTests(unittest.TestCase):
    def _failed_receipt(self):
        return IdentificationReceipt(
            model_used="m", entity_classes=[], coverage_notes=[],
            deidentification_status=DeidentificationStatus.FAILED,
        )

    def test_failed_deidentification_never_answers(self):
        outcome = assess(
            choice_question(), receipt=self._failed_receipt(),
            candidate=choice_answer(confidence=0.99),
            surface=SURFACE, runner="code", thresholds=measured_thresholds(),
        )
        self.assertEqual(outcome.outcome, "NEEDS_HUMAN")
        self.assertEqual(outcome.reason_kind, "deidentification-failed")
        self.assertIsNone(outcome.answer)
        self.assertEqual(outcome.gate_state, GateState.REVIEW_REQUIRED)

    def test_no_pii_found_still_answers(self):
        receipt = synthetic_receipt()
        receipt = receipt.model_copy(
            update={"deidentification_status": DeidentificationStatus.NO_PII_FOUND})
        outcome = assess(
            choice_question(), receipt=receipt,
            candidate=choice_answer(confidence=0.9),
            surface=SURFACE, runner="code", thresholds=measured_thresholds(),
        )
        self.assertEqual(outcome.outcome, "ANSWERED")


class ReceiptFreeTextCanaryScreenTests(unittest.TestCase):
    def test_builder_redacts_canaries_from_free_text(self):
        class Analysis:
            model_used = f"ner/{CANARY}"
            entities = []

        result = receipt_from_analysis(
            Analysis(),
            coverage_notes=[f"saw {CANARY} and {CANARY_MEMBER}"],
            deidentification_status=DeidentificationStatus.SUCCESS,
            canaries=(CANARY, CANARY_MEMBER),
        )
        self.assertEqual(result.errors, [])
        assert result.receipt is not None
        receipt_json = json.dumps(result.receipt.model_dump())
        self.assertNotIn(CANARY, receipt_json)
        self.assertNotIn(CANARY_MEMBER, receipt_json)

    def test_assess_screens_receipt_free_text_for_canaries(self):
        leaky = IdentificationReceipt(
            model_used=f"ner/{CANARY}", entity_classes=[], coverage_notes=[],
            deidentification_status=DeidentificationStatus.SUCCESS,
        )
        outcome = assess(
            choice_question(), receipt=leaky, candidate=choice_answer(),
            surface=SURFACE, runner="code", thresholds=measured_thresholds(),
        )
        self.assertEqual(outcome.outcome, "NEEDS_HUMAN")
        self.assertEqual(outcome.reason_kind, "invalid-receipt")
        self.assertIsNone(outcome.answer)
        wrapper_json = json.dumps(outcome.model_dump())
        self.assertNotIn(CANARY, wrapper_json)

    def test_default_canaries_screen_without_explicit_argument(self):
        # redact_text/DEFAULT_CANARIES discipline: the screen is on by
        # default (house canaries), not only when canaries are passed.
        leaky = IdentificationReceipt(
            model_used="m", entity_classes=[], coverage_notes=[CANARY_MEMBER],
            deidentification_status=DeidentificationStatus.SUCCESS,
        )
        outcome = assess(
            choice_question(), receipt=leaky, candidate=choice_answer(),
            surface=SURFACE, runner="code", thresholds=measured_thresholds(),
        )
        self.assertEqual(outcome.reason_kind, "invalid-receipt")


class NumpyFloatDtypeTests(unittest.TestCase):
    def setUp(self):
        try:
            import numpy  # noqa: F401
        except ImportError:
            self.skipTest("numpy not available")
        import numpy as np
        self.np = np

    def test_float64_and_float32_accepted(self):
        answer = ChoiceAnswer(question_id="q", value="a", probability=0.5,
                              confidence=self.np.float64(0.95))
        self.assertIsInstance(answer.confidence, float)
        self.assertEqual(answer.confidence, 0.95)
        answer32 = NoulAnswer(question_id="q",
                              probability_true=self.np.float32(0.5),
                              confidence=self.np.float32(0.9))
        self.assertEqual(answer32.probability_true, 0.5)

    def test_numpy_int_and_bool_rejected(self):
        for bad in (self.np.int64(1), self.np.bool_(True), self.np.int32(1)):
            with self.subTest(value=bad):
                with self.assertRaises(ValidationError):
                    ChoiceAnswer(question_id="q", value="a", probability=0.5,
                                 confidence=bad)

    def test_numpy_confidence_assesses_end_to_end(self):
        # The J2 local-ml runner's natural dtype flows through the gate
        # without a per-call-site conversion tax.
        outcome = assess(
            choice_question(), receipt=synthetic_receipt(),
            candidate={"question_id": "q-urgency", "value": "clinician-visit",
                       "probability": 0.5, "confidence": self.np.float64(0.95),
                       "score_source": "raw"},
            surface=SURFACE, runner="local-ml",
            thresholds=measured_thresholds(),
        )
        self.assertEqual(outcome.outcome, "ANSWERED")
        self.assertEqual(outcome.answer.confidence, 0.95)


if __name__ == "__main__":
    unittest.main()
