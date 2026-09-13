"""Machine-readable allowlist of audited artifacts for the core path.

The registry is the only source of truth for what may ship. Anything present
in requirements, containers, or declared optional adapters that is not listed
and approved fails the gate.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from healthadvocate.governance.models import (
    APPROVED_DATA_LICENSES,
    APPROVED_SOFTWARE_LICENSES,
    REJECTED_LICENSE_MARKERS,
    ApprovalResult,
    ArtifactKind,
    ArtifactRecord,
)

DATA_DIR = Path(__file__).resolve().parent / "data"
DEFAULT_REGISTRY_PATH = DATA_DIR / "artifact_registry.json"

TOOL_VERSION = "healthadvocate.governance/1.0.0"


def load_registry(path: Path | None = None) -> dict[str, Any]:
    registry_path = path or DEFAULT_REGISTRY_PATH
    with registry_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _normalize_license(value: str) -> str:
    return (value or "").strip()


def _license_is_rejected(license_id: str) -> str | None:
    lowered = license_id.lower().strip()
    if not lowered or lowered in REJECTED_LICENSE_MARKERS:
        return f"license is unknown or explicitly rejected: {license_id!r}"
    for marker in REJECTED_LICENSE_MARKERS:
        if marker in lowered:
            return f"license matches rejected marker {marker!r}: {license_id!r}"
    return None


def approve_record(record: ArtifactRecord) -> ArtifactRecord:
    """Return a new record with approval result and rejection reason set."""
    license_id = _normalize_license(record.license)
    rejection = _license_is_rejected(license_id)
    if rejection:
        return ArtifactRecord(
            **{
                **record.__dict__,
                "approval": ApprovalResult.REJECTED,
                "rejection_reason": rejection,
            }
        )

    if record.kind in {
        ArtifactKind.APPLICATION_PACKAGE,
        ArtifactKind.MODEL_RUNTIME,
    }:
        if license_id not in APPROVED_SOFTWARE_LICENSES:
            return ArtifactRecord(
                **{
                    **record.__dict__,
                    "approval": ApprovalResult.REJECTED,
                    "rejection_reason": (
                        f"software license not in approved OSI set: {license_id!r}"
                    ),
                }
            )
    elif record.kind == ArtifactKind.DATASET:
        if license_id not in APPROVED_DATA_LICENSES | APPROVED_SOFTWARE_LICENSES:
            return ArtifactRecord(
                **{
                    **record.__dict__,
                    "approval": ApprovalResult.REJECTED,
                    "rejection_reason": (
                        f"dataset license not in approved open/public set: {license_id!r}"
                    ),
                }
            )
    elif record.kind == ArtifactKind.MODEL_ARTIFACT:
        if license_id not in APPROVED_SOFTWARE_LICENSES | APPROVED_DATA_LICENSES:
            return ArtifactRecord(
                **{
                    **record.__dict__,
                    "approval": ApprovalResult.REJECTED,
                    "rejection_reason": (
                        f"model artifact license not approved for redistribution: "
                        f"{license_id!r}"
                    ),
                }
            )

    # Provenance and checksum policy are mandatory for shipped artifacts.
    if not record.source.strip():
        return ArtifactRecord(
            **{
                **record.__dict__,
                "approval": ApprovalResult.REJECTED,
                "rejection_reason": "missing source URL or repository reference",
            }
        )
    if not record.version.strip() or record.version.strip().lower() in {
        "unknown",
        "latest",
        "*",
    }:
        return ArtifactRecord(
            **{
                **record.__dict__,
                "approval": ApprovalResult.REJECTED,
                "rejection_reason": f"unpinned or unknown version: {record.version!r}",
            }
        )
    if not record.provenance.strip():
        return ArtifactRecord(
            **{
                **record.__dict__,
                "approval": ApprovalResult.REJECTED,
                "rejection_reason": "missing provenance description",
            }
        )
    if not record.checksum_policy.strip():
        return ArtifactRecord(
            **{
                **record.__dict__,
                "approval": ApprovalResult.REJECTED,
                "rejection_reason": "missing checksum policy",
            }
        )

    return ArtifactRecord(
        **{
            **record.__dict__,
            "approval": ApprovalResult.APPROVED,
            "rejection_reason": "",
        }
    )


def record_from_registry_entry(
    entry: dict[str, Any],
    kind: ArtifactKind,
) -> ArtifactRecord:
    base = ArtifactRecord(
        artifact_id=entry["artifact_id"],
        kind=kind,
        name=entry["name"],
        source=entry["source"],
        version=entry["version"],
        license=entry["license"],
        provenance=entry["provenance"],
        checksum_policy=entry["checksum_policy"],
        redistribution=entry.get("redistribution", "see-license"),
        attribution=entry.get("attribution", entry["name"]),
        required_for_manual_workflow=bool(
            entry.get("required_for_manual_workflow", False)
        ),
        notes=entry.get("notes", ""),
    )
    status = entry.get("shipped_status", "shipped")
    if status == "not_shipped":
        return ArtifactRecord(
            **{
                **base.__dict__,
                "approval": ApprovalResult.NOT_SHIPPED,
                "rejection_reason": "",
            }
        )
    if status == "rejected":
        return ArtifactRecord(
            **{
                **base.__dict__,
                "approval": ApprovalResult.REJECTED,
                "rejection_reason": entry.get(
                    "rejection_reason",
                    "explicitly rejected by open-boundary decision (issue 78)",
                ),
                "catalog_denylist": True,
            }
        )
    return approve_record(base)
