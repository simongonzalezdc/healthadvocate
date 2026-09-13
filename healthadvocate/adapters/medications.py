"""Medication adapters: RxNorm CPC, DailyMed, openFDA (fixture-backed)."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from healthadvocate.adapters.base import AdapterEvidence, ClaimContractError, assert_no_forbidden_keys

FIXTURES = Path(__file__).resolve().parent / "fixtures"

RXNORM_FORBIDDEN = frozenset(
    {"interaction_clearance", "dose", "diagnosis", "treatment", "coverage"}
)
LABEL_FORBIDDEN = frozenset(
    {"personalized_advice", "causation", "dose_instruction_for_patient"}
)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _checksum(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_fixture(name: str) -> dict[str, Any]:
    path = FIXTURES / name
    raw = path.read_bytes()
    return {"data": json.loads(raw.decode("utf-8")), "raw": raw, "path": str(path)}


def normalize_medication_rxnorm_cpc(
    name: str,
    *,
    fixture: str = "rxnorm_cpc_sample.json",
) -> AdapterEvidence:
    """Identity mapping only from RxNorm Current Prescribable Content boundary."""
    loaded = _load_fixture(fixture)
    data = loaded["data"]
    needle = name.strip().lower()
    match = None
    for row in data.get("concepts", []):
        if needle in row.get("name", "").lower() or needle == row.get("rxcui", "").lower():
            match = row
            break
    if match is None:
        payload = {"status": "unknown", "query": name, "rxcui": None, "name": None}
    else:
        payload = {
            "status": "matched",
            "query": name,
            "rxcui": match.get("rxcui"),
            "name": match.get("name"),
            "tty": match.get("tty"),
        }
    assert_no_forbidden_keys(payload, RXNORM_FORBIDDEN)
    return AdapterEvidence(
        source="RxNorm Current Prescribable Content",
        source_revision=data.get("release", "fixture"),
        retrieved_at=_now(),
        checksum=_checksum(loaded["raw"]),
        claim_class="official_source",
        permitted_claims=("normalized_identity", "rxcui", "tty"),
        forbidden_claims=tuple(sorted(RXNORM_FORBIDDEN)),
        payload=payload,
        notes="CPC identity only; not full RxNorm; no safety or coverage claims.",
    )


def dailymed_label_evidence(
    rxcui_or_name: str,
    *,
    fixture: str = "dailymed_sample.json",
) -> AdapterEvidence:
    loaded = _load_fixture(fixture)
    data = loaded["data"]
    key = rxcui_or_name.strip().lower()
    row = None
    for item in data.get("labels", []):
        if key in (item.get("name", "").lower(), item.get("rxcui", "").lower()):
            row = item
            break
    payload = {
        "status": "matched" if row else "unknown",
        "query": rxcui_or_name,
        "label_excerpt": (row or {}).get("excerpt"),
        "setid": (row or {}).get("setid"),
        "effective_date": (row or {}).get("effective_date"),
    }
    assert_no_forbidden_keys(payload, LABEL_FORBIDDEN)
    return AdapterEvidence(
        source="DailyMed bulk SPL",
        source_revision=data.get("release", "fixture"),
        retrieved_at=_now(),
        checksum=_checksum(loaded["raw"]),
        claim_class="official_source",
        permitted_claims=("dated_label_excerpt", "setid", "effective_date"),
        forbidden_claims=tuple(sorted(LABEL_FORBIDDEN)),
        payload=payload,
        notes="Dated official label passage only; not individualized advice.",
    )


def openfda_safety_evidence(
    name: str,
    *,
    fixture: str = "openfda_sample.json",
) -> AdapterEvidence:
    loaded = _load_fixture(fixture)
    data = loaded["data"]
    key = name.strip().lower()
    row = None
    for item in data.get("records", []):
        if key in item.get("name", "").lower():
            row = item
            break
    payload = {
        "status": "matched" if row else "unknown",
        "query": name,
        "recalls": (row or {}).get("recalls", []),
        "shortages": (row or {}).get("shortages", []),
        "report_count": (row or {}).get("report_count"),
        "effective_date": (row or {}).get("effective_date"),
    }
    # Explicitly refuse causation
    if "causation" in payload:
        raise ClaimContractError("causation forbidden")
    return AdapterEvidence(
        source="openFDA",
        source_revision=data.get("release", "fixture"),
        retrieved_at=_now(),
        checksum=_checksum(loaded["raw"]),
        claim_class="official_source",
        permitted_claims=("dated_recalls", "shortages", "report_counts"),
        forbidden_claims=("causation", "personal_risk", "diagnosis"),
        payload=payload,
        notes="Report counts do not establish causation.",
    )


def refuse_clinical_verdict(kind: str) -> dict[str, Any]:
    return {
        "allowed": False,
        "kind": kind,
        "reason": (
            "HealthAdvocate will not diagnose, clear interactions, calculate dose, "
            "infer adverse-event causation, or recommend treatment changes."
        ),
    }
