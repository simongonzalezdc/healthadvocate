"""Fail-closed license and provenance gate for the exact shipped build."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from healthadvocate.governance.inventory import build_all_inventories
from healthadvocate.governance.models import (
    ApprovalResult,
    ArtifactInventory,
    ArtifactKind,
    GateReport,
)
from healthadvocate.governance.registry import TOOL_VERSION


def _git_revision(project_root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=project_root,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip() or "unknown"
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _collect_failures(inventories: dict[str, ArtifactInventory]) -> list[str]:
    failures: list[str] = []
    for inv in inventories.values():
        for artifact in inv.artifacts:
            if artifact.catalog_denylist:
                # Permanent denylist rows are evidence, not shipped failures.
                continue
            if artifact.approval == ApprovalResult.REJECTED:
                failures.append(
                    f"[{inv.kind.value}] {artifact.artifact_id}: "
                    f"{artifact.rejection_reason or 'rejected'}"
                )
            elif artifact.approval == ApprovalResult.UNKNOWN:
                failures.append(
                    f"[{inv.kind.value}] {artifact.artifact_id}: unknown approval state"
                )
    return failures


def _manual_workflow_intact(inventories: dict[str, ArtifactInventory]) -> list[str]:
    """Manual Coverage workflow must not hard-require models or optional datasets."""
    failures: list[str] = []

    for artifact in inventories[ArtifactKind.MODEL_ARTIFACT.value].artifacts:
        if artifact.required_for_manual_workflow:
            failures.append(
                "manual Coverage workflow must not require a model artifact; "
                f"found required {artifact.artifact_id}"
            )

    for artifact in inventories[ArtifactKind.MODEL_RUNTIME.value].artifacts:
        if artifact.required_for_manual_workflow:
            failures.append(
                f"model runtime {artifact.artifact_id} must not be required "
                "for the manual Coverage workflow"
            )

    for artifact in inventories[ArtifactKind.DATASET.value].artifacts:
        if artifact.required_for_manual_workflow:
            failures.append(
                f"dataset {artifact.artifact_id} is marked required_for_manual_workflow; "
                "manual path must work with optional datasets disabled"
            )

    return failures


def _cross_inventory_rules(inventories: dict[str, ArtifactInventory]) -> list[str]:
    """Runtime approval must never silently approve model artifacts or datasets."""
    failures: list[str] = []
    approved_runtimes = [
        a
        for a in inventories[ArtifactKind.MODEL_RUNTIME.value].artifacts
        if a.approval == ApprovalResult.APPROVED
    ]
    # Even if a runtime is approved, every model artifact and dataset must still
    # carry its own approval result. Unknown/rejected artifacts already fail via
    # _collect_failures. Here we only guard against an empty model inventory
    # being treated as "approved because a runtime exists".
    model_artifacts = inventories[ArtifactKind.MODEL_ARTIFACT.value].artifacts
    if approved_runtimes and not model_artifacts:
        failures.append(
            "approved model runtime present but model-artifact inventory is empty; "
            "declare each weight/tokenizer/template/conversion/quantization or an "
            "explicit not_shipped placeholder"
        )
    return failures


def evaluate_shipped_build(
    project_root: Path,
    registry_path: Path | None = None,
    build_revision: str | None = None,
) -> GateReport:
    inventories = build_all_inventories(project_root, registry_path=registry_path)
    failures = _collect_failures(inventories)
    failures.extend(_manual_workflow_intact(inventories))
    failures.extend(_cross_inventory_rules(inventories))

    return GateReport(
        build_revision=build_revision or _git_revision(project_root),
        generated_at=_utc_now(),
        tool_version=TOOL_VERSION,
        inventories=inventories,
        passed=not failures,
        failures=failures,
    )


def generate_attribution(report: GateReport) -> str:
    lines = [
        "# HealthAdvocate attribution report",
        "",
        f"Evidence ID: {report.evidence_id}",
        f"Build revision: {report.build_revision}",
        f"Generated at: {report.generated_at}",
        f"Gate result: {'pass' if report.passed else 'fail'}",
        "",
        "Inventories are separate. Approving a model runtime does not approve",
        "model weights, tokenizers, templates, conversions, quantizations, or datasets.",
        "",
    ]
    titles = {
        ArtifactKind.APPLICATION_PACKAGE.value: "Application / runtime packages",
        ArtifactKind.MODEL_RUNTIME.value: "Model runtimes",
        ArtifactKind.MODEL_ARTIFACT.value: "Model artifacts",
        ArtifactKind.DATASET.value: "Datasets",
    }
    for key, title in titles.items():
        inv = report.inventories[key]
        lines.append(f"## {title}")
        lines.append("")
        if not inv.artifacts:
            lines.append("_None declared._")
            lines.append("")
            continue
        for artifact in inv.artifacts:
            lines.append(
                f"- **{artifact.name}** (`{artifact.artifact_id}`) — "
                f"version `{artifact.version}`, license `{artifact.license}`, "
                f"approval `{artifact.approval.value}`"
            )
            lines.append(f"  - Source: {artifact.source}")
            lines.append(f"  - Provenance: {artifact.provenance}")
            lines.append(f"  - Checksum policy: {artifact.checksum_policy}")
            lines.append(f"  - Redistribution: {artifact.redistribution}")
            lines.append(f"  - Attribution: {artifact.attribution}")
            if artifact.rejection_reason:
                lines.append(f"  - Rejection: {artifact.rejection_reason}")
        lines.append("")
    lines.append("## PHI notice")
    lines.append("")
    lines.append(
        "This receipt is generated from package metadata only and must never "
        "contain real PHI, personal identifiers, or case content."
    )
    lines.append("")
    return "\n".join(lines)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_receipts(
    report: GateReport,
    output_dir: Path,
) -> dict[str, Path]:
    """Write PHI-free license inventories and attribution receipts."""
    output_dir.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}

    report_path = output_dir / "license-provenance-gate.json"
    report_bytes = json.dumps(report.to_dict(), indent=2, sort_keys=True).encode(
        "utf-8"
    )
    report_path.write_bytes(report_bytes)
    written["gate_report"] = report_path

    for key, inv in report.inventories.items():
        inv_path = output_dir / f"inventory-{key}.json"
        inventory_ok = not inv.has_rejection and not inv.has_unknown
        payload = {
            "evidence_id": report.evidence_id,
            "build_revision": report.build_revision,
            "generated_at": report.generated_at,
            "tool_version": report.tool_version,
            "result": "pass" if inventory_ok else "fail",
            "reviewer": report.reviewer,
            "stop_rule": report.stop_rule,
            "inventory": inv.to_dict(),
            "artifact_checksum": _sha256_bytes(
                json.dumps(inv.to_dict(), sort_keys=True).encode("utf-8")
            ),
        }
        inv_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        written[f"inventory_{key}"] = inv_path

    attribution = generate_attribution(report)
    attr_path = output_dir / "ATTRIBUTION.md"
    attr_path.write_text(attribution, encoding="utf-8")
    written["attribution"] = attr_path

    envelope = {
        "evidence_id": report.evidence_id,
        "build_revision": report.build_revision,
        "generated_at": report.generated_at,
        "tool_version": report.tool_version,
        "result": "pass" if report.passed else "fail",
        "reviewer": report.reviewer,
        "stop_rule": report.stop_rule,
        "artifact_checksum": _sha256_bytes(report_bytes),
        "artifact_path": str(report_path.name),
        "contains_real_phi": False,
        "failures": report.failures,
    }
    env_path = output_dir / "receipt-license-attribution.json"
    env_path.write_text(json.dumps(envelope, indent=2, sort_keys=True) + "\n")
    written["receipt"] = env_path
    return written


def assert_no_phi_markers(text: str, canaries: list[str]) -> None:
    lowered = text.lower()
    for canary in canaries:
        if canary.lower() in lowered:
            raise AssertionError(
                f"synthetic canary {canary!r} leaked into license receipt"
            )
