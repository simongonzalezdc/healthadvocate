"""HA-JEV J2-b contract tests: the insurance denial-reason pick routes
through the typed-decision layer (design 2026-09-22 §5, surface
`denial-classifier`).

Pinned here: the canonical denial-reason ChoiceQuestion; the receipt built
from the REAL identify stage (condition + medication NER) stating the
call's real deidentification status; measured surface-linked thresholds
(the measurement is the frozen synthetic corpus inside the module — the
tests re-run it); every fail-closed leg mapping to the surface's existing
safe fallback (empty denial_reason) with the NEEDS_HUMAN wrapper as audit;
the canary PHI-free tripwire for this surface; caller-shape stability (the
app endpoint keys and the CLI denial-checklist consumption); idempotency.
Synthetic fixtures only; no model runtime needed (structured_model_call is
patched — the model gate itself is J1-pinned elsewhere).
"""

from __future__ import annotations

import json
import unittest
from unittest import mock

from healthadvocate.cli import denial_checklist
from healthadvocate.core import insurance_fighter
from healthadvocate.core.insurance_fighter import (
    DENIAL_CLASSIFIER_SURFACE,
    DENIAL_CLASSIFIER_THRESHOLDS,
    DENIAL_REASON_OPTIONS,
    DENIAL_REASON_QUESTION_ID,
    _denial_reason_from_outcome,
    _denial_reason_question,
    _normalize_denial_reason,
    classify_denial_reason,
)
from healthadvocate.core.llm_client import unavailable_structured_fallback
from healthadvocate.decisions import (
    FAIL_CLOSED_SENTENCE,
    ChoiceAnswer,
    IdentificationReceipt,
    Outcome,
    ThresholdData,
    assess,
)
from healthadvocate.privacy.boundary import DeidentificationStatus

CANARY = "CANARY_PATIENT_ALPHA_9f3c"
CANARY_MEMBER = "MEMBER-ID-SYNTH-42"
RAW_ENTITY_TEXTS = (CANARY, CANARY_MEMBER, "Synthetic Patient Name")

CANONICAL_PICK = "not medically necessary under the plan criteria"
CANARY_DENIAL_TEXT = (
    f"Claim for {CANARY} (member {CANARY_MEMBER}) is denied: "
    "not medically necessary."
)


class StubEntity:
    """EntityMatch-shaped stand-in carrying RAW text (engine.py:59-66) —
    exactly what the receipt must NOT copy."""

    def __init__(self, text: str, label: str, confidence: float, category: str) -> None:
        self.text = text
        self.label = label
        self.confidence = confidence
        self.category = category


class StubAnalysis:
    def __init__(self, entities, model_used: str) -> None:
        self.entities = entities
        self.model_used = model_used


def default_analyses():
    return [
        StubAnalysis(
            [
                StubEntity(CANARY, "Disease", 0.91, "disease"),
                StubEntity("Synthetic Patient Name", "Disease", 0.84, "disease"),
            ],
            "disease_detection_superclinical",
        ),
        StubAnalysis(
            [StubEntity(CANARY_MEMBER, "Drug", 0.99, "drug")],
            "pharma_detection_superclinical",
        ),
    ]


class StubEngine:
    """Deidentify/extract run no models; deidentification_for_llm reports a
    configurable status exactly like the real engine's mapping keys."""

    def __init__(self, status: str = "success", analyses=None) -> None:
        self._status = status
        self._analyses = analyses if analyses is not None else default_analyses()

    def deidentify_for_llm(self, text, method="mask"):
        mapping = {"[BLOCK]": "REDACTED", "_deidentification_status": self._status}
        if self._status == "failed":
            mapping["_deidentification_failed"] = "deidentify_exception"
        return "deidentified-synthetic-denial-text", mapping

    def extract_diseases(self, text, confidence=0.65):
        return self._analyses[0]

    def extract_drugs(self, text, confidence=0.70):
        return self._analyses[1]


