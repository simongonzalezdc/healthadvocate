"""Commitment Gate: classify intents; never execute external side effects.

HA-JEV J2-a (2026-09-22): the intent classification routes through the
typed-decision layer (healthadvocate/coverage/intent_decision.py) when the
caller supplies the identify stage's evidence. The conversion is additive:

- Without identify evidence the gate decides exactly as before — the typed
  layer never engages and no receipt is fabricated.
- With identify evidence (an analysis plus its stated deidentification
  status), the classifier's pick is adjudicated behind the receipt
  contract. Any fail-closed typed leg (NEEDS_HUMAN wrapper or identify
  errors) DOWNGRADES an otherwise-allowed intent to review-only with the
  existing fail-closed sentence — never a new permissive path. Prohibited
  intents stay byte-equivalent regardless of the typed outcome: the set
  logic below is untouched and dominates the wrapper (audit numbers, not
  permissions). See intent_decision.py for the receipt, confidence, and
  threshold policy of this surface.
"""

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

_INTENT_VALUES: frozenset[str] = frozenset(intent.value for intent in Intent)

# The product's core fail-closed sentence — byte-identical to the BLOCKED
# reason below; decisions.FAIL_CLOSED_SENTENCE is pinned equal to it by
# tests/test_ha_jev_decisions.py.
_FAIL_CLOSED_REASON = (
    "HealthAdvocate will not perform this action. It requires a "
    "human decision outside this application."
)

_REVIEW_REASON = (
    "This action could create an external, financial, coverage, or "
    "communication commitment. Review it yourself before acting outside "
    "the app. HealthAdvocate will not submit or send anything."
)

_REVIEW_STEPS = [
    "Review prepared materials",
    "Generate a deterministic script",
    "Act only through official portals or people you choose",
]


@dataclass
class GateDecision:
    gate_state: GateState
    intent: Intent
    reason: str
    allowed_next_steps: list[str] = field(default_factory=list)
    side_effects: list[str] = field(default_factory=list)
    # HA-JEV J2-a audit additives (annotations stay stringified — the
    # decisions package imports this module, so the types are never
    # imported here at runtime). Deliberately NOT serialized: to_dict()
    # keeps the exact legacy payload shape for the /api/coverage/
    # commitment-gate endpoint.
    typed_decision: "DecisionOutcome | None" = None
    identify_errors: "list[StrippedValidationError]" = field(
        default_factory=list
    )

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


def _intent_key(raw: str) -> str:
    return (raw or "").strip().lower().replace("-", "_").replace(" ", "_")


def normalize_intent(raw: str | Intent) -> Intent:
    if isinstance(raw, Intent):
        return raw
    key = _intent_key(raw)
    if not key:
        return Intent.UNKNOWN
    if key in _ALIASES:
        return _ALIASES[key]
    try:
        return Intent(key)
    except ValueError:
        return Intent.UNKNOWN


def exact_intent_match(raw: str | Intent) -> bool:
    """True when the classifier's pick is an exact table/enum match.

    False for the UNKNOWN fallback (no alias, no enum value matched) —
    the distinction the typed layer's confidence constants are built on.
    An Intent instance is exact by definition.
    """
    if isinstance(raw, Intent):
        return True
    key = _intent_key(raw)
    return bool(key) and (key in _ALIASES or key in _INTENT_VALUES)


