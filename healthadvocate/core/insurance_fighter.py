"""Insurance denial fighter — PII-safe NER + structured LLM appeal generation.

HA-JEV J2-b (design docs/HA-JEV-TYPED-DECISIONS-DESIGN-2026-09-22.md §4-5):
the denial-reason pick routes through the typed-decision layer. The
free-text reason the structured model returns is normalized by a
deterministic `code`-runner rule onto the canonical denial-reason set,
adjudicated by `assess` behind the identification-receipt contract, and
only an ANSWERED wrapper yields a denial reason. Every fail-closed leg —
below threshold, invalid receipt, failed deidentification, unknown
deidentification status, hostile or ambiguous pick — maps to this
surface's existing safe fallback (the empty string callers always received
when no reason could be classified), while the NEEDS_HUMAN wrapper rides
along as the audit trail. The deidentify-before-reasoning order is
untouched: denial text still flows through the privacy boundary first.

Calibration honesty on this surface: the rule is deterministic, so its
confidence distribution on the frozen synthetic measurement corpus is
degenerate at 1.0 — a fired rule is certain of its mapping or it does not
fire. The measured, surface-linked threshold is accordingly 1.0 (the most
conservative policy: only exact, unambiguous matches clear it), and the
provenance records the real measurement (corpus size, date). Anything
below it — from any future runner — fails closed to the fallback.
"""

from __future__ import annotations

from collections.abc import Sequence

from .engine import AnalysisResult, HealthEngine, format_entities_with_confidence
from .cross_validation import cross_validate
from healthadvocate.decisions import (
    DEFAULT_RUNNER,
    FAIL_CLOSED_SENTENCE,
    ChoiceAnswer,
    ChoiceQuestion,
    ClassThreshold,
    DecisionOutcome,
    IdentificationReceipt,
    Outcome,
    StrippedValidationError,
    ThresholdData,
    ThresholdProvenance,
    assess,
    receipt_from_analysis,
)
from healthadvocate.privacy.boundary import DeidentificationStatus
from healthadvocate.privacy.gated_model import structured_model_call

#: The converted surface name (threshold provenance is surface-linked).
DENIAL_CLASSIFIER_SURFACE = "denial-classifier"

#: Stable question id for the denial-reason Choice.
DENIAL_REASON_QUESTION_ID = "q-denial-reason"

#: The canonical denial-reason set — the options of the ChoiceQuestion.
#: Free-text picks never reach callers; only a canonical option does.
DENIAL_REASON_OPTIONS: tuple[str, ...] = (
    "not medically necessary",
    "prior authorization required",
    "experimental or investigational",
    "out-of-network",
    "not a covered benefit",
    "formulary exclusion",
    "insufficient documentation",
)

#: Lowercase alias substrings per canonical option. A pick must match
#: aliases of exactly ONE option; zero or several canonical matches fail
#: closed (no confident answer from an ambiguous or unknown letter).
_DENIAL_REASON_ALIASES: dict[str, tuple[str, ...]] = {
    "not medically necessary": (
        "not medically necessary",
        "lack of medical necessity",
        "lacks medical necessity",
        "no medical necessity",
        "does not meet medical necessity",
        "failed medical necessity",
    ),
    "prior authorization required": (
        "prior authorization",
        "prior approval",
        "preauthorization",
        "pre-authorization",
    ),
    "experimental or investigational": (
        "experimental",
        "investigational",
    ),
    "out-of-network": (
        "out of network",
        "out-of-network",
        "non-participating provider",
        "nonparticipating provider",
    ),
    "not a covered benefit": (
        "not covered",
        "not a covered benefit",
        "non-covered service",
        "excluded service",
        "coverage exclusion",
    ),
    "formulary exclusion": (
        "formulary",
    ),
    "insufficient documentation": (
        "insufficient documentation",
        "documentation is insufficient",
        "records insufficient",
        "lack of documentation",
        "incomplete documentation",
        "additional documentation required",
        "documentation required",
    ),
}

#: The confidence a fired deterministic rule asserts — degenerate
#: distribution: the rule maps its input certainly or does not fire.
_DENIAL_REASON_RULE_CONFIDENCE = 1.0

