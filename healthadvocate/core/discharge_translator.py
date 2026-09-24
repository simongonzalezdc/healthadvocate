"""Discharge translator — PII-safe NER + structured LLM plain language conversion."""

from __future__ import annotations

from .engine import HealthEngine, format_entities_with_confidence
from .cross_validation import cross_validate
from .llm_client import urgency_from_output
from healthadvocate.privacy.gated_model import structured_model_call


def translate_discharge(engine: HealthEngine, text: str, lang: str = "en", profile_id: str | None = None) -> dict:
    if not text or not text.strip():
        return {"explanation": "No discharge text provided.", "action_items": [], "red_flags": [], "validation": None}

    diseases = engine.extract_diseases(text, confidence=0.5)
    drugs = engine.extract_drugs(text, confidence=0.5)
    anatomy = engine.extract_anatomy(text, confidence=0.5)

    # Deidentify before LLM
    safe_text, pii_map = engine.deidentify_for_llm(text, method="mask")

    all_entities = list(diseases.entities) + list(drugs.entities) + list(anatomy.entities)
    entity_desc = format_entities_with_confidence(all_entities)

    prompt = (
        f"A patient received these discharge instructions:\n\n{safe_text[:2000]}\n\n"
        f"NER Analysis:\n{entity_desc}\n\n"
        "Translate these discharge instructions into plain language. "
        "Be very clear about warning signs that require immediate medical attention."
    )

    system = (
        "You are a patient health advocate translating discharge instructions into plain language. "
        "Medical jargon must become everyday English. Be very clear about warning signs "
        "that require immediate medical attention."
    )

    llm_output = structured_model_call(
        engine, prompt, module_type="discharge_translation", system=system,
        profile_id=profile_id,
    )
    validation = cross_validate(all_entities, llm_output)

    return {
        "medications_detected": [{"name": e.text, "label": e.label, "confidence": round(e.confidence, 2)} for e in drugs.entities],
        "conditions_detected": [{"name": e.text, "label": e.label, "confidence": round(e.confidence, 2)} for e in diseases.entities],
        "anatomy_detected": [{"name": e.text, "label": e.label, "confidence": round(e.confidence, 2)} for e in anatomy.entities],
        "explanation": llm_output.get("summary", ""),
        "urgency": urgency_from_output(llm_output),
        "action_items": llm_output.get("action_items", []),
        "red_flags": llm_output.get("red_flags", []),
        "medication_instructions": llm_output.get("medication_instructions", []),
        "warning_signs": llm_output.get("warning_signs", []),
        "follow_up_steps": llm_output.get("follow_up_steps", []),
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
        "pii_scrubbed": len(pii_map) > 0,
        "pii_found_and_masked": HealthEngine.pii_was_found_and_masked(pii_map),
    }