def model_output(pick=..., include_key: bool = True) -> dict:
    out = {
        "summary": "synthetic summary",
        "urgency": "medium",
        "action_items": ["gather records"],
        "red_flags": [],
        "appeal_arguments": ["medical necessity criteria not met"],
        "draft_appeal": "Dear insurer, please reconsider.",
        "deidentification_status": "success",
        "pii_mapping_size": 1,
    }
    if include_key:
        out["denial_reason"] = pick
    return out


def run_fight_denial(engine=None, llm_output=None, denial_text=None, patient_info: str = "") -> dict:
    engine = engine if engine is not None else StubEngine()
    output = llm_output if llm_output is not None else model_output(pick=CANONICAL_PICK)
    text = denial_text if denial_text is not None else CANARY_DENIAL_TEXT
    with mock.patch.object(
        insurance_fighter, "structured_model_call", return_value=output
    ):
        return insurance_fighter.fight_denial(engine, text, patient_info)


# ---------------------------------------------------------------------------
# The deterministic normalization rule (the code runner)
# ---------------------------------------------------------------------------


class NormalizationRuleTests(unittest.TestCase):
    def test_corpus_fixtures_each_map_to_exactly_one_canonical(self):
        # The measurement behind DENIAL_CLASSIFIER_THRESHOLDS: every frozen
        # corpus fixture must normalize to one canonical option.
        corpus = insurance_fighter._DENIAL_REASON_MEASUREMENT_CORPUS
        self.assertTrue(corpus)
        for fixture in corpus:
            with self.subTest(fixture=fixture[:40]):
                normalized = _normalize_denial_reason(fixture)
                self.assertIn(normalized, DENIAL_REASON_OPTIONS)

    def test_every_canonical_option_is_reachable(self):
        reached = {
            _normalize_denial_reason(fixture)
            for fixture in insurance_fighter._DENIAL_REASON_MEASUREMENT_CORPUS
        }
        self.assertEqual(reached, set(DENIAL_REASON_OPTIONS))

    def test_exact_option_string_maps_to_itself(self):
        for option in DENIAL_REASON_OPTIONS:
            with self.subTest(option=option):
                self.assertEqual(_normalize_denial_reason(option), option)
                self.assertEqual(_normalize_denial_reason(option.upper()), option)

    def test_zero_match_returns_none(self):
        for pick in ("", "   ", "we simply refuse to pay", None, 42, b"denied", {"reason": "x"}):
            with self.subTest(pick=pick):
                self.assertIsNone(_normalize_denial_reason(pick))

    def test_multi_match_returns_none_fail_closed(self):
        # A pick citing two canonical reasons is ambiguous: no confident
        # answer, the human decides (the letter cites both).
        for pick in (
            "not covered because it is excluded from the formulary",
            "prior authorization and additional documentation required",
            "experimental and out of network",
        ):
            with self.subTest(pick=pick):
                self.assertIsNone(_normalize_denial_reason(pick))


# ---------------------------------------------------------------------------
# The question + threshold provenance (surface-linked, measured)
# ---------------------------------------------------------------------------


