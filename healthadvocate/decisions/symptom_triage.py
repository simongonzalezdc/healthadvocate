"""J2-c: the symptom-triage surface wired onto the HA-JEV typed layer.

Design 2026-09-22 §5 J2, first Score-question conversion. The symptom
assessor's urgency pick becomes a typed decision: a ScoreQuestion with
a fixed rubric, an IdentificationReceipt from the REAL identify stage
(engine.extract_diseases), surface-linked threshold data, and the
load-bearing safety mapping — every NEEDS_HUMAN leg and every
urgency_disagreement surfaces as the conservative highest urgency,
with one honesty carve-out (audit D2, below): a model-UNAVAILABLE
placeholder externalizes as "unavailable", never a fabricated "high".

Rubric order (documented per the J2-c spec): `ScoreAnswer.level`
indexes the rubric ASCENDING in severity — 0=low, 1=medium, 2=high —
which is the J1 convention (design §4 Score: an ordered rubric; the
J1 score fixtures order low->high). Ascending order makes the
conservative fail-closed answer derivable, not hardcoded: it is the
LAST label (`URGENCY_RUBRIC[-1]`), the highest urgency.

Confidence honesty on this surface: the urgency pick comes from the
gated model's structured output through a deterministic mapping
(runner `code`), and NO measured confidence distribution exists for
it yet. The candidate's confidence is therefore a binary VALIDITY
signal, not a calibrated probability, and is documented as such:

- 1.0 — the pick is the model's real structured judgment (a clean
  parse with no placeholder markers);
- 0.0 — the output was a placeholder (model blocked or unparseable;
  `unavailable_structured_fallback` / `_raw_text` shapes), backed by
  zero measurement.

The policy threshold (0.5, policy-tier provenance in
`SYMPTOM_TRIAGE_THRESHOLDS`) separates exactly those two states.
Its only reachable effect is ESCALATION to the conservative urgency:
relative to the pre-conversion surface, which trusted every pick
unconditionally, the threshold is purely subtractive — it can remove
trust, never grant it. `score_source=RAW` marks the numbers as raw,
not calibrated. When measured distributions exist for this surface,
they replace the policy tier (see thresholds.py).

Triage honesty (audit D2, 2026-09-24): the below-threshold leg has
TWO different external readings, and the surface distinguishes them.
MODEL-UNAVAILABLE — the gated call returned the model-off fallback
(`unavailable_structured_fallback` shape, `_model_blocked` marker;
disabled, blocked, or transport failure) — carries NO structured
judgment, so escalating its placeholder to the conservative urgency
fabricated an assessment in the documented default build (model off
labeled every symptom HIGH). `external_urgency` externalizes exactly
that leg as MODEL_UNAVAILABLE_URGENCY with a model-off explanation.
GENUINELY-ANSWERED-BELOW-THRESHOLD — a real structured pick whose
confidence is under the bar — every other NEEDS_HUMAN leg, and every
urgency_disagreement keep the conservative highest urgency unchanged
(the safety rules are untouched; disagreement dominates the carve-out).

`per_level_probabilities` is a point mass on the picked level: the
pipeline makes a hard pick and claims no calibrated distribution —
the coherent encoding of a hard pick under a schema that requires a
distribution.
"""

from __future__ import annotations

from collections.abc import Mapping

from healthadvocate.decisions.assess import DecisionOutcome, Outcome
from healthadvocate.decisions.receipt import IdentificationReceipt
from healthadvocate.decisions.runners import DEFAULT_RUNNER
from healthadvocate.decisions.schemas import (
    ScoreAnswer,
    ScoreLevel,
    ScoreQuestion,
    ScoreSource,
)
from healthadvocate.decisions.thresholds import (
    ClassThreshold,
    ThresholdData,
    ThresholdProvenance,
)
from healthadvocate.privacy.boundary import DeidentificationStatus

#: The converted surface's name — threshold data is surface-linked to it.
TRIAGE_SURFACE = "symptom-triage"

#: Fixed ordered rubric, ascending severity; level indexes it.
URGENCY_RUBRIC: tuple[str, ...] = ("low", "medium", "high")