#: The frozen synthetic corpus the threshold was measured on (synthetic-
#: only law; every fixture normalizes to exactly one canonical option —
#: pinned by tests that re-run the measurement). sample_size in the
#: provenance below is this corpus's length.
_DENIAL_REASON_MEASUREMENT_CORPUS: tuple[str, ...] = (
    # not medically necessary
    "The requested service is not medically necessary under the plan criteria.",
    "Coverage denied: the claim lacks medical necessity for this diagnosis.",
    # prior authorization required
    "No prior authorization was obtained before the date of service.",
    "Preauthorization is required for this imaging study; the claim is denied.",
    # experimental or investigational
    "The requested treatment is experimental and not proven effective.",
    "Denied as investigational therapy under the plan's coverage policy.",
    # out-of-network
    "The rendering provider is out of network and no exception applies.",
    "Services from a non-participating provider are denied as out of network.",
    # not a covered benefit
    "The service is not covered under this benefit plan.",
    "Excluded service: this procedure is not a covered benefit.",
    # formulary exclusion
    "The requested drug is excluded from the plan formulary.",
    "Non-formulary medication denied: the product is not on formulary.",
    # insufficient documentation
    "Insufficient documentation was submitted to support the claim.",
    "Additional documentation required: the records are insufficient for review.",
)

#: Measured threshold data for this surface (design §4 calibration honesty
#: rule): conservative (1.0 — only exact deterministic matches clear it),
#: surface-linked, with the real measurement recorded in the provenance.
#: No defaults: this is the only threshold set the surface knows.
DENIAL_CLASSIFIER_THRESHOLDS = ThresholdData(
    surface=DENIAL_CLASSIFIER_SURFACE,
    thresholds={
        "choice": ClassThreshold(
            question_class="choice",
            min_confidence=1.0,
            provenance=ThresholdProvenance(
                source="measured",
                surface=DENIAL_CLASSIFIER_SURFACE,
                measured_on="2026-09-22",
                sample_size=len(_DENIAL_REASON_MEASUREMENT_CORPUS),
            ),
        )
    },
)


def _normalize_denial_reason(pick: object) -> str | None:
    """Deterministic code-runner rule: map a free-text denial-reason pick
    onto exactly one canonical option (case-insensitive alias match).

    Returns None when the pick is not a string, is blank, matches no
    canonical option, or matches several — every such case fails closed;
    ambiguity is a human decision, never a confident answer.
    """
    if not isinstance(pick, str) or not pick.strip():
        return None
    lowered = pick.lower()
    matched = {
        option
        for option in DENIAL_REASON_OPTIONS
        if any(alias in lowered for alias in _DENIAL_REASON_ALIASES[option])
    }
    if len(matched) == 1:
        return matched.pop()
    return None


def _denial_reason_question() -> ChoiceQuestion:
    """The ChoiceQuestion over the canonical denial-reason set."""
    return ChoiceQuestion(
        id=DENIAL_REASON_QUESTION_ID,
        options=list(DENIAL_REASON_OPTIONS),
        context_ref=f"{DENIAL_CLASSIFIER_SURFACE}:identify-receipt",
    )


class _DenialIdentifyAnalysis:
    """Aggregate of the REAL identify-stage runs (condition and medication
    NER over the denial text — plus patient context when supplied).

    `model_used` is the sorted union of the analyses' own model names —
    derived, never fabricated; `entities` are the analyses' own entity
    objects, whose raw text the receipt builder structurally never copies.
    """

    def __init__(self, analyses: Sequence[AnalysisResult]) -> None:
        self.entities = [entity for analysis in analyses for entity in analysis.entities]
        used = sorted(
            {
                analysis.model_used.strip()
                for analysis in analyses
                if isinstance(analysis.model_used, str) and analysis.model_used.strip()
            }
        )
        self.model_used = "+".join(used)


def _deidentification_status_from_mapping(
    mapping: object,
) -> DeidentificationStatus | None:
    """The real status of THIS call's privacy-boundary run, exactly as the
    engine reports it. Unknown or missing status → None: the receipt must
    state a real status or not exist (never fabricated)."""
    status = mapping.get("_deidentification_status") if isinstance(mapping, dict) else None
    try:
        return DeidentificationStatus(status)
    except ValueError:
        return None


