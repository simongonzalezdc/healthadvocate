"""HA-JEV J2-a: Commitment Gate intent classification routed through the
typed-decision layer (docs/HA-JEV-TYPED-DECISIONS-DESIGN-2026-09-22.md
§5 J2; surface "commitment-gate").

The conversion is an adjudication ceiling with audit numbers — never a
permission source. The gate's external contract (states, reasons, steps,
endpoint payload) is unchanged; prohibited intents stay prohibited
regardless of the typed outcome.

- Question: a ChoiceQuestion whose options are the Intent enum values in
  use; the deterministic classifier's pick (commitment_gate
  .normalize_intent) becomes the ChoiceAnswer candidate.
- Confidence honesty: the classifier is a table lookup with no measured
  confidence, so the candidate carries documented conservative constants —
  probability/confidence 1.0 for an exact alias/enum match (correct by
  construction of the alias table, not by calibration) and 0.0 for the
  UNKNOWN fallback (the classifier's own admission that it matched
  nothing — the "knows when it doesn't know" posture). score_source stays
  None: the honesty field describes local-ml answers, and this surface
  runs the `code` runner.
- Receipts: built ONLY from a caller-supplied identify stage (a
  HealthEngine analysis plus its stated deidentification status) via
  receipt_from_analysis. No analysis → no receipt → the typed layer does
  not engage and the gate decides exactly as before; a receipt is never
  fabricated. A failed build (hostile analysis, unstated status) fails
  closed carrying the builder's stripped errors — no assessment runs.

NO PRODUCTION THRESHOLDS SHIP FOR THIS SURFACE (deliberate, J2-a stop):
ClassThreshold requires provenance.source == "measured" (a Literal — a
"policy default" ThresholdData is unconstructible without dishonest
provenance), and the design's calibration honesty rule says a threshold
invented from defaults is not a threshold; a surface without measured
data answers NEEDS_HUMAN. The production call therefore passes
thresholds=None → threshold-data-missing → NEEDS_HUMAN → the gate's
review-only downgrade for allowed intents, until measured confidence
distributions exist for surface "commitment-gate". Synthetic measured
fixtures in tests (the J1 pattern) exercise the ANSWERED and
below-threshold legs; they are the only thresholds this surface knows.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from healthadvocate.coverage.commitment_gate import (
    Intent,
    exact_intent_match,
    normalize_intent,
)
from healthadvocate.decisions import (
    ChoiceAnswer,
    ChoiceQuestion,
    DecisionOutcome,
    StrippedValidationError,
    assess,
    receipt_from_analysis,
)
from healthadvocate.decisions.thresholds import ThresholdData

#: The converted surface's name — threshold data measured on any other
#: surface never applies here (assess fails closed on mismatch).
COMMITMENT_GATE_SURFACE = "commitment-gate"

#: Stable question id for audit correlation across calls.
INTENT_QUESTION_ID = "commitment-gate-intent"

#: Conservative confidence constants (see module docstring): an exact
#: alias/enum match is correct by construction; the UNKNOWN fallback is
#: the classifier admitting it matched nothing.
EXACT_MATCH_PROBABILITY = 1.0
EXACT_MATCH_CONFIDENCE = 1.0
FALLBACK_PROBABILITY = 0.0
FALLBACK_CONFIDENCE = 0.0

#: Static coverage note carried on every receipt this surface builds —
#: static by construction, so it can never echo input text.
_SURFACE_NOTE = "commitment-gate intent classification"


def intent_question() -> ChoiceQuestion:
    """The intent ChoiceQuestion: options are the Intent values in use."""
    return ChoiceQuestion(
        id=INTENT_QUESTION_ID,
        options=[intent.value for intent in Intent],
        context_ref=f"receipt:{COMMITMENT_GATE_SURFACE}",
    )


def intent_candidate(raw_intent: str | Intent) -> ChoiceAnswer:
    """The classifier's pick as a typed candidate answer.

    The value is always one of the question's options (normalize_intent
    only returns Intent members). Confidence is the documented constant —
    1.0 for exact matches, 0.0 for the UNKNOWN fallback — never a
    fabricated calibration. score_source stays None: the runner is
    `code`, not local-ml.
    """
    intent = normalize_intent(raw_intent)
    if exact_intent_match(raw_intent):
        probability, confidence = (
            EXACT_MATCH_PROBABILITY,
            EXACT_MATCH_CONFIDENCE,
        )
    else:
        probability, confidence = (
            FALLBACK_PROBABILITY,
            FALLBACK_CONFIDENCE,
        )
    return ChoiceAnswer(
        question_id=INTENT_QUESTION_ID,
        value=intent.value,
        probability=probability,
        confidence=confidence,
    )


def adjudicate_intent(
    raw_intent: str | Intent,
    *,
    analysis: object,
    deidentification_status: object,
    canaries: Sequence[str] = (),
    thresholds: ThresholdData | Mapping[str, object] | None = None,
) -> tuple[DecisionOutcome | None, list[StrippedValidationError]]:
    """Adjudicate the intent pick behind the receipt contract.

    Returns (typed outcome, identify errors): when the identify stage
    yields no valid receipt the outcome is None and the builder's
    stripped errors ride along — no receipt, no assessment, and the
    caller fails closed on the identify errors.
    """
    built = receipt_from_analysis(
        analysis,
        coverage_notes=(_SURFACE_NOTE,),
        deidentification_status=deidentification_status,  # type: ignore[arg-type]
        canaries=canaries,
    )
    if built.receipt is None:
        return None, list(built.errors)
    outcome = assess(
        intent_question(),
        receipt=built.receipt,
        candidate=intent_candidate(raw_intent),
        surface=COMMITMENT_GATE_SURFACE,
        runner="code",
        thresholds=thresholds,
        canaries=tuple(canaries),
    )
    return outcome, []
