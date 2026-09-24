"""J2-c contract tests: symptom-triage urgency routed through HA-JEV.

Converts the symptom assessor's urgency pick to a typed ScoreQuestion
(design 2026-09-22 §5 J2, surface: symptom-triage) behind the J1 layer:
identification receipt from the REAL identify stage, surface-linked
threshold data with honest (policy-tier) provenance, and the load-bearing
safety rule — every NEEDS_HUMAN leg and every urgency_disagreement
surfaces externally as the conservative highest urgency ("high"), never
"low", with the audit numbers attached.

Pinned pre-conversion behaviors (the surface had no direct tests): the
normal low/medium/high picks surface as-is; the missing-urgency default
is "medium"; NER/LLM urgency disagreement escalates to "high"; empty
input returns the early "low" dict unchanged. Synthetic fixtures only.

Triage honesty (audit D2, 2026-09-24): the documented default build runs
with the optional local model OFF, and that build must not label every
symptom HIGH. A model-unavailable output (unavailable_structured_fallback
shape, `_model_blocked` marker) carries NO structured judgment — its
placeholder pick escalates to a fabricated "high". The external value for
exactly that leg is now "unavailable" with a model-off explanation, while
the two safety escalations are untouched and pinned in BOTH directions:
a GENUINELY answered below-threshold pick still surfaces "high", and any
urgency_disagreement still dominates everything.
"""

from __future__ import annotations

import inspect
import json
import unittest
from unittest import mock

from healthadvocate.core.engine import AnalysisResult, EntityMatch
from healthadvocate.core import symptom_assessor
from healthadvocate.decisions import DecisionOutcome, Outcome, assess
from healthadvocate.decisions.thresholds import ThresholdData
from healthadvocate.privacy.boundary import DeidentificationStatus

CANARY = "CANARY_PATIENT_ALPHA_9f3c"
CANARY_MEMBER = "MEMBER-ID-SYNTH-42"
RAW_ENTITY_TEXTS = (CANARY, CANARY_MEMBER)

BENIGN_OUTPUT = {
    "summary": "Mild symptoms; monitor at home.",
    "urgency": "low",
    "action_items": ["Rest and hydrate"],
    "red_flags": [],
    "deidentification_status": "success",
}


def make_engine(entities=None, model_used="disease_detection_superclinical"):
    """A stub HealthEngine whose identify stage is deterministic."""
    engine = mock.Mock(spec=["extract_diseases"])
    engine.extract_diseases.return_value = AnalysisResult(
        entities=[
            EntityMatch(
                text=e["text"], label=e.get("label", "Disease"),
                confidence=e["confidence"], start=0, end=1,
                category=e.get("category", "disease"),
            )
            for e in (entities or [])
        ],
        model_used=model_used,
        processing_time=0.01,
    )
    return engine


def run_assessment(engine, llm_output, symptoms="mild headache for a day"):
    """Call assess_symptoms with structured_model_call patched to a canned,
    already-deidentified output (the boundary itself is tested elsewhere)."""
    with mock.patch.object(
        symptom_assessor, "structured_model_call", return_value=dict(llm_output)
    ):
        return symptom_assessor.assess_symptoms(engine, symptoms)


def decision(result):
    return result["urgency_decision"]


def receipt_json(result):
    return json.dumps(result["urgency_receipt"])


def decision_json(result):
    return json.dumps(decision(result))


class RubricAndQuestionTests(unittest.TestCase):
    def test_rubric_is_ascending_with_conservative_last(self):
        from healthadvocate.decisions.symptom_triage import (
            CONSERVATIVE_URGENCY, URGENCY_QUESTION, URGENCY_RUBRIC,
        )
        from healthadvocate.decisions import question_class

        # Documented order: ScoreAnswer.level ASCENDS in severity —
        # 0=low, 1=medium, 2=high — so the conservative fail-closed label
        # is the LAST rubric entry (J1 schema convention: level indexes
        # the rubric; J1 fixtures order low->high).
        self.assertEqual(URGENCY_RUBRIC, ("low", "medium", "high"))
        self.assertEqual(CONSERVATIVE_URGENCY, "high")
        self.assertEqual(CONSERVATIVE_URGENCY, URGENCY_RUBRIC[-1])
        self.assertEqual(question_class(URGENCY_QUESTION), "score")
        self.assertEqual(
            [level.label for level in URGENCY_QUESTION.rubric],
            ["low", "medium", "high"],
        )


