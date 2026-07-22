"""Public Coverage workflow service (synthetic cases only)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

from healthadvocate.coverage.domain import CoverageCase
from healthadvocate.coverage.keystore import (
    InMemoryKeyStore,
    KeyStore,
    default_data_dir,
)
from healthadvocate.coverage.store import CaseStore, CaseStoreError

_DEFAULT_STORE: Optional[CaseStore] = None


def get_default_store(
    *,
    data_dir: Optional[Path | str] = None,
    keystore: Optional[KeyStore] = None,
    reset: bool = False,
) -> CaseStore:
    global _DEFAULT_STORE
    if reset:
        if _DEFAULT_STORE is not None:
            _DEFAULT_STORE.close()
        _DEFAULT_STORE = None
    if _DEFAULT_STORE is None:
        root = Path(data_dir or default_data_dir())
        root.mkdir(parents=True, exist_ok=True)
        path = root / "coverage_cases.haenc"
        ks = keystore or InMemoryKeyStore()
        create = not path.exists()
        _DEFAULT_STORE = CaseStore(path, ks, create=create)
    return _DEFAULT_STORE


def create_synthetic_case(
    title: str,
    *,
    next_action: str = "Review coverage situation and list deadlines",
    store: Optional[CaseStore] = None,
) -> dict[str, Any]:
    s = store or get_default_store()
    case = s.create_case(title, next_action=next_action, synthetic=True)
    return case.to_dict()


def get_case(case_id: str, *, store: Optional[CaseStore] = None) -> dict[str, Any]:
    s = store or get_default_store()
    return s.get_case(case_id).to_dict()


def list_cases(*, store: Optional[CaseStore] = None) -> list[dict[str, Any]]:
    s = store or get_default_store()
    return s.list_cases()


def update_case(
    case_id: str,
    *,
    title: Optional[str] = None,
    next_action: Optional[str] = None,
    lifecycle: Optional[str] = None,
    deadlines: Optional[list[dict[str, str]]] = None,
    store: Optional[CaseStore] = None,
) -> dict[str, Any]:
    s = store or get_default_store()
    return s.update_case(
        case_id,
        title=title,
        next_action=next_action,
        lifecycle=lifecycle,
        deadlines=deadlines,
    ).to_dict()


def resume_case(case_id: str, *, store: Optional[CaseStore] = None) -> dict[str, Any]:
    """Re-open a store read path and return the case (restart/resume)."""
    s = store or get_default_store()
    case = s.get_case(case_id)
    return {
        "case": case.to_dict(),
        "resumed": True,
        "next_action": case.next_action,
        "lifecycle": case.lifecycle.value,
    }
