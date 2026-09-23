"""HA-JEV question/answer schemas (design 2026-09-22 §4).

Typed, calibrated decision primitives — no prose. Cross-field validation
(amendment c) lives at the schema layer for what a model can know about
itself, and in `answer_question_pair_errors` for (question, answer) pairs.

Strict typing (ADV-001): every input model runs pydantic strict mode, and
every probability/confidence field is an exact-float `Probability` —
pydantic 2.13.5 lax mode coerces str/bytes/bool/int into floats and bytes
into option strings, which drove ANSWERED outcomes on untyped input;
strict mode alone still accepts int (verified live), so the exact-float
before-validator is load-bearing, not redundant.

Leak discipline (consensus amendment, round 3): every error object this
package emits is a `StrippedValidationError` built from
`errors(include_input=False, include_context=False)`. On pydantic 2.13.5
the raw form carries the rejected value under `input` and `str(exc)`
embeds it, while the stripped form yields loc/msg/type/url only (verified
live in this tree, 2026-09-22). Custom validator messages are therefore
STATIC — a rejected value is never interpolated into a message, or it
would sail straight through the stripped form.
"""

from __future__ import annotations

from enum import Enum
from typing import Annotated

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
)

_SUM_TOLERANCE = 1e-6

_STRICT = ConfigDict(strict=True)


def _require_exact_float(value: object) -> object:
    """ADV-001: the calibrated gate consumes floats only — never a value
    coerced from str/bytes/bool/int (bool True and int 1 both become 1.0
    and would pass every threshold). Static message; input never echoed."""
    if type(value) is not float:
        raise ValueError(
            "probability and confidence values must be provided as exact "
            "floats; coerced values are not accepted"
        )
    return value


#: A calibrated probability or confidence in [0, 1] — exact float only.
Probability = Annotated[
    float, BeforeValidator(_require_exact_float), Field(ge=0.0, le=1.0)
]


class ScoreSource(str, Enum):
    """Honesty field (amendment d): what backs a local-ml answer's numbers."""

    RAW = "raw"
    CALIBRATED = "calibrated"


class StrippedValidationError(BaseModel):
    """A pydantic ValidationError reduced to loc/msg/type/url.

    Never carries the rejected input (no `input`, no `ctx`), never
    `str(exc)`. This is the only error shape allowed inside a wrapper.
    """

    model_config = ConfigDict(frozen=True)

    loc: tuple[str | int, ...]
    msg: str
    type: str
    url: str | None = None


def stripped_validation_errors(
    exc: ValidationError,
) -> list[StrippedValidationError]:
    """Strip a pydantic ValidationError for wrapper consumption.

    The reflex path — `str(exc)` or raw `errors()` — embeds the rejected
    value (canary/PHI leak vector); this helper is the only sanctioned
    conversion (design §4 amendment b, generalized round 3).
    """
    return [
        StrippedValidationError(
            loc=tuple(error["loc"]),
            msg=error["msg"],
            type=error["type"],
            url=error.get("url"),
        )
        for error in exc.errors(include_input=False, include_context=False)
    ]


def _stripped(
    loc: tuple[str | int, ...],
    msg: str,
    error_type: str,
) -> StrippedValidationError:
    """Static-message pair-level error (no input ever embedded)."""
    return StrippedValidationError(
        loc=loc, msg=msg, type=error_type, url=None
    )


# ---------------------------------------------------------------------------
# Questions
# ---------------------------------------------------------------------------


class ScoreLevel(BaseModel):
    """One ordered rubric level; `ScoreAnswer.level` indexes the rubric."""

    model_config = ConfigDict(strict=True, frozen=True)

    label: str = Field(min_length=1)


class ChoiceQuestion(BaseModel):
    """Jev Choice primitive: pick from at most 255 options."""

    model_config = _STRICT

    id: str = Field(min_length=1)
    options: list[str] = Field(min_length=1, max_length=255)
    context_ref: str = Field(min_length=1)

    @field_validator("options")
    @classmethod
    def _options_unique_and_non_blank(
        cls, value: list[str]
    ) -> list[str]:
        if len(set(value)) != len(value):
            raise ValueError("options must be unique")
        if any(not option.strip() for option in value):
            raise ValueError("options must not contain blank strings")
        return value


