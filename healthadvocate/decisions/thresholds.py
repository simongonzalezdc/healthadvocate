"""Threshold data (design 2026-09-22 §4, calibration honesty rule).

Thresholds per question class, stored as data, with MEASURED, SURFACE-
LINKED provenance as a shipping condition: a threshold invented from
defaults is not a threshold, and a threshold measured on one surface is
not a threshold for another. `ThresholdData.surface` names the converted
surface the whole file was measured on; `assess` takes the surface it is
adjudicating for and fails closed on mismatch — cross-application is
loud, never silent.

J1 shipped no production threshold defaults (synthetic test fixtures
only). J2-c (2026-09-22) adds the first production threshold data —
symptom-triage, score class — on the additive, honestly-labeled POLICY
provenance tier (see ThresholdProvenance): it exists because a surface
converting before measured data exists must not choose between fabricat-
ing a measurement and breaking its preserved behaviors; it says what it
is and cannot borrow measured-tier fields. Measured data replaces it
when it exists. Every other J1 rule is unchanged: no defaults without
provenance, surface linkage enforced, malformed data fails closed.

This model is a pydantic-validated input to `assess`; a ValidationError
here feeds the NEEDS_HUMAN wrapper through the stripped-errors rule
(consensus amendment, round 3) — never `str(exc)`, never raw errors()`.
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
    """Where a threshold's confidence distribution was measured.

    Two honestly-separated tiers (J2-c amendment, 2026-09-22):

    - ``measured`` — unchanged J1 semantics: derived from a measured
      confidence distribution on the named surface, with sample size
      and date. Still the only tier that claims calibration.
    - ``policy`` — an additive, explicitly-labeled bridge tier for a
      surface that converts BEFORE measured data exists (first
      consumer: symptom-triage). It carries an adoption date and a
      rationale instead of a sample, and is FORBIDDEN from carrying
      ``sample_size``/``measured_on`` — a policy threshold can never
      masquerade as a measured one.

    Why the policy tier does not weaken the calibration-honesty rule
    (design §4): on a converting surface the pre-conversion baseline is
    an UNGATED decision (every pick trusted). A threshold there can
    only REMOVE trust (push candidates to NEEDS_HUMAN, which surfaces
    conservatively per the surface's fail-closed mapping) — never grant
    trust a measured threshold would deny. The rule's failure mode,
    unearned trust from an invented number, is unreachable. Measured
    data replaces the policy tier when it exists (same surface, same
    class), and nothing else about the assess() flow changes.
    """

    model_config = _STRICT

    source: Literal["measured", "policy"]
    surface: str = Field(min_length=1)
    # measured tier (required together when source == "measured"):
    measured_on: str | None = None
    sample_size: int | None = Field(default=None, ge=1)
    # policy tier (required together when source == "policy"):
    adopted_on: str | None = None
    rationale: str | None = None

    @field_validator("measured_on", "adopted_on")
    @classmethod
    def _iso_date_when_present(cls, value: str | None) -> str | None:
        if value is None:
            return value
        try:
            date.fromisoformat(value)
        except ValueError:
            raise ValueError(
                "measured_on/adopted_on must be an ISO date (YYYY-MM-DD)"
            ) from None
        return value

    @model_validator(mode="after")
    def _per_source_fields(self) -> "ThresholdProvenance":
        # Static messages; a rejected value is never interpolated.
        if self.source == "measured":
            if self.measured_on is None:
                raise ValueError(
                    "measured provenance requires measured_on (ISO date)"
                )
            if self.sample_size is None:
                raise ValueError(
                    "measured provenance requires sample_size (>= 1)"
                )
            if self.adopted_on is not None or self.rationale is not None:
                raise ValueError(
                    "measured provenance must not carry policy-tier fields"
                )
        else:  # policy
            if self.adopted_on is None:
                raise ValueError(
                    "policy provenance requires adopted_on (ISO date)"
                )
            if not (self.rationale and self.rationale.strip()):
                raise ValueError(
                    "policy provenance requires a non-blank rationale"
                )
            if self.sample_size is not None or self.measured_on is not None:
                raise ValueError(
                    "policy provenance must not claim measurement fields; "
                    "a policy threshold is not a measured one"
                )
        return self


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
