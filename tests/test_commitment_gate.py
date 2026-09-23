"""Commitment Gate zero-side-effect tests (issue 82).

HA-JEV J2-a extension (design 2026-09-22 §5): the intent classification
routes through the typed-decision layer when identify-stage evidence is
supplied. These tests pin the conversion's safety posture: prohibited
intents stay prohibited regardless of the typed outcome, every
NEEDS_HUMAN leg maps to review-only, canary-bearing identify input never
leaks into any serialized wrapper, and the no-evidence path stays
byte-identical to the pre-conversion gate.
"""

from __future__ import annotations

import json
import unittest

from healthadvocate.coverage.commitment_gate import (
    PROHIBITED_INTENTS,
    GateState,
    Intent,
    OutboundRecorder,
    evaluate_intent,
    request_commitment,
    reset_outbound_recorder,
)
from healthadvocate.coverage.intent_decision import (
    COMMITMENT_GATE_SURFACE,
    intent_candidate,
    intent_question,
)
from healthadvocate.decisions import ThresholdData
from healthadvocate.privacy.boundary import DeidentificationStatus

# Canary constants pattern (tests/test_privacy_boundary.py:33-34).
CANARY = "CANARY_PATIENT_ALPHA_9f3c"
CANARY_MEMBER = "MEMBER-ID-SYNTH-42"
RAW_ENTITY_TEXTS = (CANARY, CANARY_MEMBER, "Synthetic Patient Name")

ALLOWED_INTENTS = (
    "local_save",
    "local_view",
    "generate_script",
    "attach_evidence",
    "append_contact_note",
    "export_local",
)


def measured_thresholds(
    min_confidence: float = 0.80, surface: str = COMMITMENT_GATE_SURFACE
) -> ThresholdData:
    """Synthetic measured fixture — the only threshold data this surface
    ever sees in tests (J1 law: no production threshold defaults)."""
    return ThresholdData.model_validate({
        "surface": surface,
        "thresholds": {
            "choice": {
                "question_class": "choice",
                "min_confidence": min_confidence,
                "provenance": {
                    "source": "measured",
                    "surface": surface,
                    "measured_on": "2026-09-22",
                    "sample_size": 200,
                },
            }
        },
    })


class CanaryEntity:
    """EntityMatch stand-in carrying RAW text (engine.py:59-66 shape) —
    exactly what the receipt and wrapper must never copy."""

    def __init__(self, text: str, label: str, confidence: float) -> None:
        self.text = text
        self.label = label
        self.category = "pii"
        self.confidence = confidence


class CanaryAnalysis:
    model_used = "synthetic-ner-fixture"

    def __init__(self) -> None:
        self.entities = [
            CanaryEntity(CANARY, "PatientName", 0.91),
            CanaryEntity(CANARY_MEMBER, "MemberID", 0.99),
            CanaryEntity("Synthetic Patient Name", "PatientName", 0.84),
        ]


def typed_kwargs(**overrides):
    """Identify-stage evidence kwargs for evaluate_intent."""
    kwargs = {
        "analysis": CanaryAnalysis(),
        "deidentification_status": DeidentificationStatus.SUCCESS,
    }
    kwargs.update(overrides)
    return kwargs