class QuestionAndThresholdTests(unittest.TestCase):
    def test_question_is_a_choice_over_the_canonical_set(self):
        question = _denial_reason_question()
        self.assertEqual(question.id, DENIAL_REASON_QUESTION_ID)
        self.assertEqual(tuple(question.options), DENIAL_REASON_OPTIONS)
        self.assertEqual(len(set(question.options)), len(question.options))
        self.assertLessEqual(len(question.options), 255)

    def test_threshold_data_is_surface_linked_and_conservative(self):
        data = DENIAL_CLASSIFIER_THRESHOLDS
        self.assertIsInstance(data, ThresholdData)
        self.assertEqual(data.surface, DENIAL_CLASSIFIER_SURFACE)
        self.assertEqual(data.surface, "denial-classifier")
        choice = data.for_class("choice")
        self.assertIsNotNone(choice)
        assert choice is not None
        self.assertEqual(choice.min_confidence, 1.0)  # conservative: exact matches only

    def test_threshold_provenance_is_measured_and_honest(self):
        choice = DENIAL_CLASSIFIER_THRESHOLDS.for_class("choice")
        assert choice is not None
        provenance = choice.provenance
        self.assertEqual(provenance.source, "measured")
        self.assertEqual(provenance.surface, DENIAL_CLASSIFIER_SURFACE)
        # The honest sample: the frozen synthetic corpus in the module.
        self.assertEqual(
            provenance.sample_size,
            len(insurance_fighter._DENIAL_REASON_MEASUREMENT_CORPUS),
        )
        import datetime

        datetime.date.fromisoformat(provenance.measured_on)  # raises if not ISO

    def test_measurement_reproduces_the_threshold(self):
        # Re-running the rule over the corpus fires at the rule confidence
        # and clears the measured threshold — the provenance claim is
        # reproducible, not decorative.
        choice = DENIAL_CLASSIFIER_THRESHOLDS.for_class("choice")
        assert choice is not None
        rule_confidence = insurance_fighter._DENIAL_REASON_RULE_CONFIDENCE
        for fixture in insurance_fighter._DENIAL_REASON_MEASUREMENT_CORPUS:
            with self.subTest(fixture=fixture[:40]):
                self.assertIsNotNone(_normalize_denial_reason(fixture))
        self.assertGreaterEqual(rule_confidence, choice.min_confidence)

    def test_no_threshold_leg_beyond_choice_exists(self):
        # The surface asks exactly one question class; nothing else gates.
        self.assertEqual(set(DENIAL_CLASSIFIER_THRESHOLDS.thresholds), {"choice"})


# ---------------------------------------------------------------------------
# Receipt from the real identify stage
# ---------------------------------------------------------------------------


class ReceiptFromRealIdentifyTests(unittest.TestCase):
    def test_classify_builds_receipt_from_real_analyses_and_status(self):
        analyses = default_analyses()
        outcome, receipt = classify_denial_reason(
            CANONICAL_PICK, analyses, DeidentificationStatus.SUCCESS
        )
        self.assertIsNotNone(receipt)
        assert receipt is not None
        self.assertEqual(
            receipt.model_used,
            "disease_detection_superclinical+pharma_detection_superclinical",
        )
        labels = {(e.label, e.category, e.count) for e in receipt.entity_classes}
        self.assertIn(("Disease", "disease", 2), labels)
        self.assertIn(("Drug", "drug", 1), labels)
        self.assertIs(
            receipt.deidentification_status, DeidentificationStatus.SUCCESS
        )
        self.assertEqual(outcome.reason_kind, "answered")

    def test_no_known_status_means_no_receipt_no_assessment(self):
        outcome, receipt = classify_denial_reason(CANONICAL_PICK, default_analyses(), None)
        self.assertIsNone(receipt)
        self.assertEqual(outcome.outcome, Outcome.NEEDS_HUMAN)
        self.assertEqual(outcome.reason_kind, "invalid-receipt")
        self.assertEqual(outcome.reason, FAIL_CLOSED_SENTENCE)
        types = {e.type for e in outcome.validation_errors}
        self.assertIn("deidentification_status_unknown", types)

    def test_hostile_analysis_builds_no_receipt(self):
        hostile = [
            StubAnalysis(
                [StubEntity(CANARY, "Disease", "0.91", "disease")],  # coerced confidence
                "disease_detection_superclinical",
            ),
            StubAnalysis([], "pharma_detection_superclinical"),
        ]
        outcome, receipt = classify_denial_reason(
            CANONICAL_PICK, hostile, DeidentificationStatus.SUCCESS
        )
        self.assertIsNone(receipt)
        self.assertEqual(outcome.reason_kind, "invalid-receipt")
        self.assertEqual(outcome.reason, FAIL_CLOSED_SENTENCE)

    def test_hand_built_no_receipt_wrapper_matches_assess_vocabulary(self):
        # Non-divergence pin: the no-receipt wrapper uses exactly the
        # invalid-receipt vocabulary assess itself produces.
        reference = assess(
            _denial_reason_question(),
            receipt={"model_used": 42},
            candidate=None,
            surface=DENIAL_CLASSIFIER_SURFACE,
            runner="code",
            thresholds=DENIAL_CLASSIFIER_THRESHOLDS,
        )
        hand_built = classify_denial_reason(
            CANONICAL_PICK, default_analyses(), None
        )[0]
        self.assertEqual(hand_built.reason_kind, reference.reason_kind)
        self.assertEqual(hand_built.reason, reference.reason)
        self.assertEqual(hand_built.allowed_next_steps, reference.allowed_next_steps)
        self.assertEqual(hand_built.outcome, reference.outcome)


