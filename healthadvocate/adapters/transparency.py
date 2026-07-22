"""CMS Transparency in Coverage research path — disabled until budgets attached."""

from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any, Iterator


FEATURE_FLAG = "HEALTHADVOCATE_CMS_TIC_ENABLED"


@dataclass
class ResourceBudget:
    max_disk_bytes: int
    max_memory_bytes: int
    max_duration_seconds: float


# Placeholder budgets must be replaced with measured values before enablement.
DEFAULT_BUDGET = ResourceBudget(
    max_disk_bytes=50_000_000,
    max_memory_bytes=100_000_000,
    max_duration_seconds=30.0,
)


def feature_enabled(env: dict[str, str] | None = None) -> bool:
    source = env if env is not None else os.environ
    return source.get(FEATURE_FLAG, "0").strip().lower() in {"1", "true", "yes", "on"}


def stream_sample_rows(sample: list[dict[str, Any]]) -> Iterator[dict[str, Any]]:
    """Stream rows without requiring the core workflow to load bulk files."""
    for row in sample:
        yield row


def research_negotiated_rates(
    sample: list[dict[str, Any]],
    *,
    env: dict[str, str] | None = None,
    budget: ResourceBudget = DEFAULT_BUDGET,
) -> dict[str, Any]:
    if not feature_enabled(env):
        return {
            "enabled": False,
            "message": (
                "CMS Transparency in Coverage research remains disabled until "
                "representative disk/memory/duration measurements are attached."
            ),
            "budget": {
                "max_disk_bytes": budget.max_disk_bytes,
                "max_memory_bytes": budget.max_memory_bytes,
                "max_duration_seconds": budget.max_duration_seconds,
                "measured": False,
            },
            "not_guaranteed_patient_price": True,
            "not_network_truth": True,
        }

    start = time.perf_counter()
    results = []
    bytes_seen = 0
    for row in stream_sample_rows(sample):
        bytes_seen += len(str(row))
        if bytes_seen > budget.max_disk_bytes:
            break
        results.append(
            {
                "payer": row.get("payer"),
                "billing_code": row.get("billing_code"),
                "negotiated_rate": row.get("negotiated_rate"),
                "meaning": "source_specific_negotiated_rate_evidence",
                "not_guaranteed_patient_price": True,
                "not_network_truth": True,
            }
        )
        if time.perf_counter() - start > budget.max_duration_seconds:
            break

    return {
        "enabled": True,
        "rows": results,
        "duration_seconds": round(time.perf_counter() - start, 4),
        "budget": {
            "max_disk_bytes": budget.max_disk_bytes,
            "max_memory_bytes": budget.max_memory_bytes,
            "max_duration_seconds": budget.max_duration_seconds,
            "measured": False,
        },
        "not_guaranteed_patient_price": True,
        "not_network_truth": True,
        "notes": (
            "Negotiated rates are source-specific evidence only, not guaranteed "
            "patient price or provider-network truth."
        ),
    }
