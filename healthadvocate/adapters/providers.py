"""NPPES provider identity adapter — identity/taxonomy only."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from healthadvocate.adapters.base import AdapterEvidence, assert_no_forbidden_keys

FIXTURES = Path(__file__).resolve().parent / "fixtures"

NPPES_FORBIDDEN = frozenset(
    {
        "network_participation",
        "in_network",
        "licensure",
        "license_status",
        "availability",
        "quality",
        "appointment_access",
        "accepting_patients",
    }
)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def match_provider_nppes(
    query: str,
    *,
    fixture: str = "nppes_sample.json",
) -> AdapterEvidence:
    path = FIXTURES / fixture
    raw = path.read_bytes()
    data = json.loads(raw.decode("utf-8"))
    needle = query.strip().lower()
    matches = []
    for row in data.get("providers", []):
        name = (row.get("name") or "").lower()
        npi = str(row.get("npi") or "")
        if needle in name or needle == npi:
            matches.append(
                {
                    "npi": row.get("npi"),
                    "name": row.get("name"),
                    "taxonomy": row.get("taxonomy"),
                    "address_city": row.get("address_city"),
                    "address_state": row.get("address_state"),
                    "match_rationale": row.get("match_rationale")
                    or "name_or_npi_equality",
                }
            )
    if len(matches) == 0:
        status = "unknown"
    elif len(matches) == 1:
        status = "matched"
    else:
        status = "conflicted"

    payload: dict[str, Any] = {
        "status": status,
        "query": query,
        "matches": matches,
        # Explicit unknowns for forbidden claim classes
        "network_participation": "unknown",
        "licensure": "unknown",
        "availability": "unknown",
        "quality": "unknown",
        "appointment_access": "unknown",
    }
    # Forbidden keys must not carry asserted true/false network claims.
    for key in ("network_participation", "licensure", "availability", "quality", "appointment_access"):
        if payload[key] not in {"unknown", None}:
            raise AssertionError("NPPES must not assert non-identity claims")

    return AdapterEvidence(
        source="CMS NPPES",
        source_revision=data.get("release", "fixture"),
        retrieved_at=_now(),
        checksum=hashlib.sha256(raw).hexdigest(),
        claim_class="official_source" if status == "matched" else status,
        permitted_claims=("provider_identity", "npi", "taxonomy", "address"),
        forbidden_claims=tuple(sorted(NPPES_FORBIDDEN)),
        payload=payload,
        notes=(
            "NPPES identity match never upgrades network, licensure, availability, "
            "quality, or appointment access."
        ),
    )