def _no_receipt_outcome(
    errors: Sequence[StrippedValidationError],
) -> DecisionOutcome:
    """No valid identification receipt → no assessment (the load-bearing
    rule), expressed with assess's own invalid-receipt vocabulary — the
    fail-closed sentence, the same leg, the same next steps (pinned
    equal to assess's wrapper by tests)."""
    return DecisionOutcome(
        outcome=Outcome.NEEDS_HUMAN,
        reason_kind="invalid-receipt",
        question_id=DENIAL_REASON_QUESTION_ID,
        question_class="choice",
        runner=DEFAULT_RUNNER,
        answer=None,
        threshold_applied=None,
        reason=FAIL_CLOSED_SENTENCE,
        allowed_next_steps=[
            "Run the identify stage and pass its identification receipt",
            "Decide as a human outside this application",
        ],
        validation_errors=list(errors),
    )


def classify_denial_reason(
    pick: object,
    analyses: Sequence[AnalysisResult],
    deidentification_status: DeidentificationStatus | None,
) -> tuple[DecisionOutcome, IdentificationReceipt | None]:
    """Route the model's free-text denial-reason pick through the HA-JEV
    typed-decision gate behind the identification-receipt contract.

    Returns (wrapper, receipt): the wrapper is always a DecisionOutcome —
    ANSWERED only when the receipt is valid, the pick normalizes to
    exactly one canonical option, and the deterministic candidate clears
    the measured threshold; every other path is NEEDS_HUMAN carrying the
    numbers. The receipt is the one the gate consumed, or None when none
    could be built from the real identify stage.
    """
    question = _denial_reason_question()

    if deidentification_status is not None:
        built = receipt_from_analysis(
            _DenialIdentifyAnalysis(analyses),
            coverage_notes=(
                "denial surface identify stage: condition and medication NER",
            ),
            deidentification_status=deidentification_status,
        )
        receipt = built.receipt
        build_errors: list[StrippedValidationError] = list(built.errors)
    else:
        receipt = None
        build_errors = [
            StrippedValidationError(
                loc=("deidentification_status",),
                msg=(
                    "The engine's deidentification run reported no known "
                    "status; no receipt can state one honestly"
                ),
                type="deidentification_status_unknown",
                url=None,
            )
        ]

    if receipt is None:
        return _no_receipt_outcome(build_errors), None

    normalized = _normalize_denial_reason(pick)
    candidate: ChoiceAnswer | None = None
    if normalized is not None:
        candidate = ChoiceAnswer(
            question_id=DENIAL_REASON_QUESTION_ID,
            value=normalized,
            probability=_DENIAL_REASON_RULE_CONFIDENCE,
            confidence=_DENIAL_REASON_RULE_CONFIDENCE,
        )

    outcome = assess(
        question,
        receipt=receipt,
        candidate=candidate,
        surface=DENIAL_CLASSIFIER_SURFACE,
        runner=DEFAULT_RUNNER,
        thresholds=DENIAL_CLASSIFIER_THRESHOLDS,
    )
    return outcome, receipt


def _denial_reason_from_outcome(outcome: DecisionOutcome) -> str:
    """Map a wrapper to the surface's denial-reason value: an ANSWERED
    choice yields its canonical option; ANY NEEDS_HUMAN leg yields the
    surface's existing safe fallback — the empty string (never a new
    confident answer from a failed leg)."""
    if outcome.outcome is Outcome.ANSWERED and isinstance(outcome.answer, ChoiceAnswer):
        return outcome.answer.value
    return ""


