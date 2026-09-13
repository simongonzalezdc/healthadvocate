"""Build the four separate inventories for an exact shipped build."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from healthadvocate.governance.models import (
    ApprovalResult,
    ArtifactInventory,
    ArtifactKind,
    ArtifactRecord,
)
from healthadvocate.governance.registry import (
    load_registry,
    record_from_registry_entry,
)

REQUIREMENT_LINE = re.compile(
    r"^\s*([A-Za-z0-9_.\-]+(?:\[[^\]]+\])?)\s*([<>=!~].+)?$"
)


def parse_requirements(path: Path) -> dict[str, str]:
    """Map normalized package name -> version specifier from requirements.txt."""
    packages: dict[str, str] = {}
    if not path.is_file():
        return packages
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        match = REQUIREMENT_LINE.match(line)
        if not match:
            continue
        name = match.group(1).split("[", 1)[0].lower().replace("_", "-")
        version = (match.group(2) or "").strip() or "unspecified"
        packages[name] = version
    return packages


def _entries(registry: dict[str, Any], key: str) -> list[dict[str, Any]]:
    return list(registry.get(key) or [])


def build_application_inventory(
    registry: dict[str, Any],
    requirements_path: Path,
) -> ArtifactInventory:
    declared = parse_requirements(requirements_path)
    artifacts: list[ArtifactRecord] = []
    covered_requirements: set[str] = set()

    for entry in _entries(registry, "application_packages"):
        record = record_from_registry_entry(entry, ArtifactKind.APPLICATION_PACKAGE)
        req_name = (entry.get("requirement_name") or "").lower().replace("_", "-")
        if req_name:
            covered_requirements.add(req_name)
            if req_name not in declared and entry.get("shipped_status") == "shipped":
                # healthadvocate itself is not a pip requirement line.
                if req_name != "healthadvocate":
                    record = ArtifactRecord(
                        **{
                            **record.__dict__,
                            "approval": ApprovalResult.REJECTED,
                            "rejection_reason": (
                                f"registry marks {req_name!r} shipped but it is "
                                "absent from requirements.txt"
                            ),
                        }
                    )
            elif req_name in declared:
                # Align version display with requirements pin when present.
                record = ArtifactRecord(
                    **{
                        **record.__dict__,
                        "version": declared[req_name],
                    }
                )
                if record.approval != ApprovalResult.REJECTED:
                    from healthadvocate.governance.registry import approve_record

                    record = approve_record(record)
        artifacts.append(record)

    # Any requirements.txt package not covered by the registry fails closed.
    for name, version in sorted(declared.items()):
        if name in covered_requirements:
            continue
        artifacts.append(
            ArtifactRecord(
                artifact_id=f"pkg-unregistered-{name}",
                kind=ArtifactKind.APPLICATION_PACKAGE,
                name=name,
                source="",
                version=version,
                license="unknown",
                provenance="present in requirements.txt without registry entry",
                checksum_policy="",
                redistribution="unknown",
                attribution=name,
                required_for_manual_workflow=False,
                approval=ApprovalResult.REJECTED,
                rejection_reason=(
                    f"package {name!r} is in requirements.txt but has no "
                    "audited registry entry"
                ),
            )
        )

    forbidden = {
        n.lower().replace("_", "-")
        for n in (registry.get("forbidden_requirement_names") or [])
    }
    for name in declared:
        if name in forbidden:
            artifacts.append(
                ArtifactRecord(
                    artifact_id=f"pkg-forbidden-{name}",
                    kind=ArtifactKind.APPLICATION_PACKAGE,
                    name=name,
                    source="",
                    version=declared[name],
                    license="proprietary",
                    provenance="forbidden by open-boundary decision",
                    checksum_policy="",
                    redistribution="not permitted",
                    attribution=name,
                    approval=ApprovalResult.REJECTED,
                    rejection_reason=(
                        f"package {name!r} is on the forbidden dependency list"
                    ),
                )
            )

    return ArtifactInventory(
        kind=ArtifactKind.APPLICATION_PACKAGE,
        artifacts=artifacts,
    )


def build_kind_inventory(
    registry: dict[str, Any],
    registry_key: str,
    kind: ArtifactKind,
) -> ArtifactInventory:
    artifacts = [
        record_from_registry_entry(entry, kind)
        for entry in _entries(registry, registry_key)
    ]
    return ArtifactInventory(kind=kind, artifacts=artifacts)


def build_all_inventories(
    project_root: Path,
    registry_path: Path | None = None,
) -> dict[str, ArtifactInventory]:
    registry = load_registry(registry_path)
    requirements = project_root / "healthadvocate" / "requirements.txt"
    return {
        ArtifactKind.APPLICATION_PACKAGE.value: build_application_inventory(
            registry, requirements
        ),
        ArtifactKind.MODEL_RUNTIME.value: build_kind_inventory(
            registry, "model_runtimes", ArtifactKind.MODEL_RUNTIME
        ),
        ArtifactKind.MODEL_ARTIFACT.value: build_kind_inventory(
            registry, "model_artifacts", ArtifactKind.MODEL_ARTIFACT
        ),
        ArtifactKind.DATASET.value: build_kind_inventory(
            registry, "datasets", ArtifactKind.DATASET
        ),
    }
