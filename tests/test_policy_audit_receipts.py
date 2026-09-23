"""Wave 2a contract tests: opt-in policy profiles + audit receipts (RALPLAN row 4).

Scope (docs/OPENMED-UPSTREAM-LEVERAGE-2026-09-17.md line 116, selective
adoption): ``HealthEngine.deidentify_for_llm_result`` gains an OPT-IN
``policy`` kwarg. The default path (``policy=None``) must stay byte-identical
to the pre-wave behavior. Permitted policies are pinned constants enumerated
from the installed openmed 2.5.0 (openmed/core/policy.py ``PolicyName``: 20
canonical values, verified 2026-09-22); unknown names fail closed.

Policy-leg seam (review finding 1, 2026-09-22): the stock top-level
``openmed.deidentify`` can never return text AND audit evidence — it attaches
``audit_report`` only under ``audit=True`` (pii.py:2338-2341) and then returns
the BARE AuditReport (pii.py:2866-2867). The policy leg therefore drives the
same ``openmed.core.pipeline.Pipeline`` the top-level function constructs for
this kwarg set (pii.py:2822-2846), with ``run(..., audit=True)`` taking
``PipelineResult.deidentification_result`` — the full result object carrying
``deidentified_text``, ``mapping``, and ``audit_report``. This is the
extension shape upstream's own doctest documents (pii.py docstring example
patches ``openmed.core.pipeline.Pipeline``).

Fail-closed posture is sacred: every failure leg returns
``DEIDENTIFICATION_FAILED_PLACEHOLDER`` through the existing boundary path
and writes a text-free governance receipt into the HA-E78 ledger.

Adversarial hardening (2026-09-22, findings ADV-004/005/008/009): the
verified report must be bound to THIS run — a real AuditReport instance
with a canonical-format hash, self-consistent, built under the REQUESTED
policy, and hash-bound to the assembled input and the returned output.
Unvalidated (attacker-controlled) hash values never reach the ledger, and
the ledger sanitizes every free-form field at write time.

Review round 2 (2026-09-22): reachable pass leg (Pipeline+audit seam),
non-string policy handled with a receipt (digest guarded), failure volume
evidenced via run_input_digest, atomic + self-healing ledger writes, and
result/verification_result reconciliation at the ledger boundary.

Synthetic inputs only. No model loads: ``openmed.deidentify`` and
``openmed.core.pipeline.Pipeline`` are patched in every test that reaches
the engine.
"""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

import openmed
import openmed.core.pipeline
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

# A second synthetic run, for reports that must NOT bind to the primary one.
OTHER_INPUT = "Patient Kai Synth-Prime emailed about insulin on 2026-09-02."
OTHER_SAFE_TEXT = "Patient [NAME] emailed about insulin on [DATE]."

# Hostile raw-PHI passthrough payload (synthetic), from the ADV-005 finding.
HOSTILE_RAW_TEXT = "UNDEID Mr Smith SSN 123-45-6789 Dr House metformin 555-0100 x1"

# Pinned pre-Wave-2a default-path behavior, captured against the unmodified
# engine on 2026-09-22 (worktree healthadvocate-pm-verify-20260917):
PINNED_ASSEMBLED = SYNTH_INPUT  # no profile/metadata/notes sections
PINNED_RESULT = DeidentificationResult(
    status=DeidentificationStatus.SUCCESS,
    safe_text=SYNTH_SAFE_TEXT,
    mapping=dict(SYNTH_MAPPING),
    error_code="",
)


