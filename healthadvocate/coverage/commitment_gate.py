"""Commitment Gate: classify intents; never execute external side effects."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Callable, Optional


class GateState(str, Enum):
    ALLOWED = "allowed"
    REVIEW_REQUIRED = "review_required"
    BLOCKED = "blocked"
    NOT_APPLICABLE = "not_applicable"


class Intent(str, Enum):
    # Allowed local preparation
    LOCAL_SAVE = "local_save"
    LOCAL_VIEW = "local_view"
    GENERATE_SCRIPT = "generate_script"
    ATTACH_EVIDENCE = "attach_evidence"
    APPEND_CONTACT_NOTE = "append_contact_note"
    EXPORT_LOCAL = "export_local"
    # Prohibited / review
    PAYMENT = "payment"
    SUBMISSION = "submission"
    WITHDRAWAL = "withdrawal"
    PLAN_SELECTION = "plan_selection"
    PLAN_CHANGE = "plan_change"
    CANCELLATION = "cancellation"
    OUTBOUND_MESSAGE = "outbound_message"
    PRESCRIBE = "prescribe"
    DOSE_CHANGE = "dose_change"
    TREATMENT_CHANGE = "treatment_change"
    UNKNOWN = "unknown"


_ALLOWED = frozenset(
    {
        Intent.LOCAL_SAVE,
        Intent.LOCAL_VIEW,
        Intent.GENERATE_SCRIPT,
        Intent.ATTACH_EVIDENCE,
        Intent.APPEND_CONTACT_NOTE,
        Intent.EXPORT_LOCAL,
    }
)

_BLOCKED = frozenset(
    {
        Intent.PAYMENT,
        Intent.PRESCRIBE,
        Intent.DOSE_CHANGE,
        Intent.TREATMENT_CHANGE,
    }
)

_REVIEW = frozenset(
    {
        Intent.SUBMISSION,
        Intent.WITHDRAWAL,
        Intent.PLAN_SELECTION,
        Intent.PLAN_CHANGE,
        Intent.CANCELLATION,
        Intent.OUTBOUND_MESSAGE,
        Intent.UNKNOWN,
    }
)

_ALIASES: dict[str, Intent] = {
    "pay": Intent.PAYMENT,
    "payment": Intent.PAYMENT,
    "charge": Intent.PAYMENT,
    "purchase": Intent.PAYMENT,
    "submit": Intent.SUBMISSION,
    "submission": Intent.SUBMISSION,
    "submit_application": Intent.SUBMISSION,
    "withdraw": Intent.WITHDRAWAL,
    "withdrawal": Intent.WITHDRAWAL,
    "select_plan": Intent.PLAN_SELECTION,
    "plan_selection": Intent.PLAN_SELECTION,
    "change_plan": Intent.PLAN_CHANGE,
    "plan_change": Intent.PLAN_CHANGE,
    "cancel": Intent.CANCELLATION,
    "cancellation": Intent.CANCELLATION,
    "cancel_coverage": Intent.CANCELLATION,
    "message": Intent.OUTBOUND_MESSAGE,
    "send_message": Intent.OUTBOUND_MESSAGE,
    "email": Intent.OUTBOUND_MESSAGE,
    "sms": Intent.OUTBOUND_MESSAGE,
    "outbound_message": Intent.OUTBOUND_MESSAGE,
    "prescribe": Intent.PRESCRIBE,
    "prescription": Intent.PRESCRIBE,
    "dose": Intent.DOSE_CHANGE,
    "dose_change": Intent.DOSE_CHANGE,
    "change_dose": Intent.DOSE_CHANGE,
    "treatment_change": Intent.TREATMENT_CHANGE,
    "change_treatment": Intent.TREATMENT_CHANGE,
    "local_save": Intent.LOCAL_SAVE,
    "save": Intent.LOCAL_SAVE,
    "local_view": Intent.LOCAL_VIEW,
    "view": Intent.LOCAL_VIEW,
    "generate_script": Intent.GENERATE_SCRIPT,
    "script": Intent.GENERATE_SCRIPT,
    "attach_evidence": Intent.ATTACH_EVIDENCE,
    "evidence": Intent.ATTACH_EVIDENCE,
    "append_contact_note": Intent.APPEND_CONTACT_NOTE,
    "contact_note": Intent.APPEND_CONTACT_NOTE,
    "export_local": Intent.EXPORT_LOCAL,
    "export": Intent.EXPORT_LOCAL,
}


@dataclass
class GateDecision:
    gate_state: GateState
    intent: Intent
    reason: str
    allowed_next_steps: list[str] = field(default_factory=list)
    side_effects: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate_state": self.gate_state.value,
            "intent": self.intent.value,
            "reason": self.reason,
            "allowed_next_steps": list(self.allowed_next_steps),
            "side_effects": list(self.side_effects),
        }


class OutboundRecorder:
    """Records attempted outbound calls for tests. Production uses a no-op."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def record(self, kind: str, **payload: Any) -> None:
        self.calls.append({"kind": kind, **payload})

    @property
    def count(self) -> int:
        return len(self.calls)

    def clear(self) -> None:
        self.calls.clear()


