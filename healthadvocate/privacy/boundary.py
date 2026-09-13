"""Central Privacy Boundary for assembled model input."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Mapping, Optional

from healthadvocate.privacy.endpoint_policy import (
    EndpointPolicyError,
    assert_loopback_model_url,
)
from healthadvocate.privacy.logging_redaction import redact_text

logger = logging.getLogger(__name__)

DEIDENTIFICATION_FAILED_PLACEHOLDER = (
    "[Input withheld because de-identification failed. "
    "Retry locally before sending this text to a model.]"
)


class DeidentificationStatus(str, Enum):
    SUCCESS = "success"
    NO_PII_FOUND = "no_pii_found"
    FAILED = "failed"


class PrivacyBoundaryError(RuntimeError):
    """Raised when model processing must not proceed."""


@dataclass(frozen=True)
class DeidentificationResult:
    status: DeidentificationStatus
    safe_text: str
    mapping: Mapping[str, str] = field(default_factory=dict)
    error_code: str = ""

    @property
    def allows_model_call(self) -> bool:
        return self.status in {
            DeidentificationStatus.SUCCESS,
            DeidentificationStatus.NO_PII_FOUND,
        }


DeidentifyFn = Callable[[str], tuple[str, dict[str, str]]]


class PrivacyBoundary:
    """Assemble context, deidentify, and gate model destination policy."""

    def __init__(
        self,
        deidentify_fn: Optional[DeidentifyFn] = None,
        canaries: Optional[list[str]] = None,
    ) -> None:
        self._deidentify_fn = deidentify_fn
        self._canaries = list(canaries or [])

    def assemble_context(
        self,
        user_text: str,
        *,
        profile_context: str = "",
        evidence_metadata: str = "",
        notes: str = "",
        extra_sections: Optional[Mapping[str, str]] = None,
    ) -> str:
        sections: list[str] = []
        if profile_context.strip():
            sections.append(profile_context.strip())
        if evidence_metadata.strip():
            sections.append("Evidence metadata:\n" + evidence_metadata.strip())
        if notes.strip():
            sections.append("Notes:\n" + notes.strip())
        if extra_sections:
            for title, body in extra_sections.items():
                if body and str(body).strip():
                    sections.append(f"{title}:\n{str(body).strip()}")
        if user_text.strip():
            sections.append(user_text.strip())
        return "\n\n".join(sections)

    def deidentify_assembled(
        self,
        assembled_text: str,
    ) -> DeidentificationResult:
        if self._deidentify_fn is None:
            return DeidentificationResult(
                status=DeidentificationStatus.FAILED,
                safe_text=DEIDENTIFICATION_FAILED_PLACEHOLDER,
                mapping={},
                error_code="deidentify_unavailable",
            )
        try:
            safe_text, mapping = self._deidentify_fn(assembled_text)
        except Exception as exc:  # noqa: BLE001 — fail closed
            logger.error(
                "privacy.deidentify_failed code=deidentify_exception detail=%s",
                type(exc).__name__,
            )
            return DeidentificationResult(
                status=DeidentificationStatus.FAILED,
                safe_text=DEIDENTIFICATION_FAILED_PLACEHOLDER,
                mapping={},
                error_code="deidentify_exception",
            )

        if mapping.get("_deidentification_failed"):
            return DeidentificationResult(
                status=DeidentificationStatus.FAILED,
                safe_text=DEIDENTIFICATION_FAILED_PLACEHOLDER,
                mapping={},
                error_code="deidentify_engine_failed",
            )

        # Defensive: if configured canaries remain, treat as failure.
        for canary in self._canaries:
            if canary and canary in safe_text:
                logger.error(
                    "privacy.deidentify_failed code=canary_remained"
                )
                return DeidentificationResult(
                    status=DeidentificationStatus.FAILED,
                    safe_text=DEIDENTIFICATION_FAILED_PLACEHOLDER,
                    mapping={},
                    error_code="canary_remained",
                )

        if mapping:
            status = DeidentificationStatus.SUCCESS
        else:
            status = DeidentificationStatus.NO_PII_FOUND
        return DeidentificationResult(
            status=status,
            safe_text=safe_text,
            mapping=dict(mapping),
            error_code="",
        )

    def prepare_model_input(
        self,
        user_text: str,
        *,
        profile_context: str = "",
        evidence_metadata: str = "",
        notes: str = "",
        extra_sections: Optional[Mapping[str, str]] = None,
    ) -> DeidentificationResult:
        assembled = self.assemble_context(
            user_text,
            profile_context=profile_context,
            evidence_metadata=evidence_metadata,
            notes=notes,
            extra_sections=extra_sections,
        )
        return self.deidentify_assembled(assembled)

    def assert_model_allowed(
        self,
        result: DeidentificationResult,
        model_url: str,
    ) -> str:
        """Return validated model URL or raise PrivacyBoundaryError."""
        if not result.allows_model_call:
            raise PrivacyBoundaryError(
                "Model call blocked: deidentification status is "
                f"{result.status.value}"
            )
        try:
            return assert_loopback_model_url(model_url, allow_redirects=False)
        except EndpointPolicyError as exc:
            # Do not include the raw URL if it might embed userinfo secrets.
            raise PrivacyBoundaryError(
                "Model call blocked: endpoint policy rejected destination"
            ) from exc

    def safe_error_message(self, exc: BaseException) -> str:
        return redact_text(str(exc), self._canaries)
