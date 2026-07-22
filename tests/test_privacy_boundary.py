"""Privacy boundary and fail-closed runtime tests (issue 80 / HA-E72)."""

from __future__ import annotations

import io
import logging
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from healthadvocate.coverage import manual_workflow_status
from healthadvocate.privacy.boundary import (
    DEIDENTIFICATION_FAILED_PLACEHOLDER,
    DeidentificationStatus,
    PrivacyBoundary,
    PrivacyBoundaryError,
)
from healthadvocate.privacy.endpoint_policy import (
    EndpointPolicyError,
    assert_loopback_bind_host,
    assert_loopback_model_url,
    is_loopback_host,
)
from healthadvocate.privacy.logging_redaction import (
    CanaryRedactingFilter,
    redact_text,
)

ROOT = Path(__file__).resolve().parents[1]

CANARY = "CANARY_PATIENT_ALPHA_9f3c"
CANARY_MEMBER = "MEMBER-ID-SYNTH-42"


class LoopbackPolicyTests(unittest.TestCase):
    def test_loopback_hosts_allowed(self):
        for host in ("127.0.0.1", "localhost", "::1", "[::1]"):
            self.assertTrue(is_loopback_host(host), host)
        assert_loopback_bind_host("127.0.0.1")
        assert_loopback_bind_host("localhost")
        assert_loopback_bind_host("::1")
        assert_loopback_model_url("http://127.0.0.1:11434/v1")
        assert_loopback_model_url("http://localhost:1234/v1")
        assert_loopback_model_url("http://[::1]:11434/v1")

    def test_non_loopback_bind_rejected(self):
        for host in ("0.0.0.0", "::", "*", "8.8.8.8", "example.com"):
            with self.assertRaises(EndpointPolicyError):
                assert_loopback_bind_host(host)

    def test_non_loopback_model_urls_rejected(self):
        bad_urls = [
            "http://8.8.8.8:11434/v1",
            "http://example.com/v1",
            "https://api.openai.com/v1",
            "http://user:pass@127.0.0.1:11434/v1",
            "ftp://127.0.0.1/v1",
            "",
        ]
        for url in bad_urls:
            with self.assertRaises(EndpointPolicyError):
                assert_loopback_model_url(url)

    def test_redirects_never_allowed(self):
        with self.assertRaises(EndpointPolicyError):
            assert_loopback_model_url(
                "http://127.0.0.1:11434/v1",
                allow_redirects=True,
            )

    def test_ipv4_mapped_and_ambiguous_variants(self):
        # Literal loopback variants.
        self.assertTrue(is_loopback_host("127.0.0.1"))
        self.assertTrue(is_loopback_host("127.1.2.3"))  # 127/8
        self.assertFalse(is_loopback_host("10.0.0.1"))
        self.assertFalse(is_loopback_host("169.254.1.1"))
        with self.assertRaises(EndpointPolicyError):
            assert_loopback_model_url("http://169.254.169.254/v1")


class DockerfileComposeDefaultsTests(unittest.TestCase):
    def test_dockerfile_binds_loopback(self):
        dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
        self.assertIn('--host", "127.0.0.1"', dockerfile)
        self.assertNotIn("0.0.0.0", dockerfile)

    def test_compose_is_loopback_without_traefik(self):
        compose = (ROOT / "docker-compose.yaml").read_text(encoding="utf-8")
        self.assertIn("127.0.0.1:8080:8080", compose)
        self.assertNotIn("traefik.enable", compose)
        self.assertNotIn("traefik.http", compose)
        self.assertNotIn("networks:", compose)


