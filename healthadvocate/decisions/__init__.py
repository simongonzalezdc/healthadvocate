"""HA-JEV: the typed, calibrated decision layer (design 2026-09-22, J1).

New package; no existing surface changes until each converts (J2).
Implements docs/HA-JEV-TYPED-DECISIONS-DESIGN-2026-09-22.md §4-5 with the
consensus amendments applied, including the round-3 generalization: every
wrapper field derived from ANY pydantic ValidationError — invalid receipt,
threshold data, provenance, candidate — carries stripped error
types/locs only, never str(exc) or raw errors().
"""

from __future__ import annotations

from healthadvocate.decisions.assess import (
    FAIL_CLOSED_SENTENCE,
    DecisionOutcome,
    Outcome,
    assess,
)
from healthadvocate.decisions.receipt import (
    EntityClassSummary,
    IdentificationReceipt,
    ReceiptBuildResult,
    receipt_from_analysis,
)
from healthadvocate.decisions.runners import (
    DEFAULT_RUNNER,
    HOSTED_JEV_GATE_MESSAGE,
    HostedJevGateError,
    RunnerSpec,
    get_runner,
    hosted_jev_call,
    runner_names,
)
from healthadvocate.decisions.schemas import (
    Answer,
    ChoiceAnswer,
    ChoiceQuestion,
    NoulAnswer,
    NoulQuestion,
    Question,
    ScoreAnswer,
    ScoreLevel,
    ScoreQuestion,
    ScoreSource,
    StrippedValidationError,
    answer_question_pair_errors,
    is_real_float,
    question_class,
    stripped_validation_errors,
)
from healthadvocate.decisions.thresholds import (
    QUESTION_CLASSES,
    ClassThreshold,
    ThresholdData,
    ThresholdProvenance,
)

__all__ = [
    "DEFAULT_RUNNER",
    "FAIL_CLOSED_SENTENCE",
    "HOSTED_JEV_GATE_MESSAGE",
    "QUESTION_CLASSES",
    "Answer",
    "ChoiceAnswer",
    "ChoiceQuestion",
    "ClassThreshold",
    "DecisionOutcome",
    "EntityClassSummary",
    "HostedJevGateError",
    "IdentificationReceipt",
    "NoulAnswer",
    "NoulQuestion",
    "Outcome",
    "Question",
    "ReceiptBuildResult",
    "RunnerSpec",
    "ScoreAnswer",
    "ScoreLevel",
    "ScoreQuestion",
    "ScoreSource",
    "StrippedValidationError",
    "ThresholdData",
    "ThresholdProvenance",
    "answer_question_pair_errors",
    "assess",
    "get_runner",
    "hosted_jev_call",
    "is_real_float",
    "question_class",
    "receipt_from_analysis",
    "runner_names",
    "stripped_validation_errors",
]