class CommitmentGateTests(unittest.TestCase):
    def setUp(self) -> None:
        reset_outbound_recorder()

    def test_every_prohibited_intent_maps_to_gate_state(self):
        expected = {
            "payment": GateState.BLOCKED,
            "submission": GateState.REVIEW_REQUIRED,
            "withdrawal": GateState.REVIEW_REQUIRED,
            "plan_selection": GateState.REVIEW_REQUIRED,
            "plan_change": GateState.REVIEW_REQUIRED,
            "cancellation": GateState.REVIEW_REQUIRED,
            "outbound_message": GateState.REVIEW_REQUIRED,
            "prescribe": GateState.BLOCKED,
            "dose_change": GateState.BLOCKED,
            "treatment_change": GateState.BLOCKED,
            "unknown": GateState.REVIEW_REQUIRED,
        }
        for name, state in expected.items():
            decision = evaluate_intent(name)
            self.assertEqual(decision.gate_state, state, name)
            self.assertEqual(decision.side_effects, [])

    def test_allowed_local_intents(self):
        for name in (
            "local_save",
            "local_view",
            "generate_script",
            "attach_evidence",
            "append_contact_note",
            "export_local",
        ):
            decision = evaluate_intent(name)
            self.assertEqual(decision.gate_state, GateState.ALLOWED, name)

    def test_unknown_defaults_to_review_required(self):
        decision = evaluate_intent("teleport_money_to_insurer")
        self.assertEqual(decision.gate_state, GateState.REVIEW_REQUIRED)
        self.assertEqual(decision.intent, Intent.UNKNOWN)

    def test_zero_side_effects_for_prohibited_intents(self):
        recorder = OutboundRecorder()
        executed_flags = []

        def boom():
            executed_flags.append(True)
            recorder.record("http", url="https://evil.example/pay")
            return "sent"

        for intent in PROHIBITED_INTENTS:
            before = recorder.count
            result = request_commitment(intent, recorder=recorder, execute=boom)
            self.assertFalse(result["executed"], intent)
            self.assertEqual(result["side_effects"], [])
            self.assertEqual(recorder.count, before, intent)
            self.assertIn(result["gate_state"], {"blocked", "review_required"})

        self.assertEqual(executed_flags, [])
        self.assertEqual(recorder.count, 0)

    def test_allowed_intent_may_run_local_execute(self):
        recorder = OutboundRecorder()
        result = request_commitment(
            "local_save",
            recorder=recorder,
            execute=lambda: {"saved": True},
        )
        self.assertTrue(result["executed"])
        self.assertEqual(result["result"], {"saved": True})
        self.assertEqual(recorder.count, 0)

    def test_api_response_shape_is_understandable(self):
        result = request_commitment("payment")
        for key in (
            "gate_state",
            "intent",
            "reason",
            "allowed_next_steps",
            "side_effects",
            "executed",
        ):
            self.assertIn(key, result)
        self.assertTrue(result["reason"])
        self.assertTrue(result["allowed_next_steps"])
        self.assertEqual(result["side_effects"], [])
        self.assertFalse(result["executed"])


class TypedConversionProhibitedTests(unittest.TestCase):
    """Point 4 of the J2-a spec: a prohibited intent is blocked regardless
    of the typed outcome — the wrapper adds audit numbers, not permissions."""

    def test_every_intent_with_answered_wrapper_keeps_legacy_state(self):
        # Property-style over the whole enum: even a fully-answered typed
        # adjudication (valid receipt + measured fixture thresholds) never
        # changes any intent's legacy gate state.
        for intent in Intent:
            with self.subTest(intent=intent.value):
                legacy = evaluate_intent(intent.value)
                typed = evaluate_intent(
                    intent.value,
                    **typed_kwargs(thresholds=measured_thresholds()),
                )
                self.assertEqual(typed.gate_state, legacy.gate_state)
                self.assertIsNotNone(typed.typed_decision)
                self.assertEqual(typed.typed_decision.outcome.value, "ANSWERED")

    def test_prohibited_intents_never_allowed_even_when_answered(self):
        for name in PROHIBITED_INTENTS:
            with self.subTest(intent=name):
                decision = evaluate_intent(
                    name, **typed_kwargs(thresholds=measured_thresholds())
                )
                self.assertIn(
                    decision.gate_state,
                    {GateState.BLOCKED, GateState.REVIEW_REQUIRED},
                )

    def test_prohibited_payloads_byte_equivalent_with_and_without_typing(self):
        # The wrapper must not change a single byte of the prohibited
        # decision's serialized payload.
        for name in PROHIBITED_INTENTS:
            with self.subTest(intent=name):
                legacy = evaluate_intent(name).to_dict()
                typed = evaluate_intent(
                    name, **typed_kwargs(thresholds=measured_thresholds())
                ).to_dict()
                self.assertEqual(typed, legacy)
                typed_needs_human = evaluate_intent(
                    name, **typed_kwargs()  # threshold-data-missing leg
                ).to_dict()
                self.assertEqual(typed_needs_human, legacy)

    def test_prohibited_intents_with_typing_never_execute(self):
        recorder = OutboundRecorder()
        for name in PROHIBITED_INTENTS:
            with self.subTest(intent=name):
                result = request_commitment(
                    name,
                    recorder=recorder,
                    execute=lambda: "must never run",
                    **typed_kwargs(thresholds=measured_thresholds()),
                )
                self.assertFalse(result["executed"])
                self.assertEqual(result["side_effects"], [])
        self.assertEqual(recorder.count, 0)