#: The conservative (fail-closed / disagreement) external answer.
CONSERVATIVE_URGENCY = URGENCY_RUBRIC[-1]

#: External urgency when the gated model made NO structured judgment
#: (model disabled, blocked, or transport failure — the
#: `unavailable_structured_fallback` shape). An EXTERNAL value only:
#: it is deliberately not a rubric level, so it can never be mistaken
#: for a model assessment and never round-trips back in as a pick
#: (`build_urgency_candidate` rejects it as out-of-rubric).
MODEL_UNAVAILABLE_URGENCY = "unavailable"

#: Deterministic explanation paired with MODEL_UNAVAILABLE_URGENCY —
#: the honest statement that the optional local model is off while the
#: deterministic preparation steps remain (mirrors the fallback's own
#: sentence in `healthadvocate.core.llm_client`).
MODEL_UNAVAILABLE_EXPLANATION = (
    "The optional local model is unavailable or blocked by the privacy "
    "boundary, so no model urgency judgment was made. Deterministic "
    "preparation steps remain available."
)

#: The urgency question this surface asks.
URGENCY_QUESTION = ScoreQuestion(
    id="symptom-triage-urgency",
    rubric=[ScoreLevel(label=label) for label in URGENCY_RUBRIC],
)

#: Policy bar: strictly between the two validity confidences (0.0 and
#: 1.0) so it separates placeholders from real picks and nothing else.
_SCORE_POLICY_BAR = 0.5

_SYMPTOM_TRIAGE_POLICY_PROVENANCE = ThresholdProvenance(
    source="policy",
    surface=TRIAGE_SURFACE,
    adopted_on="2026-09-22",
    rationale=(
        "Conservative bridge until measured confidence distributions "
        "exist for symptom-triage: the code-runner urgency candidate "
        "carries a binary validity confidence (1.0 real structured "
        "pick, 0.0 placeholder), so the 0.5 bar only escalates "
        "placeholders to the conservative urgency; it never grants "
        "trust a measured threshold would deny."
    ),
)

#: Production threshold data for this surface (the J2-c policy tier;
#: see thresholds.py for the honesty argument). Replaced by measured
#: data when a distribution exists for this surface and class.
SYMPTOM_TRIAGE_THRESHOLDS = ThresholdData(
    surface=TRIAGE_SURFACE,
    thresholds={
        "score": ClassThreshold(
            question_class="score",
            min_confidence=_SCORE_POLICY_BAR,
            provenance=_SYMPTOM_TRIAGE_POLICY_PROVENANCE,
        )
    },
)

#: Placeholder markers in the gated model output: a pick read from one
#: of these shapes is the pipeline's own "no judgment was made" signal
#: (unavailable_structured_fallback sets _model_blocked; the unparseable
#: path sets _raw_text), not an assessment.
_PLACEHOLDER_MARKERS = ("_model_blocked", "_raw_text")


def build_urgency_candidate(llm_output: Mapping[str, object]) -> ScoreAnswer | None:
    """Type the current urgency pick as a ScoreAnswer candidate.

    The pick semantics are the pre-conversion ones: the structured
    output's ``urgency`` when the key is present, else "medium". A pick
    outside the rubric (any value a model may emit that is not exactly
    low/medium/high) types to NO candidate — the gate then fails closed
    on invalid-answer, which the surface maps to the conservative
    urgency (the pre-conversion surface would have surfaced such a
    string verbatim; this is the conservative hardening of that hole).
    """
    if not isinstance(llm_output, Mapping):
        return None
    pick = llm_output.get("urgency", "medium")
    if pick not in URGENCY_RUBRIC:
        return None
    level = URGENCY_RUBRIC.index(pick)
    probabilities = [0.0] * len(URGENCY_RUBRIC)
    probabilities[level] = 1.0
    placeholder = any(llm_output.get(marker) for marker in _PLACEHOLDER_MARKERS)
    return ScoreAnswer(
        question_id=URGENCY_QUESTION.id,
        level=level,
        per_level_probabilities=probabilities,
        confidence=0.0 if placeholder else 1.0,
        score_source=ScoreSource.RAW,
    )


