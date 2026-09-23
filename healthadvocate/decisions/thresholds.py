"""Threshold data (design 2026-09-22 §4, calibration honesty rule).

Thresholds per question class, stored as data, with MEASURED, SURFACE-
LINKED provenance as a shipping condition: a threshold invented from
defaults is not a threshold, and a threshold measured on one surface is
not a threshold for another. `ThresholdData.surface` names the converted
surface the whole file was measured on; `assess` takes the surface it is
adjudicating for and fails closed on mismatch — cross-application is
loud, never silent. J1 ships NO production threshold defaults;
thresholds exist only in synthetic test fixtures. Until measured data
exists for a surface, `assess` fails closed on the
threshold-data-missing-or-malformed leg and the surface answers
NEEDS_HUMAN.

This model is a pydantic-validated input to `assess`; a ValidationError
here feeds the NEEDS_HUMAN wrapper through the stripped-errors rule
(consensus amendment, round 3) — never `str(exc)`, never raw `errors()`.
Validator messages are STATIC: rejected values are never interpolated.
"""

from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from healthadvocate.decisions.schemas import Probability

QUESTION_CLASSES: tuple[str, ...] = ("choice", "score", "noul")

QuestionClass = Literal["choice", "score", "noul"]

_STRICT = ConfigDict(strict=True)


class ThresholdProvenance(BaseModel):
    """Where a threshold's confidence distribution was measured."""

    model_config = _STRICT

    source: Literal["measured"]
    surface: str = Field(min_length=1)
    measured_on: str = Field(min_length=1)
    sample_size: int = Field(ge=1)

    @field_validator("measured_on")
    @classmethod
    def _measured_on_is_iso_date(cls, value: str) -> str:
        try:
            date.fromisoformat(value)
        except ValueError:
            raise ValueError(
                "measured_on must be an ISO date (YYYY-MM-DD)"
            ) from None
        return value


class ClassThreshold(BaseModel):
    """Minimum acceptable calibrated confidence for one question class."""

    model_config = _STRICT

    question_class: QuestionClass
    min_confidence: Probability
    provenance: ThresholdProvenance  # required — no default thresholds ever


class ThresholdData(BaseModel):
    """The threshold file shape: one measured entry per question class,
    all measured on the one named surface."""

    model_config = _STRICT

    surface: str = Field(min_length=1)
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

    @model_validator(mode="after")
    def _provenance_surface_matches(self) -> "ThresholdData":
        for entry in self.thresholds.values():
            if entry.provenance.surface != self.surface:
                raise ValueError(
                    "threshold provenance surface must match the "
                    "ThresholdData surface"
                )
        return self

    def for_class(self, name: str) -> ClassThreshold | None:
        return self.thresholds.get(name)