class ThresholdHonestyTests(unittest.TestCase):
    def test_thresholds_are_surface_linked_and_policy_honest(self):
        from healthadvocate.decisions.symptom_triage import (
            SYMPTOM_TRIAGE_THRESHOLDS, TRIAGE_SURFACE,
        )
        self.assertEqual(TRIAGE_SURFACE, "symptom-triage")
        data = SYMPTOM_TRIAGE_THRESHOLDS
        self.assertIsInstance(data, ThresholdData)
        self.assertEqual(data.surface, TRIAGE_SURFACE)
        score = data.for_class("score")
        self.assertIsNotNone(score, "the surface asks a score question")
        prov = score.provenance
        # Honest provenance: a policy threshold SAYS it is policy — it
        # never masquerades as measured — and carries dated rationale.
        self.assertEqual(prov.source, "policy")
        self.assertEqual(prov.surface, TRIAGE_SURFACE)
        self.assertTrue(prov.adopted_on)
        self.assertTrue(prov.rationale and prov.rationale.strip())

    def test_cross_surface_threshold_data_fails_closed_here_too(self):
        from healthadvocate.decisions.symptom_triage import (
            SYMPTOM_TRIAGE_THRESHOLDS,
        )
        wrong = SYMPTOM_TRIAGE_THRESHOLDS.model_copy(
            update={"surface": "denial-classifier"}
        )
        # model_copy bypasses validators; rebuild honestly instead.
        payload = SYMPTOM_TRIAGE_THRESHOLDS.model_dump()
        payload["surface"] = "denial-classifier"
        for entry in payload["thresholds"].values():
            entry["provenance"]["surface"] = "denial-classifier"
        wrong = ThresholdData.model_validate(payload)
        outcome = assess(
            _question(), receipt=_receipt(), candidate=_candidate("low"),
            surface="symptom-triage", runner="code", thresholds=wrong,
        )
        self.assertEqual(outcome.reason_kind, "threshold-surface-mismatch")
        self.assertEqual(outcome.outcome, "NEEDS_HUMAN")


def _question():
    from healthadvocate.decisions.symptom_triage import URGENCY_QUESTION
    return URGENCY_QUESTION


def _receipt():
    from healthadvocate.decisions.receipt import IdentificationReceipt
    return IdentificationReceipt(
        model_used="disease_detection_superclinical",
        entity_classes=[],
        coverage_notes=[],
        deidentification_status=DeidentificationStatus.SUCCESS,
    )


def _candidate(pick="low", confidence=1.0):
    from healthadvocate.decisions import ScoreAnswer
    level = {"low": 0, "medium": 1, "high": 2}[pick]
    probs = [0.0, 0.0, 0.0]
    probs[level] = 1.0
    return ScoreAnswer(
        question_id="symptom-triage-urgency", level=level,
        per_level_probabilities=probs, confidence=confidence,
    )


class NormalLegsPreservedTests(unittest.TestCase):
    def test_llm_pick_surfaces_as_is(self):
        for urgency in ("low", "medium", "high"):
            with self.subTest(urgency=urgency):
                output = dict(BENIGN_OUTPUT, urgency=urgency)
                result = run_assessment(make_engine(), output)
                self.assertEqual(result["urgency"], urgency)
                self.assertEqual(decision(result)["outcome"], "ANSWERED")
                self.assertEqual(decision(result)["answer"]["level"],
                                 {"low": 0, "medium": 1, "high": 2}[urgency])
                self.assertEqual(decision(result)["threshold_applied"], 0.5)

    def test_missing_urgency_defaults_to_medium(self):
        output = dict(BENIGN_OUTPUT)
        del output["urgency"]
        result = run_assessment(make_engine(), output)
        self.assertEqual(result["urgency"], "medium")
        self.assertEqual(decision(result)["answer"]["level"], 1)

    def test_answered_carries_audit_numbers(self):
        result = run_assessment(make_engine(), dict(BENIGN_OUTPUT))
        wrapper = decision(result)
        self.assertEqual(wrapper["question_id"], "symptom-triage-urgency")
        self.assertEqual(wrapper["question_class"], "score")
        self.assertEqual(wrapper["runner"], "code")
        self.assertEqual(wrapper["answer"]["confidence"], 1.0)
        self.assertEqual(wrapper["answer"]["per_level_probabilities"],
                         [1.0, 0.0, 0.0])
        self.assertEqual(wrapper["answer"]["score_source"], "raw")
        self.assertTrue(wrapper["reason"])
        self.assertTrue(wrapper["allowed_next_steps"])


