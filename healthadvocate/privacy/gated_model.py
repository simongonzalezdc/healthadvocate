"""Gate model calls behind full-context deidentification and endpoint policy."""

from __future__ import annotations

from typing import Any, Optional

from healthadvocate.core.engine import HealthEngine
from healthadvocate.core.llm_client import (
    chat_structured,
    unavailable_structured_fallback,
)
from healthadvocate.core import family_tracker
from healthadvocate.privacy.boundary import DeidentificationStatus


def structured_model_call(
    engine: HealthEngine,
    user_text: str,
    *,
    module_type: str,
    system: str,
    profile_id: str | None = None,
    evidence_metadata: str = "",
    notes: str = "",
    canaries: Optional[list[str]] = None,
    max_tokens: int = 1200,
) -> dict[str, Any]:
    """Assemble context, deidentify, then optionally call the local model.

    On deidentification failure or disabled model, returns a safe fallback
    with zero outbound model side effects when the runtime is absent/blocked.
    """
    profile_context = ""
    if profile_id:
        profile = family_tracker.get_profile(profile_id)
        profile_context = family_tracker.format_family_context(profile)

    result = engine.deidentify_for_llm_result(
        user_text,
        profile_context=profile_context,
        evidence_metadata=evidence_metadata,
        notes=notes,
        canaries=canaries,
    )
    if result.status == DeidentificationStatus.FAILED:
        fallback = unavailable_structured_fallback(reason="deidentification_failed")
        fallback["deidentification_status"] = result.status.value
        fallback["summary"] = (
            "Model processing was blocked because privacy protection failed. "
            "No model request was sent."
        )
        return fallback

    output = chat_structured(
        result.safe_text,
        module_type=module_type,
        system=system,
        max_tokens=max_tokens,
    )
    if isinstance(output, dict):
        output = dict(output)
        output["deidentification_status"] = result.status.value
        output["pii_mapping_size"] = len(result.mapping)
    return output
