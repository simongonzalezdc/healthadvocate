"""Appeal letter generator (F1a, 2026-09-24) — structured case file + letter.

Honesty contract (brief D119):
- The case file is assembled DETERMINISTICALLY from text the user provided:
  denial reason (canonical alias match, fail-closed on ambiguity), dates,
  dollar amounts, and verbatim plan-language quotes. Every case-file field
  carries the source it was extracted from, and every claim in the letter
  must trace back to one of those fields.
- The letter itself is drafted by the LOCAL champion lane through the
  existing gated client (``structured_model_call`` — deidentify first,
  loopback-only endpoint policy, no new network dependency).
- Model-off path: a letter skeleton assembled ONLY from the user-provided
  case-file facts. Sections without source data are dropped, never
  invented, and the response says the model did not draft it.
- Nothing leaves the device except through the loopback model lane; the
  download/write of the letter is a user action client-side.
"""

from __future__ import annotations

import re
from datetime import date

from .engine import HealthEngine
from healthadvocate.privacy.gated_model import structured_model_call

#: Reuse the canonical denial-reason alias table so the appeal letter and
#: the denial fighter can never disagree about vocabulary. Import the
#: module (not the private symbol alone) so tests can pin the reuse.
from . import insurance_fighter as _fighter

_DENIAL_REASON_ALIASES = _fighter._DENIAL_REASON_ALIASES  # noqa: SLF001 — same package, pinned by tests
_DENIAL_REASON_OPTIONS = _fighter.DENIAL_REASON_OPTIONS

_SOURCE_DENIAL = "denial letter"
_SOURCE_RECORD = "related record"
_SOURCE_WORDS = "your words"

# ---------------------------------------------------------------------------
# Deterministic extraction
# ---------------------------------------------------------------------------

_MONTHS = (
    "January|February|March|April|May|June|July|August|September|October|"
    "November|December|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec"
)

_DATE_PATTERNS = (
    # 2026-09-08
    r"\b\d{4}-\d{2}-\d{2}\b",
    # September 8, 2026 / Sep 8 / September 8th
    rf"\b(?:{_MONTHS})\.?\s+\d{{1,2}}(?:st|nd|rd|th)?(?:,?\s+\d{{4}})?\b",
    # 8 September 2026
    rf"\b\d{{1,2}}(?:st|nd|rd|th)?\s+(?:{_MONTHS})\.?(?:,?\s+\d{{4}})?\b",
    # 09/08/2026 · 9/8/26
    r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
)

_AMOUNT_RE = re.compile(r"\$\s?\d[\d,]*(?:\.\d+)?")

_PLAN_LANGUAGE_HINTS = (
    "plan", "coverage", "covered", "denial", "denied", "appeal",
    "medically necessary", "medical necessity", "formulary", "network",
    "authorization", "benefit", "exclusion", "investigational",
    "experimental", "policy",
)


def extract_dates(text: str) -> list[str]:
    """Deterministic date extraction; ordered by first appearance."""
    found: list[str] = []
    for pattern in _DATE_PATTERNS:
        for m in re.finditer(pattern, text, re.IGNORECASE):
            if m.group(0) not in found:
                found.append(m.group(0))
    return found[:8]


def extract_amounts(text: str) -> list[str]:
    """Deterministic dollar-amount extraction; ordered by first appearance."""
    found: list[str] = []
    for m in _AMOUNT_RE.finditer(text):
        if m.group(0) not in found:
            found.append(m.group(0))
    return found[:8]


def classify_reason(text: str) -> str | None:
    """Deterministic canonical denial-reason match over the user's text.

    Same fail-closed rule as the fighter: zero matches or matches for
    several canonical options return None (a human decides, the machine
    does not guess).
    """
    if not text:
        return None
    lowered = text.lower()
    matched = {
        option
        for option in _DENIAL_REASON_OPTIONS
        if any(alias in lowered for alias in _DENIAL_REASON_ALIASES[option])
    }
    if len(matched) == 1:
        return matched.pop()
    return None


def extract_plan_language(text: str, limit: int = 4) -> list[str]:
    """Verbatim sentences from the letter that state plan positions."""
    if not text:
        return []
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    picked: list[str] = []
    for sentence in sentences:
        lowered = sentence.lower()
        if any(hint in lowered for hint in _PLAN_LANGUAGE_HINTS):
            picked.append(sentence)
        if len(picked) >= limit:
            break
    return picked