# ---------------------------------------------------------------------------
# Fail-closed legs map to the existing safe fallback (""), audit attached
# ---------------------------------------------------------------------------


class FailClosedLegsTests(unittest.TestCase):
    def assert_fallback(self, result: dict, reason_kind: str) -> None:
        # The existing safe fallback for unknown/unclassifiable denials is
        # the empty string — exactly what callers got before conversion
        # whenever the model named no reason.
        self.assertEqual(result["denial_reason"], "")
        decision = result["denial_reason_decision"]
        self.assertEqual(decision["outcome"], "NEEDS_HUMAN")
        self.assertEqual(decision["reason_kind"], reason_kind)
        self.assertEqual(decision["question_id"], DENIAL_REASON_QUESTION_ID)
        self.assertEqual(decision["gate_state"], "review_required")
        self.assertTrue(decision["allowed_next_steps"])

    def test_model_unavailable_pick_missing_falls_back(self):
        llm_output = unavailable_structured_fallback(reason="PrivacyBoundaryError")
        llm_output["deidentification_status"] = "success"
        result = run_fight_denial(llm_output=llm_output)
        self.assert_fallback(result, "invalid-answer")

    def test_unknown_pick_falls_back(self):
        result = run_fight_denial(llm_output=model_output(pick="we simply refuse to pay"))
        self.assert_fallback(result, "invalid-answer")

    def test_blank_pick_falls_back(self):
        result = run_fight_denial(llm_output=model_output(pick="   "))
        self.assert_fallback(result, "invalid-answer")

    def test_non_string_pick_falls_back(self):
        result = run_fight_denial(llm_output=model_output(pick=42))
        self.assert_fallback(result, "invalid-answer")

    def test_ambiguous_pick_falls_back(self):
        result = run_fight_denial(
            llm_output=model_output(pick="not covered because excluded from the formulary")
        )
        self.assert_fallback(result, "invalid-answer")

    def test_failed_deidentification_falls_back(self):
        result = run_fight_denial(engine=StubEngine(status="failed"))
        self.assert_fallback(result, "deidentification-failed")

    def test_unknown_deidentification_status_falls_back(self):
        result = run_fight_denial(engine=StubEngine(status="garbage"))
        self.assert_fallback(result, "invalid-receipt")

    def test_every_needs_human_reason_kind_maps_to_fallback(self):
        # The mapping rule itself: ANY NEEDS_HUMAN wrapper — whatever leg —
        # yields the fallback, never a confident answer. Representative
        # legs built through the real assess gate.
        question = _denial_reason_question()
        receipt = IdentificationReceipt(
            model_used="synthetic-ner-fixture",
            entity_classes=[],
            coverage_notes=[],
            deidentification_status=DeidentificationStatus.SUCCESS,
        )
        good = ChoiceAnswer(
            question_id=DENIAL_REASON_QUESTION_ID,
            value="not medically necessary",
            probability=1.0,
            confidence=1.0,
        )
        weak = ChoiceAnswer(
            question_id=DENIAL_REASON_QUESTION_ID,
            value="not medically necessary",
            probability=0.5,
            confidence=0.5,
        )
        cases = {
            "below-threshold": dict(
                receipt=receipt, candidate=weak, runner="code",
                thresholds=DENIAL_CLASSIFIER_THRESHOLDS,
            ),
            "threshold-data-missing": dict(
                receipt=receipt, candidate=good, runner="code", thresholds=None
            ),
            "unknown-runner": dict(
                receipt=receipt, candidate=good, runner="gpt-9-magic",
                thresholds=DENIAL_CLASSIFIER_THRESHOLDS,
            ),
            "invalid-answer": dict(
                receipt=receipt, candidate=None, runner="code",
                thresholds=DENIAL_CLASSIFIER_THRESHOLDS,
            ),
            "invalid-receipt": dict(
                receipt={"model_used": 42}, candidate=good, runner="code",
                thresholds=DENIAL_CLASSIFIER_THRESHOLDS,
            ),
        }
        for kind, kwargs in cases.items():
            with self.subTest(reason_kind=kind):
                outcome = assess(
                    question,
                    surface=DENIAL_CLASSIFIER_SURFACE,
                    **kwargs,
                )
                self.assertEqual(outcome.reason_kind, kind)
                self.assertEqual(outcome.outcome, Outcome.NEEDS_HUMAN)
                self.assertEqual(_denial_reason_from_outcome(outcome), "")

    def test_answered_outcome_maps_to_the_canonical_value(self):
        outcome = classify_denial_reason(
            CANONICAL_PICK, default_analyses(), DeidentificationStatus.SUCCESS
        )[0]
        self.assertEqual(outcome.outcome, Outcome.ANSWERED)
        self.assertEqual(
            _denial_reason_from_outcome(outcome), "not medically necessary"
        )


