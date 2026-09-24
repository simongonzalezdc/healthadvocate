"""Model-off honesty pins (Lane C fix, 2026-09-24 findings 1/2/4/5).

The model runtime is OFF by default (HEALTHADVOCATE_MODEL_ENABLED
defaults to "0", healthadvocate/core/llm_client.py). With it off:

- the fallback shape must carry urgency "unavailable" — a hardcoded
  "medium" is a fabricated judgment served on every generative surface;
- the symptom surface must surface urgency "unavailable": the typed
  decision layer maps the no-judgment placeholder (`_model_blocked`)
  to the honest state, not to the conservative alarm "high", which made
  "model off" indistinguishable from a real emergency;
- every OTHER fail-closed leg keeps the conservative "high": a real but
  unparseable model response (`_raw_text`), a deidentification failure,
  an unbuildable receipt, an out-of-rubric pick, and any NER/LLM
  urgency disagreement. The safety guarantee is unchanged — only the
  no-judgment leg stops pretending a judgment exists.
"""

from __future__ import annotations

import unittest
from unittest import mock

from healthadvocate.core.engine import AnalysisResult, EntityMatch
from healthadvocate.core import symptom_assessor
from healthadvocate.core.llm_client import unavailable_structured_fallback
from healthadvocate.decisions import DecisionOutcome, Outcome
from healthadvocate.decisions.symptom_triage import (
    MODEL_UNAVAILABLE_URGENCY as UNAVAILABLE_URGENCY,
    URGENCY_QUESTION,
    external_urgency,
)


def make_engine(model_used="disease_detection_superclinical"):
    """A stub HealthEngine whose identify stage is deterministic
    (tests/test_symptom_triage_jev.py:43 pattern)."""
    engine = mock.Mock(spec=["extract_diseases"])
    engine.extract_diseases.return_value = AnalysisResult(
        entities=[
            EntityMatch(
                text="headache", label="Disease", confidence=0.95,
                start=0, end=1, category="disease",
            )
        ],
        model_used=model_used,
        processing_time=0.01,
    )
    return engine


def run_assessment(llm_output, symptoms="mild headache for a day"):
    """assess_symptoms with the gated model call canned (no model, no
    network; the privacy boundary itself is tested elsewhere).

    Mirrors privacy/gated_model.py: the gated call always stamps the
    measured deidentification status onto its output — the model-off
    fallback carries status "success" (the deidentification itself is
    deterministic and ran)."""
    output = dict(llm_output)
    output.setdefault("deidentification_status", "success")
    with mock.patch.object(
        symptom_assessor, "structured_model_call", return_value=output
    ):
        return symptom_assessor.assess_symptoms(make_engine(), symptoms)


def needs_human(kind="invalid-answer"):
    return DecisionOutcome(
        outcome=Outcome.NEEDS_HUMAN, reason_kind=kind,
        question_id=URGENCY_QUESTION.id, question_class="score",
        runner="code", reason="synthetic leg",
        allowed_next_steps=["Decide as a human"],
    )


class FallbackShapeTests(unittest.TestCase):
    def test_fallback_urgency_is_unavailable_not_a_guess(self):
        fallback = unavailable_structured_fallback()
        self.assertEqual(fallback["urgency"], "unavailable")
        self.assertTrue(fallback["_model_blocked"])
        self.assertEqual(fallback["red_flags"], [])

    def test_fallback_is_the_no_judgment_shape(self):
        # The summary says no judgment was made; action items point at
        # the manual workflows (llm_client.unavailable_structured_fallback).
        fallback = unavailable_structured_fallback()
        self.assertIn("unavailable", fallback["summary"].lower())
        self.assertTrue(fallback["action_items"])


class SymptomSurfaceModelOffTests(unittest.TestCase):
    """Findings 1/2: model-off symptoms must not read as an emergency."""

    def test_model_off_urgency_is_unavailable(self):
        result = run_assessment(unavailable_structured_fallback())
        self.assertEqual(result["urgency"], "unavailable")

    def test_model_off_decision_is_needs_human_with_steps(self):
        result = run_assessment(unavailable_structured_fallback())
        decision = result["urgency_decision"]
        self.assertEqual(decision["outcome"], "NEEDS_HUMAN")
        self.assertTrue(decision["allowed_next_steps"])
        self.assertTrue(decision["reason"])

    def test_model_off_explanation_is_the_unavailable_notice(self):
        result = run_assessment(unavailable_structured_fallback())
        self.assertIn("unavailable", result["explanation"].lower())
        self.assertFalse(result["validation"]["urgency_disagreement"])

    def test_model_off_is_not_the_disagreement_rule(self):
        # The benign entity at 0.95 must NOT trip the NER/LLM
        # disagreement escalation (that rule needs a real LLM "low").
        result = run_assessment(unavailable_structured_fallback())
        self.assertNotEqual(result["urgency"], "high")


