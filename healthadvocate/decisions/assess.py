"""The assess gate (design 2026-09-22 §4): identification before
assessment, calibrated honesty, fail-closed on every leg.

Flow: runner policy → question validity → receipt (canary screen,
deidentification status) → threshold data (surface match) → candidate →
threshold comparison. Every fail-closed leg (see ReasonKind) returns a
NEEDS_HUMAN WRAPPER carrying the numbers (amendment b) — never a sentinel
inside an answer's value/level:

  answered                        confidence met the measured threshold
  below-threshold                 confidence under the measured threshold
  threshold-data-missing          no measured data for the question class
  threshold-data-malformed        threshold payload failed pydantic validation
  threshold-surface-mismatch      threshold data measured on another surface
  unknown-runner                  runner name not in the registry
  invalid-receipt                 receipt failed validation, carries a
                                  canary, or reports failed deidentification
                                  (the deidentification-failed kind)
  invalid-question                first argument is not a typed Question
                                  (ADV-004: fail closed, never an unhandled
                                  ValueError/AttributeError/KeyError)
  invalid-answer                  candidate failed model or pair validation

Hostile input on ANY parameter fails closed into a wrapper or raises the
hosted-jev CEO-gate error — never an unhandled crash.

Every wrapper field derived from ANY pydantic ValidationError — invalid
receipt, threshold data, provenance, candidate — carries stripped error
types/locs only (consensus amendment, round 3): `str(exc)` and raw
`errors()` embed the rejected value on pydantic 2.13.5 and are never
used. No parallel gate vocabulary (amendment f): the wrapper maps to the
existing GateState (ANSWERED→ALLOWED, NEEDS_HUMAN→REVIEW_REQUIRED) and
reuses the Commitment Gate's fail-closed sentence verbatim.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
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
from healthadvocate.privacy.boundary import DeidentificationStatus
from healthadvocate.privacy.logging_redaction import DEFAULT_CANARIES

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
    "threshold-surface-mismatch",
    "unknown-runner",
    "invalid-receipt",
    "deidentification-failed",
    "invalid-question",
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
    "threshold-surface-mismatch": (
        "Provide thresholds measured on this surface",
        "Decide as a human until surface-matched measured data exists",
    ),
    "unknown-runner": (
        "Use a registered local runner: code or local-ml",
        "Decide as a human",
    ),
    "invalid-receipt": (
        "Run the identify stage and pass its identification receipt",
        "Decide as a human outside this application",
    ),
    "deidentification-failed": (
        "Re-run the identify stage until deidentification succeeds",
        "Decide as a human outside this application",
    ),
    "invalid-question": (
        "Pass a typed ChoiceQuestion, ScoreQuestion, or NoulQuestion",
        "Decide as a human",
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
    "threshold-surface-mismatch": (
        "The threshold data was measured on a different surface; "
        "HealthAdvocate will not cross-apply it to this one."
    ),
    "unknown-runner": (
        "The named runner is not registered; no assessment ran."
    ),
    "invalid-receipt": FAIL_CLOSED_SENTENCE,
    "deidentification-failed": (
        "The identification receipt reports that deidentification "
        "failed; HealthAdvocate will not consume this decision input."
    ),
    "invalid-question": (
        "The question is not a typed HA-JEV question; no assessment ran."
    ),
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


# Keyed by question_class() name, NOT by exact type(): a question
# subclass is a real question and must map to its base class's answer
# type (ADV-004 round 2 — type()-keying raised KeyError for subclasses).
# The keys are exactly what question_class() can return, so the lookup
# cannot miss for any question that passed the validity gate.
_ANSWER_TYPES: dict[str, type[BaseModel]] = {
    "choice": ChoiceAnswer,
    "score": ScoreAnswer,
    "noul": NoulAnswer,
}


def invalid_receipt_outcome(
    question: Question,
    *,
    runner: str = DEFAULT_RUNNER,
    errors: list[StrippedValidationError] | None = None,
) -> DecisionOutcome:
    """The invalid-receipt wrapper for a receipt that could not be BUILT.

    J2-c: `receipt_from_analysis` is total — a hostile identify-stage
    result yields stripped errors, not an exception and not a fabricated
    receipt. The converting surface routes that failure through the
    SAME wrapper shape `assess` uses for the invalid-receipt leg (gate
    sentence, deterministic steps, stripped errors only), so no receipt
    build failure can bypass the typed layer's audit trail.
    """
    return _static("invalid-receipt", question, runner, None, None, errors)


def _runner_label(runner: object) -> str:
    """Hostile runner values (unhashable, non-str) never reach the dict
    lookup and never serialize into the wrapper; a non-str runner is not
    a registered runner and its value is not echoed."""
    return runner if isinstance(runner, str) else ""


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


def _invalid_question(runner: str) -> DecisionOutcome:
    """ADV-004: a hostile or non-Question first argument fails closed.

    `question_id`/`question_class` are unavailable by construction and
    stay empty — the hostile input is never echoed into the wrapper.
    """
    return DecisionOutcome(
        outcome=Outcome.NEEDS_HUMAN,
        reason_kind="invalid-question",
        question_id="",
        question_class="",
        runner=runner,
        answer=None,
        threshold_applied=None,
        reason=_REASONS["invalid-question"],
        allowed_next_steps=list(_NEXT_STEPS["invalid-question"]),
        validation_errors=[
            StrippedValidationError(
                loc=("question",),
                msg=(
                    "The question must be a ChoiceQuestion, ScoreQuestion, "
                    "or NoulQuestion instance"
                ),
                type="invalid_question",
            )
        ],
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
    expected = _ANSWER_TYPES[question_class(question)]
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


def _receipt_contains_canary(
    receipt: IdentificationReceipt, canaries: Sequence[str]
) -> bool:
    return any(
        canary and canary in receipt.model_dump_json() for canary in canaries
    )


def assess(
    question: Question,
    *,
    receipt: IdentificationReceipt,
    candidate: Answer | None,
    surface: str,
    runner: object = DEFAULT_RUNNER,
    thresholds: ThresholdData | Mapping[str, object] | None = None,
    canaries: Sequence[str] = (),
) -> DecisionOutcome:
    """Adjudicate a runner-produced answer behind the receipt contract.

    `receipt` is a REQUIRED argument (amendment a): every assess entry
    point carries it, and an invalid receipt fails closed with the gate
    sentence plus stripped errors only. `surface` names the converted
    surface asking the question; threshold data measured on any other
    surface fails closed (the design's shipping condition, enforced). A
    receipt that reports failed deidentification, or whose serialized
    form contains a configured canary (supplied canaries plus the
    defensive defaults), never yields ANSWERED. A surface without
    measured threshold data gets NEEDS_HUMAN — never a default
    threshold.
    """
    # 1. Runner policy. Hosted-jev is a CEO-gated external act: it raises
    #    (PrivacyBoundary posture), it does not wrap. An unregistered or
    #    hostile (non-str, unhashable) runner is a configuration
    #    mistake: fail closed into the wrapper (review round 3).
    runner_label = _runner_label(runner)
    spec = get_runner(runner) if isinstance(runner, str) else None
    if spec is not None and spec.hosted:
        hosted_jev_call(question=question, receipt=receipt)

    # 2. Question validity (ADV-004): anything that is not a typed
    #    Question fails closed into the wrapper BEFORE any leg reads
    #    question.id or derives its class — no unhandled crashes.
    #    question_class() is type-based (issubclass of type(question)),
    #    which is what stops __class__-faking proxies: isinstance can be
    #    fooled by a shadowed __class__ attribute even when the proxy
    #    carries .id, but issubclass walks the real MRO and cannot be
    #    (ADV-004 round 2 — 5ad9e2d wrongly credited the .id probe with
    #    proxy coverage). The .id probe stays as defense-in-depth against
    #    attribute-access failures on otherwise-valid instances.
    try:
        question_class(question)
        question.id
    except (AttributeError, TypeError, ValueError):
        return _invalid_question(runner_label)

    if spec is None:
        return _static("unknown-runner", question, runner_label, None, None)

    # 3. Receipt (the load-bearing rule): no valid receipt, no
    #    assessment. The serialized receipt is screened for canaries
    #    (supplied plus defensive defaults — PrivacyBoundary's
    #    canary-remained discipline), and a FAILED deidentification
    #    status never clears a decision.
    try:
        receipt_obj = IdentificationReceipt.model_validate(receipt)
    except ValidationError as exc:
        return _static(
            "invalid-receipt",
            question,
            runner_label,
            None,
            None,
            stripped_validation_errors(exc),
        )
    if _receipt_contains_canary(receipt_obj, tuple(canaries) or DEFAULT_CANARIES):
        return _static(
            "invalid-receipt",
            question,
            runner_label,
            None,
            None,
            [
                StrippedValidationError(
                    loc=("receipt",),
                    msg=(
                        "A configured canary remains in the receipt; it is "
                        "not safe to consume"
                    ),
                    type="canary_in_receipt",
                )
            ],
        )
    if receipt_obj.deidentification_status is DeidentificationStatus.FAILED:
        return _static(
            "deidentification-failed", question, runner_label, None, None
        )

    # 4. Threshold data: missing or malformed fails closed (never a
    #    default), and data measured on another surface is never
    #    cross-applied; a validating candidate still rides along as
    #    numbers.
    if thresholds is None:
        answer, errors = _validated_answer(question, candidate, runner_label)
        return _static(
            "threshold-data-missing", question, runner_label, answer, None, errors
        )
    try:
        data = ThresholdData.model_validate(thresholds)
    except ValidationError as exc:
        answer, errors = _validated_answer(question, candidate, runner_label)
        return _static(
            "threshold-data-malformed",
            question,
            runner_label,
            answer,
            None,
            stripped_validation_errors(exc) + errors,
        )
    if data.surface != surface:
        answer, errors = _validated_answer(question, candidate, runner_label)
        return _static(
            "threshold-surface-mismatch",
            question,
            runner_label,
            answer,
            None,
            errors,
        )
    threshold = data.for_class(question_class(question))
    if threshold is None:
        answer, errors = _validated_answer(question, candidate, runner_label)
        return _static(
            "threshold-data-missing", question, runner_label, answer, None, errors
        )

    # 5. Candidate: invalid answers fail closed with stripped errors.
    answer, errors = _validated_answer(question, candidate, runner_label)
    if errors:
        return _static(
            "invalid-answer", question, runner_label, None, None, errors
        )

    # 6. Calibration honesty: below threshold is not a best guess — it is
    #    NEEDS_HUMAN with the calibrated numbers attached.
    if answer.confidence >= threshold.min_confidence:
        return _static(
            "answered", question, runner_label, answer, threshold.min_confidence
        )
    return _static(
        "below-threshold", question, runner_label, answer, threshold.min_confidence
    )
