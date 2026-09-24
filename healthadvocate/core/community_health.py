"""Community health scanner — NER + structured LLM bulletin analysis."""

from __future__ import annotations

from .engine import HealthEngine, format_entities_with_confidence
from .cross_validation import cross_validate
from .llm_client import urgency_from_output
from healthadvocate.privacy.gated_model import structured_model_call


def scan_bulletin(engine: HealthEngine, text: str) -> dict:
    if not text or not text.strip():
        return {"explanation": "No bulletin text provided.", "action_items": [], "red_flags": [], "validation": None}

    diseases = engine.extract_diseases(text, confidence=0.5)
    drugs = engine.extract_drugs(text, confidence=0.5)

    all_entities = list(diseases.entities) + list(drugs.entities)
    entity_desc = format_entities_with_confidence(all_entities)

    safe_text, pii_map = engine.deidentify_for_llm(text, method="mask")

    prompt = (
        f"A patient found this health bulletin or alert:\n\n{safe_text}\n\n"
        f"NER Analysis:\n{entity_desc}\n\n"
        "As a health advocate, help the patient understand whether this is a real health concern "
        "or potentially misleading information. Be balanced and evidence-based."
    )

    system = (
        "You are a patient health advocate analyzing health bulletins and alerts. "
        "Help patients distinguish real health risks from hype. "
        "Be balanced, evidence-based, and practical."
    )

    llm_output = structured_model_call(
        engine, prompt, module_type="bulletin_analysis", system=system,
    )
    validation = cross_validate(all_entities, llm_output)

    return {
        "conditions_detected": [{"name": e.text, "label": e.label, "confidence": round(e.confidence, 2)} for e in diseases.entities],
        "treatments_detected": [{"name": e.text, "label": e.label, "confidence": round(e.confidence, 2)} for e in drugs.entities],
        "explanation": llm_output.get("summary", ""),
        "urgency": urgency_from_output(llm_output),
        "action_items": llm_output.get("action_items", []),
        "red_flags": llm_output.get("red_flags", []),
        "credibility": llm_output.get("credibility", "medium"),
        "scientific_context": llm_output.get("scientific_context", ""),
        "recommended_action": llm_output.get("recommended_action", ""),
        # DEPRECATED 2026-09-24 (glass honesty, audit B3): `pii_scrubbed`
        # reads as a guarantee that scrubbing happened; kept one release
        # for older clients. The honest key is `pii_found_and_masked` —
        # True only when PII was found AND masked; False/absent means
        # none was found, never a guarantee that none slipped through.
        "pii_scrubbed": len(pii_map) > 0,
        "pii_found_and_masked": HealthEngine.pii_was_found_and_masked(pii_map),
        "structured_output": llm_output,
        "validation": {
            "confirmed": validation.confirmed,
            "ner_only": validation.ner_only,
            "llm_only": validation.llm_only,
            "reliability": validation.reliability,
            "urgency_disagreement": validation.urgency_disagreement,
        },
    }
