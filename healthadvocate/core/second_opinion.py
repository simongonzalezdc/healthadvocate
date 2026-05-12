"""Second opinion brief — structure medical records for specialist review."""

from __future__ import annotations

from .engine import HealthEngine
from .document_decoder import LABEL_EXPLANATIONS


def _generate_specialist_questions(conditions: list, medications: list) -> list[str]:
    """Generate questions to ask the second-opinion specialist."""
    questions = []

    for cond in conditions:
        name = cond["text"]
        questions.append(f"Is {name} being treated optimally with the current approach?")
        questions.append(f"Are there newer treatments for {name} that I should consider?")

    for med in medications[:3]:
        name = med["text"]
        questions.append(f"Are there alternatives to {name} with fewer side effects?")
        questions.append(f"Is {name} still the best option given my current condition?")

    questions.append("Is there anything in my records that concerns you?")
    questions.append("Would you recommend any additional tests or evaluations?")

    return questions[:10]


def create_brief(engine: HealthEngine, records: str, lang: str = "en") -> dict:
    """Create a structured, de-identified brief for a second opinion consult."""
    if not records or not records.strip():
        return {
            "deidentified_summary": "",
            "conditions": [],
            "medications": [],
            "anatomy": [],
            "procedures": [],
            "questions_for_specialist": [],
        }

    diseases = engine.extract_diseases(records, confidence=0.5)
    drugs = engine.extract_drugs(records, confidence=0.5)
    anatomy = engine.extract_anatomy(records, confidence=0.5)

    errors = [r.error for r in (diseases, drugs, anatomy) if r.error]
    if errors and not any((diseases.entities, drugs.entities, anatomy.entities)):
        return {
            "deidentified_summary": "",
            "conditions": [],
            "medications": [],
            "anatomy": [],
            "procedures": [],
            "questions_for_specialist": [],
            "error": "; ".join(errors),
        }

    conditions = [{"text": e.text, "label": e.label, "confidence": round(e.confidence, 2)} for e in diseases.entities]
    medications = [{"text": e.text, "label": e.label, "confidence": round(e.confidence, 2)} for e in drugs.entities]
    anatomy_items = [{"text": e.text, "label": e.label} for e in anatomy.entities]

    # De-identify for sharing
    deidentified = engine.deidentify(records, method="mask")

    # Build structured summary
    summary_parts = []
    if conditions:
        cond_names = ", ".join(set(c["text"] for c in conditions))
        summary_parts.append(f"Conditions: {cond_names}")
    if medications:
        med_names = ", ".join(set(m["text"] for m in medications))
        summary_parts.append(f"Medications: {med_names}")
    if anatomy_items:
        anat_names = ", ".join(set(a["text"] for a in anatomy_items))
        summary_parts.append(f"Body areas mentioned: {anat_names}")

    deidentified_summary = "\n".join(summary_parts) if summary_parts else "See de-identified records below."

    # Generate specialist questions
    questions = _generate_specialist_questions(conditions, medications)

    return {
        "deidentified_summary": deidentified_summary,
        "deidentified_records": deidentified,
        "conditions": conditions,
        "medications": medications,
        "anatomy": anatomy_items,
        "procedures": [],
        "questions_for_specialist": questions,
    }