_DEFAULT_RECORDER = OutboundRecorder()


def get_outbound_recorder() -> OutboundRecorder:
    return _DEFAULT_RECORDER


def reset_outbound_recorder() -> None:
    _DEFAULT_RECORDER.clear()


def normalize_intent(raw: str | Intent) -> Intent:
    if isinstance(raw, Intent):
        return raw
    key = (raw or "").strip().lower().replace("-", "_").replace(" ", "_")
    if not key:
        return Intent.UNKNOWN
    if key in _ALIASES:
        return _ALIASES[key]
    try:
        return Intent(key)
    except ValueError:
        return Intent.UNKNOWN


def evaluate_intent(raw_intent: str | Intent) -> GateDecision:
    intent = normalize_intent(raw_intent)
    if intent in _ALLOWED:
        return GateDecision(
            gate_state=GateState.ALLOWED,
            intent=intent,
            reason="Local preparation action with no external commitment.",
            allowed_next_steps=["Continue in the Coverage workflow"],
            side_effects=[],
        )
    if intent in _BLOCKED:
        return GateDecision(
            gate_state=GateState.BLOCKED,
            intent=intent,
            reason=(
                "HealthAdvocate will not perform this action. It requires a "
                "human decision outside this application."
            ),
            allowed_next_steps=[
                "Prepare a script or checklist",
                "Record the outcome later as a Contact Event",
            ],
            side_effects=[],
        )
    # review_required for review set and any unknown
    return GateDecision(
        gate_state=GateState.REVIEW_REQUIRED,
        intent=intent,
        reason=(
            "This action could create an external, financial, coverage, or "
            "communication commitment. Review it yourself before acting outside "
            "the app. HealthAdvocate will not submit or send anything."
        ),
        allowed_next_steps=[
            "Review prepared materials",
            "Generate a deterministic script",
            "Act only through official portals or people you choose",
        ],
        side_effects=[],
    )


def request_commitment(
    raw_intent: str | Intent,
    *,
    recorder: Optional[OutboundRecorder] = None,
    execute: Optional[Callable[[], Any]] = None,
) -> dict[str, Any]:
    """Evaluate an intent and refuse execution for non-allowed states.

    `execute` is only invoked when the gate state is ALLOWED. Prohibited
    intents never call execute and never record outbound side effects.
    """
    decision = evaluate_intent(raw_intent)
    rec = recorder or get_outbound_recorder()
    executed = False
    result_payload: Any = None

    if decision.gate_state == GateState.ALLOWED:
        if execute is not None:
            result_payload = execute()
            executed = True
    else:
        # Explicitly do not call execute; assert zero outbound growth.
        if execute is not None:
            # Swallow: never run external work for blocked/review paths.
            pass
        # Do not record outbound calls for blocked intents.
        _ = rec.count

    payload = decision.to_dict()
    payload["executed"] = executed
    payload["result"] = result_payload
    return payload


PROHIBITED_INTENTS: tuple[str, ...] = tuple(
    i.value for i in sorted(_BLOCKED | _REVIEW, key=lambda x: x.value)
)
