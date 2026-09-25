"""F1a appeal letter generator — backend pins.

Covers the honesty contract: deterministic case-file assembly (every
field source-cited), model-off letter assembly from user facts only
(no invented dates/amounts), model-on letter flow through the shared
gated client (loopback-only by construction), and the HTTP surface
including the machine-distinguishable fallback marker.
"""

from __future__ import annotations

import unittest
from unittest import mock

from fastapi.testclient import TestClient

from healthadvocate.core import appeal_letter
from healthadvocate.core import appeal_letter as healthadvocate_module
from healthadvocate.core.appeal_letter import (
    build_case_file,
    classify_reason,
    extract_amounts,
    extract_dates,
    extract_plan_language,
    generate_appeal_letter,
)
from healthadvocate.core.llm_client import unavailable_structured_fallback

DENIAL = (
    "Date: September 8, 2026. Reference A-2291. "
    "Dear Member: Your claim for MRI of the right knee is denied as "
    "not medically necessary under the plan criteria. "
    "You may file a first-level appeal within 30 days of this letter. "
    "The total charge was $1,200.00."
)

RECORD = (
    "Physical therapy notes dated August 2, 2026: six weeks of "
    "documented therapy, total billed $480.00."
)


def _stub_engine():
    return mock.Mock(spec=["deidentify_for_llm_result", "extract_diseases", "extract_drugs"])


class TestCaseFileExtraction(unittest.TestCase):
    def test_dates_from_both_documents_with_sources(self):
        cf = build_case_file(DENIAL, RECORD)
        values = [d["value"] for d in cf["dates"]]
        self.assertIn("September 8, 2026", values)
        self.assertIn("August 2, 2026", values)
        sources = {d["value"]: d["source"] for d in cf["dates"]}
        self.assertEqual(sources["September 8, 2026"], "denial letter")
        self.assertEqual(sources["August 2, 2026"], "related record")

    def test_amounts_extracted(self):
        self.assertEqual(extract_amounts(DENIAL + " " + RECORD), ["$1,200.00", "$480.00"])

    def test_denial_reason_canonical_match(self):
        self.assertEqual(classify_reason(DENIAL), "not medically necessary")

    def test_denial_reason_ambiguous_fails_closed(self):
        # Matches two canonical options -> no confident reason.
        text = "Denied as experimental and out of network."
        self.assertIsNone(classify_reason(text))
        cf = build_case_file(text)
        self.assertTrue(cf["denial_reason"]["needs_human"])
        self.assertEqual(cf["denial_reason"]["value"], "")

    def test_denial_reason_reason_in_record_attributes_source(self):
        cf = build_case_file("Claim denied.", RECORD.replace("Physical therapy", "formulary"))
        # formulary alias lives in the record text, not the denial
        self.assertEqual(cf["denial_reason"]["value"], "formulary exclusion")
        self.assertEqual(cf["denial_reason"]["source"], "related record")

    def test_plan_language_quotes_are_verbatim(self):
        quotes = extract_plan_language(DENIAL)
        self.assertTrue(quotes, "at least one plan sentence quoted")
        for q in quotes:
            self.assertIn(q, DENIAL)

    def test_citation_list_only_from_present_facts(self):
        cf = build_case_file(DENIAL, RECORD, user_words="PT came first and I followed the plan.")
        citations = appeal_letter._case_file_citations(cf)
        facts = " | ".join(c["fact"] for c in citations)
        self.assertIn("$1,200.00", facts)
        self.assertIn("September 8, 2026", facts)
        self.assertIn("the user's own words", facts)
        for c in citations:
            self.assertTrue(c["source"], "every citation names its source")


class TestModelOffLetter(unittest.TestCase):
    def _generate_model_off(self, denial=DENIAL, record=RECORD, words="I did the therapy first."):
        engine = _stub_engine()
        fallback = unavailable_structured_fallback(reason="model_disabled")
        with mock.patch.object(appeal_letter, "structured_model_call", return_value=fallback):
            return generate_appeal_letter(engine, denial, record, words)

    def test_letter_contains_only_user_provided_facts(self):
        result = self._generate_model_off()
        self.assertFalse(result["model_generated"])
        self.assertIn("not medically necessary", result["letter"])
        self.assertIn("$1,200.00", result["letter"])
        self.assertIn("September 8, 2026", result["letter"])
        self.assertIn("I did the therapy first.", result["letter"])

    def test_letter_never_invents_amounts_or_dates(self):
        result = self._generate_model_off(denial="Claim denied as not medically necessary.")
        for amount in extract_amounts(DENIAL):
            self.assertNotIn(amount, result["letter"])
        self.assertNotIn("September 8, 2026", result["letter"])
        # honest note explains assembly
        self.assertIn("assembled on this device", result["note"])

    def test_marker_nested_for_acceptance_shape(self):
        result = self._generate_model_off()
        self.assertTrue(result["structured_output"].get("_model_blocked"))

    def test_empty_denial_short_circuits_without_model(self):
        engine = _stub_engine()
        with mock.patch.object(
            appeal_letter, "structured_model_call"
        ) as call:
            result = generate_appeal_letter(engine, "  ")
            call.assert_not_called()
        self.assertEqual(result["letter"], "")
        self.assertTrue(result["needs_human"])


