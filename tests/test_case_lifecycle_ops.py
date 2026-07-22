"""Export/redact/delete/recovery tests (issue 87)."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from healthadvocate.coverage.keystore import InMemoryKeyStore
from healthadvocate.coverage.lifecycle_ops import (
    delete_case,
    private_export,
    redacted_export,
    rotate_store_key,
    write_export,
)
from healthadvocate.coverage.store import CaseStore, CaseStoreError

CANARY = "CANARY_PATIENT_ALPHA_9f3c"
MEMBER = "MEMBER-ID-SYNTH-42"


class LifecycleOpsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "cases.haenc"
        self.ks = InMemoryKeyStore()
        self.store = CaseStore(self.path, self.ks, create=True)
        self.case = self.store.create_case("Lifecycle case")
        self.store.add_evidence(
            self.case.case_id,
            title="Notice",
            source="user",
            summary=f"Patient {CANARY} {MEMBER} ssn 000-00-0000",
        )
        self.store.add_fact(
            self.case.case_id,
            label="member_id",
            value=MEMBER,
            provenance="synthetic",
        )
        self.case = self.store.get_case(self.case.case_id)

    def tearDown(self) -> None:
        self.store.close()
        self.tmp.cleanup()

    def test_private_and_redacted_exports_distinct(self):
        priv = private_export(self.case)
        red = redacted_export(self.case)
        self.assertEqual(priv["mode"], "private")
        self.assertEqual(red["mode"], "redacted")
        self.assertIsNone(priv["residual_risk_warning"])
        self.assertIn("not a guarantee", red["residual_risk_warning"])
        priv_blob = json.dumps(priv)
        red_blob = json.dumps(red)
        self.assertIn(CANARY, priv_blob)
        self.assertNotIn(CANARY, red_blob)
        self.assertNotIn(MEMBER, red_blob)
        self.assertIn("[REDACTED", red_blob)

    def test_export_requires_review(self):
        payload = private_export(self.case)
        dest = Path(self.tmp.name) / "out.json"
        with self.assertRaises(CaseStoreError):
            write_export(payload, dest, reviewed=False)
        write_export(payload, dest, reviewed=True)
        self.assertTrue(dest.is_file())

    def test_delete_reports_unowned_sources(self):
        unowned = ["/not/owned/source.pdf"]
        result = delete_case(
            self.store,
            self.case.case_id,
            unowned_source_paths=unowned,
        )
        self.assertTrue(result["application_owned_removed"])
        self.assertEqual(result["unowned_sources_reported"], unowned)
        self.assertFalse(result["unowned_sources_deleted"])
        with self.assertRaises(CaseStoreError):
            self.store.get_case(self.case.case_id)

    def test_key_rotation_preserves_data(self):
        case_id = self.case.case_id
        rotate_store_key(self.store)
        self.store.close()
        reopened = CaseStore(self.path, self.ks, create=False)
        loaded = reopened.get_case(case_id)
        self.assertEqual(loaded.case_id, case_id)
        reopened.close()


if __name__ == "__main__":
    unittest.main()