# ---------------------------------------------------------------------------
# Caller-shape stability (app endpoint keys + CLI checklist consumption)
# ---------------------------------------------------------------------------


class CallerShapeTests(unittest.TestCase):
    def test_result_keeps_every_existing_key_and_type(self):
        result = run_fight_denial()
        for key in (
            "denial_text", "entities_found", "explanation", "urgency",
            "action_items", "red_flags", "denial_reason", "appeal_arguments",
            "draft_appeal", "structured_output", "validation", "pii_scrubbed",
        ):
            self.assertIn(key, result, key)
        self.assertIsInstance(result["action_items"], list)
        self.assertIsInstance(result["red_flags"], list)
        self.assertIsInstance(result["appeal_arguments"], list)
        self.assertIsInstance(result["draft_appeal"], str)
        self.assertIsInstance(result["urgency"], str)

    def test_decision_audit_is_additive(self):
        result = run_fight_denial()
        self.assertIn("denial_reason_decision", result)
        self.assertIn("denial_reason_receipt", result)
        decision = result["denial_reason_decision"]
        self.assertEqual(decision["outcome"], "ANSWERED")
        self.assertEqual(decision["reason_kind"], "answered")
        self.assertEqual(decision["question_class"], "choice")
        self.assertEqual(decision["runner"], "code")
        self.assertEqual(decision["threshold_applied"], 1.0)
        self.assertEqual(decision["gate_state"], "allowed")
        self.assertEqual(decision["answer"]["value"], "not medically necessary")

    def test_classified_reason_feeds_the_cli_checklist(self):
        result = run_fight_denial()
        checklist = denial_checklist({"denial_reason": result["denial_reason"]})
        self.assertEqual(checklist["denial_reason"], "not medically necessary")
        self.assertTrue(checklist["checklist"])
        self.assertTrue(
            any("not medically necessary" in frame for frame in checklist["appeal_frame"])
        )

    def test_fallback_reason_feeds_the_cli_checklist_safely(self):
        result = run_fight_denial(llm_output=model_output(pick="refused"))
        self.assertEqual(result["denial_reason"], "")
        checklist = denial_checklist({"denial_reason": result["denial_reason"]})
        # The CLI's existing default phrasing absorbs the empty fallback.
        self.assertEqual(
            checklist["denial_reason"], "the stated denial reason"
        )

    def test_identical_inputs_are_idempotent(self):
        first = run_fight_denial()
        second = run_fight_denial()
        self.assertEqual(first["denial_reason"], second["denial_reason"])
        self.assertEqual(
            json.dumps(first["denial_reason_decision"], sort_keys=True),
            json.dumps(second["denial_reason_decision"], sort_keys=True),
        )
        self.assertEqual(
            json.dumps(first["denial_reason_receipt"], sort_keys=True),
            json.dumps(second["denial_reason_receipt"], sort_keys=True),
        )

    def test_empty_denial_text_short_circuits_without_audit_noise(self):
        result = insurance_fighter.fight_denial(StubEngine(), "   ")
        self.assertEqual(
            result,
            {"explanation": "No denial text provided.", "action_items": [],
             "red_flags": [], "validation": None},
        )


