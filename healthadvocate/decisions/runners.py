"""Runner registry (design 2026-09-22 §4).

Three runners, pluggable behind the existing model gate pattern:

1. `code` — deterministic rules (the default; most current decision
   points).
2. `local-ml` — openmed NER/PII confidences feeding typed decisions; its
   answers carry the `score_source` honesty field (amendment d).
3. `hosted-jev` — the actual Jev API. INERT stub (amendment e): no URL,
   no HTTP client, no env read. OFF by default and CEO-gated forever —
   the gate flag does not exist in code, and absence IS the gate. Zero
   active code path until the CEO's dated word (J3, additive tier; leaves
   assert_loopback_model_url and PrivacyBoundary.assert_model_allowed
   untouched).
"""

from __future__ import annotations

from dataclasses import dataclass

DEFAULT_RUNNER = "code"


class HostedJevGateError(RuntimeError):
    """Any attempt to exercise the hosted-jev runner fails loudly.

    Mirrors the PrivacyBoundary error posture (policy violations raise;
    calibration and data problems fail closed into the NEEDS_HUMAN
    wrapper instead).
    """


HOSTED_JEV_GATE_MESSAGE = (
    "hosted-jev runner is CEO-gated and structurally OFF: the gate flag "
    "does not exist in code — absence IS the gate (design §4 runner 3; "
    "lands only in J3 with the CEO's dated word)"
)


@dataclass(frozen=True)
class RunnerSpec:
    """Static runner metadata — J1 ships no runner execution; surfaces
    supply the deterministic rule or openmed-derived candidate and the
    gate in `assess` adjudicates it."""

    name: str
    description: str
    hosted: bool = False


RUNNERS: dict[str, RunnerSpec] = {
    "code": RunnerSpec(
        name="code",
        description=(
            "Deterministic rules where the four-question test says code "
            "wins; the default runner for most current decision points."
        ),
    ),
    "local-ml": RunnerSpec(
        name="local-ml",
        description=(
            "openmed NER/PII confidences feeding typed decisions; answers "
            "must carry score_source (raw|calibrated) honesty."
        ),
    ),
    "hosted-jev": RunnerSpec(
        name="hosted-jev",
        description=HOSTED_JEV_GATE_MESSAGE,
        hosted=True,
    ),
}


def runner_names() -> tuple[str, ...]:
    return tuple(RUNNERS)


def get_runner(name: str) -> RunnerSpec | None:
    return RUNNERS.get(name)


def hosted_jev_call(*args: object, **kwargs: object) -> None:
    """The hosted-jev stub. Structurally OFF: it does only this, forever,
    until J3 — and J3 itself requires the CEO's dated word."""
    raise HostedJevGateError(HOSTED_JEV_GATE_MESSAGE)
