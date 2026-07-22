"""Optional unofficial PolicyEngine-style eligibility estimate (feature-flagged)."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any


FEATURE_FLAG = "HEALTHADVOCATE_POLICYENGINE_ENABLED"
ENGINE_NAME = "policyengine-us-unofficial-stub"
RULE_VERSION = "fixture-rules-2026.07"


def feature_enabled(env: dict[str, str] | None = None) -> bool:
    source = env if env is not None else os.environ
    return source.get(FEATURE_FLAG, "0").strip().lower() in {"1", "true", "yes", "on"}


def unofficial_eligibility_estimate(
    inputs: dict[str, Any],
    *,
    env: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Return an explicitly unofficial estimate or a disabled response.

    This is a local deterministic stub of the PolicyEngine US workflow shape.
    It does not call the network and does not submit applications.
    """
    if not feature_enabled(env):
        return {
            "enabled": False,
            "label": "unofficial_estimate_disabled",
            "message": (
                "PolicyEngine US estimate is disabled by default. "
                "The manual Coverage workflow does not depend on it."
            ),
            "official_verification_action": (
                "Use official county/state/marketplace channels to verify eligibility."
            ),
        }

    missing = [
        key
        for key in ("household_size", "monthly_income", "state")
        if inputs.get(key) in (None, "", [])
    ]
    assumptions = {
        "engine": ENGINE_NAME,
        "rule_version": RULE_VERSION,
        "inputs_used": {
            k: inputs.get(k) for k in ("household_size", "monthly_income", "state", "age")
        },
        "missing_inputs": missing,
        "calculation_date": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
    }

    # Deterministic toy band — not official eligibility.
    estimate = "unknown"
    if not missing:
        size = float(inputs["household_size"])
        income = float(inputs["monthly_income"])
        fpl_proxy = 1000 * size
        if income <= fpl_proxy:
            estimate = "may_qualify_for_further_official_review"
        else:
            estimate = "may_not_qualify_based_on_income_proxy_only"

    return {
        "enabled": True,
        "label": "unofficial_estimate",
        "not_official_eligibility": True,
        "estimate": estimate,
        "engine": ENGINE_NAME,
        "rule_version": RULE_VERSION,
        "assumptions": assumptions,
        "missing_inputs": missing,
        "calculation_date": assumptions["calculation_date"],
        "official_verification_action": (
            "Verify through official Medi-Cal / Medicaid / marketplace channels. "
            "This estimate does not submit an application and is not a determination."
        ),
        "side_effects": [],
    }