class TypedNeedsHumanMappingTests(unittest.TestCase):
    """Point 3: below-threshold or any fail-closed leg produces review-only
    behavior with the existing fail-closed sentence — never a new
    permissive path."""

    def _assert_review_only(self, decision, intent_name):
        self.assertEqual(decision.gate_state, GateState.REVIEW_REQUIRED,
                         intent_name)
        self.assertEqual(
            decision.reason,
            "HealthAdvocate will not perform this action. It requires a "
            "human decision outside this application.",
            intent_name,
        )
        self.assertNotEqual(decision.intent, Intent.UNKNOWN)

    def test_threshold_data_missing_downgrades_allowed_to_review(self):
        # Production posture: no measured thresholds exist for this
        # surface, so the typed path answers NEEDS_HUMAN.
        for name in ALLOWED_INTENTS:
            with self.subTest(intent=name):
                decision = evaluate_intent(name, **typed_kwargs())
                self._assert_review_only(decision, name)
                self.assertEqual(
                    decision.typed_decision.reason_kind,
                    "threshold-data-missing",
                )
                self.assertTrue(decision.typed_decision.allowed_next_steps)

    def test_threshold_missing_for_choice_class_downgrades(self):
        data = measured_thresholds()
        data.thresholds.pop("choice")
        decision = evaluate_intent(
            "local_save", **typed_kwargs(thresholds=data)
        )
        self._assert_review_only(decision, "local_save")
        self.assertEqual(
            decision.typed_decision.reason_kind, "threshold-data-missing"
        )

    def test_malformed_thresholds_downgrade(self):
        payload = measured_thresholds().model_dump()
        payload["thresholds"]["choice"]["min_confidence"] = "0.9"
        decision = evaluate_intent(
            "local_save", **typed_kwargs(thresholds=payload)
        )
        self._assert_review_only(decision, "local_save")
        self.assertEqual(
            decision.typed_decision.reason_kind, "threshold-data-malformed"
        )

    def test_cross_surface_thresholds_downgrade(self):
        decision = evaluate_intent(
            "local_save",
            **typed_kwargs(
                thresholds=measured_thresholds(surface="other-surface"),
            ),
        )
        self._assert_review_only(decision, "local_save")
        self.assertEqual(
            decision.typed_decision.reason_kind, "threshold-surface-mismatch"
        )

    def test_failed_deidentification_downgrades(self):
        decision = evaluate_intent(
            "local_save",
            **typed_kwargs(
                deidentification_status=DeidentificationStatus.FAILED,
                thresholds=measured_thresholds(),
            ),
        )
        self._assert_review_only(decision, "local_save")
        self.assertEqual(
            decision.typed_decision.reason_kind, "deidentification-failed"
        )

    def test_hostile_analysis_fails_closed_on_identify_errors(self):
        class HostileAnalysis:
            model_used = ""  # degenerate identify output

        decision = evaluate_intent(
            "local_save",
            analysis=HostileAnalysis(),
            deidentification_status=DeidentificationStatus.SUCCESS,
            thresholds=measured_thresholds(),
        )
        self._assert_review_only(decision, "local_save")
        self.assertIsNone(decision.typed_decision)  # no receipt, no assess
        self.assertTrue(decision.identify_errors)
        # No wrapper -> the legacy review steps ride along.
        self.assertEqual(
            decision.allowed_next_steps,
            [
                "Review prepared materials",
                "Generate a deterministic script",
                "Act only through official portals or people you choose",
            ],
        )

    def test_unstated_deidentification_status_fails_closed(self):
        decision = evaluate_intent(
            "local_save",
            analysis=CanaryAnalysis(),
            deidentification_status=None,  # never stated -> no receipt
            thresholds=measured_thresholds(),
        )
        self._assert_review_only(decision, "local_save")
        self.assertIsNone(decision.typed_decision)
        self.assertTrue(decision.identify_errors)

    def test_downgrade_never_executes(self):
        recorder = OutboundRecorder()
        result = request_commitment(
            "local_save",
            recorder=recorder,
            execute=lambda: "must never run",
            **typed_kwargs(),
        )
        self.assertFalse(result["executed"])
        self.assertEqual(recorder.count, 0)
        self.assertEqual(result["gate_state"], "review_required")

    def test_unknown_fallback_is_below_threshold_and_stays_review(self):
        # The UNKNOWN fallback carries 0.0 confidence: under fixture
        # thresholds the typed layer says below-threshold, and the
        # external decision stays exactly the legacy review decision.
        legacy = evaluate_intent("teleport_money_to_insurer").to_dict()
        decision = evaluate_intent(
            "teleport_money_to_insurer",
            **typed_kwargs(thresholds=measured_thresholds()),
        )
        self.assertEqual(decision.gate_state, GateState.REVIEW_REQUIRED)
        self.assertEqual(decision.typed_decision.reason_kind,
                         "below-threshold")
        self.assertEqual(decision.typed_decision.answer.value, "unknown")
        self.assertEqual(decision.to_dict(), legacy)

    def test_answered_with_measured_fixture_keeps_today_behavior(self):
        # With (fixture) measured thresholds and an exact match, the typed
        # layer answers and the allowed intent stays allowed.
        for name in ALLOWED_INTENTS:
            with self.subTest(intent=name):
                decision = evaluate_intent(
                    name, **typed_kwargs(thresholds=measured_thresholds())
                )
                self.assertEqual(decision.gate_state, GateState.ALLOWED)
                self.assertEqual(
                    decision.typed_decision.outcome.value, "ANSWERED"
                )
                self.assertEqual(decision.typed_decision.answer.value, name)
                self.assertEqual(decision.typed_decision.threshold_applied,
                                 0.80)


