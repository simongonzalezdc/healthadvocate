"""Discharge instruction translator — convert medical jargon to plain language."""

from __future__ import annotations

import re
from .engine import HealthEngine

MEDICAL_TO_PLAIN: dict[str, str] = {
    "hypertension": "high blood pressure",
    "hypotension": "low blood pressure",
    "myocardial infarction": "heart attack",
    "cerebrovascular accident": "stroke",
    "edema": "swelling",
    "dyspnea": "difficulty breathing",
    "pruritus": "itching",
    "syncope": "fainting",
    "hemorrhage": "bleeding",
    "tachycardia": "fast heart rate",
    "bradycardia": "slow heart rate",
    "arrhythmia": "irregular heartbeat",
    "diagnosis": "identification of your condition",
    "prognosis": "expected outcome",
    "benign": "not cancerous",
    "malignant": "cancerous",
    "chronic": "long-lasting or ongoing",
    "acute": "sudden or short-term",
    "prophylactic": "preventive",
    "subcutaneous": "under the skin",
    "intravenous": "through a vein (IV)",
    "oral": "by mouth",
    "topical": "applied to the skin",
    "discharge": "allowed to go home",
    "follow-up": "return visit",
    "nausea": "feeling like you might throw up",
    "vomiting": "throwing up",
    "diarrhea": "loose or watery stools",
    "constipation": "difficulty having bowel movements",
    "fatigue": "feeling very tired",
    "malaise": "feeling unwell",
    "anesthesia": "medicine that makes you sleep during a procedure",
    "antibiotic": "medicine that fights bacterial infections",
    "analgesic": "pain medicine",
    "anti-inflammatory": "medicine that reduces swelling",
    "antihypertensive": "blood pressure medicine",
    "contraindication": "reason not to use a treatment",
    "adverse effect": "side effect or unwanted reaction",
    "therapeutic": "healing or treatment-related",
    "palliative": "focused on comfort and quality of life",
    "necrosis": "tissue death",
    "stenosis": "narrowing",
    "thrombosis": "blood clot",
    "embolism": "blocked blood vessel",
    "sepsis": "life-threatening infection response",
    "intubation": "placing a breathing tube",
    "extubation": "removing the breathing tube",
    "catheter": "a thin tube placed in the body",
    "incision": "surgical cut",
    "suture": "stitch",
    "dressing": "bandage",
    "ambulate": "walk",
    "nil per os": "nothing to eat or drink",
    "prn": "as needed",
    "bid": "twice a day",
    "tid": "three times a day",
    "qid": "four times a day",
    "qd": "once a day",
    "qhs": "at bedtime",
    "stat": "immediately",
}

_WARNING_KEYWORDS = [
    "emergency", "call 911", "seek immediate", "go to er", "go to the er",
    "return immediately", "warning", "danger", "urgent", "do not",
    "avoid", "stop taking",
]

_FOLLOWUP_PATTERN = re.compile(
    r'(?:follow\s*up|follow-up|return|see|visit|appointment).*?'
    r'(\d+\s*(?:day|week|month)s?)',
    re.IGNORECASE,
)


def _build_plain_language(text: str, entities: list) -> str:
    """Replace medical terms with plain language equivalents."""
    result = text
    # Sort by length descending so longer phrases match first
    sorted_terms = sorted(MEDICAL_TO_PLAIN.keys(), key=len, reverse=True)
    for term in sorted_terms:
        plain = MEDICAL_TO_PLAIN[term]
        result = re.sub(re.escape(term), f"{term} ({plain})", result, flags=re.IGNORECASE)
    return result


def _extract_warnings(text: str) -> list[str]:
    """Extract warning statements from discharge text."""
    warnings: list[str] = []
    seen: set[str] = set()
    # Split on both periods and newlines to handle prose and structured formats
    segments = re.split(r'[.\n]', text)
    for segment in segments:
        segment_stripped = segment.strip()
        if not segment_stripped or len(segment_stripped) > 300:
            continue
        segment_lower = segment_stripped.lower()
        for keyword in _WARNING_KEYWORDS:
            if keyword in segment_lower:
                if segment_stripped not in seen:
                    warnings.append(segment_stripped)
                    seen.add(segment_stripped)
                break
    return warnings


def _extract_followup(text: str) -> list[str]:
    """Extract follow-up instructions."""
    matches = _FOLLOWUP_PATTERN.findall(text)
    if matches:
        return [f"Follow-up in {m}" for m in matches]
    return ["Check with your doctor about when to schedule a follow-up visit."]


def translate_discharge(engine: HealthEngine, text: str, lang: str = "en") -> dict:
    """Translate discharge instructions into plain language."""
    if not text or not text.strip():
        return {
            "plain_language": "",
            "medications": [],
            "follow_up": [],
            "warnings": [],
            "entities_explained": [],
        }

    diseases = engine.extract_diseases(text, confidence=0.5)
    drugs = engine.extract_drugs(text, confidence=0.5)
    anatomy = engine.extract_anatomy(text, confidence=0.5)

    errors = [r.error for r in (diseases, drugs, anatomy) if r.error]
    if errors and not any((diseases.entities, drugs.entities, anatomy.entities)):
        return {
            "plain_language": "",
            "medications": [],
            "follow_up": [],
            "warnings": [],
            "entities_explained": [],
            "error": "; ".join(errors),
        }

    # Build plain language version
    plain = _build_plain_language(text, diseases.entities + drugs.entities + anatomy.entities)

    # Extract structured information
    medications = [{"name": e.text, "label": e.label} for e in drugs.entities]
    follow_up = _extract_followup(text)
    warnings = _extract_warnings(text)

    # Explain detected entities
    entities_explained = []
    for e in diseases.entities:
        plain_name = MEDICAL_TO_PLAIN.get(e.text.lower(), "a medical condition")
        entities_explained.append({"term": e.text, "explanation": plain_name})
    for e in drugs.entities:
        entities_explained.append({"term": e.text, "explanation": "a medication"})
    for e in anatomy.entities:
        entities_explained.append({"term": e.text, "explanation": "a body part"})

    return {
        "plain_language": plain,
        "medications": medications,
        "follow_up": follow_up,
        "warnings": warnings,
        "entities_explained": entities_explained,
    }
