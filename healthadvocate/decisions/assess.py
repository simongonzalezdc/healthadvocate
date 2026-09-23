"""The assess gate (design 2026-09-22 §4): identification before
assessment, calibrated honesty, fail-closed on every leg.

Flow: runner policy → receipt → thresholds → candidate → threshold
comparison. Four fail-closed legs return a NEEDS_HUMAN WRAPPER carrying
the numbers (amendment b) — never a sentinel inside an answer's
value/level:

  below-threshold                confidence under the measured threshold
  threshold-data-missing         no measured data for the question class
  threshold-data-malformed       threshold payload failed pydantic validation
  unknown-runner                 runner name not in the registry
  invalid-receipt                receipt failed pydantic validation
  invalid-answer                 candidate failed model or pair validation

Every wrapper field derived from ANY pydantic ValidationError — invalid
receipt, threshold data, provenance, candidate — carries stripped error
types/locs only (consensus amendment, round 3): `str(exc)` and raw
`errors()` embed the rejected value on pydantic 2.13.5 and are never
used. No parallel gate vocabulary (amendment f): the wrapper maps to the
existing GateState (ANSWERED→ALLOWED, NEEDS_HUMAN→REVIEW_REQUIRED) and
reuses the Commitment Gate's fail-closed sentence verbatim.
"""

from __future__ import annotations

from collections.abc import Mapping
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field, ValidationError, computed_field

from healthadvocate.coverage.commitment_gate import GateState
from healthadvocate.decisions.receipt import IdentificationReceipt
from healthadvocate.decisions.runners import (
    DEFAULT_RUNNER,
    get_runner,
    hosted_jev_call,
)
from healthadvocate.decisions.schemas import (
    Answer,
    ChoiceAnswer,
    ChoiceQuestion,
    NoulAnswer,
    NoulQuestion,
    Question,
    ScoreAnswer,
    ScoreQuestion,
    ScoreSource,
    StrippedValidationError,
    answer_question_pair_errors,
    question_class,
    stripped_validation_errors,
)
from healthadvocate.decisions.thresholds import ThresholdData

# The Commitment Gate's BLOCKED sentence (commitment_gate.py:188-191),
# reused verbatim — no receipt means the same refusal, generalized to
# every decision point. tests/test_ha_jev_decisions.py pins the two
# strings cannot diverge.
FAIL_CLOSED_SENTENCE = (
    "HealthAdvocate will not perform this action. It requires a "
    "human decision outside this application."
)

ReasonKind = Literal[
    "answered",
    "below-threshold",
    "threshold-data-missing",
    "threshold-data-malformed",
    "unknown-runner",
    "invalid-receipt",
    "invalid-answer",
]

LOCAL_ML_RUNNER = "local-ml"

# Deterministic allowed_next_steps per leg (amendment g) — static lists,
# never computed from inputs (commitment_gate.py:192-196 pattern).
_NEXT_STEPS: dict[str, tuple[str, ...]] = {
    "answered": ("Consume the typed answer",),
    "below-threshold": (
        "Review the attached calibrated numbers",
        "Make the decision as a human",
        "Record the human decision against this question id",
    ),
    "threshold-data-missing": (
        "Derive thresholds from measured confidence distributions for this surface",
        "Decide as a human until measured data exists",
    ),
    "threshold-data-malformed": (
        "Fix the threshold data using the stripped validation errors",
        "Decide as a human until valid measured data exists",
    ),
    "unknown-runner": (
        "Use a registered local runner: code or local-ml",
        "Decide as a human",
    ),
    "invalid-receipt": (
        "Run the identify stage and pass its identification receipt",
        "Decide as a human outside this application",
    ),
    "invalid-answer": (
        "Fix the candidate answer using the stripped validation errors",
        "Decide as a human",
    ),
}

# Static reasons per leg — the numbers live in fields (answer,
# threshold_applied), never in prose, so no leg can echo an input.
_REASONS: dict[str, str] = {
    "answered": (
        "Calibrated confidence met the measured threshold for this "
        "question class."
    ),
    "below-threshold": (
        "Calibrated confidence is below the measured threshold for this "
        "question class; the numbers are attached for a human decision."
    ),
    "threshold-data-missing": (
        "No measured threshold data exists for this question class; "
        "HealthAdvocate will not guess one."
    ),
    "threshold-data-malformed": (
        "Threshold data is malformed (see the stripped validation "
        "errors); HealthAdvocate will not guess a threshold."
    ),
    "unknown-runner": (
        "The named runner is not registered; no assessment ran."
    ),
    "invalid-receipt": FAIL_CLOSED_SENTENCE,
    "invalid-answer": (
        "The candidate answer failed validation; see the stripped "
        "validation errors."
    ),
}


class Outcome(str, Enum):
    """The wrapper outcome. NEEDS_HUMAN is a wrapper state only — answers
    themselves never carry a sentinel value."""

    ANSWERED = "ANSWERED"
    NEEDS_HUMAN = "NEEDS_HUMAN"


