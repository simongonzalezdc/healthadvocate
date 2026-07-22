"""Deterministic Coverage scripts — no model, no invented facts."""

from __future__ import annotations

from typing import Any


def _fact_map(case: dict[str, Any]) -> dict[str, str]:
    out: dict[str, str] = {}
    for fact in case.get("facts") or []:
        label = str(fact.get("label") or "").strip()
        value = str(fact.get("value") or "").strip()
        status = str(fact.get("status") or "unknown")
        if not label:
            continue
        if status in {"unknown", "stale", "conflicted"} or not value:
            out[label] = "[unknown]"
        else:
            out[label] = value
    return out


def _val(facts: dict[str, str], key: str) -> str:
    return facts.get(key) or "[unknown]"


def generate_script(case: dict[str, Any], kind: str) -> dict[str, Any]:
    facts = _fact_map(case)
    kind_norm = (kind or "").strip().lower()
    next_action = case.get("next_action") or "[unknown]"
    title = case.get("title") or "[unknown]"

    if kind_norm == "county":
        steps = [
            f"Say: I am calling about coverage after a job change for case '{title}'.",
            f"Confirm the office: {_val(facts, 'county_office')}.",
            f"State my coverage end date: {_val(facts, 'coverage_end_date')}.",
            f"Ask what documents are needed by: {_val(facts, 'document_deadline')}.",
            "Ask for the worker name, callback number, and confirmation number.",
            "Do not agree to any payment or plan selection on this call.",
        ]
        purpose = "County eligibility interview preparation"
    elif kind_norm == "provider":
        providers = [
            t.get("name") or "[unknown]"
            for t in case.get("targets") or []
            if t.get("kind") == "provider"
        ]
        provider_name = providers[0] if providers else "[unknown]"
        steps = [
            f"Say: I need to confirm continuity of care with {provider_name}.",
            f"Ask whether they can see me if my coverage changes on {_val(facts, 'coverage_end_date')}.",
            "Ask about self-pay, hardship, delayed billing, or payment plans — without agreeing yet.",
            "Ask how to request records or a referral if needed.",
            "Write down the name of the person you spoke with and the date.",
        ]
        purpose = "Provider continuity call preparation"
    elif kind_norm == "billing":
        steps = [
            "Say: I am reviewing a bill and need itemized charges before any payment.",
            f"Reference account or claim id: {_val(facts, 'claim_or_account_id')}.",
            "Ask for an itemized statement and coding explanations.",
            "Ask about financial assistance or payment plans without authorizing a charge.",
            "Do not provide a card number on this call unless you choose to outside this app.",
        ]
        purpose = "Billing and cash-price inquiry preparation"
    elif kind_norm == "pharmacy":
        meds = [
            t.get("name") or "[unknown]"
            for t in case.get("targets") or []
            if t.get("kind") == "medication"
        ]
        med = meds[0] if meds else _val(facts, "medication_name")
        steps = [
            f"Say: I need a refill bridge for {med}.",
            f"Confirm pharmacy: {_val(facts, 'pharmacy_name')}.",
            f"Ask about cash price and refill date: {_val(facts, 'refill_date')}.",
            "Ask what prior authorization or formulary issues exist — do not change treatment.",
            "Do not approve a substitute therapy without speaking to a clinician.",
        ]
        purpose = "Pharmacy and refill-bridge preparation"
    else:
        return {
            "kind": kind_norm or "unknown",
            "purpose": "Unknown script type",
            "steps": [],
            "error": "Supported scripts: county, provider, billing, pharmacy",
            "unknown_fields_policy": "Unknown values appear as [unknown]",
        }

    return {
        "kind": kind_norm,
        "purpose": purpose,
        "case_title": title,
        "related_next_action": next_action,
        "steps": steps,
        "unknown_fields_policy": "Unknown values appear as [unknown]; nothing is invented",
        "commitment_note": (
            "This script prepares speech only. Payment, submission, messaging, "
            "and treatment changes remain blocked by the Commitment Gate."
        ),
    }
