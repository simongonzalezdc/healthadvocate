"""Insurance denial fighter — analyze denials and generate appeal letters."""

from __future__ import annotations

from .engine import HealthEngine

APPEAL_TEMPLATE = """Dear Insurance Appeals Board,

I am writing to formally appeal the denial of coverage for the treatment(s) and/or procedure(s) listed below.

DENIAL SUMMARY:
{denial_summary}

MEDICAL CONDITIONS IDENTIFIED IN THE DENIAL:
{conditions_list}

MEDICATIONS/TREATMENTS MENTIONED:
{medications_list}

ARGUMENTS FOR APPEAL:
{key_arguments}

Based on the medical evidence documented above, I respectfully request a thorough
review of this denial. The identified conditions support the medical necessity of
the proposed treatment(s).

I am prepared to provide additional documentation, including letters of medical
necessity from my treating physician, relevant medical records, and peer-reviewed
literature supporting the prescribed course of treatment.

Please confirm receipt of this appeal and provide the timeline for review.

Sincerely,
[Patient Name]
[Date: {date}]
[Claim/Reference Number: ___________]"""

_DENIAL_REASON_KEYWORDS = {
    "not medically necessary": "medical_necessity",
    "experimental": "experimental",
    "investigational": "experimental",
    "pre-existing": "preexisting",
    "prior authorization": "prior_auth",
    "out of network": "out_of_network",
    "not covered": "exclusion",
    "cosmetic": "cosmetic",
    "lifetime maximum": "lifetime_max",
    "expired": "timely_filing",
}

_ARGUMENT_TEMPLATES = {
    "medical_necessity": "The treatment is medically necessary as documented by the treating physician for the management of {condition}. Denial of this treatment may result in worsening of the condition and increased healthcare costs.",
    "experimental": "The treatment in question is not experimental. It is an established, evidence-based treatment for {condition} recognized by major medical organizations.",
    "preexisting": "The denial based on pre-existing condition status may be in violation of current patient protection regulations. The condition requires ongoing management regardless of when it was first diagnosed.",
    "prior_auth": "If prior authorization was not obtained, I request that the plan consider a retrospective authorization based on the urgent medical circumstances documented by my physician.",
    "out_of_network": "The out-of-network provider was necessary because no in-network providers were available with the required specialization for {condition}. I request an in-network exception.",
    "exclusion": "The treatment for {condition} should be covered under the plan benefits. I request a detailed explanation of the specific exclusion being applied.",
    "cosmetic": "The treatment is medically indicated for {condition}, not cosmetic. The medical necessity has been documented by the treating physician.",
    "lifetime_max": "I request a review of the lifetime maximum calculation and a detailed accounting of how the maximum was reached.",
    "timely_filing": "Any filing delay was due to circumstances beyond my control. I request a waiver of the timely filing requirement.",
}

_DEFAULT_ARGUMENT = "The documented presence of {condition} medically justifies the prescribed treatment. I request that the full clinical context be considered in this appeal."


def _identify_denial_reason(text: str) -> tuple[str, str]:
    """Identify the type of denial reason from the text."""
    text_lower = text.lower()
    for keyword, reason_type in _DENIAL_REASON_KEYWORDS.items():
        if keyword in text_lower:
            return reason_type, keyword
    return "unspecified", "unknown"


def fight_denial(engine: HealthEngine, denial_text: str, patient_info: str = "") -> dict:
    """Analyze an insurance denial and generate an appeal letter."""
    if not denial_text or not denial_text.strip():
        return {
            "denial_reason": "No denial text provided.",
            "denial_type": "unknown",
            "entities_found": {"conditions": [], "medications": []},
            "key_arguments": [],
            "appeal_letter": "",
        }

    diseases = engine.extract_diseases(denial_text, confidence=0.5)
    drugs = engine.extract_drugs(denial_text, confidence=0.5)

    # Also analyze patient_info if provided
    if patient_info and patient_info.strip():
        pi_diseases = engine.extract_diseases(patient_info, confidence=0.5)
        pi_drugs = engine.extract_drugs(patient_info, confidence=0.5)
        diseases.entities.extend(pi_diseases.entities)
        drugs.entities.extend(pi_drugs.entities)

    conditions = [{"text": e.text, "label": e.label, "confidence": round(e.confidence, 2)} for e in diseases.entities]
    medications = [{"text": e.text, "label": e.label, "confidence": round(e.confidence, 2)} for e in drugs.entities]

    denial_type, denial_keyword = _identify_denial_reason(denial_text)
    denial_reason = f"The denial appears to be based on: {denial_keyword} (category: {denial_type})"

    # Build key arguments
    key_arguments = []
    argument_template = _ARGUMENT_TEMPLATES.get(denial_type, _DEFAULT_ARGUMENT)

    if conditions:
        for cond in conditions[:5]:
            arg = argument_template.format(condition=cond["text"])
            if arg not in key_arguments:
                key_arguments.append(arg)
    else:
        key_arguments.append("I believe this denial is incorrect and request a full review of the medical evidence.")

    # Generate appeal letter
    from datetime import date
    conditions_list = "\n".join(f"  - {c['text']} ({c['label']})" for c in conditions) or "  (None specifically identified)"
    medications_list = "\n".join(f"  - {m['text']} ({m['label']})" for m in medications) or "  (None specifically identified)"
    arguments_text = "\n".join(f"  {i+1}. {arg}" for i, arg in enumerate(key_arguments))

    appeal_letter = APPEAL_TEMPLATE.format(
        denial_summary=denial_text[:500].strip(),
        conditions_list=conditions_list,
        medications_list=medications_list,
        key_arguments=arguments_text,
        date=date.today().isoformat(),
    )

    if patient_info and patient_info.strip():
        appeal_letter = appeal_letter.replace(
            "ARGUMENTS FOR APPEAL:",
            f"PATIENT CONTEXT:\n  {patient_info.strip()[:400]}\n\nARGUMENTS FOR APPEAL:",
        )

    return {
        "denial_reason": denial_reason,
        "denial_type": denial_type,
        "entities_found": {
            "conditions": conditions,
            "medications": medications,
        },
        "key_arguments": key_arguments,
        "appeal_letter": appeal_letter,
        "processing_time": {
            "diseases": diseases.processing_time,
            "drugs": drugs.processing_time,
        },
    }
