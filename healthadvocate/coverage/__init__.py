"""Coverage Continuity Track public surface.

The manual workflow is available without a local model and without optional
datasets. Encrypted case persistence and adapters arrive in later tickets.
"""

from __future__ import annotations

from dataclasses import dataclass

from healthadvocate.coverage.service import (
    create_synthetic_case,
    get_case,
    list_cases,
    resume_case,
    update_case,
)


@dataclass(frozen=True)
class ManualWorkflowStatus:
    """Public proof that the manual path has no model/dataset hard dependency."""

    available: bool
    requires_model: bool
    requires_optional_dataset: bool
    mode: str
    notes: str


def manual_workflow_status() -> ManualWorkflowStatus:
    return ManualWorkflowStatus(
        available=True,
        requires_model=False,
        requires_optional_dataset=False,
        mode="manual_evidence",
        notes=(
            "Deterministic Coverage Case management works with user-entered "
            "synthetic evidence only. Models and open-data adapters are optional."
        ),
    )


__all__ = [
    "ManualWorkflowStatus",
    "manual_workflow_status",
    "create_synthetic_case",
    "get_case",
    "list_cases",
    "resume_case",
    "update_case",
]
