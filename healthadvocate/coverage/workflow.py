"""Low-energy Coverage workflow view-model (one primary action)."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from healthadvocate.coverage.scripts import generate_script


def _parse_due(raw: str | None) -> date | None:
    if not raw:
        return None
    try:
        return date.fromisoformat(raw[:10])
    except ValueError:
        return None


def classify_deadline(due_raw: str | None, *, today: date | None = None) -> str:
    due = _parse_due(due_raw)
    if due is None:
        return "unknown"
    day = today or date.today()
    if due < day:
        return "overdue"
    if (due - day).days <= 14:
        return "approaching"
    return "scheduled"


def build_coverage_view(
    case: dict[str, Any],
    *,
    today: date | None = None,
) -> dict[str, Any]:
    """Public view model for the critical Coverage screen."""
    risks: list[dict[str, str]] = []

    for deadline in case.get("deadlines") or []:
        status = classify_deadline(deadline.get("due"), today=today)
        risks.append(
            {
                "kind": "deadline",
                "label": deadline.get("label") or "Deadline",
                "due": deadline.get("due") or "[unknown]",
                "status": status,
            }
        )

    for fact in case.get("facts") or []:
        status = fact.get("status") or "unknown"
        if status in {"unknown", "stale", "conflicted"}:
            risks.append(
                {
                    "kind": "fact",
                    "label": fact.get("label") or "Fact",
                    "due": fact.get("observed_at") or "",
                    "status": status,
                }
            )

    # Order risks: overdue, conflicted, stale, approaching, unknown, scheduled
    order = {
        "overdue": 0,
        "conflicted": 1,
        "stale": 2,
        "approaching": 3,
        "unknown": 4,
        "scheduled": 5,
    }
    risks.sort(key=lambda r: order.get(r["status"], 9))

    primary = {
        "label": case.get("next_action") or "Review your Coverage Case",
        "intent": "local_view",
        "is_primary": True,
    }

    return {
        "case_id": case.get("case_id"),
        "title": case.get("title"),
        "lifecycle": case.get("lifecycle"),
        "primary_action": primary,
        "secondary_actions": [
            {"label": "View evidence", "intent": "local_view", "is_primary": False},
            {"label": "Generate script", "intent": "generate_script", "is_primary": False},
        ],
        "risks": risks,
        "targets": case.get("targets") or [],
        "evidence": case.get("evidence") or [],
        "contacts": case.get("contacts") or [],
        "scripts_available": ["county", "provider", "billing", "pharmacy"],
        "ui": {
            "one_primary_action": True,
            "progressive_disclosure": True,
            "requires_model": False,
        },
    }


def script_for_case(case: dict[str, Any], kind: str) -> dict[str, Any]:
    return generate_script(case, kind)