def deidentification_status_from_output(value: object) -> DeidentificationStatus:
    """Map the gated call's reported status onto the boundary vocabulary.

    Unknown or missing values map to FAILED — the receipt then fails
    the deidentification gate in `assess` and the surface escalates
    conservatively. Never guesses SUCCESS.
    """
    if value == DeidentificationStatus.SUCCESS.value:
        return DeidentificationStatus.SUCCESS
    if value == DeidentificationStatus.NO_PII_FOUND.value:
        return DeidentificationStatus.NO_PII_FOUND
    return DeidentificationStatus.FAILED


def is_model_unavailable(llm_output: object) -> bool:
    """True when the gated call's output is the model-unavailable
    fallback shape — NO structured judgment exists (model disabled,
    blocked, or transport failure; `unavailable_structured_fallback`
    sets `_model_blocked` on every path that produces it).

    A `_raw_text` output is deliberately NOT model-unavailable: the
    model ran and answered, just unparseably — its placeholder pick
    keeps the conservative escalation (fail closed on an unknown
    model answer, audit D2 changes nothing there).
    """
    return isinstance(llm_output, Mapping) and bool(
        llm_output.get("_model_blocked")
    )


def external_urgency(
    outcome: DecisionOutcome,
    urgency_disagreement: bool,
    *,
    model_unavailable: bool = False,
) -> str:
    """The external answer from the typed outcome (the safety mapping).

    NEEDS_HUMAN on ANY leg, or an urgency disagreement, surfaces as the
    conservative highest urgency — never below the answered level. An
    ANSWERED outcome surfaces its rubric label; a missing or out-of-
    range answer on an ANSWERED outcome (unreachable via `assess`, but
    defended here anyway) is conservative too.

    The audit-D2 honesty carve-out: a below-threshold outcome produced
    by a MODEL-UNAVAILABLE placeholder (`model_unavailable=True`, from
    `is_model_unavailable`) externalizes as MODEL_UNAVAILABLE_URGENCY —
    "high" there fabricated an assessment in the documented default
    build. The carve-out is scoped to exactly that leg: a genuinely
    answered below-threshold pick (`model_unavailable=False`) and every
    other NEEDS_HUMAN leg keep the conservative urgency, and an
    urgency_disagreement dominates the carve-out (safety first — the
    real fallback never says "low", so the two cannot co-occur end to
    end, but the ordering is defended anyway).
    """
    if urgency_disagreement:
        return CONSERVATIVE_URGENCY
    if model_unavailable and outcome.reason_kind == "below-threshold":
        return MODEL_UNAVAILABLE_URGENCY
    if outcome.outcome is not Outcome.ANSWERED:
        return CONSERVATIVE_URGENCY
    answer = outcome.answer
    if answer is None or not 0 <= answer.level < len(URGENCY_RUBRIC):
        return CONSERVATIVE_URGENCY
    return URGENCY_RUBRIC[answer.level]


def assess_urgency(
    *,
    receipt: IdentificationReceipt,
    llm_output: Mapping[str, object],
) -> DecisionOutcome:
    """Adjudicate this surface's urgency question through the J1 gate.

    Thin wrapper so the converting surface reads as one typed call:
    fixed question, surface, code runner, and the surface-linked policy
    threshold data.
    """
    from healthadvocate.decisions.assess import assess

    return assess(
        URGENCY_QUESTION,
        receipt=receipt,
        candidate=build_urgency_candidate(llm_output),
        surface=TRIAGE_SURFACE,
        runner=DEFAULT_RUNNER,
        thresholds=SYMPTOM_TRIAGE_THRESHOLDS,
    )


__all__ = [
    "CONSERVATIVE_URGENCY",
    "MODEL_UNAVAILABLE_EXPLANATION",
    "MODEL_UNAVAILABLE_URGENCY",
    "SYMPTOM_TRIAGE_THRESHOLDS",
    "TRIAGE_SURFACE",
    "URGENCY_QUESTION",
    "URGENCY_RUBRIC",
    "assess_urgency",
    "build_urgency_candidate",
    "deidentification_status_from_output",
    "external_urgency",
    "is_model_unavailable",
]
