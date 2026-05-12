"""Appointment preparation — generate talking points and advocacy scripts."""

from __future__ import annotations

from .engine import HealthEngine

_CONDITION_QUESTIONS: dict[str, list[str]] = {
    "diabetes": [
        "What is my current A1C level and what should my target be?",
        "Should I be monitoring my blood sugar at home? How often?",
        "What dietary changes would help manage my condition?",
        "Are there any complications I should be watching for?",
    ],
    "hypertension": [
        "What is my current blood pressure reading?",
        "What lifestyle changes can help lower my blood pressure?",
        "Do I need medication, or can we try lifestyle changes first?",
        "How often should I have my blood pressure checked?",
    ],
    "cancer": [
        "What stage is my condition and what does that mean?",
        "What are all my treatment options?",
        "What are the side effects of each treatment?",
        "Should I get a second opinion?",
        "Are there any clinical trials I should consider?",
    ],
    "asthma": [
        "What are my triggers and how can I avoid them?",
        "Do I need a rescue inhaler and a maintenance inhaler?",
        "When should I go to the emergency room for breathing difficulty?",
        "Should I have an asthma action plan?",
    ],
    "depression": [
        "What treatment options are available (therapy, medication, or both)?",
        "How long before I should expect to feel better?",
        "What side effects should I watch for with medication?",
        "Are there lifestyle changes that could help?",
    ],
    "anxiety": [
        "Could my anxiety be related to a physical condition?",
        "What treatment approach do you recommend?",
        "Should I see a therapist in addition to medication?",
        "Are there techniques I can use to manage anxiety attacks?",
    ],
    "arthritis": [
        "What type of arthritis do I have?",
        "What can I do to protect my joints?",
        "Should I see a physical therapist?",
        "What pain management options are available besides medication?",
    ],
}

_SYMPTOM_QUESTIONS: dict[str, str] = {
    "pain": "Where exactly is the pain, and how would you rate it on a scale of 1-10?",
    "fever": "How high has my fever been and how long has it lasted?",
    "fatigue": "Could my fatigue be related to a medical condition or medication?",
    "rash": "Could this rash be a reaction to a medication?",
    "headache": "Should I be concerned about these headaches? What tests are needed?",
    "dizziness": "What could be causing my dizziness? Should I be worried about falls?",
    "swelling": "What is causing this swelling? Should I be concerned about fluid retention?",
    "cough": "How long has this cough lasted? Do I need a chest X-ray?",
    "nausea": "Could my nausea be related to a medication I'm taking?",
}


def prepare_appointment(engine: HealthEngine, symptoms: str, concern: str = "") -> dict:
    """Generate pre-appointment talking points, questions, and advocacy script."""
    combined_text = f"{symptoms} {concern}".strip()
    if not combined_text:
        return {
            "talking_points": [],
            "conditions_to_mention": [],
            "questions_to_ask": [],
            "medications_to_list": [],
            "advocacy_script": "Please provide your symptoms or concerns to generate preparation materials.",
        }

    diseases = engine.extract_diseases(combined_text, confidence=0.5)
    drugs = engine.extract_drugs(combined_text, confidence=0.5)
    anatomy = engine.extract_anatomy(combined_text, confidence=0.5)

    errors = [r.error for r in (diseases, drugs, anatomy) if r.error]
    if errors and not any((diseases.entities, drugs.entities, anatomy.entities)):
        return {
            "talking_points": [],
            "conditions_to_mention": [],
            "questions_to_ask": ["What do you think is causing my symptoms?"],
            "medications_to_list": [],
            "advocacy_script": "Unable to analyze your symptoms. Please describe your concerns directly to your doctor.",
            "error": "; ".join(errors),
        }

    conditions_to_mention = [{"text": e.text, "label": e.label} for e in diseases.entities]
    medications_to_list = [{"text": e.text, "label": e.label} for e in drugs.entities]
    anatomy_mentioned = [{"text": e.text, "label": e.label} for e in anatomy.entities]

    # Build talking points
    talking_points = []
    if symptoms.strip():
        talking_points.append(f"Primary concern: {symptoms.strip()}")
    if concern.strip():
        talking_points.append(f"Specific question/worry: {concern.strip()}")
    if conditions_to_mention:
        names = ", ".join(c["text"] for c in conditions_to_mention)
        talking_points.append(f"Conditions to discuss: {names}")
    if medications_to_list:
        names = ", ".join(m["text"] for m in medications_to_list)
        talking_points.append(f"Current medications to review: {names}")

    # Build questions
    questions_to_ask = []
    for cond in conditions_to_mention:
        cond_lower = cond["text"].lower()
        for key, qs in _CONDITION_QUESTIONS.items():
            if key in cond_lower:
                questions_to_ask.extend(qs)
                break

    if not questions_to_ask:
        questions_to_ask = [
            "What do you think is causing my symptoms?",
            "What tests or evaluations do you recommend?",
            "What are my treatment options?",
            "When should I follow up?",
        ]

    # Add symptom-specific questions
    symptoms_lower = combined_text.lower()
    for keyword, question in _SYMPTOM_QUESTIONS.items():
        if keyword in symptoms_lower and question not in questions_to_ask:
            questions_to_ask.append(question)

    # Build advocacy script
    script_parts = [
        "ADVOCACY SCRIPT FOR YOUR APPOINTMENT:",
        "",
    ]
    if talking_points:
        script_parts.append("BEFORE YOU GO IN — Know what you want to say:")
        for i, point in enumerate(talking_points, 1):
            script_parts.append(f"  {i}. {point}")
        script_parts.append("")

    if questions_to_ask:
        script_parts.append("DURING THE VISIT — Ask these questions:")
        for i, q in enumerate(questions_to_ask[:8], 1):
            script_parts.append(f"  {i}. {q}")
        script_parts.append("")

    script_parts.append("BEFORE YOU LEAVE — Make sure you know:")
    script_parts.append("  - What the next steps are (tests, referrals, prescriptions)")
    script_parts.append("  - When to follow up")
    script_parts.append("  - What warning signs should bring you back sooner")
    script_parts.append("  - How to reach the office if you have questions later")

    return {
        "talking_points": talking_points,
        "conditions_to_mention": conditions_to_mention,
        "questions_to_ask": questions_to_ask,
        "medications_to_list": medications_to_list,
        "anatomy_mentioned": anatomy_mentioned,
        "advocacy_script": "\n".join(script_parts),
    }
