"""Medical bill decoder — extract line items and flag potential errors."""

from __future__ import annotations

import re
from .engine import HealthEngine

# Pattern matchers for bill elements
_CPT_PATTERN = re.compile(r'\b(\d{5})\b')
_ICD_PATTERN = re.compile(r'\b([A-Z]\d{2}(?:\.\d{1,4})?)\b')
_PRICE_PATTERN = re.compile(r'\$\s?([\d,]+(?:\.\d{2})?)')
_DATE_PATTERN = re.compile(r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b')

# Known upcode patterns (same procedure, different inflated descriptions)
_UPCODE_PATTERNS = {
    "99213": {"normal": "Office visit - established patient, low complexity", "upcode": "99214"},
    "99214": {"normal": "Office visit - established patient, moderate complexity", "upcode": "99215"},
    "99215": {"normal": "Office visit - established patient, high complexity", "upcode": None},
    "99281": {"normal": "ER visit, low severity", "upcode": "99282"},
    "99282": {"normal": "ER visit, low-moderate severity", "upcode": "99283"},
    "99283": {"normal": "ER visit, moderate severity", "upcode": "99284"},
    "99284": {"normal": "ER visit, high severity", "upcode": "99285"},
}

_CPT_DESCRIPTIONS = {
    "99213": "Office visit - established patient, low complexity",
    "99214": "Office visit - established patient, moderate complexity",
    "99215": "Office visit - established patient, high complexity",
    "99281": "Emergency department visit, low severity",
    "99282": "Emergency department visit, low-moderate severity",
    "99283": "Emergency department visit, moderate severity",
    "99284": "Emergency department visit, high severity",
    "99285": "Emergency department visit, very high severity",
    "99211": "Office visit - established patient, may not require physician",
    "99212": "Office visit - established patient, straightforward",
    "36415": "Venipuncture (blood draw)",
    "80053": "Comprehensive metabolic panel",
    "85025": "Complete blood count (CBC)",
    "81001": "Urinalysis with microscopy",
    "90834": "Psychotherapy, 45 minutes",
    "90837": "Psychotherapy, 60 minutes",
    "93000": "Electrocardiogram (ECG)",
    "71046": "Chest X-ray, 2 views",
    "99144": "Moderate sedation, first 30 minutes",
}


def _parse_line_items(text: str) -> list[dict]:
    """Extract bill line items from text."""
    lines = text.split('\n')
    items = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        prices = _PRICE_PATTERN.findall(line)
        cpt_codes = _CPT_PATTERN.findall(line)
        icd_codes = _ICD_PATTERN.findall(line)

        for code in cpt_codes:
            price = None
            if prices:
                price_str = prices[0].replace(',', '')
                try:
                    price = float(price_str)
                except ValueError:
                    pass

            items.append({
                "description": _CPT_DESCRIPTIONS.get(code, line[:80]),
                "cpt_code": code,
                "amount": price,
                "raw_line": line[:120],
            })

    if not items and _PRICE_PATTERN.search(text):
        prices = _PRICE_PATTERN.findall(text)
        for price_str in prices:
            try:
                amount = float(price_str.replace(',', ''))
                items.append({
                    "description": "Unspecified charge",
                    "cpt_code": None,
                    "amount": amount,
                    "raw_line": "",
                })
            except ValueError:
                pass

    return items


def _flag_issues(items: list[dict], text: str) -> list[dict]:
    """Flag potential billing issues."""
    flags = []

    # Check for duplicate CPT codes
    cpt_counts: dict[str, int] = {}
    for item in items:
        code = item.get("cpt_code")
        if code:
            cpt_counts[code] = cpt_counts.get(code, 0) + 1

    for code, count in cpt_counts.items():
        if count > 1:
            flags.append({
                "type": "duplicate_code",
                "detail": f"CPT code {code} appears {count} times. Verify each occurrence is a separate service.",
                "severity": "warning",
            })

    # Check for potential upcoding
    for code in cpt_counts:
        if code in _UPCODE_PATTERNS:
            upcode = _UPCODE_PATTERNS[code].get("upcode")
            if upcode and upcode in cpt_counts:
                flags.append({
                    "type": "potential_upcode",
                    "detail": f"Both {code} and {upcode} billed. {code} is: {_CPT_DESCRIPTIONS.get(code, 'N/A')}. {upcode} is: {_CPT_DESCRIPTIONS.get(upcode, 'N/A')}. Verify the higher-level service was actually provided.",
                    "severity": "warning",
                })

    # Check for missing descriptions
    for item in items:
        if item["description"] == "Unspecified charge" or not item.get("cpt_code"):
            flags.append({
                "type": "missing_description",
                "detail": f"Charge of ${item['amount']:.2f} has no procedure code or description. Request itemization.",
                "severity": "info",
            })

    # Check for unusually high charges
    for item in items:
        amt = item.get("amount")
        if amt and amt > 5000:
            flags.append({
                "type": "high_charge",
                "detail": f"Charge of ${amt:.2f} for '{item['description']}' is unusually high. Compare with fair price databases.",
                "severity": "warning",
            })

    return flags


def decode_bill(engine: HealthEngine, bill_text: str) -> dict:
    """Decode a medical bill and flag potential issues."""
    if not bill_text or not bill_text.strip():
        return {
            "line_items": [],
            "flags": [],
            "total": None,
            "flagged_issues": [],
            "entities_found": {"diseases": [], "drugs": []},
        }

    diseases = engine.extract_diseases(bill_text, confidence=0.5)
    drugs = engine.extract_drugs(bill_text, confidence=0.5)

    errors = [r.error for r in (diseases, drugs) if r.error]
    if errors and not any((diseases.entities, drugs.entities)):
        return {
            "line_items": [],
            "flags": [],
            "total": None,
            "flagged_issues": [],
            "entities_found": {"diseases": [], "drugs": []},
            "error": "; ".join(errors),
        }

    items = _parse_line_items(bill_text)
    flags = _flag_issues(items, bill_text)

    total = None
    amounts = [item["amount"] for item in items if item.get("amount") is not None]
    if amounts:
        total = round(sum(amounts), 2)

    return {
        "line_items": items,
        "flags": flags,
        "total": f"${total:.2f}" if total is not None else None,
        "flagged_issues": [f["detail"] for f in flags],
        "entities_found": {
            "diseases": [{"text": e.text, "label": e.label} for e in diseases.entities],
            "drugs": [{"text": e.text, "label": e.label} for e in drugs.entities],
        },
        "processing_time": {
            "diseases": diseases.processing_time,
            "drugs": drugs.processing_time,
        },
    }