# ---------------------------------------------------------------------------
# Canary PHI-free tripwire (this surface): canary-bearing denial_text never
# leaks into the serialized decision wrapper or receipt.
# ---------------------------------------------------------------------------


class CanaryPhiFreeTripwireTests(unittest.TestCase):
    def test_answered_path_wrapper_and_receipt_stay_clean(self):
        result = run_fight_denial(
            engine=StubEngine(),
            llm_output=model_output(pick=CANONICAL_PICK),
            denial_text=CANARY_DENIAL_TEXT,
            patient_info=f"Patient {CANARY} member {CANARY_MEMBER}",
        )
        self.assertEqual(result["denial_reason"], "not medically necessary")
        wrapper_json = json.dumps(result["denial_reason_decision"])
        receipt_json = json.dumps(result["denial_reason_receipt"])
        for text in RAW_ENTITY_TEXTS:
            self.assertNotIn(text, wrapper_json)
            self.assertNotIn(text, receipt_json)

    def test_fail_closed_path_wrapper_stays_clean(self):
        result = run_fight_denial(
            llm_output=model_output(pick=f"refused for {CANARY} reasons")
        )
        self.assertEqual(result["denial_reason"], "")
        wrapper_json = json.dumps(result["denial_reason_decision"])
        for text in RAW_ENTITY_TEXTS:
            self.assertNotIn(text, wrapper_json)

    def test_wrapper_from_non_string_pick_never_echoes_value(self):
        result = run_fight_denial(llm_output=model_output(pick=[CANARY]))
        self.assertEqual(result["denial_reason"], "")
        wrapper_json = json.dumps(result["denial_reason_decision"])
        self.assertNotIn(CANARY, wrapper_json)

    def test_receipt_rejected_by_the_gate_is_never_attached(self):
        # Belt-and-braces: the builder redacts free text, so a canary in a
        # hostile engine's model_used never survives into a receipt this
        # surface builds. Whatever happens, the attached receipt (when any)
        # is canary-free, and a receipt the gate rejected never rides into
        # the result as audit.
        canary_model = [
            StubAnalysis([], f"ner-with-{CANARY}"),
            StubAnalysis([], "pharma_detection_superclinical"),
        ]
        result = run_fight_denial(engine=StubEngine(analyses=canary_model))
        receipt_json = json.dumps(result["denial_reason_receipt"])
        self.assertNotIn(CANARY, receipt_json)
        self.assertNotIn(CANARY_MEMBER, receipt_json)
        if result["denial_reason_decision"]["reason_kind"] == "invalid-receipt":
            self.assertIsNone(result["denial_reason_receipt"])


if __name__ == "__main__":
    unittest.main()
