"""Adapter claim-contract tests for issues 84-86."""

from __future__ import annotations

import unittest

from healthadvocate.adapters.medications import (
    dailymed_label_evidence,
    normalize_medication_rxnorm_cpc,
    openfda_safety_evidence,
    refuse_clinical_verdict,
)
from healthadvocate.adapters.pricing import drugcentral_reference, nadac_benchmark
from healthadvocate.adapters.providers import match_provider_nppes


class MedicationAdapterTests(unittest.TestCase):
    def test_rxnorm_cpc_identity_only(self):
        ev = normalize_medication_rxnorm_cpc("Synthastatin")
        self.assertEqual(ev.payload["status"], "matched")
        self.assertIn("rxcui", ev.payload)
        for bad in ("interaction_clearance", "dose", "diagnosis", "treatment"):
            self.assertNotIn(bad, ev.payload)
        self.assertIn("CPC", ev.notes)

    def test_dailymed_and_openfda_dated(self):
        label = dailymed_label_evidence("Synthastatin")
        self.assertTrue(label.source_revision)
        self.assertTrue(label.retrieved_at)
        self.assertTrue(label.checksum)
        self.assertTrue(
            label.payload.get("label_excerpt") or label.payload.get("status") == "unknown"
        )

        safety = openfda_safety_evidence("Synthastatin")
        self.assertTrue(safety.checksum)
        self.assertNotIn("causation", safety.payload)
        self.assertIn("do not establish causation", safety.notes.lower())

    def test_clinical_verdicts_refused(self):
        for kind in ("interaction", "dose", "diagnosis", "treatment_change"):
            result = refuse_clinical_verdict(kind)
            self.assertFalse(result["allowed"])


class ProviderAdapterTests(unittest.TestCase):
    def test_nppes_identity_not_network(self):
        ev = match_provider_nppes("Dr Synthetic Example")
        self.assertEqual(ev.payload["status"], "matched")
        self.assertEqual(ev.payload["network_participation"], "unknown")
        self.assertEqual(ev.payload["licensure"], "unknown")
        self.assertEqual(ev.payload["availability"], "unknown")
        self.assertTrue(ev.payload["matches"][0]["match_rationale"])
        self.assertTrue(ev.retrieved_at)
        self.assertTrue(ev.source_revision)

    def test_ambiguous_match_conflicted(self):
        # Query matching multiple names partially
        ev = match_provider_nppes("Synthetic")
        self.assertIn(ev.payload["status"], {"conflicted", "matched", "unknown"})
        if len(ev.payload["matches"]) > 1:
            self.assertEqual(ev.payload["status"], "conflicted")


class PricingAdapterTests(unittest.TestCase):
    def test_nadac_is_benchmark_not_patient_price(self):
        ev = nadac_benchmark("Synthastatin")
        self.assertEqual(ev.payload["benchmark_meaning"], "acquisition_cost_benchmark")
        self.assertTrue(ev.payload["not_a_patient_price"])
        self.assertTrue(ev.payload["not_pharmacy_quote"])
        self.assertTrue(ev.payload.get("effective_date") or ev.payload["status"] == "unknown")
        self.assertIn("source_name", ev.payload)
        self.assertIn("unit", ev.payload)

    def test_drugcentral_attribution(self):
        ev = drugcentral_reference("Synthastatin")
        self.assertIn("CC BY-SA", ev.attribution)
        self.assertIn("share_alike_notice", ev.payload)
        self.assertIn("share-alike", ev.payload["share_alike_notice"].lower())


if __name__ == "__main__":
    unittest.main()