class DeidentificationBoundaryTests(unittest.TestCase):
    def test_full_context_includes_profile_and_canary_failure(self):
        def fake_deidentify(text: str):
            # Pretend scrubber leaves canary in place.
            return text, {"NAME": "Alice"}

        boundary = PrivacyBoundary(
            deidentify_fn=fake_deidentify,
            canaries=[CANARY],
        )
        assembled = boundary.assemble_context(
            "headache",
            profile_context=f"Patient Profile ({CANARY}, self): notes",
            evidence_metadata=f"member={CANARY_MEMBER}",
        )
        self.assertIn(CANARY, assembled)
        result = boundary.deidentify_assembled(assembled)
        self.assertEqual(result.status, DeidentificationStatus.FAILED)
        self.assertEqual(result.safe_text, DEIDENTIFICATION_FAILED_PLACEHOLDER)
        self.assertFalse(result.allows_model_call)

    def test_success_and_no_pii_statuses(self):
        boundary = PrivacyBoundary(
            deidentify_fn=lambda t: (t.replace("Alice", "[NAME]"), {"Alice": "[NAME]"}),
        )
        ok = boundary.deidentify_assembled("Hello Alice")
        self.assertEqual(ok.status, DeidentificationStatus.SUCCESS)
        self.assertTrue(ok.allows_model_call)

        none = PrivacyBoundary(
            deidentify_fn=lambda t: (t, {}),
        ).deidentify_assembled("no identifiers")
        self.assertEqual(none.status, DeidentificationStatus.NO_PII_FOUND)
        self.assertTrue(none.allows_model_call)

    def test_failure_blocks_model_url_assertion(self):
        boundary = PrivacyBoundary(deidentify_fn=None)
        result = boundary.prepare_model_input("x")
        self.assertEqual(result.status, DeidentificationStatus.FAILED)
        with self.assertRaises(PrivacyBoundaryError):
            boundary.assert_model_allowed(result, "http://127.0.0.1:11434/v1")

    def test_remote_url_blocked_even_after_success(self):
        boundary = PrivacyBoundary(deidentify_fn=lambda t: (t, {}))
        result = boundary.prepare_model_input("hello")
        with self.assertRaises(PrivacyBoundaryError):
            boundary.assert_model_allowed(result, "https://api.openai.com/v1")


class LoggingRedactionTests(unittest.TestCase):
    def test_canaries_redacted_from_logs_and_errors(self):
        self.assertNotIn(CANARY, redact_text(f"error for {CANARY}"))
        self.assertNotIn(CANARY_MEMBER, redact_text(f"id={CANARY_MEMBER}"))

        stream = io.StringIO()
        handler = logging.StreamHandler(stream)
        handler.addFilter(CanaryRedactingFilter(canaries=[CANARY, CANARY_MEMBER]))
        log = logging.getLogger("healthadvocate.test.privacy")
        log.handlers.clear()
        log.addHandler(handler)
        log.setLevel(logging.INFO)
        log.info("patient %s member %s", CANARY, CANARY_MEMBER)
        handler.flush()
        output = stream.getvalue()
        self.assertNotIn(CANARY, output)
        self.assertNotIn(CANARY_MEMBER, output)
        self.assertIn("[REDACTED", output)


class ModelClientPolicyTests(unittest.TestCase):
    def test_default_model_disabled_returns_fallback(self):
        from healthadvocate.core import llm_client

        with mock.patch.object(llm_client, "_MODEL_ENABLED", False):
            result = llm_client.chat_structured("hello", module_type="symptom_assessment")
        self.assertTrue(result.get("_model_blocked"))
        self.assertNotIn(CANARY, str(result))

    def test_non_loopback_env_url_blocks_model(self):
        from healthadvocate.core import llm_client

        with mock.patch.object(llm_client, "_MODEL_ENABLED", True), mock.patch.object(
            llm_client,
            "_MODEL_URL",
            "https://api.openai.com/v1",
        ):
            result = llm_client.chat_structured("hello", module_type="symptom_assessment")
        self.assertTrue(result.get("_model_blocked"))


class CoverageWithoutModelTests(unittest.TestCase):
    def test_manual_coverage_works_without_model(self):
        status = manual_workflow_status()
        self.assertTrue(status.available)
        self.assertFalse(status.requires_model)


class DeploymentSourceGuards(unittest.TestCase):
    def test_no_unauthenticated_traefik_in_default_compose(self):
        compose = (ROOT / "docker-compose.yaml").read_text(encoding="utf-8")
        self.assertNotIn("traefik.http.routers", compose)

    def test_startup_bind_helper_rejects_public(self):
        from healthadvocate.privacy.startup import validate_startup_bind_policy

        with self.assertRaises(SystemExit):
            validate_startup_bind_policy({"HEALTHADVOCATE_BIND_HOST": "0.0.0.0"})


if __name__ == "__main__":
    unittest.main()