class TestModelOnLetter(unittest.TestCase):
    def test_model_letter_flows_through_and_citations_survive(self):
        engine = _stub_engine()
        canned = {
            "letter": "Subject: Formal appeal\n\nDear Appeals Department, ...",
            "summary": "uses the case file",
            "deidentification_status": "success",
        }
        with mock.patch.object(
            appeal_letter, "structured_model_call", return_value=canned
        ) as call:
            result = generate_appeal_letter(engine, DENIAL, RECORD, "my words")
            call.assert_once = None  # pyflakes silence; assertion below
            self.assertEqual(call.call_count, 1)
            prompt = call.call_args.kwargs.get("user_text") or call.call_args.args[1]
            self.assertIn("not medically necessary", prompt)
            self.assertIn("$1,200.00", prompt)
        self.assertTrue(result["model_generated"])
        self.assertIn("Formal appeal", result["letter"])
        self.assertEqual(result["note"], "")
        self.assertTrue(result["citations"])

    def test_prompt_carries_user_words_and_record_quotes(self):
        engine = _stub_engine()
        canned = {"letter": "Subject: x", "summary": "ok"}
        with mock.patch.object(
            appeal_letter, "structured_model_call", return_value=canned
        ) as call:
            generate_appeal_letter(engine, DENIAL, RECORD, "six weeks of PT")
            prompt = call.call_args.kwargs.get("user_text") or call.call_args.args[1]
        self.assertIn("six weeks of PT", prompt)
        self.assertIn("Physical therapy notes", prompt)

    def test_unparseable_model_output_falls_back_to_deterministic_letter(self):
        engine = _stub_engine()
        canned = {"summary": "partial text without a letter", "_raw_text": True}
        with mock.patch.object(appeal_letter, "structured_model_call", return_value=canned):
            result = generate_appeal_letter(engine, DENIAL, RECORD)
        self.assertFalse(result["model_generated"])
        self.assertIn("$1,200.00", result["letter"])


class TestNoNewNetworkSurface(unittest.TestCase):
    def test_module_reuses_the_gated_client_no_direct_http(self):
        import inspect
        from pathlib import Path

        source = Path(appeal_letter.__file__).read_text()
        for banned in ("import httpx", "import openai", "requests.", "urllib.request"):
            self.assertNotIn(banned, source, f"appeal_letter must not import its own transport ({banned})")

    def test_reason_vocabulary_is_shared_with_the_fighter(self):
        self.assertIs(
            appeal_letter._DENIAL_REASON_ALIASES,
            __import__(
                "healthadvocate.core.insurance_fighter", fromlist=["x"]
            )._DENIAL_REASON_ALIASES,
        )


class TestAppealLetterHttp(unittest.TestCase):
    def setUp(self):
        from healthadvocate.app import app
        self.client = TestClient(app)

    def test_model_off_endpoint_returns_letter_and_marker(self):
        # Hermetic: the acceptance session can leave a model-success env
        # active until session teardown, so the model-off leg is forced at
        # the module seam rather than trusted from process env.
        fallback = unavailable_structured_fallback(reason="model_disabled")
        with mock.patch.object(
            healthadvocate_module, "structured_model_call", return_value=fallback
        ):
            response = self.client.post(
                "/api/insurance/appeal-letter",
                json={"denial_text": DENIAL, "record_text": RECORD, "user_words": "PT first."},
            )
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertFalse(body["model_generated"])
        self.assertTrue(body["structured_output"].get("_model_blocked"))
        self.assertIn("$1,200.00", body["letter"])
        self.assertTrue(body["citations"])

    def test_length_validation(self):
        response = self.client.post(
            "/api/insurance/appeal-letter",
            json={"denial_text": "x" * 60_000},
        )
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
