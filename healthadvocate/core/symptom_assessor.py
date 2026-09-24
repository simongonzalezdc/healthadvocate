"""Symptom assessment — NER extraction + structured LLM analysis.

J2-c (2026-09-22): the urgency pick is routed through the HA-JEV
typed-decision layer (healthadvocate/decisions/symptom_triage.py).
The public API and every pre-conversion behavior is preserved; the
typed layer adds auditability (identification receipt, calibrated
gate, NEEDS_HUMAN wrapper) and never lowers urgency — any fail-closed
leg and any urgency_disagreement surfaces as the conservative
highest urgency, exactly as the disagreement rule did before.
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
    URGENCY_QUESTION,
    assess_urgency,
    deidentification_status_from_output,
    external_urgency,
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
    urgency = external_urgency(decision, validation.urgency_disagreement)

    status = llm_output.get("deidentification_status", "unknown")
    # B3 glass honesty: the flag must describe the PERSON's text, so it
    # derives from a deidentify pass over the raw symptoms (the same
    # pattern the document/bill/discharge surfaces use for their PII
    # flags) — NOT from the assembled-context mapping size, whose fixed
    # prompt scaffolding ("health advocate" masked as an [occupation])
    # would make the flag vacuously true for every input.
    symptom_pii_map = engine.deidentify_for_llm(symptoms)[1]
    pii_found_and_masked = HealthEngine.pii_was_found_and_masked(symptom_pii_map)
    return {
        "conditions": conditions,
        "urgency": urgency,
        "explanation": llm_output.get("summary", ""),
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
        # DEPRECATED 2026-09-24 (glass honesty, audit B3): `pii_scrubbed`
        # reported the deidentification status, which reads as a guarantee;
        # kept one release for older clients. The honest key is
        # `pii_found_and_masked` — True only when PII in the person's own
        # text was found and masked; False/absent means none was found,
        # never a guarantee that none slipped through.
        "pii_scrubbed": status == "success",
        "pii_found_and_masked": pii_found_and_masked,
        "urgency_decision": decision.model_dump(mode="json"),
        "urgency_receipt": (
            built.receipt.model_dump(mode="json") if built.receipt else None
        ),
    }
