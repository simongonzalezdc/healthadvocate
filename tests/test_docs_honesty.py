"""Docs-honesty pins (Lane C, 2026-09-24): the README must tell one true story.

Every pin here is grounded in shipped behavior:

- the no-model table must match the real fallback shape
  (``healthadvocate/core/llm_client.py::unavailable_structured_fallback``);
- the configuration table must document every model-related env var with
  the defaults the code actually ships (``llm_client.py`` module header,
  ``privacy/endpoint_policy.py::default_model_base_url``);
- the retired "endpoints return errors" claim must stay retired — the
  code answers with the unavailable fallback, never a raw error
  (``llm_client.py::chat_structured`` catches both the disabled-model
  ``PrivacyBoundaryError`` and transport failures into the fallback);
- the mission / not-a-doctor boundary must be stated plainly;
- the CHANGELOG must carry the Unreleased docs entry.
"""

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

README = (ROOT / "README.md").read_text()
CHANGELOG = (ROOT / "CHANGELOG.md").read_text()
LLM_CLIENT = (ROOT / "healthadvocate" / "core" / "llm_client.py").read_text()
ENDPOINT_POLICY = (
    ROOT / "healthadvocate" / "privacy" / "endpoint_policy.py"
).read_text()
CROSS_VALIDATION = (
    ROOT / "healthadvocate" / "core" / "cross_validation.py"
).read_text()


def readme_section(title: str) -> str:
    """Return one `## ` section body (up to the next `## ` heading)."""
    parts = README.split(title, 1)
    assert len(parts) == 2, f"README has no {title!r} section"
    return parts[1].split("\n## ", 1)[0]


class NoModelTableTests(unittest.TestCase):
    """Spec 1: every feature surface, stated plainly, deterministic vs degraded."""

    def setUp(self):
        self.section = readme_section("## What works without a model")

    def test_fallback_shape_is_described_from_the_code(self):
        # llm_client.py:190-204 — the shape every generative surface returns
        # when the runtime is off: honest summary, manual-workflow actions,
        # empty red flags, _model_blocked marker.
        self.assertIn("_model_blocked", LLM_CLIENT)
        self.assertIn("_model_blocked", self.section)
        self.assertIn("red flags", self.section.lower())
        self.assertIn("unavailable", self.section.lower())

    def test_urgency_reads_unavailable_not_an_alarm(self):
        # The README claim must be TRUE IN CODE, not just prose: the
        # no-judgment fallback carries the honest "unavailable" urgency
        # (finding: the old pin only checked README text while the code
        # shipped a guessed "medium" / an alarm "high").
        from healthadvocate.core.llm_client import (
            unavailable_structured_fallback,
        )
        from healthadvocate.decisions.symptom_triage import (
            MODEL_UNAVAILABLE_URGENCY,
        )

        self.assertEqual(unavailable_structured_fallback()["urgency"], "unavailable")
        self.assertEqual(MODEL_UNAVAILABLE_URGENCY, "unavailable")
        self.assertIn("unavailable", self.section.lower())
        self.assertIn("emergency-class terms", self.section.lower())

    def test_every_generative_surface_has_a_row(self):
        for surface in (
            "Symptom Assessment",
            "Insurance Denial Fighter",
            "Medical Bill Decoder",
            "Document Decoder",
            "Drug Checker",
            "Appointment Prep",
            "Discharge Translator",
            "Second Opinion Brief",
            "Community Health Scanner",
        ):
            self.assertIn(surface, self.section, f"no table row for {surface}")

    def test_every_deterministic_surface_has_a_row(self):
        for surface in (
            "Family Health Tracker",
            "Health Tracks",
            "Coverage Continuity Track",
            "CLI",
            "MCP",
        ):
            self.assertIn(surface, self.section, f"no table row for {surface}")

    def test_deterministic_prep_is_separated_from_generative(self):
        # the table must name what keeps working (deterministic) and what
        # degrades (generative) — two columns, stated plainly
        self.assertIn("Deterministic", self.section)
        self.assertIn("Generative", self.section)


