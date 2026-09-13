"""Optional PolicyEngine and CMS TiC adapter tests (issues 88-89)."""

from __future__ import annotations

import unittest

from healthadvocate.adapters.eligibility import (
    FEATURE_FLAG as PE_FLAG,
    unofficial_eligibility_estimate,
)
from healthadvocate.adapters.transparency import (
    FEATURE_FLAG as TIC_FLAG,
    research_negotiated_rates,
)
from healthadvocate.coverage import manual_workflow_status


class PolicyEngineEstimateTests(unittest.TestCase):
    def test_disabled_by_default_and_manual_independent(self):
        result = unofficial_eligibility_estimate(
            {"household_size": 2, "monthly_income": 1500, "state": "CA"},
            env={},
        )
        self.assertFalse(result["enabled"])
        status = manual_workflow_status()
        self.assertTrue(status.available)
        self.assertFalse(status.requires_optional_dataset)

    def test_enabled_estimate_is_unofficial(self):
        result = unofficial_eligibility_estimate(
            {"household_size": 2, "monthly_income": 1500, "state": "CA"},
            env={PE_FLAG: "1"},
        )
        self.assertTrue(result["enabled"])
        self.assertEqual(result["label"], "unofficial_estimate")
        self.assertTrue(result["not_official_eligibility"])
        self.assertTrue(result["engine"])
        self.assertTrue(result["rule_version"])
        self.assertTrue(result["calculation_date"])
        self.assertIn("official_verification_action", result)
        self.assertEqual(result["side_effects"], [])


class TransparencyResearchTests(unittest.TestCase):
    def test_disabled_until_budgets_attached(self):
        result = research_negotiated_rates(
            [{"payer": "PayerA", "billing_code": "99213", "negotiated_rate": 100}],
            env={},
        )
        self.assertFalse(result["enabled"])
        self.assertFalse(result["budget"]["measured"])
        self.assertTrue(result["not_guaranteed_patient_price"])

    def test_enabled_stream_preserves_meaning(self):
        result = research_negotiated_rates(
            [{"payer": "PayerA", "billing_code": "99213", "negotiated_rate": 100}],
            env={TIC_FLAG: "1"},
        )
        self.assertTrue(result["enabled"])
        self.assertTrue(result["rows"])
        self.assertTrue(result["rows"][0]["not_guaranteed_patient_price"])
        self.assertTrue(result["rows"][0]["not_network_truth"])
        self.assertEqual(
            result["rows"][0]["meaning"],
            "source_specific_negotiated_rate_evidence",
        )


if __name__ == "__main__":
    unittest.main()