class DisagreementEscalationTests(unittest.TestCase):
    """The pre-conversion safety escalation, unchanged in strength."""

    def test_ner_high_urgency_disagreement_forces_high(self):
        engine = make_engine([{"text": "chest pain", "confidence": 0.85}])
        result = run_assessment(engine, dict(BENIGN_OUTPUT, urgency="low"))
        # The wrapper may say ANSWERED at level 0 — disagreement
        # DOMINATES the external answer anyway (today's behavior).
        self.assertEqual(result["urgency"], "high")
        self.assertTrue(result["validation"]["urgency_disagreement"])

    def test_below_trigger_confidence_keeps_low(self):
        engine = make_engine([{"text": "chest pain", "confidence": 0.79}])
        result = run_assessment(engine, dict(BENIGN_OUTPUT, urgency="low"))
        self.assertEqual(result["urgency"], "low")
        self.assertFalse(result["validation"]["urgency_disagreement"])

    def test_benign_entity_keeps_low(self):
        engine = make_engine([{"text": "mild headache", "confidence": 0.95}])
        result = run_assessment(engine, dict(BENIGN_OUTPUT, urgency="low"))
        self.assertEqual(result["urgency"], "low")


class FailClosedLegsEscalateTests(unittest.TestCase):
    """Load-bearing: every NEEDS_HUMAN leg surfaces as the conservative
    highest urgency with audit numbers — never "low", never silent.
    (One carve-out since audit D2: the model-UNAVAILABLE placeholder leg
    externalizes as "unavailable" — see ModelUnavailableHonestyTests; a
    `_raw_text` output is NOT model-unavailable and still escalates.)"""

    def test_deidentification_failed_escalates(self):
        output = dict(BENIGN_OUTPUT, urgency="medium",
                      deidentification_status="failed", _model_blocked=True)
        result = run_assessment(make_engine(), output)
        self.assertEqual(result["urgency"], "high")
        self.assertEqual(decision(result)["reason_kind"],
                         "deidentification-failed")
        self.assertIsNone(decision(result)["answer"])

    def test_unparseable_raw_text_placeholder_escalates(self):
        output = dict(BENIGN_OUTPUT, urgency="low", _raw_text=True)
        result = run_assessment(make_engine(), output)
        self.assertEqual(result["urgency"], "high")
        self.assertEqual(decision(result)["reason_kind"], "below-threshold")

    def test_out_of_rubric_urgency_string_escalates(self):
        output = dict(BENIGN_OUTPUT, urgency="urgent-ish")
        result = run_assessment(make_engine(), output)
        self.assertEqual(result["urgency"], "high")
        wrapper = decision(result)
        self.assertEqual(wrapper["reason_kind"], "invalid-answer")
        self.assertIsNone(wrapper["answer"])
        self.assertTrue(wrapper["validation_errors"])

    def test_non_string_urgency_escalates(self):
        for bad in (3, None, ["high"], {"level": 2}):
            with self.subTest(bad=bad):
                output = dict(BENIGN_OUTPUT, urgency=bad)
                result = run_assessment(make_engine(), output)
                self.assertEqual(result["urgency"], "high")
                self.assertEqual(decision(result)["reason_kind"],
                                 "invalid-answer")

    def test_unbuildable_receipt_fails_closed(self):
        # Hostile identify-stage output (blank model_used): no receipt
        # can be built, none is fabricated, the decision fails closed.
        engine = make_engine([], model_used="")
        result = run_assessment(engine, dict(BENIGN_OUTPUT))
        self.assertEqual(result["urgency"], "high")
        wrapper = decision(result)
        self.assertEqual(wrapper["reason_kind"], "invalid-receipt")
        self.assertTrue(wrapper["validation_errors"])
        self.assertIsNone(result["urgency_receipt"])

    def test_every_needs_human_kind_maps_conservative(self):
        from healthadvocate.decisions.symptom_triage import external_urgency
        kinds = (
            "below-threshold", "threshold-data-missing",
            "threshold-data-malformed", "threshold-surface-mismatch",
            "unknown-runner", "invalid-receipt", "deidentification-failed",
            "invalid-question", "invalid-answer",
        )
        for kind in kinds:
            with self.subTest(kind=kind):
                outcome = DecisionOutcome(
                    outcome=Outcome.NEEDS_HUMAN, reason_kind=kind,
                    question_id="symptom-triage-urgency", question_class="score",
                    runner="code", reason="synthetic leg",
                    allowed_next_steps=["Decide as a human"],
                )
                self.assertEqual(external_urgency(outcome, False), "high")
                self.assertNotEqual(external_urgency(outcome, False), "low")

    def test_disagreement_dominates_answered_in_mapping(self):
        from healthadvocate.decisions.symptom_triage import external_urgency
        answered = DecisionOutcome(
            outcome=Outcome.ANSWERED, reason_kind="answered",
            question_id="symptom-triage-urgency", question_class="score",
            runner="code", reason="synthetic", allowed_next_steps=[],
            answer=_candidate("low"), threshold_applied=0.5,
        )
        self.assertEqual(external_urgency(answered, False), "low")
        self.assertEqual(external_urgency(answered, True), "high")