class ConfigurationTableTests(unittest.TestCase):
    """Spec 2: the missing env vars, with the defaults the code ships."""

    def setUp(self):
        parts = README.split("### Configuration", 1)
        assert len(parts) == 2, "README has no Configuration section"
        self.table = parts[1].split("\n### ", 1)[0].split("\n## ", 1)[0]

    def test_all_model_env_vars_are_documented(self):
        for var in (
            "HEALTHADVOCATE_MODEL_ENABLED",
            "HEALTHADVOCATE_MODEL_URL",
            "LM_STUDIO_URL",
            "MEDICAL_LLM_MODEL",
            "HEALTHADVOCATE_ALLOW_ORIGINS",
            # The four vars the code reads but the table omitted
            # (finding: 5 documented vs 9 read).
            "HEALTHADVOCATE_BIND_HOST",
            "HEALTHADVOCATE_CASE_DIR",
            "HEALTHADVOCATE_CMS_TIC_ENABLED",
            "HEALTHADVOCATE_POLICYENGINE_ENABLED",
        ):
            self.assertIn(f"`{var}`", self.table, f"{var} missing from config table")

    def test_env_vars_table_matches_code_reads(self):
        # Cross-check the table against every os.environ read in the
        # package: a var the code reads must appear in the table.
        import re

        sources = "\n".join(
            p.read_text() for p in (ROOT / "healthadvocate").rglob("*.py")
        )
        code_vars = set(re.findall(r'"(HEALTHADVOCATE_[A-Z_]+)"', sources)) | {
            "LM_STUDIO_URL", "MEDICAL_LLM_MODEL"
        }
        table_vars = set(re.findall(r"`(HEALTHADVOCATE_[A-Z_]+|LM_STUDIO_URL|MEDICAL_LLM_MODEL)`", self.table))
        self.assertEqual(code_vars - table_vars, set(),
                         f"env vars read by code but missing from README table: "
                         f"{sorted(code_vars - table_vars)}")

    def test_enabled_switch_is_documented_as_the_off_by_default_master(self):
        rows = [l for l in self.table.splitlines() if "HEALTHADVOCATE_MODEL_ENABLED" in l]
        self.assertEqual(len(rows), 1)
        self.assertIn("`0`", rows[0])
        self.assertIn("off by default", rows[0].lower())

    def test_lm_studio_url_is_marked_deprecated(self):
        rows = [l for l in self.table.splitlines() if "LM_STUDIO_URL" in l]
        self.assertTrue(rows and "deprecated" in rows[0].lower())

    def test_documented_defaults_match_the_code(self):
        # llm_client.py: _MODEL_NAME = os.environ.get("MEDICAL_LLM_MODEL", "local-model")
        self.assertIn('"local-model"', LLM_CLIENT)
        self.assertIn("`local-model`", self.table)
        # endpoint_policy.py::default_model_base_url()
        self.assertIn("http://127.0.0.1:11434/v1", ENDPOINT_POLICY)
        self.assertIn("http://127.0.0.1:11434/v1", self.table)

    def test_meditron_default_overclaim_is_retired(self):
        # the old table claimed MEDICAL_LLM_MODEL defaults to meditron3-8b;
        # the shipped default is local-model
        self.assertNotIn("`MEDICAL_LLM_MODEL` | `meditron3-8b`", README)


class ErrorClaimReconciliationTests(unittest.TestCase):
    """Spec 2: reconcile 'endpoints return errors' with the silent fallback."""

    def test_endpoints_return_errors_claim_is_retired(self):
        self.assertNotIn("endpoints return errors", README.lower())

    def test_fallback_not_error_is_stated(self):
        self.assertIn("unavailable fallback", README.lower())


class MissionAndBoundaryTests(unittest.TestCase):
    """Specs 3+4: why this exists, what it is not, hero alignment."""

    def test_why_this_exists_section(self):
        section = readme_section("## Why this exists").lower()
        self.assertIn("hope", section)
        self.assertIn("free", section)
        self.assertIn("open source", section)
        self.assertIn("local-first", section)

    def test_not_a_doctor_boundary_is_stated(self):
        section = readme_section("## Why this exists").lower()
        self.assertIn("not a doctor", section)
        self.assertIn("not a diagnosis", section)
        self.assertIn("not verified medical advice", section)

    def test_hero_carries_the_mission_line(self):
        head = README.split("---", 1)[0].lower()
        self.assertIn("hope", head)
        self.assertIn("free", head)

    def test_no_clinical_authority_overclaims(self):
        for banned in (
            "clinically verified",
            "clinically validated",
            "medically verified",
            "fda-approved",
            "fda approved",
            "guaranteed accurate",
        ):
            self.assertNotIn(banned, README.lower())

    def test_cross_validation_confidence_matches_the_code(self):
        # cross_validation.py requires e.confidence >= 0.80; the old
        # README claimed "90%+ confidence"
        self.assertIn("0.80", CROSS_VALIDATION)
        self.assertNotIn("90%+", README)


class ChangelogTests(unittest.TestCase):
    """Spec 5: Unreleased docs entry."""

    def test_unreleased_carries_docs_entry(self):
        unreleased = CHANGELOG.split("## [Unreleased]", 1)[1].split("\n## ", 1)[0]
        parts = unreleased.split("### Docs", 1)
        self.assertEqual(len(parts), 2, "Unreleased must carry a ### Docs section")
        self.assertIn("What works without a model", parts[1])
        self.assertIn("HEALTHADVOCATE_MODEL_ENABLED", parts[1])
        self.assertIn("endpoints return errors", parts[1])


if __name__ == "__main__":
    unittest.main()
