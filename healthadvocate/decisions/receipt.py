"""Identification receipts (design 2026-09-22 §4).

The load-bearing rule: identification owed before assessment. Every
assessment surface must carry an identification receipt produced by the
identify stage; no receipt, no assessment, the fail-closed sentence.

Leak grounds: `_extract_entities` stores raw entity text plus offsets in
EntityMatch (healthadvocate/core/engine.py:59-66), so a naive receipt
would leak exactly what the privacy boundary exists to strip. This module
therefore carries entity CLASSES with confidences — never raw text, never
offsets — and reuses the existing PrivacyBoundary status vocabulary
(DeidentificationStatus) rather than forking it.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence

from pydantic import BaseModel, ConfigDict, Field

from healthadvocate.decisions.schemas import Probability
from healthadvocate.privacy.boundary import DeidentificationStatus


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


def receipt_from_analysis(
    analysis: object,
    *,
    coverage_notes: Sequence[str] = (),
    deidentification_status: DeidentificationStatus,
) -> IdentificationReceipt:
    """Build a receipt from an engine AnalysisResult-like object.

    Reads only `label`, `category`, `confidence` and `model_used` — the
    raw `text` and offset fields of EntityMatch are never copied. The
    deidentification status must be stated by the caller (PrivacyBoundary
    semantics, reused — not forked).
    """
    aggregated: dict[tuple[str, str], list[float]] = {}
    entities: Iterable[object] = getattr(analysis, "entities", None) or ()
    for entity in entities:
        label = str(getattr(entity, "label", "") or "")
        category = str(getattr(entity, "category", "") or "")
        confidence = float(getattr(entity, "confidence", 0.0))
        if not label or not category:
            continue
        key = (label, category)
        bucket = aggregated.setdefault(key, [])
        bucket.append(confidence)

    entity_classes = [
        EntityClassSummary(
            label=label,
            category=category,
            count=len(confidences),
            max_confidence=max(confidences),
        )
        for (label, category), confidences in sorted(aggregated.items())
    ]
    return IdentificationReceipt(
        model_used=str(getattr(analysis, "model_used", "") or ""),
        entity_classes=entity_classes,
        coverage_notes=list(coverage_notes),
        deidentification_status=deidentification_status,
    )