class SevereModelOffSafetyTests(unittest.TestCase):
    """Audit D2 round 2 (2026-09-24): the carve-out must not swallow the
    SEVERE input leg on the real default build (model off). The fallback
    placeholder urgency is "medium", so the original disagreement rule
    (fires only on llm urgency "low") was unreachable model-off, and the
    D2 carve-out surfaced every NER high-urgency term as "unavailable" —
    while the parent commit escalated this same leg to HIGH. The
    generalized rule pinned here: a PLACEHOLDER urgency is not a rating,
    so the NER high-urgency trigger escalates regardless (README:111's
    override is reachable on the default build)."""

    def _model_off_output(self):
        """The REAL default-build output: unavailable_structured_fallback
        plus the fields structured_model_call adds on the success path."""
        from healthadvocate.core.llm_client import unavailable_structured_fallback
        output = unavailable_structured_fallback(reason="PrivacyBoundaryError")
        output["deidentification_status"] = "success"
        output["pii_mapping_size"] = 0
        return output

    def test_every_high_urgency_term_surfaces_high_with_model_off(self):
        from healthadvocate.core.cross_validation import _HIGH_URGENCY_TERMS
        self.assertEqual(len(_HIGH_URGENCY_TERMS), 13)  # the finding's count
        for term in sorted(_HIGH_URGENCY_TERMS):
            with self.subTest(term=term):
                engine = make_engine([{"text": term, "confidence": 0.99}])
                result = run_assessment(
                    engine, self._model_off_output(),
                    symptoms=f"patient reports {term}",
                )
                # NEVER "unavailable" when NER flags a severe input.
                self.assertEqual(result["urgency"], "high")
                self.assertNotEqual(result["urgency"], "unavailable")
                # The payload self-explains the escalation (the glass
                # renders the disagreement safety flag from this).
                self.assertTrue(result["validation"]["urgency_disagreement"])
                # The audit trail is unchanged: still below-threshold
                # with the zero-measurement numbers attached.
                self.assertEqual(decision(result)["reason_kind"],
                                 "below-threshold")

    def test_sub_trigger_confidence_severe_term_stays_unavailable(self):
        # 0.79 < the 0.80 trigger bar: no NER signal, so the honest
        # model-off value stands (same bar as the model-on rule).
        engine = make_engine([{"text": "chest pain", "confidence": 0.79}])
        result = run_assessment(engine, self._model_off_output())
        self.assertEqual(result["urgency"], "unavailable")
        self.assertFalse(result["validation"]["urgency_disagreement"])

    def test_benign_entity_stays_unavailable_model_off(self):
        engine = make_engine([{"text": "mild headache", "confidence": 0.95}])
        result = run_assessment(engine, self._model_off_output())
        self.assertEqual(result["urgency"], "unavailable")
        self.assertFalse(result["validation"]["urgency_disagreement"])

    def test_unparseable_with_severe_term_escalates_with_disagreement(self):
        # The placeholder "urgency" in the _raw_text shape is not a
        # rating either; the marker (not the value) drives the rule.
        engine = make_engine([{"text": "chest pain", "confidence": 0.85}])
        output = dict(BENIGN_OUTPUT, urgency="medium", _raw_text=True)
        result = run_assessment(engine, output)
        self.assertEqual(result["urgency"], "high")
        self.assertTrue(result["validation"]["urgency_disagreement"])

    def test_genuine_medium_answer_keeps_disagreement_off(self):
        # A GENUINE "medium" rating is a real model judgment; the
        # pre-existing rule's acceptance of it is unchanged.
        engine = make_engine([{"text": "chest pain", "confidence": 0.85}])
        result = run_assessment(engine, dict(BENIGN_OUTPUT, urgency="medium"))
        self.assertFalse(result["validation"]["urgency_disagreement"])
        self.assertEqual(result["urgency"], "medium")