class TypedConversionCanaryTripwireTests(unittest.TestCase):
    """Point 5: canary-bearing identify input never leaks into any
    serialized wrapper, identify errors, or endpoint payload."""

    def _assert_clean(self, decision):
        blobs = [json.dumps(decision.to_dict())]
        if decision.typed_decision is not None:
            blobs.append(decision.typed_decision.model_dump_json())
        if decision.identify_errors:
            blobs.append(
                json.dumps([e.model_dump() for e in decision.identify_errors])
            )
        for blob in blobs:
            for text in RAW_ENTITY_TEXTS:
                self.assertNotIn(text, blob)

    def test_answered_wrapper_is_canary_free(self):
        decision = evaluate_intent(
            "local_save", **typed_kwargs(thresholds=measured_thresholds())
        )
        self.assertEqual(decision.gate_state, GateState.ALLOWED)
        self._assert_clean(decision)

    def test_needs_human_wrapper_is_canary_free(self):
        decision = evaluate_intent("local_save", **typed_kwargs())
        self.assertEqual(decision.typed_decision.reason_kind,
                         "threshold-data-missing")
        self._assert_clean(decision)

    def test_identify_errors_are_canary_free(self):
        class LeakyHostileAnalysis:
            model_used = f"ner/{CANARY}"  # redacted by the builder

        decision = evaluate_intent(
            "local_save",
            analysis=LeakyHostileAnalysis(),
            deidentification_status=DeidentificationStatus.SUCCESS,
        )
        # Builder redaction keeps model_used usable, so a receipt exists;
        # the assess screen then keeps the wrapper clean either way.
        self._assert_clean(decision)

        class BlankLabelAnalysis:
            model_used = "m"

            entities = [CanaryEntity(CANARY, "", 0.9)]  # rejected label

        decision2 = evaluate_intent(
            "local_save",
            analysis=BlankLabelAnalysis(),
            deidentification_status=DeidentificationStatus.SUCCESS,
        )
        self.assertIsNone(decision2.typed_decision)
        self.assertTrue(decision2.identify_errors)
        self._assert_clean(decision2)

    def test_endpoint_payload_never_carries_identify_material(self):
        result = request_commitment(
            "payment", **typed_kwargs(thresholds=measured_thresholds())
        )
        payload = json.dumps(result)
        for text in RAW_ENTITY_TEXTS:
            self.assertNotIn(text, payload)


