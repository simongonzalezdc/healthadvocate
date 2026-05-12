"""Community health scanner — analyze public health bulletins and alerts."""

from __future__ import annotations

from .engine import HealthEngine

_ALERT_KEYWORDS = {
    "outbreak", "epidemic", "pandemic", "recall", "warning", "alert",
    "emergency", "contamination", "infection", "exposure", "hazardous",
    "toxic", "poisoning", "contagious", "quarantine", "isolat",
}


def _get_context(text: str, start: int, end: int, window: int = 40) -> str:
    """Extract text around an entity with context window."""
    ctx_start = max(0, start - window)
    ctx_end = min(len(text), end + window)
    prefix = "..." if ctx_start > 0 else ""
    suffix = "..." if ctx_end < len(text) else ""
    return f"{prefix}{text[ctx_start:ctx_end]}{suffix}"


def _detect_alerts(text: str) -> list[str]:
    """Detect health alert signals in the text."""
    text_lower = text.lower()
    alerts: list[str] = []
    seen: set[str] = set()
    for keyword in _ALERT_KEYWORDS:
        if keyword in text_lower:
            for sentence in text.replace('\n', '.').split('.'):
                if keyword in sentence.lower() and sentence.strip():
                    cleaned = sentence.strip()
                    if cleaned not in seen:
                        alerts.append(cleaned)
                        seen.add(cleaned)
                    break
    return alerts


def scan_bulletin(engine: HealthEngine, text: str) -> dict:
    """Analyze a health bulletin or alert for conditions, treatments, and warnings."""
    if not text or not text.strip():
        return {
            "findings": [],
            "health_alerts": [],
            "affected_conditions": [],
            "mentioned_treatments": [],
        }

    diseases = engine.extract_diseases(text, confidence=0.5)
    drugs = engine.extract_drugs(text, confidence=0.5)

    errors = [r.error for r in (diseases, drugs) if r.error]
    if errors and not any((diseases.entities, drugs.entities)):
        return {
            "findings": [],
            "health_alerts": [],
            "affected_conditions": [],
            "mentioned_treatments": [],
            "error": "; ".join(errors),
        }

    # Build findings with context
    findings = []
    for entity in diseases.entities:
        findings.append({
            "entity": entity.text,
            "type": "condition",
            "label": entity.label,
            "confidence": round(entity.confidence, 2),
            "context": _get_context(text, entity.start, entity.end),
        })
    for entity in drugs.entities:
        findings.append({
            "entity": entity.text,
            "type": "treatment",
            "label": entity.label,
            "confidence": round(entity.confidence, 2),
            "context": _get_context(text, entity.start, entity.end),
        })

    # Detect health alerts
    health_alerts = _detect_alerts(text)

    affected_conditions = [{"name": e.text, "label": e.label} for e in diseases.entities]
    mentioned_treatments = [{"name": e.text, "label": e.label} for e in drugs.entities]

    return {
        "findings": findings,
        "health_alerts": health_alerts,
        "affected_conditions": affected_conditions,
        "mentioned_treatments": mentioned_treatments,
    }