class ModelUnavailableHonestyTests(unittest.TestCase):
    """Audit D2 (2026-09-24): the documented default build (model OFF)
    must not label every symptom HIGH. A model-unavailable output is the
    pipeline's own "no structured judgment was made" signal; escalating
    its placeholder to "high" fabricates an assessment. External value:
    "unavailable" (not a rubric level, so no high badge can render),
    with an explanation naming the model being off and deterministic
    preparation remaining. The audit wrapper keeps its honest audit
    trail (below-threshold, confidence 0.0, threshold attached)."""

    def _default_build_output(self):
        """The REAL model-off shape: unavailable_structured_fallback plus
        the fields structured_model_call adds on the deid-success path."""
        from healthadvocate.core.llm_client import unavailable_structured_fallback
        output = unavailable_structured_fallback(reason="PrivacyBoundaryError")
        output["deidentification_status"] = "success"
        output["pii_mapping_size"] = 0
        return output

    def test_model_off_mild_input_is_unavailable_never_high(self):
        result = run_assessment(make_engine(), self._default_build_output())
        # Direction (a) of the D2 split: model made no structured
        # judgment, so the external urgency is "unavailable" — never
        # "high" (and never a rubric label at all).
        self.assertEqual(result["urgency"], "unavailable")
        self.assertNotEqual(result["urgency"], "high")
        # The audit trail is unchanged: the placeholder pick is still
        # below-threshold with zero-measurement confidence attached.
        wrapper = decision(result)
        self.assertEqual(wrapper["reason_kind"], "below-threshold")
        self.assertEqual(wrapper["outcome"], "NEEDS_HUMAN")
        self.assertEqual(wrapper["answer"]["confidence"], 0.0)
        self.assertEqual(wrapper["answer"]["level"], 1)
        self.assertEqual(wrapper["threshold_applied"], 0.5)

    def test_model_off_explanation_names_model_off_and_deterministic_prep(self):
        from healthadvocate.decisions.symptom_triage import (
            MODEL_UNAVAILABLE_EXPLANATION,
        )
        result = run_assessment(make_engine(), self._default_build_output())
        explanation = result["explanation"]
        self.assertEqual(explanation, MODEL_UNAVAILABLE_EXPLANATION)
        lowered = explanation.lower()
        self.assertIn("optional local model", lowered)
        self.assertIn("unavailable", lowered)
        self.assertIn("deterministic", lowered)

    def test_marker_only_output_also_maps_unavailable(self):
        # The marker alone (not the full fallback shape) is the
        # model-unavailable signal; the explanation stays total even
        # when the crafted output carried no summary of its own.
        output = {"urgency": "medium", "_model_blocked": True,
                  "deidentification_status": "success"}
        result = run_assessment(make_engine(), output)
        self.assertEqual(result["urgency"], "unavailable")
        self.assertIn("optional local model",
                      result["explanation"].lower())

    def test_is_model_unavailable_detects_exactly_the_fallback_shape(self):
        from healthadvocate.core.llm_client import (
            unavailable_structured_fallback,
        )
        from healthadvocate.decisions.symptom_triage import (
            MODEL_UNAVAILABLE_URGENCY, URGENCY_RUBRIC, build_urgency_candidate,
            is_model_unavailable,
        )
        self.assertTrue(is_model_unavailable(
            unavailable_structured_fallback()))
        self.assertTrue(is_model_unavailable(
            {"urgency": "low", "_model_blocked": True}))
        # The model RAN here — unparseable output is NOT model-unavailable
        # (its conservative escalation stays; see the fail-closed class).
        self.assertFalse(is_model_unavailable(
            {"urgency": "low", "_raw_text": True}))
        self.assertFalse(is_model_unavailable(dict(BENIGN_OUTPUT)))
        self.assertFalse(is_model_unavailable(None))
        # "unavailable" is an EXTERNAL value only: it is not a rubric
        # level, and a model emitting it as its urgency pick is
        # out-of-rubric (invalid-answer -> conservative), so the value
        # can never round-trip back in as a judgment.
        self.assertEqual(MODEL_UNAVAILABLE_URGENCY, "unavailable")
        self.assertNotIn(MODEL_UNAVAILABLE_URGENCY, URGENCY_RUBRIC)
        self.assertIsNone(
            build_urgency_candidate({"urgency": "unavailable"}))


