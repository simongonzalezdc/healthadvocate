"""Wave 2a contract tests: opt-in policy profiles + audit receipts (RALPLAN row 4).

Scope (docs/OPENMED-UPSTREAM-LEVERAGE-2026-09-17.md line 116, selective
adoption): ``HealthEngine.deidentify_for_llm_result`` gains an OPT-IN
``policy`` kwarg threaded to ``openmed.deidentify(..., policy=...)``. The
default path (``policy=None``) must stay byte-identical to the pre-wave
behavior. Permitted policies are pinned constants enumerated from the
installed openmed 2.5.0 (openmed/core/policy.py ``PolicyName``: 20 canonical
values, verified 2026-09-22); unknown names fail closed.

Audit contract reality in openmed 2.5.0 (openmed/core/pii.py): the
``DeidentificationResult.audit_report`` field is populated only under
``audit=True`` (pii.py:2338-2341), and then the top-level ``deidentify``
returns the bare ``AuditReport`` instead of the result object (pii.py:2866-
2867). HA therefore never passes ``audit=True`` (it would destroy the
deidentified-text return) and instead duck-types: a policy run passes only
when the returned object carries a verifiable ``audit_report``. Against the
stock 2.5.0 top-level API that means policy runs fail closed with
``policy_audit_missing`` — the pass leg is proven here with a fake result
object carrying a REAL AuditReport built by the upstream builder
(``openmed.core.pii._build_audit_report``), exactly the way the upstream API
builds it.

Fail-closed posture is sacred: every failure leg returns
``DEIDENTIFICATION_FAILED_PLACEHOLDER`` through the existing boundary path
and writes a text-free governance receipt into the HA-E78 ledger.

Synthetic inputs only. No model loads: ``openmed.deidentify`` is patched in
every test that reaches the engine.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import openmed
from openmed.core import pii as openmed_pii
from openmed.core.pii import PIIEntity

from healthadvocate.core.engine import HealthEngine
from healthadvocate.privacy.boundary import (
    DEIDENTIFICATION_FAILED_PLACEHOLDER,
    DeidentificationResult,
    DeidentificationStatus,
)

CANARY = "CANARY_PATIENT_OMEGA_7c1d"

SYNTH_INPUT = "Patient Rio Synth-Case called about metformin on 2026-09-01."
SYNTH_SAFE_TEXT = "Patient [NAME] called about metformin on [DATE]."
SYNTH_MAPPING = {"[NAME]": "Rio Synth-Case", "[DATE]": "2026-09-01"}

# Pinned pre-Wave-2a default-path behavior, captured against the unmodified
# engine on 2026-09-22 (worktree healthadvocate-pm-verify-20260917):
PINNED_ASSEMBLED = SYNTH_INPUT  # no profile/metadata/notes sections
PINNED_RESULT = DeidentificationResult(
    status=DeidentificationStatus.SUCCESS,
    safe_text=SYNTH_SAFE_TEXT,
    mapping=dict(SYNTH_MAPPING),
    error_code="",
)


def build_real_audit_report(policy: str):
    """Build a real openmed AuditReport via the upstream builder.

    Uses ``openmed.core.pii._build_audit_report`` — the exact function the
    upstream ``deidentify(audit=True)`` path calls (pii.py:2340) — so every
    field (hashes, spans, thresholds, residual risk) is real, not hand-rolled.
    """
    entity = PIIEntity(
        text="Rio Synth-Case",
        label="NAME",
        start=8,
        end=21,
        confidence=0.98,
        redacted_text="[NAME]",
        canonical_label="NAME",
        sources=["ml"],
        threshold=0.7,
        action="mask",
    )
    return openmed_pii._build_audit_report(
        original_text=SYNTH_INPUT,
        deidentified_text=SYNTH_SAFE_TEXT,
        pii_result=None,
        pii_entities=[entity],
        effective_method="mask",
        model_name=openmed_pii._DEFAULT_EN_MODEL,
        confidence_threshold=0.7,
        keep_year=False,
        keep_mapping=True,
        lang="en",
        normalize_accents=None,
        use_smart_merging=True,
        use_safety_sweep=True,
        policy=policy,
    )


class RecordingFake:
    """Fake openmed.deidentify that records calls and returns canned results."""

    def __init__(self, results):
        self.results = list(results)
        self.calls = []

    def __call__(self, text, **kwargs):
        self.calls.append({"text": text, "kwargs": kwargs})
        item = self.results.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def make_engine(fake):
    engine = HealthEngine()
    engine._loader = SimpleNamespace()  # sentinel loader; never constructs ModelLoader
    engine.policy_audit_receipts_dir = None  # set per-test to a tmp dir
    patcher = mock.patch.object(openmed, "deidentify", fake)
    return engine, patcher


def read_receipts(receipts_dir: Path) -> list[dict]:
    files = sorted(p for p in receipts_dir.rglob("*.json") if p.is_file())
    return [json.loads(p.read_text(encoding="utf-8")) for p in files]


class DefaultPathByteIdentity(unittest.TestCase):
    """policy=None must reproduce the pre-wave call and result exactly."""

    def setUp(self):
        self.receipts = Path(tempfile.mkdtemp())
        self.fake = RecordingFake(
            [
                SimpleNamespace(
                    deidentified_text=SYNTH_SAFE_TEXT,
                    mapping=dict(SYNTH_MAPPING),
                    audit_report=None,
                )
            ]
        )
        self.engine, self.patcher = make_engine(self.fake)
        self.engine.policy_audit_receipts_dir = self.receipts
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def test_openmed_call_kwargs_are_exactly_legacy(self):
        self.engine.deidentify_for_llm_result(SYNTH_INPUT)
        self.assertEqual(len(self.fake.calls), 1)
        kwargs = self.fake.calls[0]["kwargs"]
        # Exactly the three legacy keywords — policy must NOT be threaded
        # (not even as policy=None) and audit must never appear.
        self.assertEqual(
            set(kwargs),
            {"method", "loader", "keep_mapping"},
            f"unexpected openmed.deidentify kwargs: {sorted(kwargs)}",
        )
        self.assertEqual(kwargs["method"], "mask")
        self.assertEqual(kwargs["keep_mapping"], True)
        self.assertIs(kwargs["loader"], self.engine.loader)
        self.assertEqual(self.fake.calls[0]["text"], PINNED_ASSEMBLED)

    def test_result_object_identical_to_pinned_snapshot(self):
        result = self.engine.deidentify_for_llm_result(SYNTH_INPUT)
        self.assertEqual(result, PINNED_RESULT)
        self.assertEqual(result.status, DeidentificationStatus.SUCCESS)
        self.assertEqual(result.safe_text, SYNTH_SAFE_TEXT)
        self.assertEqual(dict(result.mapping), SYNTH_MAPPING)
        self.assertEqual(result.error_code, "")
        self.assertTrue(result.allows_model_call)

    def test_default_path_writes_no_receipt(self):
        self.engine.deidentify_for_llm_result(SYNTH_INPUT)
        self.assertEqual(read_receipts(self.receipts), [])


class PolicyAllowlist(unittest.TestCase):
    """The pinned allowlist: canonical openmed 2.5.0 names only."""

    def test_permitted_set_is_pinned_to_openmed_2_5_0_canonical_names(self):
        from healthadvocate.privacy.policy_profiles import PERMITTED_POLICY_PROFILES

        self.assertEqual(
            sorted(PERMITTED_POLICY_PROFILES),
            sorted(
                {
                    "hipaa_safe_harbor",
                    "hipaa_expert_review_assist",
                    "gdpr_pseudonymization",
                    "gdpr_art9_health",
                    "research_limited_dataset",
                    "strict_no_leak",
                    "clinical_minimal_redaction",
                    "clinical_preserve",
                    "canada_pipeda",
                    "uk_ico_anonymisation",
                    "australia_privacy_act",
                    "china_pipl",
                    "india_dpdp_act",
                    "africa_malabo_baseline",
                    "za_popia",
                    "ng_ndpa",
                    "ke_dpa",
                    "india_health_id",
                    "eg_pdpl",
                    "ma_law_09_08",
                }
            ),
        )

    def test_permitted_set_covers_installed_canonical_names(self):
        # Cross-check against the installed package the constants were pinned
        # from: HA must accept exactly the canonical names, no more, no less.
        from openmed.core.policy import CANONICAL_POLICY_NAMES

        from healthadvocate.privacy.policy_profiles import PERMITTED_POLICY_PROFILES

        self.assertEqual(
            frozenset(CANONICAL_POLICY_NAMES), frozenset(PERMITTED_POLICY_PROFILES)
        )

    def test_aliases_are_not_permitted(self):
        from healthadvocate.privacy.policy_profiles import resolve_permitted_policy

        for alias in ("gdpr", "pipeda", "uk_ico", "abha", "au_privacy"):
            self.assertIsNone(resolve_permitted_policy(alias), alias)

    def test_case_variants_and_non_canonical_bundled_names_rejected(self):
        from healthadvocate.privacy.policy_profiles import resolve_permitted_policy

        for name in (
            "HIPAA_SAFE_HARBOR",
            "Strict_No_Leak",
            "fhir_hipaa_safe_harbor",  # bundled data file, not a canonical PolicyName
            "omop_research_limited_dataset",
            "",
            "total_recall_max",
        ):
            self.assertIsNone(resolve_permitted_policy(name), name)

    def test_resolution_returns_canonical_name(self):
        from healthadvocate.privacy import policy_profiles

        self.assertEqual(
            policy_profiles.resolve_permitted_policy("hipaa_safe_harbor"),
            "hipaa_safe_harbor",
        )
        self.assertIsNone(policy_profiles.resolve_permitted_policy(None))


class PermittedPolicyPassThrough(unittest.TestCase):
    """Permitted policy + real verified AuditReport -> success + pass receipt."""

    def setUp(self):
        self.receipts = Path(tempfile.mkdtemp())
        self.report = build_real_audit_report("hipaa_safe_harbor")
        self.fake = RecordingFake(
            [
                SimpleNamespace(
                    deidentified_text=SYNTH_SAFE_TEXT,
                    mapping=dict(SYNTH_MAPPING),
                    audit_report=self.report,
                )
            ]
        )
        self.engine, self.patcher = make_engine(self.fake)
        self.engine.policy_audit_receipts_dir = self.receipts
        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def test_policy_is_threaded_to_openmed_without_audit_flag(self):
        self.engine.deidentify_for_llm_result(SYNTH_INPUT, policy="hipaa_safe_harbor")
        self.assertEqual(len(self.fake.calls), 1)
        kwargs = self.fake.calls[0]["kwargs"]
        self.assertEqual(kwargs.get("policy"), "hipaa_safe_harbor")
        self.assertNotIn("audit", kwargs)
        self.assertEqual(kwargs["method"], "mask")
        self.assertEqual(kwargs["keep_mapping"], True)

    def test_success_result_uses_deidentified_text_and_mapping(self):
        result = self.engine.deidentify_for_llm_result(
            SYNTH_INPUT, policy="hipaa_safe_harbor"
        )
        self.assertEqual(result.status, DeidentificationStatus.SUCCESS)
        self.assertEqual(result.safe_text, SYNTH_SAFE_TEXT)
        self.assertEqual(dict(result.mapping), SYNTH_MAPPING)
        self.assertEqual(result.error_code, "")

    def test_pass_receipt_recorded_in_ledger(self):
        self.engine.deidentify_for_llm_result(SYNTH_INPUT, policy="hipaa_safe_harbor")
        receipts = read_receipts(self.receipts)
        self.assertEqual(len(receipts), 1)
        receipt = receipts[0]
        self.assertEqual(receipt["evidence_id"], "HA-E78")
        self.assertEqual(receipt["policy"], "hipaa_safe_harbor")
        self.assertEqual(receipt["reproducibility_hash"], self.report.repro_hash)
        self.assertTrue(receipt["verification_result"])
        self.assertEqual(receipt["result"], "pass")
        self.assertEqual(receipt["error_code"], "")
        self.assertFalse(receipt["contains_real_phi"])
        self.assertTrue(receipt["build_revision"])

    def test_every_permitted_name_reaches_openmed(self):
        from healthadvocate.privacy.policy_profiles import PERMITTED_POLICY_PROFILES

        for name in sorted(PERMITTED_POLICY_PROFILES):
            fake = RecordingFake(
                [
                    SimpleNamespace(
                        deidentified_text=SYNTH_SAFE_TEXT,
                        mapping=dict(SYNTH_MAPPING),
                        audit_report=build_real_audit_report(name),
                    )
                ]
            )
            engine, patcher = make_engine(fake)
            engine.policy_audit_receipts_dir = self.receipts
            with patcher:
                result = engine.deidentify_for_llm_result(SYNTH_INPUT, policy=name)
            self.assertEqual(result.status, DeidentificationStatus.SUCCESS, name)
            self.assertEqual(fake.calls[0]["kwargs"].get("policy"), name)


class FailClosedLegs(unittest.TestCase):
    """Unknown policy / missing audit / failed verification -> placeholder + receipt."""

    def setUp(self):
        self.receipts = Path(tempfile.mkdtemp())

    def _run(self, policy, fake):
        engine, patcher = make_engine(fake)
        engine.policy_audit_receipts_dir = self.receipts
        with patcher:
            return engine.deidentify_for_llm_result(SYNTH_INPUT, policy=policy)

    def _assert_failed(self, result):
        # The existing deid-failure path: placeholder + the boundary's error
        # code; the wave-specific code is pinned via the receipt and logs.
        self.assertEqual(result.status, DeidentificationStatus.FAILED)
        self.assertEqual(result.safe_text, DEIDENTIFICATION_FAILED_PLACEHOLDER)
        self.assertEqual(result.error_code, "deidentify_engine_failed")
        self.assertFalse(result.allows_model_call)
        self.assertEqual(dict(result.mapping), {})

    def test_unknown_policy_fails_closed_without_calling_openmed(self):
        fake = RecordingFake([])
        result = self._run("total_recall_max", fake)
        self._assert_failed(result)
        self.assertEqual(fake.calls, [])  # never handed to openmed
        receipts = read_receipts(self.receipts)
        self.assertEqual(len(receipts), 1)
        self.assertEqual(receipts[0]["result"], "fail")
        self.assertEqual(receipts[0]["error_code"], "policy_unknown")
        self.assertFalse(receipts[0]["verification_result"])

    def test_alias_policy_also_fails_closed(self):
        fake = RecordingFake([])
        result = self._run("gdpr", fake)
        self.assertEqual(result.status, DeidentificationStatus.FAILED)
        self.assertEqual(fake.calls, [])

    def test_audit_report_missing_fails_closed(self):
        fake = RecordingFake(
            [
                SimpleNamespace(
                    deidentified_text=SYNTH_SAFE_TEXT,
                    mapping=dict(SYNTH_MAPPING),
                    audit_report=None,
                )
            ]
        )
        result = self._run("hipaa_safe_harbor", fake)
        self._assert_failed(result)
        receipts = read_receipts(self.receipts)
        self.assertEqual(receipts[0]["result"], "fail")
        self.assertEqual(receipts[0]["error_code"], "policy_audit_missing")

    def test_audit_verification_failure_fails_closed(self):
        report = build_real_audit_report("hipaa_safe_harbor")
        report.policy = "strict_no_leak"  # tamper post-construction: hash mismatch
        fake = RecordingFake(
            [
                SimpleNamespace(
                    deidentified_text=SYNTH_SAFE_TEXT,
                    mapping=dict(SYNTH_MAPPING),
                    audit_report=report,
                )
            ]
        )
        result = self._run("hipaa_safe_harbor", fake)
        self._assert_failed(result)
        receipts = read_receipts(self.receipts)
        self.assertEqual(receipts[0]["result"], "fail")
        self.assertEqual(receipts[0]["error_code"], "policy_audit_verification_failed")
        self.assertFalse(receipts[0]["verification_result"])
        self.assertEqual(receipts[0]["reproducibility_hash"], report.repro_hash)

    def test_verification_exception_fails_closed(self):
        broken = SimpleNamespace(
            repro_hash="sha256:broken",
            repro_hash_matches=self._raise_value_error,
        )
        fake = RecordingFake(
            [
                SimpleNamespace(
                    deidentified_text=SYNTH_SAFE_TEXT,
                    mapping=dict(SYNTH_MAPPING),
                    audit_report=broken,
                )
            ]
        )
        result = self._run("strict_no_leak", fake)
        self.assertEqual(result.status, DeidentificationStatus.FAILED)
        self.assertEqual(result.safe_text, DEIDENTIFICATION_FAILED_PLACEHOLDER)

    def test_pass_leg_receipt_write_failure_fails_closed(self):
        report = build_real_audit_report("hipaa_safe_harbor")
        fake = RecordingFake(
            [
                SimpleNamespace(
                    deidentified_text=SYNTH_SAFE_TEXT,
                    mapping=dict(SYNTH_MAPPING),
                    audit_report=report,
                )
            ]
        )
        engine, patcher = make_engine(fake)
        # A file where the receipts directory should be: writes must fail.
        blocker = self.receipts / "blocked"
        blocker.write_text("not a dir", encoding="utf-8")
        engine.policy_audit_receipts_dir = blocker
        with patcher:
            result = engine.deidentify_for_llm_result(
                SYNTH_INPUT, policy="hipaa_safe_harbor"
            )
        self.assertEqual(result.status, DeidentificationStatus.FAILED)
        self.assertEqual(result.safe_text, DEIDENTIFICATION_FAILED_PLACEHOLDER)
        self.assertEqual(result.error_code, "deidentify_engine_failed")

    def test_fail_leg_receipt_write_error_stays_failed(self):
        # Unknown policy AND an unwritable ledger: still fail closed, no raise.
        fake = RecordingFake([])
        engine, patcher = make_engine(fake)
        blocker = self.receipts / "blocked"
        blocker.write_text("not a dir", encoding="utf-8")
        engine.policy_audit_receipts_dir = blocker
        with patcher:
            result = engine.deidentify_for_llm_result(
                SYNTH_INPUT, policy="total_recall_max"
            )
        self.assertEqual(result.status, DeidentificationStatus.FAILED)
        self.assertEqual(result.safe_text, DEIDENTIFICATION_FAILED_PLACEHOLDER)

    @staticmethod
    def _raise_value_error():
        raise ValueError("synthetic verification explosion")


class CanaryTripwire(unittest.TestCase):
    """Canaries and raw text never appear in any receipt JSON."""

    def setUp(self):
        self.receipts = Path(tempfile.mkdtemp())

    def _all_receipt_bytes(self) -> bytes:
        return b"".join(
            p.read_bytes() for p in sorted(self.receipts.rglob("*.json"))
        )

    def test_canary_absent_from_pass_and_fail_receipts(self):
        # Pass leg: input carries a canary, fake strips it.
        report = build_real_audit_report("hipaa_safe_harbor")
        canary_input = f"Patient {CANARY} called about metformin."
        fake = RecordingFake(
            [
                SimpleNamespace(
                    deidentified_text="Patient [NAME] called about metformin.",
                    mapping={"[NAME]": CANARY},
                    audit_report=report,
                )
            ]
        )
        engine, patcher = make_engine(fake)
        engine.policy_audit_receipts_dir = self.receipts
        with patcher:
            engine.deidentify_for_llm_result(
                canary_input, canaries=[CANARY], policy="hipaa_safe_harbor"
            )
        # Fail leg: unknown policy with a canary-bearing requested name.
        fake2 = RecordingFake([])
        engine2, patcher2 = make_engine(fake2)
        engine2.policy_audit_receipts_dir = self.receipts
        with patcher2:
            engine2.deidentify_for_llm_result(
                canary_input, canaries=[CANARY], policy=f"leak-{CANARY}"
            )
        blob = self._all_receipt_bytes()
        self.assertNotIn(CANARY.encode("utf-8"), blob)
        self.assertNotIn(b"Rio Synth-Case", blob)  # no raw entity text either
        self.assertNotIn(SYNTH_SAFE_TEXT.encode("utf-8"), blob)  # no safe text
        self.assertNotIn(canary_input.encode("utf-8"), blob)

    def test_unknown_policy_name_is_not_echoed_only_digested(self):
        attack = "Mr Smith SSN 123-45-6789 <script>alert(1)</script>"
        fake = RecordingFake([])
        engine, patcher = make_engine(fake)
        engine.policy_audit_receipts_dir = self.receipts
        with patcher:
            engine.deidentify_for_llm_result(SYNTH_INPUT, policy=attack)
        blob = self._all_receipt_bytes()
        self.assertNotIn(attack.encode("utf-8"), blob)
        for token in (b"Mr Smith", b"123-45-6789", b"script"):
            self.assertNotIn(token, blob)
        receipts = read_receipts(self.receipts)
        self.assertEqual(receipts[0]["error_code"], "policy_unknown")
        self.assertTrue(receipts[0]["requested_policy_digest"])


class LedgerIdempotence(unittest.TestCase):
    """Same verification event -> one stable receipt; distinct events -> distinct files."""

    def setUp(self):
        self.receipts = Path(tempfile.mkdtemp())

    def _run_pass(self):
        fake = RecordingFake(
            [
                SimpleNamespace(
                    deidentified_text=SYNTH_SAFE_TEXT,
                    mapping=dict(SYNTH_MAPPING),
                    audit_report=build_real_audit_report("hipaa_safe_harbor"),
                )
            ]
        )
        engine, patcher = make_engine(fake)
        engine.policy_audit_receipts_dir = self.receipts
        with patcher:
            return engine.deidentify_for_llm_result(
                SYNTH_INPUT, policy="hipaa_safe_harbor"
            )

    def test_repeat_calls_write_one_stable_receipt(self):
        first = self._run_pass()
        files_after_first = sorted(self.receipts.rglob("*.json"))
        self.assertEqual(len(files_after_first), 1)
        bytes_after_first = files_after_first[0].read_bytes()

        second = self._run_pass()
        files_after_second = sorted(self.receipts.rglob("*.json"))
        self.assertEqual(files_after_second, files_after_first)
        self.assertEqual(
            files_after_second[0].read_bytes(), bytes_after_first
        )  # append-once: generated_at of the first write is preserved
        self.assertEqual(first, second)

    def test_distinct_events_write_distinct_receipts(self):
        self._run_pass()

        tampered = build_real_audit_report("hipaa_safe_harbor")
        tampered.policy = "strict_no_leak"
        fake = RecordingFake(
            [
                SimpleNamespace(
                    deidentified_text=SYNTH_SAFE_TEXT,
                    mapping=dict(SYNTH_MAPPING),
                    audit_report=tampered,
                )
            ]
        )
        engine, patcher = make_engine(fake)
        engine.policy_audit_receipts_dir = self.receipts
        with patcher:
            engine.deidentify_for_llm_result(SYNTH_INPUT, policy="hipaa_safe_harbor")

        fake2 = RecordingFake([])
        engine2, patcher2 = make_engine(fake2)
        engine2.policy_audit_receipts_dir = self.receipts
        with patcher2:
            engine2.deidentify_for_llm_result(SYNTH_INPUT, policy="nope")

        results = {r["error_code"] for r in read_receipts(self.receipts)}
        self.assertEqual(results, {"", "policy_audit_verification_failed", "policy_unknown"})
        self.assertEqual(len(list(self.receipts.rglob("*.json"))), 3)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
