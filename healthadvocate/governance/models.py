"""Typed models for artifact inventories and license/provenance gates."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class ArtifactKind(str, Enum):
    """Top-level inventory category. Approvals do not cross categories."""

    APPLICATION_PACKAGE = "application_package"
    MODEL_RUNTIME = "model_runtime"
    MODEL_ARTIFACT = "model_artifact"
    DATASET = "dataset"


class ApprovalResult(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    NOT_SHIPPED = "not_shipped"
    UNKNOWN = "unknown"


# OSI-approved and public-domain data terms accepted for the core path.
# Noncommercial, proprietary, paid-only, hosted-only, and "source available"
# but non-OSI licenses are intentionally absent.
APPROVED_SOFTWARE_LICENSES: frozenset[str] = frozenset(
    {
        "MIT",
        "Apache-2.0",
        "BSD-2-Clause",
        "BSD-3-Clause",
        "ISC",
        "MPL-2.0",
        "LGPL-2.1",
        "LGPL-3.0",
        "GPL-2.0",
        "GPL-3.0",
        "AGPL-3.0",
        "Python-2.0",
        "Unlicense",
        "CC0-1.0",
        "0BSD",
    }
)

APPROVED_DATA_LICENSES: frozenset[str] = frozenset(
    {
        "public-domain",
        "CC0-1.0",
        "CC-BY-4.0",
        "CC-BY-SA-4.0",
        "U.S. Government Work",
        "ODC-By-1.0",
        "ODbL-1.0",
    }
)

REJECTED_LICENSE_MARKERS: frozenset[str] = frozenset(
    {
        "proprietary",
        "paid-only",
        "hosted-only",
        "noncommercial",
        "non-commercial",
        "cc-by-nc",
        "cc-by-nc-sa",
        "source-available-not-osi",
        "unknown",
        "all-rights-reserved",
        "commercial-only",
        "partnership-gated",
    }
)


@dataclass(frozen=True)
class ArtifactRecord:
    """One shipped or declared artifact with full provenance fields."""

    artifact_id: str
    kind: ArtifactKind
    name: str
    source: str
    version: str
    license: str
    provenance: str
    checksum_policy: str
    redistribution: str
    attribution: str
    required_for_manual_workflow: bool = False
    notes: str = ""
    approval: ApprovalResult = ApprovalResult.UNKNOWN
    rejection_reason: str = ""
    # catalog_denylist rows document forbidden products without failing the build.
    # active rejects (unregistered requirements, incompatible shipped artifacts) fail.
    catalog_denylist: bool = False

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["kind"] = self.kind.value
        data["approval"] = self.approval.value
        return data


@dataclass
class ArtifactInventory:
    """One of the four inventories. Empty is valid when nothing is shipped."""

    kind: ArtifactKind
    artifacts: list[ArtifactRecord] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind.value,
            "count": len(self.artifacts),
            "artifacts": [a.to_dict() for a in self.artifacts],
        }

    @property
    def has_rejection(self) -> bool:
        return any(
            a.approval == ApprovalResult.REJECTED and not a.catalog_denylist
            for a in self.artifacts
        )

    @property
    def has_unknown(self) -> bool:
        return any(a.approval == ApprovalResult.UNKNOWN for a in self.artifacts)


@dataclass
class GateReport:
    """Full evaluation of the exact shipped build across four inventories."""

    build_revision: str
    generated_at: str
    tool_version: str
    inventories: dict[str, ArtifactInventory]
    passed: bool
    failures: list[str] = field(default_factory=list)
    evidence_id: str = "HA-E78"
    reviewer: str = "license-provenance-gate"
    stop_rule: str = (
        "Any unknown, incompatible, proprietary, paid-only, hosted-only, "
        "or noncommercial artifact fails the build. Runtime approval never "
        "approves model artifacts or datasets."
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "build_revision": self.build_revision,
            "generated_at": self.generated_at,
            "tool_version": self.tool_version,
            "result": "pass" if self.passed else "fail",
            "reviewer": self.reviewer,
            "stop_rule": self.stop_rule,
            "failures": list(self.failures),
            "inventories": {
                key: inv.to_dict() for key, inv in self.inventories.items()
            },
            "cross_inventory_rules": {
                "runtime_approves_model_artifacts": False,
                "runtime_approves_datasets": False,
                "model_runtime_approves_weights": False,
            },
            "manual_workflow_requires_model": False,
            "manual_workflow_requires_optional_dataset": False,
        }
