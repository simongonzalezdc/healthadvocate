"""Encrypted synthetic Coverage Case tests (issue 81)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from healthadvocate.coverage.domain import (
    CaseLifecycle,
    ClaimClass,
    ContactEvent,
    EvidenceItem,
    FactStatus,
    new_id,
    utc_now_iso,
)
from healthadvocate.coverage.keystore import InMemoryKeyStore, KeyStoreError
from healthadvocate.coverage.store import CaseStore, CaseStoreError

CANARY = "CANARY_PATIENT_ALPHA_9f3c"
CANARY_MEMBER = "MEMBER-ID-SYNTH-42"


class CoverageCaseStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "cases.haenc"
        self.keystore = InMemoryKeyStore()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _store(self, *, create: bool = True, keystore=None) -> CaseStore:
        return CaseStore(
            self.path,
            keystore or self.keystore,
            create=create or not self.path.exists(),
        )

    def test_create_update_read_resume_synthetic_case(self):
        store = self._store()
        case = store.create_case(
            "Synthetic COBRA loss",
            next_action="Call county about Medi-Cal intake",
        )
        self.assertTrue(case.synthetic)
        self.assertEqual(case.lifecycle, CaseLifecycle.DRAFT)
        self.assertEqual(case.next_action, "Call county about Medi-Cal intake")

        store.add_target(case.case_id, kind="provider", name="Dr Synthetic")
        store.add_target(case.case_id, kind="medication", name="Synthastatin")
        store.add_evidence(
            case.case_id,
            title="HR termination notice",
            source="user-upload",
            summary=f"Coverage ends; ref {CANARY_MEMBER}",
            claim_class=ClaimClass.USER_REPORTED.value,
        )
        store.add_contact(
            case.case_id,
            channel="phone",
            party="County eligibility",
            summary="Left voicemail",
        )
        store.add_fact(
            case.case_id,
            label="coverage_end_date",
            value="2026-08-31",
            status=FactStatus.USER_REPORTED.value,
            provenance="user entry",
        )
        updated = store.update_case(
            case.case_id,
            lifecycle="active",
            next_action="Gather paystubs for application",
            deadlines=[{"label": "Medi-Cal docs", "due": "2026-09-15"}],
        )
        self.assertEqual(updated.lifecycle, CaseLifecycle.ACTIVE)
        self.assertEqual(len(updated.evidence), 1)
        self.assertEqual(len(updated.contacts), 1)
        self.assertEqual(len(updated.targets), 2)
        fact = updated.facts[0]
        self.assertEqual(fact.status, FactStatus.USER_REPORTED)
        self.assertTrue(fact.provenance)
        self.assertTrue(fact.observed_at)
        self.assertTrue(fact.retrieved_at)

        store.close()

        # Resume from encrypted file with same key.
        resumed = CaseStore(self.path, self.keystore, create=False)
        loaded = resumed.get_case(case.case_id)
        self.assertEqual(loaded.case_id, case.case_id)
        self.assertEqual(loaded.next_action, "Gather paystubs for application")
        self.assertEqual(len(loaded.evidence), 1)
        self.assertEqual(len(loaded.contacts), 1)
        resumed.close()

    def test_evidence_immutable_and_contacts_append_only(self):
        store = self._store()
        case = store.create_case("Immutability case")
        store.add_evidence(
            case.case_id,
            title="E1",
            source="user",
            summary="first",
        )
        loaded = store.get_case(case.case_id)
        item = loaded.evidence[0]
        with self.assertRaises(RuntimeError):
            loaded.replace_evidence(item)
        with self.assertRaises(ValueError):
            loaded.add_evidence(item)  # duplicate id
        event = ContactEvent(
            event_id=new_id("ce"),
            occurred_at=utc_now_iso(),
            channel="email",
            party="HR",
            summary="sent",
        )
        loaded.add_contact(event)
        with self.assertRaises(RuntimeError):
            loaded.update_contact(event)
        with self.assertRaises(ValueError):
            loaded.add_contact(event)

    def test_plaintext_canary_absent_from_encrypted_bytes(self):
        store = self._store()
        case = store.create_case("Canary case")
        store.add_evidence(
            case.case_id,
            title="Notice",
            source="user",
            summary=f"Patient {CANARY} member {CANARY_MEMBER}",
        )
        store.add_fact(
            case.case_id,
            label="member_id",
            value=CANARY_MEMBER,
            provenance="synthetic fixture",
        )
        store.close()

        raw = self.path.read_bytes()
        self.assertTrue(raw.startswith(b"HAC1"))
        self.assertNotIn(CANARY.encode("utf-8"), raw)
        self.assertNotIn(CANARY_MEMBER.encode("utf-8"), raw)
        # Also ensure no obvious plaintext JSON markers of the canary label.
        self.assertNotIn(b"coverage_cases", raw)

    def test_missing_key_fails_before_metadata(self):
        store = self._store()
        case = store.create_case("Key fail case", next_action="Do something")
        store.close()

        empty_ks = InMemoryKeyStore()  # no key
        with self.assertRaises(CaseStoreError) as ctx:
            CaseStore(self.path, empty_ks, create=False)
        self.assertIn("key", str(ctx.exception).lower())

    def test_wrong_key_fails_before_metadata(self):
        store = self._store()
        store.create_case("Wrong key case")
        store.close()

        wrong = InMemoryKeyStore(key=b"\x11" * 32)
        with self.assertRaises(CaseStoreError):
            CaseStore(self.path, wrong, create=False)

    def test_real_case_creation_blocked(self):
        store = self._store()
        with self.assertRaises(CaseStoreError):
            store.create_case("real", synthetic=False)


class PublicServiceWorkflowTests(unittest.TestCase):
    def test_service_create_and_resume(self):
        from healthadvocate.coverage.service import (
            create_synthetic_case,
            get_case,
            resume_case,
            update_case,
        )
        from healthadvocate.coverage.store import CaseStore

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "svc.haenc"
            ks = InMemoryKeyStore()
            store = CaseStore(path, ks, create=True)
            created = create_synthetic_case("Svc case", store=store)
            updated = update_case(
                created["case_id"],
                lifecycle="active",
                next_action="Collect documents",
                store=store,
            )
            self.assertEqual(updated["lifecycle"], "active")
            resumed = resume_case(created["case_id"], store=store)
            self.assertTrue(resumed["resumed"])
            self.assertEqual(resumed["next_action"], "Collect documents")
            loaded = get_case(created["case_id"], store=store)
            for fact in loaded.get("facts", []):
                self.assertIn("status", fact)
                self.assertIn("provenance", fact)
                self.assertIn("observed_at", fact)
            store.close()


if __name__ == "__main__":
    unittest.main()