def evaluate_intent(
    raw_intent: str | Intent,
    *,
    analysis: Any = None,
    deidentification_status: Any = None,
    canaries: Any = (),
    thresholds: Any = None,
) -> GateDecision:
    """Classify an intent and decide its gate state.

    HA-JEV J2-a: when `analysis` (identify-stage evidence) is supplied,
    the pick is additionally adjudicated behind the receipt contract via
    healthadvocate/coverage/intent_decision.py. The typed layer can only
    REMOVE permissions: an engaged-but-unanswered adjudication (any
    NEEDS_HUMAN wrapper leg, or identify errors when no receipt could be
    built) downgrades an otherwise-allowed intent to review-only with the
    existing fail-closed sentence. Prohibited and review intents return
    exactly the legacy decision in every case — the wrapper attaches
    audit numbers, never permissions. Without `analysis` the typed layer
    does not engage at all and the decision is byte-identical to the
    pre-conversion gate.
    """
    intent = normalize_intent(raw_intent)
    typed_decision: Any = None
    identify_errors: list[Any] = []
    if analysis is not None:
        # Local import: healthadvocate.decisions imports this module at
        # load time (assess -> GateState), so the dependency arrow points
        # function-ward only.
        from healthadvocate.coverage.intent_decision import adjudicate_intent

        typed_decision, identify_errors = adjudicate_intent(
            raw_intent,
            analysis=analysis,
            deidentification_status=deidentification_status,
            canaries=canaries,
            thresholds=thresholds,
        )
    typed_answered = (
        typed_decision is not None
        and typed_decision.outcome.value == "ANSWERED"
    )

    if intent in _ALLOWED:
        if analysis is not None and not typed_answered:
            # Fail-closed typed leg: review-only, the existing sentence.
            # With a wrapper, its deterministic next steps (amendment g)
            # ride along; without one (identify errors), the legacy
            # review steps.
            return GateDecision(
                gate_state=GateState.REVIEW_REQUIRED,
                intent=intent,
                reason=_FAIL_CLOSED_REASON,
                allowed_next_steps=(
                    list(typed_decision.allowed_next_steps)
                    if typed_decision is not None
                    else list(_REVIEW_STEPS)
                ),
                side_effects=[],
                typed_decision=typed_decision,
                identify_errors=list(identify_errors),
            )
        return GateDecision(
            gate_state=GateState.ALLOWED,
            intent=intent,
            reason="Local preparation action with no external commitment.",
            allowed_next_steps=["Continue in the Coverage workflow"],
            side_effects=[],
            typed_decision=typed_decision,
            identify_errors=list(identify_errors),
        )
    if intent in _BLOCKED:
        return GateDecision(
            gate_state=GateState.BLOCKED,
            intent=intent,
            reason=_FAIL_CLOSED_REASON,
            allowed_next_steps=[
                "Prepare a script or checklist",
                "Record the outcome later as a Contact Event",
            ],
            side_effects=[],
            typed_decision=typed_decision,
            identify_errors=list(identify_errors),
        )
    # review_required for review set and any unknown
    return GateDecision(
        gate_state=GateState.REVIEW_REQUIRED,
        intent=intent,
        reason=_REVIEW_REASON,
        allowed_next_steps=list(_REVIEW_STEPS),
        side_effects=[],
        typed_decision=typed_decision,
        identify_errors=list(identify_errors),
    )


def request_commitment(
    raw_intent: str | Intent,
    *,
    recorder: Optional[OutboundRecorder] = None,
    execute: Optional[Callable[[], Any]] = None,
    analysis: Any = None,
    deidentification_status: Any = None,
    canaries: Any = (),
    thresholds: Any = None,
) -> dict[str, Any]:
    """Evaluate an intent and refuse execution for non-allowed states.

    `execute` is only invoked when the gate state is ALLOWED. Prohibited
    intents never call execute and never record outbound side effects.
    The HA-JEV identify-stage keyword arguments pass through to
    evaluate_intent (additive; the endpoint payload is unchanged).
    """
    decision = evaluate_intent(
        raw_intent,
        analysis=analysis,
        deidentification_status=deidentification_status,
        canaries=canaries,
        thresholds=thresholds,
    )
    rec = recorder or get_outbound_recorder()
    executed = False
    result_payload: Any = None

    if decision.gate_state == GateState.ALLOWED:
        if execute is not None:
            result_payload = execute()
            executed = True
    # Non-allowed states deliberately do not call execute or mutate the recorder.

    payload = decision.to_dict()
    payload["executed"] = executed
    payload["result"] = result_payload
    return payload


PROHIBITED_INTENTS: tuple[str, ...] = tuple(
    i.value for i in sorted(_BLOCKED | _REVIEW, key=lambda x: x.value)
)
