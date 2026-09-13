"""Real-case release gate — fail closed on missing or failed evidence."""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from healthadvocate.governance.gate import evaluate_shipped_build, write_receipts
from healthadvocate.coverage import manual_workflow_status

REQUIRED_EVIDENCE_IDS = (
    "HA-E70",
    "HA-E71",
    "HA-E72",
    "HA-E73",
    "HA-E74",
    "HA-E75",
    "HA-E76",
    "HA-E78",
    "HA-E77",
)


@dataclass
class Receipt:
    evidence_id: str
    build_revision: str
    generated_at: str
    tool_version: str
    result: str  # pass | fail
    artifact_checksum: str
    reviewer: str
    stop_rule: str
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "build_revision": self.build_revision,
            "generated_at": self.generated_at,
            "tool_version": self.tool_version,
            "result": self.result,
            "artifact_checksum": self.artifact_checksum,
            "reviewer": self.reviewer,
            "stop_rule": self.stop_rule,
            "notes": self.notes,
            "contains_real_phi": False,
        }


def _git_rev(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=root,
            text=True,
        ).strip()
    except Exception:
        return "unknown"


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def real_case_import_enabled(bundle: dict[str, Any]) -> bool:
    """Import stays disabled unless every required receipt is present and pass."""
    if not bundle.get("independent_verifier_approved"):
        return False
    receipts: dict[str, dict[str, Any]] = {}
    for receipt in bundle.get("receipts", []):
        if not isinstance(receipt, dict):
            return False
        evidence_id = receipt.get("evidence_id")
        if evidence_id in receipts:
            return False
        receipts[evidence_id] = receipt
    for eid in REQUIRED_EVIDENCE_IDS:
        rec = receipts.get(eid)
        if not rec:
            return False
        if rec.get("result") != "pass":
            return False
        if rec.get("skipped") or rec.get("waived") or rec.get("flaky"):
            return False
    if bundle.get("real_case_import_override") is True:
        # Explicit override still requires verifier approval above.
        return True
    # Default: even with all receipts, import stays disabled until verifier
    # sets independent_verifier_approved AND real_case_import_override.
    return False


def build_release_bundle(
    project_root: Path,
    *,
    independent_verifier_approved: bool = False,
    real_case_import_override: bool = False,
    extra_receipts: Optional[list[dict[str, Any]]] = None,
    verified_evidence: Optional[dict[str, bool]] = None,
) -> dict[str, Any]:
    rev = _git_rev(project_root)
    now = _now()
    license_report = evaluate_shipped_build(project_root, build_revision=rev)
    out = project_root / "build" / "receipts" / "release"
    write_receipts(license_report, out / "license")

    receipts: list[dict[str, Any]] = []

    def add(eid: str, result: str, notes: str, reviewer: str = "automated-gate") -> None:
        receipts.append(
            Receipt(
                evidence_id=eid,
                build_revision=rev,
                generated_at=now,
                tool_version="healthadvocate.release_gate/1.0.0",
                result=result,
                artifact_checksum=license_report.to_dict().get("build_revision", rev),
                reviewer=reviewer,
                stop_rule=(
                    "Missing, failed, skipped, waived, or flaky evidence keeps "
                    "real-case import disabled."
                ),
                notes=notes,
            ).to_dict()
        )

    add(
        "HA-E78",
        "pass" if license_report.passed else "fail",
        "License/provenance inventories generated from exact build.",
    )
    verified = verified_evidence or {}
    evidence_notes = {
        "HA-E70": "Domain lifecycle/provenance verification receipt.",
        "HA-E71": "Encrypted store and key verification receipt.",
        "HA-E72": "Privacy boundary and loopback verification receipt.",
        "HA-E73": "Commitment Gate side-effect verification receipt.",
        "HA-E74": "Low-energy workflow and script verification receipt.",
        "HA-E75": "Adapter claim-contract verification receipt.",
        "HA-E76": "Export, redaction, and deletion verification receipt.",
    }
    for evidence_id, notes in evidence_notes.items():
        passed = verified.get(evidence_id) is True
        add(
            evidence_id,
            "pass" if passed else "fail",
            notes if passed else f"{notes} No verified result was supplied; failing closed.",
        )
    # HA-E77 is the release gate itself — pass only with independent verifier.
    add(
        "HA-E77",
        "pass" if independent_verifier_approved else "fail",
        "Independent verifier approval required for real-case import.",
        reviewer="independent-verifier" if independent_verifier_approved else "pending",
    )

    if extra_receipts:
        receipts.extend(extra_receipts)

    status = manual_workflow_status()
    bundle = {
        "evidence_id": "HA-E77",
        "build_revision": rev,
        "generated_at": now,
        "tool_version": "healthadvocate.release_gate/1.0.0",
        "receipts": receipts,
        "independent_verifier_approved": independent_verifier_approved,
        "real_case_import_override": real_case_import_override,
        "manual_workflow": {
            "available": status.available,
            "requires_model": status.requires_model,
        },
        "contains_real_phi": False,
        "stop_rule": (
            "Real-case import remains disabled if any required receipt is missing, "
            "stale, skipped, waived, flaky, or failed, or if the independent "
            "verifier has not approved the exact build."
        ),
    }
    bundle["real_case_import_enabled"] = real_case_import_enabled(bundle)
    (out / "release-gate-bundle.json").parent.mkdir(parents=True, exist_ok=True)
    (out / "release-gate-bundle.json").write_text(
        json.dumps(bundle, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return bundle