class BelowThresholdDirectionTests(unittest.TestCase):
    """The D2 split in BOTH directions at the gate + mapping level.

    The same below-threshold outcome is externalized two ways: with the
    model-unavailable marker it is the honest "unavailable"; with a
    GENUINE answer under the bar it keeps the conservative "high". The
    urgency_disagreement safety rule dominates the carve-out."""

    def _genuine_below_threshold_outcome(self):
        """A real structured pick whose confidence is under the bar —
        the model genuinely answered low, just weakly."""
        from healthadvocate.decisions.symptom_triage import (
            SYMPTOM_TRIAGE_THRESHOLDS, TRIAGE_SURFACE, URGENCY_QUESTION,
        )
        return assess(
            URGENCY_QUESTION, receipt=_receipt(),
            candidate=_candidate("low", confidence=0.3),
            surface=TRIAGE_SURFACE, runner="code",
            thresholds=SYMPTOM_TRIAGE_THRESHOLDS,
        )

    def test_genuine_below_threshold_answer_still_escalates_high(self):
        # Direction (b): the pre-D2 safety rule is untouched — an
        # answered-but-low-confidence pick surfaces conservative HIGH.
        from healthadvocate.decisions.symptom_triage import external_urgency
        outcome = self._genuine_below_threshold_outcome()
        self.assertEqual(outcome.reason_kind, "below-threshold")
        self.assertEqual(external_urgency(outcome, False), "high")
        self.assertEqual(
            external_urgency(outcome, False, model_unavailable=False),
            "high")

    def test_model_unavailable_marker_on_same_outcome_maps_unavailable(self):
        # Direction (a): the SAME below-threshold outcome, produced by a
        # model-unavailable placeholder, is the honest "unavailable".
        from healthadvocate.decisions.symptom_triage import external_urgency
        outcome = self._genuine_below_threshold_outcome()
        self.assertEqual(
            external_urgency(outcome, False, model_unavailable=True),
            "unavailable")

    def test_disagreement_dominates_the_unavailable_carve_out(self):
        # Safety first: an urgency_disagreement escalates to high even
        # when the model was unavailable (defensive — the real fallback
        # never says "low", so the two cannot co-occur end to end).
        from healthadvocate.decisions.symptom_triage import external_urgency
        outcome = self._genuine_below_threshold_outcome()
        self.assertEqual(
            external_urgency(outcome, True, model_unavailable=True),
            "high")

    def test_carve_out_is_scoped_to_below_threshold_only(self):
        # A model-unavailable marker cannot rename an ANSWERED decision
        # (unreachable via assess_urgency; defended here anyway): only
        # the below-threshold leg externalizes as "unavailable".
        from healthadvocate.decisions.symptom_triage import external_urgency
        answered = DecisionOutcome(
            outcome=Outcome.ANSWERED, reason_kind="answered",
            question_id="symptom-triage-urgency", question_class="score",
            runner="code", reason="synthetic", allowed_next_steps=[],
            answer=_candidate("low"), threshold_applied=0.5,
        )
        self.assertEqual(
            external_urgency(answered, False, model_unavailable=True),
            "low")


