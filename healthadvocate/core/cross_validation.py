"""Cross-validation between NER entities and LLM structured output."""

from __future__ import annotations

from dataclasses import dataclass, field

from .engine import EntityMatch


@dataclass
class ValidationResult:
    confirmed: list[str] = field(default_factory=list)
    ner_only: list[str] = field(default_factory=list)
    llm_only: list[str] = field(default_factory=list)
    reliability: str = "high"
    urgency_disagreement: bool = False


_HIGH_URGENCY_TERMS = {
    "chest pain", "shortness of breath", "difficulty breathing", "can't breathe",
    "unconscious", "severe bleeding", "stroke", "heart attack", "seizure",
    "overdose", "suicidal", "suicide", "anaphylaxis",
}

#: Placeholder markers in the gated model output: when one of these is
#: set, the output's "urgency" value is the pipeline's own fallback
#: (unavailable_structured_fallback and the unparseable path both
#: hardcode "medium" in llm_client) — NOT a rating. Consulting it would
#: suppress the safety override on the model-off default build, where
#: the NER trigger is the only urgency signal there is (audit D2
#: round 2, 2026-09-24).
_PLACEHOLDER_URGENCY_MARKERS = ("_model_blocked", "_raw_text")

# Fields where we expect entity names to appear
_ENTITY_FIELDS = {
    "summary", "red_flags", "action_items", "possible_conditions",
    "denial_reason", "appeal_arguments", "treatment_concerns",
    "key_questions", "scientific_context", "recommended_action",
    "medication_instructions", "warning_signs", "talking_points",
    "questions_to_ask", "doctor_questions", "common_side_effects",
    "warnings", "suspicious_charges", "billing_rights",
}


def _extract_llm_entity_texts(llm_output: dict) -> set[str]:
    """Extract meaningful entity-like strings from LLM output key fields."""
    texts: set[str] = set()
    for key, value in llm_output.items():
        if key.startswith("_") or key not in _ENTITY_FIELDS:
            continue
        if isinstance(value, str):
            texts.add(value.lower().strip())
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, str):
                    texts.add(item.lower().strip())
                elif isinstance(item, dict):
                    for v in item.values():
                        if isinstance(v, str):
                            texts.add(v.lower().strip())
    return texts


def _match_entities(ner_texts: set[str], llm_texts: set[str]) -> tuple[set[str], set[str], set[str]]:
    """Match NER entities against LLM texts using substring matching."""
    confirmed: set[str] = set()
    for ner in ner_texts:
        for llm in llm_texts:
            if ner in llm or llm in ner:
                confirmed.add(ner)
                break
    ner_only = ner_texts - confirmed
    llm_only = llm_texts - {llm for llm in llm_texts for n in confirmed if n in llm or llm in n}
    return confirmed, ner_only, llm_only


def ner_high_urgency_present(
    ner_entities: list[EntityMatch],
    high_urgency_terms: set[str] | None = None,
) -> bool:
    """The NER high-urgency trigger: a high-urgency term detected at or
    above 0.80 confidence. This deterministic signal must be able to
    escalate to HIGH regardless of what the optional model said — or
    whether it said anything at all (audit D2 round 2)."""
    urgency_terms = high_urgency_terms or _HIGH_URGENCY_TERMS
    return any(
        e.text.lower().strip() in urgency_terms and e.confidence >= 0.80
        for e in ner_entities
    )


def cross_validate(
    ner_entities: list[EntityMatch],
    llm_output: dict,
    high_urgency_terms: set[str] | None = None,
) -> ValidationResult:
    ner_texts = {e.text.lower().strip() for e in ner_entities}
    llm_texts = _extract_llm_entity_texts(llm_output)

    if not ner_texts and not llm_texts:
        return ValidationResult(reliability="high")

    confirmed_set, ner_only_set, llm_only_set = _match_entities(ner_texts, llm_texts)

    # Reliability based on overlap ratio
    all_entities = ner_texts | llm_texts
    if not all_entities:
        reliability = "high"
    else:
        ratio = len(confirmed_set) / len(all_entities)
        if ratio >= 0.7:
            reliability = "high"
        elif ratio >= 0.3:
            reliability = "medium"
        else:
            reliability = "low"

    # Urgency disagreement: the NER high-urgency trigger fired and the
    # LLM's GENUINE judgment does not carry it — the LLM rates urgency
    # "low", or made no urgency rating at all (placeholder output: the
    # model was blocked/unavailable or its answer was unparseable — the
    # placeholder "medium" is never a rating, so consulting it would
    # suppress the override on the model-off default build).
    urgency_terms = high_urgency_terms or _HIGH_URGENCY_TERMS
    llm_urgency = llm_output.get("urgency", "medium")
    llm_urgency_is_placeholder = any(
        llm_output.get(marker) for marker in _PLACEHOLDER_URGENCY_MARKERS
    )
    urgency_disagreement = (
        llm_urgency == "low" or llm_urgency_is_placeholder
    ) and ner_high_urgency_present(ner_entities, urgency_terms)

    return ValidationResult(
        confirmed=sorted(confirmed_set),
        ner_only=sorted(ner_only_set),
        llm_only=sorted(llm_only_set),
        reliability=reliability,
        urgency_disagreement=urgency_disagreement,
    )
