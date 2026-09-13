"""NADAC and DrugCentral reference benchmarks — not patient prices."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from healthadvocate.adapters.base import AdapterEvidence

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def nadac_benchmark(
    ndc_or_name: str,
    *,
    fixture: str = "nadac_sample.json",
) -> AdapterEvidence:
    path = FIXTURES / fixture
    raw = path.read_bytes()
    data = json.loads(raw.decode("utf-8"))
    key = ndc_or_name.strip().lower()
    row = None
    for item in data.get("rows", []):
        if key in (
            str(item.get("ndc", "")).lower(),
            str(item.get("name", "")).lower(),
        ):
            row = item
            break
    payload: dict[str, Any] = {
        "status": "matched" if row else "unknown",
        "query": ndc_or_name,
        "benchmark_meaning": "acquisition_cost_benchmark",
        "not_a_patient_price": True,
        "not_insured_price": True,
        "not_coupon_price": True,
        "not_pharmacy_quote": True,
        "unit": (row or {}).get("unit"),
        "value": (row or {}).get("nadac_per_unit"),
        "effective_date": (row or {}).get("effective_date"),
        "source_name": "CMS NADAC",
    }
    return AdapterEvidence(
        source="CMS NADAC",
        source_revision=data.get("release", "fixture"),
        retrieved_at=_now(),
        checksum=hashlib.sha256(raw).hexdigest(),
        claim_class="official_source",
        permitted_claims=("acquisition_cost_benchmark", "unit", "effective_date"),
        forbidden_claims=(
            "patient_cash_price",
            "insured_price",
            "coupon_price",
            "pharmacy_quote",
            "best_price",
        ),
        payload=payload,
        notes="NADAC is an acquisition-cost benchmark, never a guaranteed patient price.",
    )


def drugcentral_reference(
    name: str,
    *,
    fixture: str = "drugcentral_sample.json",
) -> AdapterEvidence:
    path = FIXTURES / fixture
    raw = path.read_bytes()
    data = json.loads(raw.decode("utf-8"))
    key = name.strip().lower()
    row = None
    for item in data.get("drugs", []):
        if key in item.get("name", "").lower():
            row = item
            break
    payload = {
        "status": "matched" if row else "unknown",
        "query": name,
        "structures_id": (row or {}).get("id"),
        "reference_facts": (row or {}).get("facts", []),
        "share_alike_notice": (
            "DrugCentral data is CC BY-SA 4.0. Attribution and share-alike "
            "obligations apply to redistributed derivatives."
        ),
    }
    return AdapterEvidence(
        source="DrugCentral",
        source_revision=data.get("release", "fixture"),
        retrieved_at=_now(),
        checksum=hashlib.sha256(raw).hexdigest(),
        claim_class="official_source",
        permitted_claims=("attributed_structured_facts",),
        forbidden_claims=("clinical_clearance", "interaction_verdict", "dose"),
        payload=payload,
        attribution="DrugCentral (CC BY-SA 4.0)",
        notes="Attributed reference facts only; not clinical clearance.",
    )