class CanaryTripwireTests(unittest.TestCase):
    def test_canary_never_leaks_into_receipt_or_wrapper(self):
        engine = make_engine([
            {"text": CANARY, "label": "PatientName", "confidence": 0.91,
             "category": "pii"},
            {"text": CANARY_MEMBER, "label": "MemberID", "confidence": 0.99,
             "category": "pii"},
        ])
        output = dict(BENIGN_OUTPUT, urgency="low",
                      summary=f"patient {CANARY} reports pain")
        result = run_assessment(
            engine, output,
            symptoms=f"{CANARY} reports chest discomfort",
        )
        for text in RAW_ENTITY_TEXTS:
            self.assertNotIn(text, receipt_json(result))
            self.assertNotIn(text, decision_json(result))
        # The receipt is the identify stage's, never fabricated.
        self.assertEqual(result["urgency_receipt"]["model_used"],
                         "disease_detection_superclinical")
        labels = [e["label"] for e in result["urgency_receipt"]["entity_classes"]]
        self.assertEqual(labels, ["MemberID", "PatientName"])


class IdempotenceTests(unittest.TestCase):
    def test_same_inputs_same_decision(self):
        engine_a = make_engine([{"text": "chest pain", "confidence": 0.85}])
        engine_b = make_engine([{"text": "chest pain", "confidence": 0.85}])
        output = dict(BENIGN_OUTPUT, urgency="low")
        first = run_assessment(engine_a, output)
        second = run_assessment(engine_b, output)
        self.assertEqual(first["urgency"], second["urgency"])
        self.assertEqual(decision_json(first), decision_json(second))
        self.assertEqual(receipt_json(first), receipt_json(second))


class ApiStabilityTests(unittest.TestCase):
    ORIGINAL_KEYS = {
        "conditions", "urgency", "explanation", "action_items", "red_flags",
        "possible_conditions", "recommended_specialist", "structured_output",
        "validation", "model_used", "processing_time",
        "deidentification_status", "pii_scrubbed",
    }

    def test_public_signature_unchanged(self):
        sig = inspect.signature(symptom_assessor.assess_symptoms)
        params = list(sig.parameters)
        self.assertEqual(params, ["engine", "symptoms", "profile_id"])
        self.assertIs(sig.parameters["profile_id"].default, None)

    def test_empty_input_early_return_unchanged(self):
        for empty in ("", "   "):
            with self.subTest(empty=empty):
                result = symptom_assessor.assess_symptoms(make_engine(), empty)
                self.assertEqual(result["urgency"], "low")
                self.assertEqual(result["explanation"], "No symptoms provided.")
                # No typed fields minted for a non-assessment.
                self.assertNotIn("urgency_decision", result)
                self.assertNotIn("urgency_receipt", result)

    def test_original_keys_all_present(self):
        result = run_assessment(make_engine(), dict(BENIGN_OUTPUT))
        self.assertTrue(self.ORIGINAL_KEYS <= set(result))
        # Additive typing only.
        self.assertEqual(
            set(result) - self.ORIGINAL_KEYS,
            {"urgency_decision", "urgency_receipt"},
        )


class IdentifyBeforeAssessOrderTests(unittest.TestCase):
    def test_identify_runs_before_gated_reasoning(self):
        calls = []
        engine = mock.Mock(spec=["extract_diseases"])
        engine.extract_diseases.side_effect = (
            lambda text: (calls.append("identify"),
                          AnalysisResult(entities=[], model_used="m",
                                         processing_time=0.0))[1]
        )
        with mock.patch.object(
            symptom_assessor, "structured_model_call",
            side_effect=lambda *a, **k: (calls.append("reason"),
                                         dict(BENIGN_OUTPUT))[1],
        ):
            symptom_assessor.assess_symptoms(engine, "mild cough")
        # The receipt is built from the identify stage's own result and
        # the gated call still runs exactly once, after identify —
        # deidentify-before-reasoning order untouched (PrivacyBoundary
        # first; the typed layer consumes, never replaces, it).
        self.assertEqual(calls, ["identify", "reason"])
        self.assertEqual(engine.extract_diseases.call_count, 1)


if __name__ == "__main__":
    unittest.main()
