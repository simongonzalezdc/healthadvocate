"""Release gate keeps real-case import disabled on doubt (issue 90)."""

from __future__ import annotations

import unittest
from pathlib import Path

from healthadvocate.governance.release_gate import (
    REQUIRED_EVIDENCE_IDS,
    build_release_bundle,
    real_case_import_enabled,
)

ROOT = Path(__file__).resolve().parents[1]


class ReleaseGateTests(unittest.TestCase):
    def test_import_disabled_without_verifier(self):
        bundle = build_release_bundle(
            ROOT,
            independent_verifier_approved=False,
            real_case_import_override=False,
        )
        self.assertFalse(bundle["real_case_import_enabled"])
        ids = {r["evidence_id"] for r in bundle["receipts"]}
        for eid in REQUIRED_EVIDENCE_IDS:
            self.assertIn(eid, ids)
        ha77 = next(r for r in bundle["receipts"] if r["evidence_id"] == "HA-E77")
        self.assertEqual(ha77["result"], "fail")
        self.assertFalse(bundle["contains_real_phi"])

    def test_import_still_disabled_without_explicit_override(self):
        bundle = build_release_bundle(
            ROOT,
            independent_verifier_approved=True,
            real_case_import_override=False,
        )
        # Verifier approval alone is not enough without explicit override.
        self.assertFalse(real_case_import_enabled(bundle))

    def test_import_enabled_only_with_verifier_and_override_and_all_pass(self):
        bundle = build_release_bundle(
            ROOT,
            independent_verifier_approved=True,
            real_case_import_override=True,
        )
        self.assertTrue(bundle["real_case_import_enabled"])

    def test_failed_receipt_blocks_import(self):
        bundle = build_release_bundle(
            ROOT,
            independent_verifier_approved=True,
            real_case_import_override=True,
        )
        for rec in bundle["receipts"]:
            if rec["evidence_id"] == "HA-E72":
                rec["result"] = "fail"
        self.assertFalse(real_case_import_enabled(bundle))

    def test_skipped_or_waived_blocks_import(self):
        bundle = build_release_bundle(
            ROOT,
            independent_verifier_approved=True,
            real_case_import_override=True,
        )
        bundle["receipts"][0]["waived"] = True
        self.assertFalse(real_case_import_enabled(bundle))


if __name__ == "__main__":
    unittest.main()
