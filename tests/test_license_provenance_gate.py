"""Behavior tests for the open license and provenance gate (issue 79)."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from healthadvocate.coverage import manual_workflow_status
from healthadvocate.governance.gate import (
    assert_no_phi_markers,
    evaluate_shipped_build,
    generate_attribution,
    write_receipts,
)
from healthadvocate.governance.models import ApprovalResult, ArtifactKind
from healthadvocate.governance.registry import approve_record, load_registry
from healthadvocate.governance.models import ArtifactRecord

ROOT = Path(__file__).resolve().parents[1]

# Synthetic canaries only — never real PHI.
SYNTHETIC_CANARIES = [
    "CANARY_PATIENT_ALPHA_9f3c",
    "SSN-000-00-0000",
    "MEMBER-ID-SYNTH-42",
]


class LicenseProvenanceGateTests(unittest.TestCase):
    def test_shipped_build_produces_four_separate_inventories(self):
        report = evaluate_shipped_build(ROOT, build_revision="test-rev")
        self.assertEqual(
            set(report.inventories),
            {
                ArtifactKind.APPLICATION_PACKAGE.value,
                ArtifactKind.MODEL_RUNTIME.value,
                ArtifactKind.MODEL_ARTIFACT.value,
                ArtifactKind.DATASET.value,
            },
        )
        for inv in report.inventories.values():
            self.assertGreaterEqual(len(inv.artifacts), 1)
            for artifact in inv.artifacts:
                self.assertTrue(artifact.source or artifact.approval == ApprovalResult.REJECTED)
                self.assertTrue(artifact.version)
                self.assertTrue(artifact.license)
                # Provenance + checksum required on approved/not_shipped declared items
                if artifact.approval in {
                    ApprovalResult.APPROVED,
                    ApprovalResult.NOT_SHIPPED,
                }:
                    self.assertTrue(artifact.provenance)
                    self.assertTrue(artifact.checksum_policy)
                self.assertIn(
                    artifact.approval,
                    {
                        ApprovalResult.APPROVED,
                        ApprovalResult.NOT_SHIPPED,
                        ApprovalResult.REJECTED,
                    },
                )

    def test_catalog_denylist_rows_remain_visible_but_do_not_block_gate(self):
        report = evaluate_shipped_build(ROOT, build_revision="test-rev")
        denylist = [
            a
            for inv in report.inventories.values()
            for a in inv.artifacts
            if a.catalog_denylist
        ]
        self.assertGreaterEqual(len(denylist), 2)
        self.assertTrue(
            any(a.artifact_id == "dataset-goodrx" for a in denylist),
        )
        self.assertTrue(
            any(a.artifact_id == "runtime-lm-studio" for a in denylist),
        )
        self.assertTrue(report.passed, msg=report.failures)

    def test_runtime_approval_does_not_approve_model_artifacts(self):
        report = evaluate_shipped_build(ROOT, build_revision="test-rev")
        payload = report.to_dict()
        self.assertFalse(payload["cross_inventory_rules"]["runtime_approves_model_artifacts"])
        self.assertFalse(payload["cross_inventory_rules"]["runtime_approves_datasets"])
        self.assertFalse(payload["cross_inventory_rules"]["model_runtime_approves_weights"])

        # No shipped model artifact is approved merely because runtimes exist.
        for artifact in report.inventories[ArtifactKind.MODEL_ARTIFACT.value].artifacts:
            self.assertNotEqual(
                artifact.approval,
                ApprovalResult.APPROVED,
                msg="core path must not ship approved model artifacts yet",
            )

    def test_unknown_and_proprietary_artifacts_fail_approval(self):
        bad = ArtifactRecord(
            artifact_id="pkg-bad",
            kind=ArtifactKind.APPLICATION_PACKAGE,
            name="closed-sdk",
            source="https://example.invalid/closed",
            version="1.0.0",
            license="proprietary",
            provenance="test",
            checksum_policy="sha256",
            redistribution="none",
            attribution="closed",
        )
        approved = approve_record(bad)
        self.assertEqual(approved.approval, ApprovalResult.REJECTED)

        noncommercial = ArtifactRecord(
            artifact_id="data-nc",
            kind=ArtifactKind.DATASET,
            name="nc-data",
            source="https://example.invalid/nc",
            version="1.0.0",
            license="CC-BY-NC-4.0",
            provenance="test",
            checksum_policy="sha256",
            redistribution="none",
            attribution="nc",
        )
        self.assertEqual(approve_record(noncommercial).approval, ApprovalResult.REJECTED)

        unknown = ArtifactRecord(
            artifact_id="pkg-unknown",
            kind=ArtifactKind.APPLICATION_PACKAGE,
            name="mystery",
            source="https://example.invalid/mystery",
            version="1.0.0",
            license="unknown",
            provenance="test",
            checksum_policy="sha256",
            redistribution="none",
            attribution="mystery",
        )
        self.assertEqual(approve_record(unknown).approval, ApprovalResult.REJECTED)

        unpinned = ArtifactRecord(
            artifact_id="pkg-latest",
            kind=ArtifactKind.APPLICATION_PACKAGE,
            name="floating",
            source="https://example.invalid/floating",
            version="latest",
            license="MIT",
            provenance="test",
            checksum_policy="sha256",
            redistribution="ok",
            attribution="floating",
        )
        self.assertEqual(approve_record(unpinned).approval, ApprovalResult.REJECTED)

    def test_unregistered_requirement_fails_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            # Minimal project tree with an unregistered dependency.
            (tmp_path / "healthadvocate").mkdir()
            (tmp_path / "healthadvocate" / "requirements.txt").write_text(
                "fastapi>=0.136.3\nsecret-proprietary-sdk==1.2.3\n",
                encoding="utf-8",
            )
            registry_src = (
                ROOT
                / "healthadvocate"
                / "governance"
                / "data"
                / "artifact_registry.json"
            )
            registry_dst = tmp_path / "registry.json"
            shutil.copy(registry_src, registry_dst)
            report = evaluate_shipped_build(
                tmp_path,
                registry_path=registry_dst,
                build_revision="tmp",
            )
            self.assertFalse(report.passed)
            joined = "\n".join(report.failures)
            self.assertIn("secret-proprietary-sdk", joined)

    def test_manual_coverage_workflow_usable_without_model_or_dataset(self):
        status = manual_workflow_status()
        self.assertTrue(status.available)
        self.assertFalse(status.requires_model)
        self.assertFalse(status.requires_optional_dataset)

        report = evaluate_shipped_build(ROOT, build_revision="test-rev")
        self.assertFalse(report.to_dict()["manual_workflow_requires_model"])
        self.assertFalse(report.to_dict()["manual_workflow_requires_optional_dataset"])
        for artifact in report.inventories[ArtifactKind.MODEL_RUNTIME.value].artifacts:
            self.assertFalse(artifact.required_for_manual_workflow)
        for artifact in report.inventories[ArtifactKind.MODEL_ARTIFACT.value].artifacts:
            self.assertFalse(artifact.required_for_manual_workflow)
        for artifact in report.inventories[ArtifactKind.DATASET.value].artifacts:
            self.assertFalse(artifact.required_for_manual_workflow)

    def test_receipts_are_synthetic_and_phi_free(self):
        report = evaluate_shipped_build(ROOT, build_revision="test-rev")
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_receipts(report, Path(tmp))
            combined = []
            for path in paths.values():
                text = path.read_text(encoding="utf-8")
                combined.append(text)
                assert_no_phi_markers(text, SYNTHETIC_CANARIES)
            blob = "\n".join(combined)
            # Ensure canaries were not auto-injected by the gate either.
            for canary in SYNTHETIC_CANARIES:
                self.assertNotIn(canary, blob)
            receipt = json.loads(paths["receipt"].read_text(encoding="utf-8"))
            self.assertEqual(receipt["evidence_id"], "HA-E78")
            self.assertIn(receipt["result"], {"pass", "fail"})
            self.assertFalse(receipt["contains_real_phi"])
            self.assertIn("artifact_checksum", receipt)
            self.assertTrue(receipt["tool_version"])
            self.assertTrue(receipt["generated_at"])
            self.assertTrue(receipt["build_revision"])
            self.assertTrue(receipt["stop_rule"])
            attribution = generate_attribution(report)
            self.assertIn("Application / runtime packages", attribution)
            self.assertIn("Model runtimes", attribution)
            self.assertIn("Model artifacts", attribution)
            self.assertIn("Datasets", attribution)

    def test_registry_loads_and_lists_forbidden_products(self):
        registry = load_registry()
        self.assertEqual(registry["evidence_id"], "HA-E78")
        forbidden = set(registry["forbidden_requirement_names"])
        self.assertIn("goodrx", forbidden)
        # Confirms issue 78 denylist is encoded for the gate.
        names = {
            entry["name"].lower()
            for entry in registry["datasets"] + registry["model_runtimes"]
        }
        self.assertIn("goodrx", names)
        self.assertIn("lm studio", names)


class CatalogRejectPolicyTests(unittest.TestCase):
    """Catalog denylist rows must not fail the build by themselves."""

    def test_gate_ignores_catalog_only_rejects_for_pass_fail(self):
        # After inventory policy: shipped_status=rejected is denylist evidence
        # and must not appear in failures. Only active shipped/unregistered
        # rejects fail.
        report = evaluate_shipped_build(ROOT, build_revision="test-rev")
        for failure in report.failures:
            self.assertNotIn("goodrx", failure.lower())
            self.assertNotIn("lm studio", failure.lower())
            self.assertNotIn("runtime-lm-studio", failure.lower())
            self.assertNotIn("dataset-goodrx", failure.lower())
        self.assertTrue(
            report.passed,
            msg=f"expected clean gate on current registry, failures={report.failures}",
        )


if __name__ == "__main__":
    unittest.main()
