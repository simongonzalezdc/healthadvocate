"""Threshold data (design 2026-09-22 §4, calibration honesty rule).

Thresholds per question class, stored as data, with MEASURED provenance as
a shipping condition: a threshold invented from defaults is not a
threshold. J1 ships NO production threshold defaults — thresholds exist
only in synthetic test fixtures. Until measured data exists for a surface,
`assess` fails closed on the threshold-data-missing-or-malformed leg and
the surface answers NEEDS_HUMAN.

This model is a pydantic-validated input to `assess`; a ValidationError
here feeds the NEEDS_HUMAN wrapper through the stripped-errors rule
(consensus amendment, round 3) — never `str(exc)`, never raw `errors()`.
Validator messages are STATIC: rejected values are never interpolated.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

QUESTION_CLASSES: tuple[str, ...] = ("choice", "score", "noul")

QuestionClass = Literal["choice", "score", "noul"]


class ThresholdProvenance(BaseModel):
    """Where a threshold's confidence distribution was measured."""

    source: Literal["measured"]
    surface: str = Field(min_length=1)
    measured_on: str = Field(min_length=1)
    sample_size: int = Field(ge=1)


class ClassThreshold(BaseModel):
    """Minimum acceptable calibrated confidence for one question class."""

    question_class: QuestionClass
    min_confidence: float = Field(ge=0.0, le=1.0)
    provenance: ThresholdProvenance  # required — no default thresholds ever


class ThresholdData(BaseModel):
    """The threshold file shape: one measured entry per question class."""

    thresholds: dict[str, ClassThreshold] = Field(default_factory=dict)

    @field_validator("thresholds")
    @classmethod
    def _keys_match_classes(
        cls, value: dict[str, ClassThreshold]
    ) -> dict[str, ClassThreshold]:
        for key, entry in value.items():
            if key != entry.question_class:
                raise ValueError(
                    "threshold key must equal the entry's question_class"
                )
        return value

    def for_class(self, name: str) -> ClassThreshold | None:
        return self.thresholds.get(name)
