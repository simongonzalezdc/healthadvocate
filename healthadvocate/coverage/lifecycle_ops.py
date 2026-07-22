"""Export, redaction, deletion, and recovery operations for Coverage Cases."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable, Optional

from healthadvocate.coverage.domain import CoverageCase, utc_now_iso
from healthadvocate.coverage.store import CaseStore, CaseStoreError

# Direct identifier patterns for synthetic/redaction demos (not a guarantee).
_REDACT_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"\bCANARY_PATIENT_[A-Z0-9_]+\b", re.I), "[REDACTED_NAME]"),
    (re.compile(r"\bMEMBER-ID-[A-Z0-9_-]+\b", re.I), "[REDACTED_MEMBER_ID]"),
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[REDACTED_SSN]"),
    (re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I), "[REDACTED_EMAIL]"),
    (re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"), "[REDACTED_PHONE]"),
]


def redact_text(value: str) -> str:
    out = value
    for pattern, repl in _REDACT_PATTERNS:
        out = pattern.sub(repl, out)
    return out


def _redact_obj(obj: Any) -> Any:
    if isinstance(obj, str):
        return redact_text(obj)
    if isinstance(obj, list):
        return [_redact_obj(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _redact_obj(v) for k, v in obj.items()}
    return obj


def private_export(case: CoverageCase) -> dict[str, Any]:
    return {
        "mode": "private",
        "exported_at": utc_now_iso(),
        "case": case.to_dict(),
        "residual_risk_warning": None,
        "review_required_before_share": True,
    }


def redacted_export(case: CoverageCase) -> dict[str, Any]:
    redacted = _redact_obj(case.to_dict())
    return {
        "mode": "redacted",
        "exported_at": utc_now_iso(),
        "case": redacted,
        "residual_risk_warning": (
            "Automated redaction is not a guarantee. Review the file before sharing. "
            "Indirect identifiers may remain."
        ),
        "review_required_before_share": True,
    }


def write_export(
    payload: dict[str, Any],
    destination: Path,
    *,
    reviewed: bool,
) -> Path:
    if not reviewed:
        raise CaseStoreError("export requires explicit review confirmation")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return destination


def delete_case(
    store: CaseStore,
    case_id: str,
    *,
    unowned_source_paths: Optional[Iterable[str]] = None,
) -> dict[str, Any]:
    """Delete application-owned case data; report unowned sources without deleting."""
    conn = store._require_conn()
    # Ensure exists
    store.get_case(case_id)
    conn.execute("DELETE FROM coverage_cases WHERE case_id = ?", (case_id,))
    conn.commit()
    store._persist()
    unowned = list(unowned_source_paths or [])
    return {
        "deleted_case_id": case_id,
        "application_owned_removed": True,
        "unowned_sources_reported": unowned,
        "unowned_sources_deleted": False,
        "note": "Unowned source files were not deleted.",
    }


def rotate_store_key(store: CaseStore) -> None:
    """Re-encrypt the store with a rotated key from the keystore."""
    new_key = store.keystore.rotate_key()
    store._persist(key=new_key)