class TypedConversionStabilityTests(unittest.TestCase):
    """Point 6: the public API stays stable — no-analysis calls are
    byte-identical to the pre-conversion gate, and repeated
    classifications are idempotent."""

    def test_no_analysis_leaves_typed_layer_unengaged(self):
        for name in ("local_save", "payment", "submission", "nonsense-x"):
            with self.subTest(intent=name):
                positional = evaluate_intent(name)
                kwargless = evaluate_intent(
                    name,
                    analysis=None,
                    deidentification_status=None,
                    canaries=(),
                    thresholds=None,
                )
                self.assertEqual(positional, kwargless)
                self.assertIsNone(positional.typed_decision)
                self.assertEqual(positional.identify_errors, [])

    def test_legacy_gate_state_map_is_unchanged(self):
        expected = {
            "local_save": GateState.ALLOWED,
            "payment": GateState.BLOCKED,
            "prescribe": GateState.BLOCKED,
            "dose_change": GateState.BLOCKED,
            "treatment_change": GateState.BLOCKED,
            "submission": GateState.REVIEW_REQUIRED,
            "unknown": GateState.REVIEW_REQUIRED,
        }
        for name, state in expected.items():
            self.assertEqual(evaluate_intent(name).gate_state, state, name)

    def test_to_dict_keys_are_exactly_the_legacy_five(self):
        for name in ("local_save", "payment", "withdrawal"):
            with self.subTest(intent=name):
                typed = evaluate_intent(
                    name, **typed_kwargs(thresholds=measured_thresholds())
                ).to_dict()
                self.assertEqual(
                    set(typed),
                    {
                        "gate_state",
                        "intent",
                        "reason",
                        "allowed_next_steps",
                        "side_effects",
                    },
                )

    def test_repeated_classification_is_idempotent(self):
        for kwargs in (
            {},
            typed_kwargs(),
            typed_kwargs(thresholds=measured_thresholds()),
        ):
            with self.subTest(with_typing=bool(kwargs)):
                first = evaluate_intent("local_save", **kwargs)
                second = evaluate_intent("local_save", **kwargs)
                self.assertEqual(first, second)
                self.assertEqual(first.to_dict(), second.to_dict())
                if first.typed_decision is not None:
                    self.assertEqual(first.typed_decision,
                                     second.typed_decision)

    def test_request_commitment_passes_identify_evidence_through(self):
        result = request_commitment(
            "local_save", **typed_kwargs()
        )  # NEEDS_HUMAN -> review-only, never executed
        self.assertEqual(result["gate_state"], "review_required")
        self.assertFalse(result["executed"])

    def test_question_options_are_the_intent_values(self):
        question = intent_question()
        self.assertEqual(
            question.options, [intent.value for intent in Intent]
        )
        for raw in ("save", "pay", "teleport", Intent.EXPORT_LOCAL):
            with self.subTest(raw=raw):
                candidate = intent_candidate(raw)
                self.assertIn(candidate.value, question.options)
                self.assertEqual(candidate.question_id, question.id)
                self.assertIsNone(candidate.score_source)  # runner is code

    def test_candidate_confidence_constants_are_honest(self):
        exact = intent_candidate("save")
        self.assertEqual((exact.probability, exact.confidence), (1.0, 1.0))
        fallback = intent_candidate("teleport_money_to_insurer")
        self.assertEqual(
            (fallback.probability, fallback.confidence), (0.0, 0.0)
        )
        self.assertEqual(fallback.value, "unknown")


if __name__ == "__main__":
    unittest.main()
