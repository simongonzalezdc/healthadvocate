"""F1b — share-safe pack tests (deterministic, loopback, no network)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from healthadvocate.core import share_safe


class ShareSafeTests(unittest.TestCase):
    def test_masks_names_dates_phones(self):
        r = share_safe.make_share_safe(
            "Dr. Maya Patel called John Smith on March 15, 2024. Callback 555-0123."
        )
        self.assertNotIn("Maya", r["clean_text"])
        self.assertNotIn("Smith", r["clean_text"])
        self.assertNotIn("555-0123", r["clean_text"])
        self.assertIn("[", r["clean_text"])  # type-labeled masks
        self.assertGreater(r["total"], 0)
        self.assertEqual(r["total"], sum(r["counts"].values()))

    def test_empty_is_safe_empty(self):
        r = share_safe.make_share_safe("   ")
        self.assertEqual(r, {"clean_text": "", "counts": {}, "total": 0})

    def test_counts_are_type_keyed(self):
        r = share_safe.make_share_safe("John Smith and Jane Smith met.")
        self.assertTrue(all(isinstance(k, str) and k for k in r["counts"]))

    def test_never_returns_original_as_safe(self):
        # if the deidentifier ever fails to produce output, we raise —
        # the endpoint must never hand back the ORIGINAL text as "safe"
        class Broken:
            def run(self, text):
                class R:
                    pii_entities = []
                    redacted_text = None
                return R()
        orig = share_safe._deidentifier
        share_safe._deidentifier = Broken()
        try:
            with self.assertRaises(RuntimeError):
                share_safe.make_share_safe("John Smith")
        finally:
            share_safe._deidentifier = orig


if __name__ == "__main__":
    unittest.main()
