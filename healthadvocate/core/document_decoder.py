"""Document decoder — extract and explain medical entities from documents."""

from __future__ import annotations

from .engine import HealthEngine

LABEL_EXPLANATIONS = {
    "DISEASE": "A medical condition or illness that may require treatment",
    "CONDITION": "A health condition that may need monitoring or treatment",
    "PATHOLOGY": "A disease process or abnormality found in tissues",
    "CHEM": "A chemical compound used in medical treatment",
    "DRUG": "A medication prescribed or being taken",
    "MEDICATION": "A medicine or pharmaceutical preparation",
    "Organ": "An organ in the body (e.g., heart, liver, lungs)",
    "Tissue": "A type of body tissue (e.g., muscle, nerve, connective)",
    "ANATOMY": "A part of the body's physical structure",
    "first_name": "A person's first name (PII detected)",
    "last_name": "A person's last name (PII detected)",
    "email": "An email address (PII detected)",
    "phone_number": "A phone number (PII detected)",
    "ssn": "A Social Security Number (PII detected)",
    "date_of_birth": "A date of birth (PII detected)",
    "street_address": "A street address (PII detected)",
}


def _explain_entity(entity) -> dict:
    """Build an explained entity dict."""
    label = entity.label
    explanation = LABEL_EXPLANATIONS.get(label, f"A detected entity of type: {label}")
    return {
        "text": entity.text,
        "label": label,
        "category": entity.category,
        "confidence": round(entity.confidence, 2),
        "explanation": explanation,
        "position": {"start": entity.start, "end": entity.end},
    }


def decode_document(engine: HealthEngine, text: str, lang: str = "en") -> dict:
    """Extract and explain all medical entities in a document."""
    if not text or not text.strip():
        return {
            "entities": [],
            "pii_found": [],
            "summary": "No document text provided.",
            "entity_counts": {"diseases": 0, "drugs": 0, "anatomy": 0, "pii": 0},
        }

    diseases = engine.extract_diseases(text)
    drugs = engine.extract_drugs(text)
    anatomy = engine.extract_anatomy(text)
    pii = engine.extract_pii(text, lang=lang)

    errors = [r.error for r in (diseases, drugs, anatomy, pii) if r.error]
    if errors and not any((diseases.entities, drugs.entities, anatomy.entities, pii.entities)):
        return {
            "entities": [],
            "pii_found": [],
            "summary": f"Analysis failed: {'; '.join(errors)}",
            "entity_counts": {"diseases": 0, "drugs": 0, "anatomy": 0, "pii": 0},
            "error": "; ".join(errors),
        }

    all_entities = []
    pii_entities = []

    for entity in diseases.entities + drugs.entities + anatomy.entities:
        all_entities.append(_explain_entity(entity))

    for entity in pii.entities:
        pii_entities.append(_explain_entity(entity))

    n_diseases = len(diseases.entities)
    n_drugs = len(drugs.entities)
    n_anatomy = len(anatomy.entities)
    n_pii = len(pii.entities)

    parts = []
    if n_diseases:
        parts.append(f"{n_diseases} condition{'s' if n_diseases != 1 else ''}")
    if n_drugs:
        parts.append(f"{n_drugs} medication{'s' if n_drugs != 1 else ''}")
    if n_anatomy:
        parts.append(f"{n_anatomy} body part{'s' if n_anatomy != 1 else ''}")

    if parts:
        summary = f"This document mentions {' and '.join(parts)}."
    else:
        summary = "No specific medical entities were detected in this document."

    if n_pii:
        summary += f" {n_pii} piece{'s' if n_pii != 1 else ''} of personal information were found."

    return {
        "entities": all_entities,
        "pii_found": pii_entities,
        "summary": summary,
        "entity_counts": {
            "diseases": n_diseases,
            "drugs": n_drugs,
            "anatomy": n_anatomy,
            "pii": n_pii,
        },
        "models_used": {
            "diseases": diseases.model_used,
            "drugs": drugs.model_used,
            "anatomy": anatomy.model_used,
        },
        "processing_time": {
            "diseases": diseases.processing_time,
            "drugs": drugs.processing_time,
            "anatomy": anatomy.processing_time,
        },
    }
