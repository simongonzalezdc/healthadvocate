"""Symptom assessment — identify conditions and determine urgency."""

from __future__ import annotations

from .engine import HealthEngine

# Urgency keyword sets
_HIGH_URGENCY = {
    "chest pain", "shortness of breath", "difficulty breathing", "can't breathe",
    "breathing", "unconscious", "unresponsive", "severe bleeding", "blood",
    "stroke", "heart attack", "seizure", "overdose", "suicidal", "suicide",
    "choking", "drowning", "severe burn", "head injury", "loss of consciousness",
    "paralysis", "numbness", "slurred speech", "face drooping",
}
_MEDIUM_URGENCY = {
    "fever", "pain", "swelling", "rash", "cough", "vomiting", "diarrhea",
    "headache", "dizziness", "nausea", "fatigue", "infection", "sore throat",
    "congestion", "body ache", "chills", "sweating", "insomnia",
    "anxiety", "depression", "mood",
}

_URGENCY_NOTES = {
    "high": "These symptoms may indicate a serious condition. Please seek medical attention immediately.",
    "medium": "These symptoms warrant a medical evaluation. Consider scheduling an appointment soon.",
    "low": "These symptoms are manageable but worth monitoring. Schedule a check-up if they persist.",
}

# Condition-specific recommendation templates
_CONDITION_RECOMMENDATIONS = {
    "diabetes": "Monitor blood sugar levels regularly and discuss management options with your doctor.",
    "hypertension": "Monitor your blood pressure at home and reduce sodium intake.",
    "cancer": "Ask your doctor about staging, treatment options, and second opinions.",
    "asthma": "Keep rescue inhalers accessible and identify your triggers.",
    "copd": "Discuss pulmonary rehabilitation and smoking cessation if applicable.",
    "pneumonia": "Complete the full course of any prescribed antibiotics.",
    "arthritis": "Ask about anti-inflammatory options and physical therapy.",
    "depression": "Consider speaking with a mental health professional about therapy and medication options.",
    "anxiety": "Explore stress management techniques and discuss treatment with your provider.",
}


def _determine_urgency(text: str, conditions: list) -> str:
    """Determine urgency level from symptom text and detected conditions."""
    text_lower = text.lower()

    for keyword in _HIGH_URGENCY:
        if keyword in text_lower:
            return "high"

    high_condition_keywords = {"cancer", "stroke", "heart attack", "seizure", "overdose"}
    for cond in conditions:
        for kw in high_condition_keywords:
            if kw in cond.get("name", "").lower():
                return "high"

    for keyword in _MEDIUM_URGENCY:
        if keyword in text_lower:
            return "medium"

    if conditions:
        return "medium"

    return "low"


def _get_recommendation(condition_name: str) -> str:
    name_lower = condition_name.lower()
    for key, rec in _CONDITION_RECOMMENDATIONS.items():
        if key in name_lower:
            return rec
    return f"Discuss your {condition_name} with a healthcare provider for personalized guidance."


def assess_symptoms(engine: HealthEngine, symptoms: str) -> dict:
    """Assess symptoms and return conditions, urgency, and recommendations."""
    if not symptoms or not symptoms.strip():
        return {
            "conditions": [],
            "urgency": "low",
            "explanation": "No symptoms provided.",
            "recommendations": [],
        }

    result = engine.extract_diseases(symptoms)

    if result.error:
        return {
            "conditions": [],
            "urgency": "unknown",
            "explanation": f"Unable to analyze symptoms: {result.error}",
            "recommendations": ["Please try again or consult a healthcare provider directly."],
            "model_used": result.model_used,
            "processing_time": result.processing_time,
            "error": result.error,
        }

    conditions = []
    for entity in result.entities:
        conditions.append({
            "name": entity.text,
            "confidence": round(entity.confidence, 2),
            "label": entity.label,
        })

    urgency = _determine_urgency(symptoms, conditions)

    if conditions:
        condition_names = ", ".join(c["name"] for c in conditions)
        explanation = (
            f"Based on your symptoms, we identified the following condition(s): {condition_names}. "
            f"{_URGENCY_NOTES[urgency]}"
        )
    else:
        explanation = (
            "No specific conditions were detected from your description. "
            "Consider providing more detail about your symptoms. "
            f"{_URGENCY_NOTES[urgency]}"
        )

    recommendations = []
    seen = set()
    for cond in conditions:
        name = cond["name"]
        if name.lower() not in seen:
            recommendations.append(_get_recommendation(name))
            seen.add(name.lower())

    if not recommendations:
        recommendations.append(
            "Keep a symptom diary noting when symptoms occur, their severity, and any triggers."
        )

    return {
        "conditions": conditions,
        "urgency": urgency,
        "explanation": explanation,
        "recommendations": recommendations,
        "model_used": result.model_used,
        "processing_time": result.processing_time,
    }