def extract_record_quotes(text: str, limit: int = 3) -> list[str]:
    """Verbatim quotes from the related record: plan-relevant sentences
    first; when none match, the leading sentences (the record is
    user-supplied, so quoting it verbatim is always honest)."""
    if not text:
        return []
    picked = extract_plan_language(text, limit=limit)
    if not picked:
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
        picked = sentences[:limit]
    return picked


def build_case_file(
    denial_text: str,
    record_text: str = "",
    user_words: str = "",
) -> dict:
    """Assemble the structured, source-cited case file deterministically."""
    denial_text = (denial_text or "").strip()
    record_text = (record_text or "").strip()
    user_words = (user_words or "").strip()

    reason = classify_reason(denial_text)
    reason_source = _SOURCE_DENIAL if reason else ""
    if reason is None:
        reason = classify_reason(record_text)
        reason_source = _SOURCE_RECORD if reason else ""
    denial_dates = extract_dates(denial_text)
    record_dates = [d for d in extract_dates(record_text) if d not in denial_dates]
    denial_amounts = extract_amounts(denial_text)
    record_amounts = [a for a in extract_amounts(record_text) if a not in denial_amounts]
    plan_language = extract_plan_language(denial_text)
    record_quotes = extract_record_quotes(record_text, limit=3)

    return {
        "denial_reason": {
            "value": reason or "",
            "source": reason_source,
            "needs_human": reason is None,
        },
        "dates": [{"value": d, "source": _SOURCE_DENIAL} for d in denial_dates]
        + [{"value": d, "source": _SOURCE_RECORD} for d in record_dates],
        "amounts": [{"value": a, "source": _SOURCE_DENIAL} for a in denial_amounts]
        + [{"value": a, "source": _SOURCE_RECORD} for a in record_amounts],
        "plan_language": [
            {"value": q, "source": _SOURCE_DENIAL} for q in plan_language
        ],
        "record_quotes": [
            {"value": q, "source": _SOURCE_RECORD} for q in record_quotes
        ],
        "user_words": {
            "value": user_words,
            "source": _SOURCE_WORDS if user_words else "",
        },
    }


def _case_file_citations(case_file: dict) -> list[dict]:
    """Flatten the case file into a citation list (what fed the letter)."""
    citations: list[dict] = []
    if case_file["denial_reason"]["value"]:
        citations.append({
            "fact": f"denial reason: {case_file['denial_reason']['value']}",
            "source": case_file["denial_reason"]["source"],
        })
    for item in case_file["dates"]:
        citations.append({"fact": f"date: {item['value']}", "source": item["source"]})
    for item in case_file["amounts"]:
        citations.append({"fact": f"amount: {item['value']}", "source": item["source"]})
    for item in case_file["plan_language"]:
        citations.append({
            "fact": f"plan language, quoted: “{item['value'][:120]}”",
            "source": item["source"],
        })
    for item in case_file["record_quotes"]:
        citations.append({
            "fact": f"record, quoted: “{item['value'][:120]}”",
            "source": item["source"],
        })
    if case_file["user_words"]["value"]:
        citations.append({"fact": "the user's own words", "source": _SOURCE_WORDS})
    return citations


def _deterministic_letter(case_file: dict) -> str:
    """Model-off skeleton: ONLY user-provided facts, in a professional frame.

    Every sentence that states a fact is either a verbatim quote or a
    case-file value; sections without data are dropped, never invented.
    """
    reason = case_file["denial_reason"]["value"]
    dates = [d["value"] for d in case_file["dates"]]
    amounts = [a["value"] for a in case_file["amounts"]]
    quotes = [q["value"] for q in case_file["plan_language"]]
    record_quotes = [q["value"] for q in case_file["record_quotes"]]
    user_words = case_file["user_words"]["value"]

    lines: list[str] = []
    subject_bits = []
    if reason:
        subject_bits.append(f"denied as “{reason}”")
    if dates:
        subject_bits.append(f"dated {dates[0]}")
    lines.append("Subject: Formal appeal — " + ", ".join(subject_bits) if subject_bits
                 else "Subject: Formal appeal of a denied claim")
    lines.append("")
    lines.append("To the Appeals Department:")
    lines.append("")
    lines.append("I am writing to formally appeal the denial described in your letter."
                 " Please treat this as a request for a full review of the determination.")
    lines.append("")

    section = 1
    if reason:
        lines.append(f"{section}. Reason given for the denial. The letter states the service was "
                     f"denied as “{reason}”.")
        section += 1
    if quotes:
        lines.append(f"{section}. The denial letter says, verbatim:")
        for q in quotes:
            lines.append(f"    “{q}”")
        section += 1
    if amounts:
        lines.append(f"{section}. Amounts at issue in this matter: "
                     + ", ".join(amounts) + ".")
        section += 1
    if dates:
        lines.append(f"{section}. Dates relevant to this appeal (as they appear in the documents): "
                     + ", ".join(dates) + ".")
        section += 1
    if record_quotes:
        lines.append(f"{section}. Supporting record. The related record states, verbatim:")
        for q in record_quotes:
            lines.append(f"    “{q}”")
        section += 1
    if user_words:
        lines.append(f"{section}. In my own words:")
        lines.append(f"    {user_words}")
        section += 1

    lines.append("")
    lines.append("I ask that you reconsider this determination, review the full record, "
                 "and respond in writing within the timeframe required by the plan and "
                 "applicable law. Please confirm in writing that this appeal was received.")
    lines.append("")
    lines.append("Sincerely,")
    lines.append("[Your name]")
    lines.append("[Member ID]")
    lines.append("[Claim or reference number]")
    return "\n".join(lines)