class DecisionOutcome(BaseModel):
    """The WRAPPER (amendment b): the only shape `assess` returns. Carries
    the numbers (audit trail, not silence), the deterministic next steps
    (g), stripped validation errors only, and a mapping onto the EXISTING
    GateState vocabulary (f) so downstream gate logic consumes
    commitment_gate types rather than a parallel enum.
    """

    outcome: Outcome
    reason_kind: ReasonKind
    question_id: str
    question_class: str
    runner: str
    answer: Answer | None = None
    threshold_applied: float | None = None
    reason: str
    allowed_next_steps: list[str]
    validation_errors: list[StrippedValidationError] = Field(default_factory=list)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def gate_state(self) -> GateState:
        """Existing Commitment Gate vocabulary (amendment f): an answered
        decision is consumable (ALLOWED); NEEDS_HUMAN is review (REVIEW_REQUIRED)."""
        if self.outcome is Outcome.ANSWERED:
            return GateState.ALLOWED
        return GateState.REVIEW_REQUIRED


_ANSWER_TYPES: dict[type[BaseModel], type[BaseModel]] = {
    ChoiceQuestion: ChoiceAnswer,
    ScoreQuestion: ScoreAnswer,
    NoulQuestion: NoulAnswer,
}


def _static(
    kind: ReasonKind,
    question: Question,
    runner: str,
    answer: Answer | None,
    threshold_applied: float | None,
    errors: list[StrippedValidationError] | None = None,
) -> DecisionOutcome:
    return DecisionOutcome(
        outcome=(
            Outcome.ANSWERED if kind == "answered" else Outcome.NEEDS_HUMAN
        ),
        reason_kind=kind,
        question_id=question.id,
        question_class=question_class(question),
        runner=runner,
        answer=answer,
        threshold_applied=threshold_applied,
        reason=_REASONS[kind],
        allowed_next_steps=list(_NEXT_STEPS[kind]),
        validation_errors=errors or [],
    )


def _validated_answer(
    question: Question,
    candidate: object,
    runner: str,
) -> tuple[Answer | None, list[StrippedValidationError]]:
    """Validate the candidate against the question's answer schema and
    pair rules. Returns (answer, errors): an invalid candidate is never
    attached — only its stripped errors are."""
    errors: list[StrippedValidationError] = []
    expected = _ANSWER_TYPES[type(question)]
    if candidate is None:
        errors.append(
            StrippedValidationError(
                loc=("answer",),
                msg="A candidate answer is required",
                type="candidate_required",
            )
        )
        return None, errors
    try:
        answer = expected.model_validate(candidate)
    except ValidationError as exc:
        return None, stripped_validation_errors(exc)
    errors.extend(answer_question_pair_errors(question, answer))
    if runner == LOCAL_ML_RUNNER and answer.score_source is None:
        errors.append(
            StrippedValidationError(
                loc=("score_source",),
                msg="local-ml answers must carry score_source (raw or calibrated)",
                type="score_source_required_for_local_ml",
            )
        )
    if errors:
        return None, errors
    return answer, []


def assess(
    question: Question,
    *,
    receipt: IdentificationReceipt,
    candidate: Answer | None,
    runner: str = DEFAULT_RUNNER,
    thresholds: ThresholdData | Mapping[str, object] | None = None,
) -> DecisionOutcome:
    """Adjudicate a runner-produced answer behind the receipt contract.

    `receipt` is a REQUIRED argument (amendment a): every assess entry
    point carries it, and an invalid receipt fails closed with the gate
    sentence plus stripped errors only. A surface without measured
    threshold data gets NEEDS_HUMAN — never a default threshold.
    """
    # 1. Runner policy. Hosted-jev is a CEO-gated external act: it raises
    #    (PrivacyBoundary posture), it does not wrap. An unregistered name
    #    is a configuration mistake: fail closed into the wrapper.
    spec = get_runner(runner)
    if spec is not None and spec.hosted:
        hosted_jev_call(question=question, receipt=receipt)
    if spec is None:
        return _static("unknown-runner", question, runner, None, None)

    # 2. Receipt (the load-bearing rule): no valid receipt, no assessment.
    try:
        IdentificationReceipt.model_validate(receipt)
    except ValidationError as exc:
        return _static(
            "invalid-receipt",
            question,
            runner,
            None,
            None,
            stripped_validation_errors(exc),
        )

    # 3. Threshold data: missing or malformed fails closed (never a
    #    default); a validating candidate still rides along as numbers.
    if thresholds is None:
        answer, errors = _validated_answer(question, candidate, runner)
        return _static(
            "threshold-data-missing", question, runner, answer, None, errors
        )
    try:
        data = ThresholdData.model_validate(thresholds)
    except ValidationError as exc:
        answer, errors = _validated_answer(question, candidate, runner)
        return _static(
            "threshold-data-malformed",
            question,
            runner,
            answer,
            None,
            stripped_validation_errors(exc) + errors,
        )
    threshold = data.for_class(question_class(question))
    if threshold is None:
        answer, errors = _validated_answer(question, candidate, runner)
        return _static(
            "threshold-data-missing", question, runner, answer, None, errors
        )

    # 4. Candidate: invalid answers fail closed with stripped errors.
    answer, errors = _validated_answer(question, candidate, runner)
    if errors:
        return _static("invalid-answer", question, runner, None, None, errors)

    # 5. Calibration honesty: below threshold is not a best guess — it is
    #    NEEDS_HUMAN with the calibrated numbers attached.
    if answer.confidence >= threshold.min_confidence:
        return _static(
            "answered", question, runner, answer, threshold.min_confidence
        )
    return _static(
        "below-threshold", question, runner, answer, threshold.min_confidence
    )