class ScoreQuestion(BaseModel):
    """Jev Score primitive: an ordered rubric with per-level probabilities."""

    model_config = _STRICT

    id: str = Field(min_length=1)
    rubric: list[ScoreLevel] = Field(min_length=1)

    @field_validator("rubric")
    @classmethod
    def _rubric_labels_unique(cls, value: list[ScoreLevel]) -> list[ScoreLevel]:
        labels = [level.label for level in value]
        if len(set(labels)) != len(labels):
            raise ValueError("rubric labels must be unique")
        return value


class NoulQuestion(BaseModel):
    """Jev Noul primitive: a yes/no claim with a calibrated probability."""

    model_config = _STRICT

    id: str = Field(min_length=1)
    claim: str = Field(min_length=1)


Question = ChoiceQuestion | ScoreQuestion | NoulQuestion

_QUESTION_CLASSES: tuple[tuple[type[BaseModel], str], ...] = (
    (ChoiceQuestion, "choice"),
    (ScoreQuestion, "score"),
    (NoulQuestion, "noul"),
)


def question_class(question: Question) -> str:
    """The question-class key thresholds are stored under."""
    for model, name in _QUESTION_CLASSES:
        if isinstance(question, model):
            return name
    raise ValueError("not a known HA-JEV question type")


# ---------------------------------------------------------------------------
# Answers
# ---------------------------------------------------------------------------


class ChoiceAnswer(BaseModel):
    model_config = _STRICT

    question_id: str = Field(min_length=1)
    value: str = Field(min_length=1)
    probability: Probability
    confidence: Probability
    score_source: ScoreSource | None = None


class ScoreAnswer(BaseModel):
    model_config = _STRICT

    question_id: str = Field(min_length=1)
    level: int = Field(ge=0)
    per_level_probabilities: list[Probability] = Field(min_length=1)
    confidence: Probability
    score_source: ScoreSource | None = None


class NoulAnswer(BaseModel):
    model_config = _STRICT

    question_id: str = Field(min_length=1)
    probability_true: Probability
    confidence: Probability
    score_source: ScoreSource | None = None


Answer = ChoiceAnswer | ScoreAnswer | NoulAnswer


def answer_question_pair_errors(
    question: Question,
    answer: Answer,
) -> list[StrippedValidationError]:
    """Pair-level cross validation (amendment c): the answer must reference
    its question and agree with the question's shape. Static messages only.
    """
    errors: list[StrippedValidationError] = []
    if answer.question_id != question.id:
        errors.append(
            _stripped(
                ("question_id",),
                "Answer question_id does not match the question id",
                "question_id_mismatch",
            )
        )
    if isinstance(question, ChoiceQuestion) and isinstance(answer, ChoiceAnswer):
        if answer.value not in question.options:
            errors.append(
                _stripped(
                    ("value",),
                    "Choice value is not one of the question options",
                    "value_not_in_options",
                )
            )
    if isinstance(question, ScoreQuestion) and isinstance(answer, ScoreAnswer):
        if not 0 <= answer.level < len(question.rubric):
            errors.append(
                _stripped(
                    ("level",),
                    "Score level does not index the question rubric",
                    "level_not_in_rubric",
                )
            )
        if len(answer.per_level_probabilities) != len(question.rubric):
            errors.append(
                _stripped(
                    ("per_level_probabilities",),
                    "per_level_probabilities length must equal the rubric length",
                    "per_level_length_mismatch",
                )
            )
        elif abs(sum(answer.per_level_probabilities) - 1.0) > _SUM_TOLERANCE:
            errors.append(
                _stripped(
                    ("per_level_probabilities",),
                    "per_level_probabilities must sum to 1",
                    "per_level_sum_not_one",
                )
            )
    return errors
