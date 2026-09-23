"""Identification receipts (design 2026-09-22 §4).

The load-bearing rule: identification owed before assessment. Every
assessment surface must carry an identification receipt produced by the
identify stage; no receipt, no assessment, the fail-closed sentence.

Leak grounds: `_extract_entities` stores raw entity text plus offsets in
EntityMatch (healthadvocate/core/engine.py:59-66), so a naive receipt
would leak exactly what the privacy boundary exists to strip. The
entity-derived fields therefore carry entity CLASSES with confidences —
never raw text, never offsets — structurally, at the builder.

Free-text metadata fields (model_used, coverage_notes) are caller
supplied and cannot be structurally stripped; the builder redacts them
with `redact_text` (PrivacyBoundary's own redaction, reused — not
forked; the supplied canaries plus the module's defensive defaults),
and `assess` independently screens the serialized receipt for canaries
before trusting it. Direct construction carries caller text verbatim —
surfaces must use the builder.

The builder is TOTAL (review round 3): hostile analysis shapes —
coerced confidences (str/bool/int), NaN/inf, blank labels, degenerate
model_used, wrong-typed status — yield a ReceiptBuildResult carrying
stripped, static errors, never an unhandled exception and never a
coerced value.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from healthadvocate.decisions.schemas import (
    Probability,
    StrippedValidationError,
    is_real_float,
)
from healthadvocate.privacy.boundary import DeidentificationStatus
from healthadvocate.privacy.logging_redaction import redact_text


class EntityClassSummary(BaseModel):
    """One entity class observed by the identify stage — label and counts
    only; raw entity text is deliberately absent."""

    model_config = ConfigDict(strict=True)

    label: str = Field(min_length=1)
    category: str = Field(min_length=1)
    count: int = Field(ge=1)
    max_confidence: Probability


class IdentificationReceipt(BaseModel):
    """The identify stage's output, carried into every assessment."""

    model_config = ConfigDict(strict=True)

    model_used: str = Field(min_length=1)
    entity_classes: list[EntityClassSummary] = Field(default_factory=list)
    coverage_notes: list[str] = Field(default_factory=list)
    deidentification_status: DeidentificationStatus


class ReceiptBuildResult(BaseModel):
    """Total result of `receipt_from_analysis`: a receipt, or stripped
    static errors saying why none could be built — never an exception."""

    receipt: IdentificationReceipt | None = None
    errors: list[StrippedValidationError] = Field(default_factory=list)


def _err(
    loc: tuple[str | int, ...],
    msg: str,
    error_type: str,
) -> StrippedValidationError:
    return StrippedValidationError(loc=loc, msg=msg, type=error_type, url=None)


def receipt_from_analysis(
    analysis: object,
    *,
    coverage_notes: Sequence[str] = (),
    deidentification_status: DeidentificationStatus,
    canaries: Sequence[str] = (),
) -> ReceiptBuildResult:
    """Build a receipt from an engine AnalysisResult-like object.

    Reads only `label`, `category`, `confidence` and `model_used` — the
    raw `text` and offset fields of EntityMatch are never copied.
    Confidences follow the answer path's exact-float discipline: genuine
    floats only (numpy floats accepted), str/bool/int are rejected as
    errors, not coerced. Free-text fields are canary-redacted
    (`redact_text`, supplied canaries plus defensive defaults). The
    deidentification status must be stated by the caller (PrivacyBoundary
    semantics, reused — not forked). Any hostile shape yields errors on
    the result; nothing raises.
    """
    errors: list[StrippedValidationError] = []

    model_used_raw = getattr(analysis, "model_used", "")
    if not isinstance(model_used_raw, str) or not model_used_raw.strip():
        errors.append(
            _err(
                ("model_used",),
                "Analysis model_used must be a non-empty string",
                "model_used_invalid",
            )
        )
        model_used_raw = ""
    model_used = redact_text(model_used_raw, canaries) if model_used_raw else ""

    notes: list[str] = []
    for index, note in enumerate(coverage_notes):
        if not isinstance(note, str):
            errors.append(
                _err(
                    ("coverage_notes", index),
                    "Coverage notes must be strings",
                    "coverage_note_invalid",
                )
            )
            continue
        notes.append(redact_text(note, canaries) if note else note)

    if not isinstance(deidentification_status, DeidentificationStatus):
        errors.append(
            _err(
                ("deidentification_status",),
                "deidentification_status must be a DeidentificationStatus member",
                "deidentification_status_invalid",
            )
        )

    aggregated: dict[tuple[str, str], list[float]] = {}
    entities: Sequence[Any] = getattr(analysis, "entities", None) or ()
    for index, entity in enumerate(entities):
        label = getattr(entity, "label", None)
        category = getattr(entity, "category", None)
        confidence = getattr(entity, "confidence", None)
        if not isinstance(label, str) or not label.strip():
            errors.append(
                _err(
                    ("entity_classes", index, "label"),
                    "Entity label must be a non-empty string",
                    "entity_label_invalid",
                )
            )
            continue
        if not isinstance(category, str) or not category.strip():
            errors.append(
                _err(
                    ("entity_classes", index, "category"),
                    "Entity category must be a non-empty string",
                    "entity_category_invalid",
                )
            )
            continue
        if not is_real_float(confidence) or not 0.0 <= confidence <= 1.0:
            errors.append(
                _err(
                    ("entity_classes", index, "max_confidence"),
                    "Entity confidence must be a genuine float in [0, 1]; "
                    "coerced values are not accepted",
                    "entity_confidence_invalid",
                )
            )
            continue
        aggregated.setdefault((label, category), []).append(float(confidence))

    if errors:
        return ReceiptBuildResult(receipt=None, errors=errors)

    receipt = IdentificationReceipt(
        model_used=model_used,
        entity_classes=[
            EntityClassSummary(
                label=label,
                category=category,
                count=len(confidences),
                max_confidence=max(confidences),
            )
            for (label, category), confidences in sorted(aggregated.items())
        ],
        coverage_notes=notes,
        deidentification_status=deidentification_status,
    )
    return ReceiptBuildResult(receipt=receipt)