def fight_denial(engine: HealthEngine, denial_text: str, patient_info: str = "", profile_id: str | None = None) -> dict:
    if not denial_text or not denial_text.strip():
        return {"explanation": "No denial text provided.", "action_items": [], "red_flags": [], "validation": None}

    # Deidentify before sending to LLM
    safe_denial, denial_pii = engine.deidentify_for_llm(denial_text, method="mask")
    safe_patient = ""
    if patient_info and patient_info.strip():
        safe_patient, _ = engine.deidentify_for_llm(patient_info, method="mask")

    diseases = engine.extract_diseases(denial_text, confidence=0.5)
    drugs = engine.extract_drugs(denial_text, confidence=0.5)
    if patient_info and patient_info.strip():
        pi_diseases = engine.extract_diseases(patient_info, confidence=0.5)
        pi_drugs = engine.extract_drugs(patient_info, confidence=0.5)
        diseases.entities.extend(pi_diseases.entities)
        drugs.entities.extend(pi_drugs.entities)

    entity_desc = format_entities_with_confidence(list(diseases.entities) + list(drugs.entities))

    patient_context = f"\n\nPatient context: {safe_patient.strip()[:400]}" if safe_patient else ""

    prompt = (
        f"An insurance company sent this denial letter:\n\n{safe_denial}\n\n"
        f"NER Analysis:\n{entity_desc}\n\n"
        f"{patient_context}\n\n"
        "As a patient health advocate, fight this denial. "
        "Explain what it means, why it may be wrong, and write a draft appeal letter."
    )

    system = (
        "You are a patient health advocate specializing in insurance appeals. "
        "You help patients fight unfair denials. Be knowledgeable about insurance law, "
        "appeal processes, and patients' rights. Include a draft appeal letter."
    )

    llm_output = structured_model_call(
        engine, prompt, module_type="appeal_strategy", system=system,
        profile_id=profile_id, max_tokens=2000,
    )

    # HA-JEV J2-b: the denial-reason pick is a candidate ChoiceAnswer,
    # adjudicated behind the identification-receipt contract. The identify
    # stage is the NER analysis above; the receipt states the status of
    # THIS call's real privacy-boundary run. Failure of any leg leaves the
    # denial_reason at its pre-conversion safe fallback ("").
    identify_analyses: list[AnalysisResult] = [diseases, drugs]
    deidentification_status = _deidentification_status_from_mapping(denial_pii)
    decision, denial_receipt = classify_denial_reason(
        llm_output.get("denial_reason") if isinstance(llm_output, dict) else None,
        identify_analyses,
        deidentification_status,
    )
    denial_reason = _denial_reason_from_outcome(decision)

    all_entities = list(diseases.entities) + list(drugs.entities)
    validation = cross_validate(all_entities, llm_output)

    # A receipt the gate refused to consume (invalid-receipt leg) never
    # rides into the result as audit.
    attach_receipt = denial_receipt is not None and decision.reason_kind != "invalid-receipt"

    return {
        "denial_text": denial_text[:200],
        "entities_found": {
            "conditions": [{"text": e.text, "confidence": round(e.confidence, 2)} for e in diseases.entities],
            "medications": [{"text": e.text, "confidence": round(e.confidence, 2)} for e in drugs.entities],
        },
        "explanation": llm_output.get("summary", ""),
        "urgency": llm_output.get("urgency", "medium"),
        "action_items": llm_output.get("action_items", []),
        "red_flags": llm_output.get("red_flags", []),
        "denial_reason": denial_reason,
        "appeal_arguments": llm_output.get("appeal_arguments", []),
        "draft_appeal": llm_output.get("draft_appeal", ""),
        "structured_output": llm_output,
        "validation": {
            "confirmed": validation.confirmed,
            "ner_only": validation.ner_only,
            "llm_only": validation.llm_only,
            "reliability": validation.reliability,
            "urgency_disagreement": validation.urgency_disagreement,
        },
        # DEPRECATED 2026-09-24 (glass honesty, audit B3): `pii_scrubbed`
        # reads as a guarantee that scrubbing happened; kept one release
        # for older clients. The honest key is `pii_found_and_masked` —
        # True only when PII was found AND masked; False/absent means
        # none was found, never a guarantee that none slipped through.
        "pii_scrubbed": len(denial_pii) > 0,
        "pii_found_and_masked": HealthEngine.pii_was_found_and_masked(denial_pii),
        # Additive J2-b audit: the wrapper (numbers, never prose) and the
        # consumed receipt — both canary-free by construction and pinned so.
        "denial_reason_decision": decision.model_dump(),
        "denial_reason_receipt": denial_receipt.model_dump() if attach_receipt else None,
    }