def build_real_audit_report(
    policy: str,
    *,
    original_text: str = SYNTH_INPUT,
    deidentified_text: str = SYNTH_SAFE_TEXT,
    entity_text: str = "Rio Synth-Case",
    entity_start: int = 8,
):
    """Build a real openmed AuditReport via the upstream builder.

    Uses ``openmed.core.pii._build_audit_report`` — the exact function the
    upstream ``deidentify(audit=True)`` path calls (pii.py:2340) — so every
    field (hashes, spans, thresholds, residual risk) is real, not hand-rolled.
    The report binds (via input_hash/deidentified_text_hash) to the texts
    passed here, under the policy passed here.
    """
    entity = PIIEntity(
        text=entity_text,
        label="NAME",
        start=entity_start,
        end=entity_start + len(entity_text),
        confidence=0.98,
        redacted_text="[NAME]",
        canonical_label="NAME",
        sources=["ml"],
        threshold=0.7,
        action="mask",
    )
    return openmed_pii._build_audit_report(
        original_text=original_text,
        deidentified_text=deidentified_text,
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


class FakePipeline:
    """Fake openmed.core.pipeline.Pipeline (the policy-leg seam).

    Mirrors the shape upstream's own doctest documents: instances capture
    constructor kwargs, ``run`` captures its kwargs and returns an object
    whose ``deidentification_result`` is the canned result.
    """

    results: list = []
    constructed: list["FakePipeline"] = []

    def __init__(self, **kwargs):
        self.constructor_kwargs = kwargs
        self.runs = []
        FakePipeline.constructed.append(self)

    def run(self, text, **kwargs):
        self.runs.append({"text": text, "kwargs": kwargs})
        item = FakePipeline.results.pop(0)
        if isinstance(item, Exception):
            raise item
        return SimpleNamespace(deidentification_result=item)


def make_engine(fake):
    engine = HealthEngine()
    engine._loader = SimpleNamespace()  # sentinel loader; never constructs ModelLoader
    engine.policy_audit_receipts_dir = None  # set per-test to a tmp dir
    patcher = mock.patch.object(openmed, "deidentify", fake)
    return engine, patcher


def make_policy_engine(*results):
    """Engine whose policy leg hits FakePipeline (default seam untouched)."""
    FakePipeline.results = list(results)
    FakePipeline.constructed = []
    engine = HealthEngine()
    engine._loader = SimpleNamespace()
    engine.policy_audit_receipts_dir = None
    patcher = mock.patch.object(openmed.core.pipeline, "Pipeline", FakePipeline)
    return engine, patcher


def policy_result(audit_report, deidentified_text=SYNTH_SAFE_TEXT, mapping=None):
    return SimpleNamespace(
        deidentified_text=deidentified_text,
        mapping=dict(SYNTH_MAPPING if mapping is None else mapping),
        audit_report=audit_report,
    )


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
    """Permitted policy + real verified AuditReport -> success + pass receipt.

    The policy leg drives openmed.core.pipeline.Pipeline with audit=True and
    consumes PipelineResult.deidentification_result (review finding 1): the
    stock top-level openmed.deidentify can never return text and evidence
    together, so this seam is the only reachable pass leg.
    """

    def setUp(self):
        self.receipts = Path(tempfile.mkdtemp())
        self.report = build_real_audit_report("hipaa_safe_harbor")

    def _run(self):
        engine, patcher = make_policy_engine(policy_result(self.report))
        engine.policy_audit_receipts_dir = self.receipts
        with patcher:
            result = engine.deidentify_for_llm_result(
                SYNTH_INPUT, policy="hipaa_safe_harbor"
            )
        return result

    def test_policy_leg_uses_pipeline_with_audit_true(self):
        result = self._run()
        self.assertEqual(len(FakePipeline.constructed), 1)
        constructor_kwargs = FakePipeline.constructed[0].constructor_kwargs
        run_kwargs = FakePipeline.constructed[0].runs[0]["kwargs"]
        self.assertEqual(constructor_kwargs.get("policy"), "hipaa_safe_harbor")
        self.assertIs(constructor_kwargs.get("loader"), FakePipeline.constructed[0].constructor_kwargs.get("loader"))
        self.assertEqual(run_kwargs.get("method"), "mask")
        self.assertEqual(run_kwargs.get("keep_mapping"), True)
        self.assertTrue(run_kwargs.get("audit"))
        self.assertEqual(FakePipeline.constructed[0].runs[0]["text"], SYNTH_INPUT)

    def test_policy_leg_never_calls_top_level_deidentify(self):
        fake = RecordingFake([AssertionError("must not be called")])
        engine, patcher = make_policy_engine(policy_result(self.report))
        engine.policy_audit_receipts_dir = self.receipts
        with patcher, mock.patch.object(openmed, "deidentify", fake):
            result = engine.deidentify_for_llm_result(
                SYNTH_INPUT, policy="hipaa_safe_harbor"
            )
        self.assertEqual(result.status, DeidentificationStatus.SUCCESS)

    def test_success_result_uses_deidentified_text_and_mapping(self):
        result = self._run()
        self.assertEqual(result.status, DeidentificationStatus.SUCCESS)
        self.assertEqual(result.safe_text, SYNTH_SAFE_TEXT)
        self.assertEqual(dict(result.mapping), SYNTH_MAPPING)
        self.assertEqual(result.error_code, "")

    def test_pass_receipt_recorded_in_ledger(self):
        self._run()
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

    def test_stock_upstream_doctest_shape_passes(self):
        # Finding 1 pin: the engine must consume EXACTLY the shape the real
        # pipeline produces under audit=True. This mirrors upstream's own
        # doctest (openmed/core/pii.py deidentify example): patch the
        # Pipeline class; run returns an object whose deidentification_result
        # is a REAL openmed DeidentificationResult carrying a real audit
        # report. If the pass leg were still wired to the top-level
        # openmed.deidentify, it could never see this object.
        report = build_real_audit_report("hipaa_safe_harbor")
        fixture = openmed_pii.DeidentificationResult(
            original_text=SYNTH_INPUT,
            deidentified_text=SYNTH_SAFE_TEXT,
            pii_entities=[],
            method="mask",
            timestamp=datetime.now(),
            mapping=dict(SYNTH_MAPPING),
            audit_report=report,
        )
        engine = HealthEngine()
        engine._loader = SimpleNamespace()
        engine.policy_audit_receipts_dir = self.receipts
        with mock.patch("openmed.core.pipeline.Pipeline") as pipeline_cls:
            pipeline_cls.return_value.run.return_value = SimpleNamespace(
                deidentification_result=fixture
            )
            result = engine.deidentify_for_llm_result(
                SYNTH_INPUT, policy="hipaa_safe_harbor"
            )
        self.assertEqual(result.status, DeidentificationStatus.SUCCESS)
        self.assertEqual(result.safe_text, SYNTH_SAFE_TEXT)
        self.assertTrue(
            pipeline_cls.return_value.run.call_args.kwargs.get("audit") is True
        )
        receipts = read_receipts(self.receipts)
        self.assertEqual(receipts[0]["result"], "pass")

    def test_every_permitted_name_reaches_pipeline(self):
        from healthadvocate.privacy.policy_profiles import PERMITTED_POLICY_PROFILES

        for name in sorted(PERMITTED_POLICY_PROFILES):
            engine, patcher = make_policy_engine(
                policy_result(build_real_audit_report(name))
            )
            engine.policy_audit_receipts_dir = self.receipts
            with patcher:
                result = engine.deidentify_for_llm_result(SYNTH_INPUT, policy=name)
            self.assertEqual(result.status, DeidentificationStatus.SUCCESS, name)
            self.assertEqual(
                FakePipeline.constructed[0].constructor_kwargs.get("policy"), name
            )


class FailClosedLegs(unittest.TestCase):
    """Unknown policy / missing audit / failed verification -> placeholder + receipt."""

    def setUp(self):
        self.receipts = Path(tempfile.mkdtemp())

    def _run(self, policy, *results, text=SYNTH_INPUT):
        engine, patcher = make_policy_engine(*results)
        engine.policy_audit_receipts_dir = self.receipts
        with patcher:
            return engine.deidentify_for_llm_result(text, policy=policy)

    def _assert_failed(self, result):
        # The existing deid-failure path: placeholder + the boundary's error
        # code; the wave-specific code is pinned via the receipt and logs.
        self.assertEqual(result.status, DeidentificationStatus.FAILED)
        self.assertEqual(result.safe_text, DEIDENTIFICATION_FAILED_PLACEHOLDER)
        self.assertEqual(result.error_code, "deidentify_engine_failed")
        self.assertFalse(result.allows_model_call)
        self.assertEqual(dict(result.mapping), {})

    def test_unknown_policy_fails_closed_without_calling_openmed(self):
        result = self._run("total_recall_max")
        self._assert_failed(result)
        self.assertEqual(FakePipeline.constructed, [])  # never handed to openmed
        receipts = read_receipts(self.receipts)
        self.assertEqual(len(receipts), 1)
        self.assertEqual(receipts[0]["result"], "fail")
        self.assertEqual(receipts[0]["error_code"], "policy_unknown")
        self.assertFalse(receipts[0]["verification_result"])

    def test_non_string_policy_fails_closed_with_receipt(self):
        # Review finding 2: a caller violating the str | None hint (e.g.
        # policy=42) must still get the failure receipt + policy_unknown —
        # not an AttributeError that skips the ledger (old behavior:
        # deidentify_exception via the boundary backstop, zero receipts).
        for bad in (42, 4.5, True, ["hipaa_safe_harbor"], object()):
            result = self._run(bad)
            self.assertEqual(result.status, DeidentificationStatus.FAILED, repr(bad))
            self.assertEqual(result.safe_text, DEIDENTIFICATION_FAILED_PLACEHOLDER)
            self.assertEqual(FakePipeline.constructed, [], repr(bad))
            receipts = read_receipts(self.receipts)
            self.assertEqual(receipts[-1]["error_code"], "policy_unknown", repr(bad))
            self.assertTrue(receipts[-1]["requested_policy_digest"], repr(bad))

    def test_alias_policy_also_fails_closed(self):
        result = self._run("gdpr")
        self.assertEqual(result.status, DeidentificationStatus.FAILED)
        self.assertEqual(FakePipeline.constructed, [])

    def test_audit_report_missing_fails_closed(self):
        result = self._run("hipaa_safe_harbor", policy_result(None))
        self._assert_failed(result)
        receipts = read_receipts(self.receipts)
        self.assertEqual(receipts[0]["result"], "fail")
        self.assertEqual(receipts[0]["error_code"], "policy_audit_missing")

    def test_audit_verification_failure_fails_closed(self):
        report = build_real_audit_report("hipaa_safe_harbor")
        report.policy = "strict_no_leak"  # tamper post-construction: hash mismatch
        result = self._run("hipaa_safe_harbor", policy_result(report))
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
        result = self._run("strict_no_leak", policy_result(broken))
        self.assertEqual(result.status, DeidentificationStatus.FAILED)
        self.assertEqual(result.safe_text, DEIDENTIFICATION_FAILED_PLACEHOLDER)

    def test_pass_leg_receipt_write_failure_fails_closed(self):
        report = build_real_audit_report("hipaa_safe_harbor")
        engine, patcher = make_policy_engine(policy_result(report))
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
        engine, patcher = make_policy_engine()
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
        # Pass leg: input carries a canary, fake strips it; the report is
        # genuinely bound to this run (input hash matches the canary-bearing
        # assembled input, output hash matches the deidentified text).
        canary_input = f"Patient {CANARY} called about metformin."
        canary_safe = "Patient [NAME] called about metformin."
        report = build_real_audit_report(
            "hipaa_safe_harbor",
            original_text=canary_input,
            deidentified_text=canary_safe,
            entity_text=CANARY,
        )
        engine, patcher = make_policy_engine(policy_result(report, canary_safe, {"[NAME]": CANARY}))
        engine.policy_audit_receipts_dir = self.receipts
        with patcher:
            result = engine.deidentify_for_llm_result(
                canary_input, canaries=[CANARY], policy="hipaa_safe_harbor"
            )
        self.assertEqual(result.status, DeidentificationStatus.SUCCESS)
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
        engine, patcher = make_policy_engine(
            policy_result(build_real_audit_report("hipaa_safe_harbor"))
        )
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
        engine, patcher = make_policy_engine(policy_result(tampered))
        engine.policy_audit_receipts_dir = self.receipts
        with patcher:
            engine.deidentify_for_llm_result(SYNTH_INPUT, policy="hipaa_safe_harbor")

        engine2, patcher2 = make_policy_engine()
        engine2.policy_audit_receipts_dir = self.receipts
        with patcher2:
            engine2.deidentify_for_llm_result(SYNTH_INPUT, policy="nope")

        results = {r["error_code"] for r in read_receipts(self.receipts)}
        self.assertEqual(results, {"", "policy_audit_verification_failed", "policy_unknown"})
        self.assertEqual(len(list(self.receipts.rglob("*.json"))), 3)


class AuditReportBinding(unittest.TestCase):
    """ADV-004 / ADV-005 regression pins.

    The verified AuditReport must be bound to THIS run: built under the
    requested policy, for the assembled input, and for the returned output.
    A cleanly rebuilt report under a different policy or for different text
    must fail closed — the repro-hash self-consistency check cannot catch a
    clean rebuild (AuditReport.__post_init__ recomputes the hash over whatever
    it was built under).
    """

    def setUp(self):
        self.receipts = Path(tempfile.mkdtemp())

    def _run(self, policy, result_obj, text=SYNTH_INPUT):
        engine, patcher = make_policy_engine(result_obj)
        engine.policy_audit_receipts_dir = self.receipts
        with patcher:
            return engine.deidentify_for_llm_result(text, policy=policy)

    @staticmethod
    def _result_with(audit_report, deidentified_text=SYNTH_SAFE_TEXT):
        return policy_result(audit_report, deidentified_text=deidentified_text)

    def test_report_built_under_different_policy_fails_closed(self):
        # ADV-004 exact finding: request strict_no_leak; openmed returns a
        # report cleanly REBUILT under clinical_minimal_redaction.
        report = build_real_audit_report("clinical_minimal_redaction")
        result = self._run(
            "strict_no_leak", self._result_with(report)
        )
        self.assertEqual(result.status, DeidentificationStatus.FAILED)
        self.assertEqual(result.safe_text, DEIDENTIFICATION_FAILED_PLACEHOLDER)
        self.assertFalse(result.allows_model_call)
        receipts = read_receipts(self.receipts)
        self.assertEqual(receipts[0]["result"], "fail")
        self.assertEqual(receipts[0]["policy"], "strict_no_leak")
        self.assertEqual(receipts[0]["error_code"], "policy_audit_policy_mismatch")
        self.assertFalse(receipts[0]["verification_result"])

    def test_every_permitted_name_rejects_foreign_policy_report(self):
        # Pairwise sweep of the ADV-004 space: request each permitted name
        # while the evidence report was built under a different one.
        from healthadvocate.privacy.policy_profiles import PERMITTED_POLICY_PROFILES

        names = sorted(PERMITTED_POLICY_PROFILES)
        foreign_policy = names[0]
        report = build_real_audit_report(foreign_policy)
        for requested in names:
            if requested == foreign_policy:
                continue
            fresh = self._result_with(report)
            outcome = self._run(requested, fresh)
            self.assertEqual(
                outcome.status,
                DeidentificationStatus.FAILED,
                f"mismatched pair accepted: requested={requested} built={foreign_policy}",
            )
            self.assertEqual(
                outcome.safe_text, DEIDENTIFICATION_FAILED_PLACEHOLDER, requested
            )

    def test_matched_policy_still_passes(self):
        report = build_real_audit_report("strict_no_leak")
        result = self._run("strict_no_leak", self._result_with(report))
        self.assertEqual(result.status, DeidentificationStatus.SUCCESS)

    def test_report_for_different_input_text_fails_closed(self):
        # ADV-005: report built for a DIFFERENT document's input.
        report = build_real_audit_report(
            "hipaa_safe_harbor",
            original_text=OTHER_INPUT,
            deidentified_text=OTHER_SAFE_TEXT,
            entity_text="Kai Synth-Prime",
        )
        result = self._run("hipaa_safe_harbor", self._result_with(report))
        self.assertEqual(result.status, DeidentificationStatus.FAILED)
        self.assertEqual(result.safe_text, DEIDENTIFICATION_FAILED_PLACEHOLDER)
        receipts = read_receipts(self.receipts)
        self.assertEqual(receipts[0]["error_code"], "policy_audit_input_mismatch")

    def test_report_for_different_output_text_fails_closed(self):
        # ADV-005: input hash matches, but the report attests a different
        # deidentified output than the one openmed actually returned.
        report = build_real_audit_report(
            "hipaa_safe_harbor",
            original_text=SYNTH_INPUT,
            deidentified_text=OTHER_SAFE_TEXT,
        )
        result = self._run("hipaa_safe_harbor", self._result_with(report))
        self.assertEqual(result.status, DeidentificationStatus.FAILED)
        receipts = read_receipts(self.receipts)
        self.assertEqual(receipts[0]["error_code"], "policy_audit_output_mismatch")

    def test_hostile_raw_phi_passthrough_fails_closed(self):
        # ADV-005 Case A: hostile result returns raw PHI as deidentified_text
        # with a report built for different text. Must fail closed — never a
        # verbatim passthrough with allows_model_call=True.
        report = build_real_audit_report(
            "hipaa_safe_harbor",
            original_text=OTHER_INPUT,
            deidentified_text=OTHER_SAFE_TEXT,
            entity_text="Kai Synth-Prime",
        )
        result = self._run(
            "hipaa_safe_harbor", self._result_with(report, HOSTILE_RAW_TEXT)
        )
        self.assertEqual(result.status, DeidentificationStatus.FAILED)
        self.assertEqual(result.safe_text, DEIDENTIFICATION_FAILED_PLACEHOLDER)
        self.assertNotEqual(result.safe_text, HOSTILE_RAW_TEXT)
        self.assertFalse(result.allows_model_call)
        receipts = read_receipts(self.receipts)
        self.assertEqual(receipts[0]["result"], "fail")
        blob = b"".join(p.read_bytes() for p in self.receipts.rglob("*.json"))
        self.assertNotIn(HOSTILE_RAW_TEXT.encode("utf-8"), blob)


class UntrustedHashSanitization(unittest.TestCase):
    """ADV-008 regression pins: attacker-controlled repro_hash values never
    reach the HA-E78 ledger, on any leg."""

    CANARY_HASH = f"sha256:{CANARY}"  # malformed: hex body is not [0-9a-f]{64}

    def setUp(self):
        self.receipts = Path(tempfile.mkdtemp())

    def _blob(self) -> bytes:
        return b"".join(p.read_bytes() for p in sorted(self.receipts.rglob("*.json")))

    def test_canary_hash_on_fail_leg_never_reaches_ledger(self):
        engine, patcher = make_policy_engine(
            policy_result(SimpleNamespace(repro_hash=self.CANARY_HASH))
        )
        engine.policy_audit_receipts_dir = self.receipts
        with patcher:
            result = engine.deidentify_for_llm_result(
                SYNTH_INPUT, policy="hipaa_safe_harbor"
            )
        self.assertEqual(result.status, DeidentificationStatus.FAILED)
        receipts = read_receipts(self.receipts)
        self.assertEqual(receipts[0]["reproducibility_hash"], "")
        self.assertNotIn(CANARY.encode("utf-8"), self._blob())

    def test_canary_hash_with_shadowed_matches_never_passes(self):
        # ADV-008 Leg B: a REAL AuditReport whose repro_hash carries a canary
        # and whose repro_hash_matches is instance-shadowed to return True.
        report = build_real_audit_report("hipaa_safe_harbor")
        report.repro_hash = self.CANARY_HASH
        report.repro_hash_matches = lambda: True
        engine, patcher = make_policy_engine(policy_result(report))
        engine.policy_audit_receipts_dir = self.receipts
        with patcher:
            result = engine.deidentify_for_llm_result(
                SYNTH_INPUT, policy="hipaa_safe_harbor"
            )
        self.assertEqual(result.status, DeidentificationStatus.FAILED)
        self.assertEqual(result.safe_text, DEIDENTIFICATION_FAILED_PLACEHOLDER)
        receipts = read_receipts(self.receipts)
        self.assertEqual(receipts[0]["reproducibility_hash"], "")
        self.assertEqual(receipts[0]["result"], "fail")
        self.assertNotIn(CANARY.encode("utf-8"), self._blob())

    def test_ledger_sanitizes_directly_constructed_receipts(self):
        # Defense in depth: even a hand-built PolicyAuditReceipt cannot put an
        # unvalidated hash, a non-permitted policy name, or a free-text error
        # code into the ledger file.
        from healthadvocate.governance.policy_audit import (
            PolicyAuditReceipt,
            write_policy_audit_receipt,
        )

        receipt = PolicyAuditReceipt(
            build_revision="deadbee",
            generated_at="2026-09-22T00:00:00+00:00",
            result="pass",
            policy=f"leak-{CANARY}",
            reproducibility_hash=self.CANARY_HASH,
            verification_result=True,
            error_code=f"code with spaces {CANARY}",
            requested_policy_digest="not-hex-digest",
        )
        path = write_policy_audit_receipt(receipt, self.receipts)
        written = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(written["reproducibility_hash"], "")
        self.assertEqual(written["policy"], "")
        self.assertEqual(written["error_code"], "")
        self.assertEqual(written["requested_policy_digest"], "")
        blob = self._blob()
        self.assertNotIn(CANARY.encode("utf-8"), blob)
        self.assertNotIn(b"not-hex-digest", blob)


class NonAuditReportShapes(unittest.TestCase):
    """ADV-009 regression pins: only real AuditReport instances are accepted
    as audit evidence — dicts (including {}) self-verify through upstream
    verify_repro_hash's from_dict route and must fail closed."""

    def setUp(self):
        self.receipts = Path(tempfile.mkdtemp())

    def _run(self, audit_report):
        engine, patcher = make_policy_engine(policy_result(audit_report))
        engine.policy_audit_receipts_dir = self.receipts
        with patcher:
            return engine.deidentify_for_llm_result(
                SYNTH_INPUT, policy="hipaa_safe_harbor"
            )

    def test_mapping_shapes_fail_closed(self):
        # The empty dict self-verifies upstream (from_dict -> post_init
        # recomputes); forged dicts too. All must fail closed here.
        forged = {
            "policy": "not_a_real_profile",
            "input_hash": "0" * 64,
            "document_length": 99999,
        }
        for shape in ({}, forged, {"repro_hash": f"sha256:{'a' * 64}"}):
            result = self._run(shape)
            self.assertEqual(result.status, DeidentificationStatus.FAILED, shape)
            self.assertEqual(result.safe_text, DEIDENTIFICATION_FAILED_PLACEHOLDER)

    def test_non_mapping_non_report_shapes_fail_closed(self):
        for shape in ("sha256:" + "a" * 64, 42, [], None, object()):
            result = self._run(shape)
            self.assertEqual(result.status, DeidentificationStatus.FAILED, repr(shape))

    def test_lookalike_object_is_not_evidence(self):
        # A SimpleNamespace carrying a well-formed hash is still not an
        # AuditReport instance: not acceptable evidence.
        lookalike = SimpleNamespace(
            repro_hash=f"sha256:{'a' * 64}",
            policy="hipaa_safe_harbor",
            input_hash="x",
            repro_hash_matches=lambda: True,
        )
        result = self._run(lookalike)
        self.assertEqual(result.status, DeidentificationStatus.FAILED)

    def test_invalid_report_receipt_carries_no_hash_and_error_code(self):
        self._run({})
        receipts = read_receipts(self.receipts)
        self.assertEqual(len(receipts), 1)
        self.assertEqual(receipts[0]["result"], "fail")
        self.assertEqual(receipts[0]["error_code"], "policy_audit_invalid_report")
        self.assertEqual(receipts[0]["reproducibility_hash"], "")
        self.assertFalse(receipts[0]["verification_result"])


class FailureVolumeEvidence(unittest.TestCase):
    """Review finding 3: N failing runs over N different documents must
    produce N receipts — failure volume is auditor evidence. Repeats of the
    SAME run (same input, same outcome) still collapse to one append-once
    receipt."""

    def setUp(self):
        self.receipts = Path(tempfile.mkdtemp())

    def _failing_run(self, text):
        # Permitted policy, result without audit_report -> policy_audit_missing.
        engine, patcher = make_policy_engine(policy_result(None))
        engine.policy_audit_receipts_dir = self.receipts
        with patcher:
            return engine.deidentify_for_llm_result(text, policy="hipaa_safe_harbor")

    def test_different_documents_get_distinct_failure_receipts(self):
        doc_a = "Patient Aria Synth-One called about metformin."
        doc_b = "Patient Bo Synth-Two emailed about insulin."
        doc_c = "Patient Cy Synth-Three asked about lisinopril."
        for doc in (doc_a, doc_b, doc_c):
            result = self._failing_run(doc)
            self.assertEqual(result.status, DeidentificationStatus.FAILED)
        receipts = read_receipts(self.receipts)
        self.assertEqual(len(receipts), 3)
        self.assertEqual({r["error_code"] for r in receipts}, {"policy_audit_missing"})
        digests = {r["run_input_digest"] for r in receipts}
        self.assertEqual(len(digests), 3)
        self.assertTrue(all(d for d in digests))
        for doc in (doc_a, doc_b, doc_c):
            expected = hashlib.sha256(doc.encode("utf-8")).hexdigest()[:16]
            self.assertIn(expected, digests)

    def test_same_document_repeated_still_collapses(self):
        self._failing_run(SYNTH_INPUT)
        self._failing_run(SYNTH_INPUT)
        self.assertEqual(len(list(self.receipts.rglob("*.json"))), 1)

    def test_unknown_policy_same_name_different_docs_get_distinct_receipts(self):
        for doc in ("Alpha doc synth.", "Beta doc synth."):
            engine, patcher = make_policy_engine()
            engine.policy_audit_receipts_dir = self.receipts
            with patcher:
                engine.deidentify_for_llm_result(doc, policy="nope")
        self.assertEqual(len(list(self.receipts.rglob("*.json"))), 2)


class AtomicSelfHealingLedger(unittest.TestCase):
    """Review finding 4: atomic writes, and a corrupt ledger entry self-heals
    instead of being sticky forever."""

    def setUp(self):
        self.receipts = Path(tempfile.mkdtemp())

    def _record(self):
        from healthadvocate.governance.policy_audit import record_policy_audit

        return record_policy_audit(
            policy="hipaa_safe_harbor",
            verified=True,
            repro_hash="sha256:" + "1" * 64,
            run_input_digest="a" * 16,
            receipts_dir=self.receipts,
        )

    def test_corrupt_receipt_file_is_rewritten_valid(self):
        path = self._record()
        path.write_text('{"truncated": ', encoding="utf-8")  # crash mid-write shape
        healed = self._record()
        self.assertEqual(healed, path)
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["result"], "pass")
        self.assertEqual(data["reproducibility_hash"], "sha256:" + "1" * 64)

    def test_empty_receipt_file_is_rewritten_valid(self):
        path = self._record()
        path.write_text("", encoding="utf-8")
        self._record()
        data = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(data["evidence_id"], "HA-E78")

    def test_valid_receipt_file_is_never_rewritten(self):
        path = self._record()
        before = path.read_bytes()
        mtime = path.stat().st_mtime
        self._record()
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual(path.stat().st_mtime, mtime)

    def test_no_temporary_files_left_behind(self):
        self._record()
        self._record()
        leftovers = [p for p in self.receipts.iterdir() if p.name.startswith(".")]
        self.assertEqual(leftovers, [])


class ResultReconciliation(unittest.TestCase):
    """Review finding 5: the ledger derives `result` from
    `verification_result` — contradictory pairs are reconciled at the
    boundary, whatever the calling path."""

    def _write(self, **overrides):
        from healthadvocate.governance.policy_audit import (
            PolicyAuditReceipt,
            write_policy_audit_receipt,
        )

        base = dict(
            build_revision="deadbee",
            generated_at="2026-09-22T00:00:00+00:00",
            result="fail",
            policy="hipaa_safe_harbor",
            reproducibility_hash="sha256:" + "2" * 64,
            verification_result=False,
        )
        base.update(overrides)
        receipt = PolicyAuditReceipt(**base)
        out = Path(tempfile.mkdtemp())
        path = write_policy_audit_receipt(receipt, out)
        return json.loads(path.read_text(encoding="utf-8"))

    def test_pass_result_with_failed_verification_becomes_fail(self):
        written = self._write(result="pass", verification_result=False)
        self.assertEqual(written["result"], "fail")
        self.assertFalse(written["verification_result"])

    def test_fail_result_with_true_verification_becomes_pass(self):
        written = self._write(result="fail", verification_result=True)
        self.assertEqual(written["result"], "pass")
        self.assertTrue(written["verification_result"])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