class ConservativeLegsUnchangedTests(unittest.TestCase):
    """The safety guarantee: every leg that involves a real (or
    unrejected) judgment still escalates to the conservative "high"."""

    def test_deidentification_failure_still_escalates(self):
        output = dict(
            unavailable_structured_fallback(),
            deidentification_status="failed",
        )
        result = run_assessment(output)
        self.assertEqual(result["urgency"], "high")
        self.assertEqual(
            result["urgency_decision"]["reason_kind"], "deidentification-failed"
        )

    def test_unparseable_real_response_still_escalates(self):
        # _raw_text: the model RAN and produced text we could not parse —
        # conservative, not "unavailable".
        output = {
            "summary": "unparseable model text", "urgency": "medium",
            "action_items": [], "red_flags": [], "_raw_text": True,
            "deidentification_status": "success",
        }
        result = run_assessment(output)
        self.assertEqual(result["urgency"], "high")

    def test_out_of_rubric_pick_still_escalates(self):
        result = run_assessment({
            "summary": "s", "urgency": "urgent-ish",
            "action_items": [], "red_flags": [],
            "deidentification_status": "success",
        })
        self.assertEqual(result["urgency"], "high")

    def test_unbuildable_receipt_still_escalates(self):
        with mock.patch.object(
            symptom_assessor, "structured_model_call",
            return_value={
                "summary": "s", "urgency": "low",
                "action_items": [], "red_flags": [],
                "deidentification_status": "success",
            },
        ):
            result = symptom_assessor.assess_symptoms(make_engine(model_used=""), "x")
        self.assertEqual(result["urgency"], "high")


class TriageMappingContractTests(unittest.TestCase):
    def test_unavailable_constant_exists(self):
        from healthadvocate.decisions.symptom_triage import MODEL_UNAVAILABLE_URGENCY as UNAVAILABLE_URGENCY
        self.assertEqual(UNAVAILABLE_URGENCY, "unavailable")

    def test_no_judgment_leg_maps_unavailable(self):
        self.assertEqual(
            external_urgency(needs_human(), False, model_unavailable=True),
            "unavailable",
        )

    def test_no_judgment_waives_exactly_the_silent_legs(self):
        # The no-judgment carve-out covers BOTH silent legs — the fallback
        # with a compliant-but-zero-confidence pick (below-threshold) and
        # the fallback whose honest "unavailable" urgency leaves no
        # candidate at all (invalid-answer). Every other NEEDS_HUMAN kind
        # stays conservative even when the output carried the placeholder
        # marker (merge-fix 2026-09-24: the narrower waiver was the
        # regression that made the default build scream HIGH).
        for waived in ("below-threshold", "invalid-answer"):
            with self.subTest(kind=waived):
                self.assertEqual(
                    external_urgency(needs_human(waived), False, model_unavailable=True),
                    "unavailable",
                )
        for kind in (
            "threshold-data-missing",
            "threshold-data-malformed", "threshold-surface-mismatch",
            "unknown-runner", "invalid-receipt", "deidentification-failed",
            "invalid-question",
        ):
            with self.subTest(kind=kind):
                self.assertEqual(
                    external_urgency(needs_human(kind), False, model_unavailable=True),
                    "high",
                )

    def test_real_invalid_answer_still_conservative(self):
        self.assertEqual(
            external_urgency(needs_human(), False, model_unavailable=False),
            "high",
        )

    def test_disagreement_dominates_no_judgment(self):
        answered = DecisionOutcome(
            outcome=Outcome.ANSWERED, reason_kind="answered",
            question_id=URGENCY_QUESTION.id, question_class="score",
            runner="code", reason="synthetic", allowed_next_steps=[],
            threshold_applied=0.5,
        )
        self.assertEqual(
            external_urgency(answered, True, model_unavailable=True), "high"
        )

    def test_default_mapping_unchanged_without_flag(self):
        # Back-compat: the two-argument call keeps the J2-c contract.
        self.assertEqual(external_urgency(needs_human(), False), "high")


if __name__ == "__main__":
    unittest.main()