_MODEL_OFF_NOTE = (
    "The optional local model is off, so this letter was assembled on this "
    "device from the facts you provided — every line traces to your own "
    "documents. Review and edit it before sending."
)


def generate_appeal_letter(
    engine: HealthEngine,
    denial_text: str,
    record_text: str = "",
    user_words: str = "",
    profile_id: str | None = None,
) -> dict:
    """Build the case file, then draft the letter via the champion lane."""
    denial_text = (denial_text or "").strip()
    record_text = (record_text or "").strip()
    user_words = (user_words or "").strip()

    if not denial_text:
        return {
            "letter": "",
            "case_file": build_case_file(""),
            "citations": [],
            "model_generated": False,
            "note": "No denial text provided.",
            "needs_human": True,
            "structured_output": None,
        }

    case_file = build_case_file(denial_text, record_text, user_words)

    facts = {
        "denial_reason": case_file["denial_reason"]["value"] or "not stated in the letter",
        "dates": [d["value"] for d in case_file["dates"]],
        "amounts": [a["value"] for a in case_file["amounts"]],
        "plan_language": [q["value"] for q in case_file["plan_language"]],
        "record_quotes": [q["value"] for q in case_file["record_quotes"]],
        "user_words": user_words,
    }

    system = (
        "You are a patient health advocate drafting an insurance appeal letter. "
        "Use ONLY the facts in the case file — never invent dates, amounts, "
        "diagnoses, policy numbers, or plan language. Quote plan language "
        "verbatim. Keep a professional, firm, respectful tone. Address the "
        "denial reason directly and request written confirmation."
    )
    plan_lines = "\n".join(f"- {q}" for q in facts["plan_language"]) or "- none quoted"
    record_lines = "\n".join(f"- {q}" for q in facts["record_quotes"]) or "- none quoted"
    prompt = (
        f"Case file (all facts extracted from the patient's own documents; today is {date.today().isoformat()}):\n"
        f"Denial reason: {facts['denial_reason']}\n"
        f"Dates: {', '.join(facts['dates']) or 'none stated'}\n"
        f"Amounts: {', '.join(facts['amounts']) or 'none stated'}\n"
        f"Plan language (verbatim from the denial letter):\n{plan_lines}\n"
        f"Related record quotes (verbatim):\n{record_lines}\n"
        f"The patient's own words: {facts['user_words'] or 'none provided'}\n\n"
        "Write the complete appeal letter now. Begin with the subject line."
    )

    llm_output = structured_model_call(
        engine, prompt, module_type="appeal_letter", system=system,
        profile_id=profile_id, max_tokens=2000,
    )

    model_generated = not (
        isinstance(llm_output, dict) and llm_output.get("_model_blocked")
    )
    letter = llm_output.get("letter", "") if isinstance(llm_output, dict) else ""
    if not model_generated or not str(letter).strip():
        letter = _deterministic_letter(case_file)
        model_generated = False

    needs_human = case_file["denial_reason"]["needs_human"]
    return {
        "letter": letter,
        "case_file": case_file,
        "citations": _case_file_citations(case_file),
        "model_generated": model_generated,
        "note": "" if model_generated else _MODEL_OFF_NOTE,
        "needs_human": needs_human,
        # Machine-distinguishable marker, same contract as every other
        # generative surface (acceptance gate shape).
        "structured_output": llm_output,
    }
