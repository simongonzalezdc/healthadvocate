"""Commitment Gate zero-side-effect tests (issue 82)."""

from __future__ import annotations

import unittest

from healthadvocate.coverage.commitment_gate import (
    PROHIBITED_INTENTS,
    GateState,
    Intent,
    OutboundRecorder,
    evaluate_intent,
    request_commitment,
    reset_outbound_recorder,
)


class CommitmentGateTests(unittest.TestCase):
    def setUp(self) -> None:
        reset_outbound_recorder()

    def test_every_prohibited_intent_maps_to_gate_state(self):
        expected = {
            "payment": GateState.BLOCKED,
            "submission": GateState.REVIEW_REQUIRED,
            "withdrawal": GateState.REVIEW_REQUIRED,
            "plan_selection": GateState.REVIEW_REQUIRED,
            "plan_change": GateState.REVIEW_REQUIRED,
            "cancellation": GateState.REVIEW_REQUIRED,
            "outbound_message": GateState.REVIEW_REQUIRED,
            "prescribe": GateState.BLOCKED,
            "dose_change": GateState.BLOCKED,
            "treatment_change": GateState.BLOCKED,
            "unknown": GateState.REVIEW_REQUIRED,
        }
        for name, state in expected.items():
            decision = evaluate_intent(name)
            self.assertEqual(decision.gate_state, state, name)
            self.assertEqual(decision.side_effects, [])

    def test_allowed_local_intents(self):
        for name in (
            "local_save",
            "local_view",
            "generate_script",
            "attach_evidence",
            "append_contact_note",
            "export_local",
        ):
            decision = evaluate_intent(name)
            self.assertEqual(decision.gate_state, GateState.ALLOWED, name)

    def test_unknown_defaults_to_review_required(self):
        decision = evaluate_intent("teleport_money_to_insurer")
        self.assertEqual(decision.gate_state, GateState.REVIEW_REQUIRED)
        self.assertEqual(decision.intent, Intent.UNKNOWN)

    def test_zero_side_effects_for_prohibited_intents(self):
        recorder = OutboundRecorder()
        executed_flags = []

        def boom():
            executed_flags.append(True)
            recorder.record("http", url="https://evil.example/pay")
            return "sent"

        for intent in PROHIBITED_INTENTS:
            before = recorder.count
            result = request_commitment(intent, recorder=recorder, execute=boom)
            self.assertFalse(result["executed"], intent)
            self.assertEqual(result["side_effects"], [])
            self.assertEqual(recorder.count, before, intent)
            self.assertIn(result["gate_state"], {"blocked", "review_required"})

        self.assertEqual(executed_flags, [])
        self.assertEqual(recorder.count, 0)

    def test_allowed_intent_may_run_local_execute(self):
        recorder = OutboundRecorder()
        result = request_commitment(
            "local_save",
            recorder=recorder,
            execute=lambda: {"saved": True},
        )
        self.assertTrue(result["executed"])
        self.assertEqual(result["result"], {"saved": True})
        self.assertEqual(recorder.count, 0)

    def test_api_response_shape_is_understandable(self):
        result = request_commitment("payment")
        for key in (
            "gate_state",
            "intent",
            "reason",
            "allowed_next_steps",
            "side_effects",
            "executed",
        ):
            self.assertIn(key, result)
        self.assertTrue(result["reason"])
        self.assertTrue(result["allowed_next_steps"])
        self.assertEqual(result["side_effects"], [])
        self.assertFalse(result["executed"])


if __name__ == "__main__":
    unittest.main()
