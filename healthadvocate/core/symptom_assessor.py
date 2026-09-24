"""Symptom assessment — NER extraction + structured LLM analysis.

J2-c (2026-09-22): the urgency pick is routed through the HA-JEV
typed-decision layer (healthadvocate/decisions/symptom_triage.py).
The public API and every pre-conversion behavior is preserved; the
typed layer adds auditability (identification receipt, calibrated
gate, NEEDS_HUMAN wrapper) and never lowers urgency — any fail-closed
leg and any urgency_disagreement surfaces as the conservative
highest urgency, exactly as the disagreement rule did before.

Triage honesty (audit D2, 2026-09-24): the one carve-out is the
model-UNAVAILABLE placeholder (`unavailable_structured_fallback`
shape, `_model_blocked` marker). The documented default build runs
with the optional local model off; labeling every symptom HIGH there
fabricated assessments. That one leg externalizes as "unavailable"
with a model-off explanation; a genuinely answered below-threshold
pick and every disagreement keep the conservative escalation.
Deidentify-before-reasoning order is untouched: the gated model call
still assembles and deidentifies the full context itself.
"""

from __future__ import annotations

from .engine import HealthEngine, format_entities_with_confidence
from .cross_validation import cross_validate
from healthadvocate.privacy.gated_model import structured_model_call
from healthadvocate.decisions.assess import invalid_receipt_outcome
from healthadvocate.decisions.receipt import receipt_from_analysis
from healthadvocate.decisions.symptom_triage import (
    MODEL_UNAVAILABLE_EXPLANATION,
    MODEL_UNAVAILABLE_URGENCY,
    URGENCY_QUESTION,
    assess_urgency,
    deidentification_status_from_output,
    external_urgency,
    is_model_unavailable,
)


def assess_symptoms(engine: HealthEngine, symptoms: str, profile_id: str | None = None) -> dict:
    if not symptoms or not symptoms.strip():
        return {
            "conditions": [], "urgency": "low",
            "explanation": "No symptoms provided.", "action_items": [],
            "red_flags": [], "validation": None, "structured_output": None,
        }

    result = engine.extract_diseases(symptoms)
    conditions = [{"name": e.text, "confidence": round(e.confidence, 2), "label": e.label} for e in result.entities]

    entity_desc = format_entities_with_confidence(result.entities)
    primary = (
        f"A patient reports these symptoms: {symptoms}\n\n"
        f"NER Analysis:\n{entity_desc}\n\n"
        "As a health advocate, provide a structured assessment. "
        "Assess urgency realistically — serious symptoms should be high. "
        "Mild and common symptoms should be low."
    )

    system = (
        "You are a patient health advocate helping assess symptoms. "
        "Be concise, practical, empathetic. "
        "Always recommend seeing a healthcare provider for anything beyond minor issues."
    )

    # Full assembled context (including family profile) is deidentified first.
    llm_output = structured_model_call(
        engine,
        primary,
        module_type="symptom_assessment",
        system=system,
        profile_id=profile_id,
    )
    validation = cross_validate(result.entities, llm_output)

    # J2-c: type the urgency pick through the receipt contract. The
    # receipt comes from the REAL identify stage above (never fabricated);
    # its deidentification status is the one the gated call measured. A
    # receipt that cannot be built fails closed through the same wrapper
    # shape. Disagreement dominates: it escalates to the conservative
    # urgency even when the gate answered.
    built = receipt_from_analysis(
        result,
        deidentification_status=deidentification_status_from_output(
            llm_output.get("deidentification_status", "unknown")
        ),
    )
    if built.receipt is None:
        decision = invalid_receipt_outcome(
            URGENCY_QUESTION, errors=built.errors
        )
    else:
        decision = assess_urgency(
            receipt=built.receipt, llm_output=llm_output
        )
    # Audit D2: the wiring hands the mapping the model-unavailable
    # signal from the SAME output the candidate was built from, so the
    # below-threshold placeholder leg externalizes as "unavailable"
    # while every safety escalation (disagreement, genuine
    # below-threshold answers, every other fail-closed leg) is decided
    # inside the mapping exactly as before.
    urgency = external_urgency(
        decision,
        validation.urgency_disagreement,
        model_unavailable=is_model_unavailable(llm_output),
    )
    explanation = llm_output.get("summary", "")
    if urgency == MODEL_UNAVAILABLE_URGENCY:
        # Deterministic, total pairing: whenever the external urgency
        # says no model judgment was made, the explanation says so too
        # (the model is off; deterministic preparation remains).
        explanation = MODEL_UNAVAILABLE_EXPLANATION

    status = llm_output.get("deidentification_status", "unknown")
    return {
        "conditions": conditions,
        "urgency": urgency,
        "explanation": explanation,
        "action_items": llm_output.get("action_items", []),
        "red_flags": llm_output.get("red_flags", []),
        "possible_conditions": llm_output.get("possible_conditions", []),
        "recommended_specialist": llm_output.get("recommended_specialist"),
        "structured_output": llm_output,
        "validation": {
            "confirmed": validation.confirmed,
            "ner_only": validation.ner_only,
            "llm_only": validation.llm_only,
            "reliability": validation.reliability,
            "urgency_disagreement": validation.urgency_disagreement,
        },
        "model_used": result.model_used,
        "processing_time": result.processing_time,
        "deidentification_status": status,
        "pii_scrubbed": status == "success",
        "urgency_decision": decision.model_dump(mode="json"),
        "urgency_receipt": (
            built.receipt.model_dump(mode="json") if built.receipt else None
        ),
    }
