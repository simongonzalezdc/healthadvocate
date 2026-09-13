"""Low-energy Coverage workflow and script tests (issue 83)."""

from __future__ import annotations

import re
import unittest
from datetime import date
from pathlib import Path

from healthadvocate.coverage.workflow import build_coverage_view, script_for_case

ROOT = Path(__file__).resolve().parents[1]


class CoverageWorkflowTests(unittest.TestCase):
    def sample_case(self) -> dict:
        return {
            "case_id": "case_test",
            "title": "Synthetic loss of coverage",
            "lifecycle": "active",
            "next_action": "Call county about Medi-Cal intake",
            "deadlines": [
                {"label": "Document deadline", "due": "2020-01-01"},
                {"label": "Upcoming", "due": "2099-01-01"},
            ],
            "facts": [
                {
                    "label": "coverage_end_date",
                    "value": "2026-08-31",
                    "status": "user-reported",
                    "observed_at": "2026-07-01",
                    "retrieved_at": "2026-07-01",
                    "provenance": "user",
                },
                {
                    "label": "network_status",
                    "value": "",
                    "status": "unknown",
                    "observed_at": "2026-07-01",
                    "retrieved_at": "2026-07-01",
                    "provenance": "none",
                },
                {
                    "label": "old_quote",
                    "value": "10",
                    "status": "stale",
                    "observed_at": "2020-01-01",
                    "retrieved_at": "2020-01-01",
                    "provenance": "user",
                },
            ],
            "targets": [
                {"kind": "provider", "name": "Dr Synthetic"},
                {"kind": "medication", "name": "Synthastatin"},
            ],
            "evidence": [],
            "contacts": [],
        }

    def test_one_primary_action(self):
        view = build_coverage_view(self.sample_case(), today=date(2026, 7, 22))
        self.assertTrue(view["ui"]["one_primary_action"])
        self.assertTrue(view["primary_action"]["is_primary"])
        self.assertEqual(
            view["primary_action"]["label"],
            "Call county about Medi-Cal intake",
        )
        self.assertTrue(all(not a["is_primary"] for a in view["secondary_actions"]))

    def test_risk_statuses_distinct(self):
        view = build_coverage_view(self.sample_case(), today=date(2026, 7, 22))
        statuses = {r["status"] for r in view["risks"]}
        self.assertIn("overdue", statuses)
        self.assertIn("unknown", statuses)
        self.assertIn("stale", statuses)

    def test_scripts_deterministic_and_unknown_safe(self):
        case = self.sample_case()
        for kind in ("county", "provider", "billing", "pharmacy"):
            script = script_for_case(case, kind)
            self.assertTrue(script["steps"])
            joined = "\n".join(script["steps"])
            self.assertNotRegex(joined, re.compile(r"\bTODO\b"))
            self.assertIn("Commitment Gate", script["commitment_note"])
            self.assertIn("[unknown]", script["unknown_fields_policy"])
        # Missing fields render as [unknown], not invented values.
        county = script_for_case(case, "county")
        self.assertTrue(any("[unknown]" in step for step in county["steps"]))
        billing = script_for_case(case, "billing")
        self.assertTrue(any("[unknown]" in step for step in billing["steps"]))

    def test_ui_has_single_primary_and_live_region(self):
        html = (ROOT / "healthadvocate" / "static" / "index.html").read_text()
        self.assertIn('data-view="coverage"', html)
        self.assertIn('id="view-coverage"', html)
        self.assertIn('aria-live="polite"', html)
        self.assertIn('data-action="coverage-create"', html)
        # Only one btn-primary inside coverage panel primary region.
        self.assertIn("coverage-primary-btn", html)
        app_js = (ROOT / "healthadvocate" / "static" / "app.js").read_text()
        self.assertIn("'coverage-create'", app_js)
        self.assertIn("safeRiskStatus", app_js)
        css = (ROOT / "healthadvocate" / "static" / "styles.css").read_text()
        self.assertIn("prefers-reduced-motion", css)
        self.assertIn("risk-overdue", css)
        self.assertIn("risk-conflicted", css)


if __name__ == "__main__":
    unittest.main()
