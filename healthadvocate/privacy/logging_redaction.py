"""Redact configured canaries and obvious identifier patterns from logs."""

from __future__ import annotations

import logging
import re
from typing import Iterable

# Synthetic canaries used in tests and defensive redaction.
DEFAULT_CANARIES: tuple[str, ...] = (
    "CANARY_PATIENT_ALPHA_9f3c",
    "CANARY_MEMBER_SYNTH_42",
    "SSN-000-00-0000",
    "MEMBER-ID-SYNTH-42",
)

_SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
_MEMBER_RE = re.compile(r"\bMEMBER-ID-[A-Z0-9_-]+\b", re.IGNORECASE)
_CANARY_RE_TEMPLATE = r"(?i){}"


class CanaryRedactingFilter(logging.Filter):
    def __init__(self, canaries: Iterable[str] | None = None) -> None:
        super().__init__()
        self._canaries = tuple(canaries or DEFAULT_CANARIES)

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            message = record.getMessage()
        except Exception:
            record.msg = "[log message unavailable]"
            record.args = ()
            return True
        redacted = redact_text(message, self._canaries)
        if redacted != message:
            record.msg = redacted
            record.args = ()
        # Never attach raw request bodies.
        if hasattr(record, "request_body"):
            record.request_body = "[redacted]"
        return True


def redact_text(text: str, canaries: Iterable[str] | None = None) -> str:
    if not text:
        return text
    result = text
    for canary in canaries or DEFAULT_CANARIES:
        if not canary:
            continue
        result = re.sub(
            _CANARY_RE_TEMPLATE.format(re.escape(canary)),
            "[REDACTED_CANARY]",
            result,
        )
    result = _SSN_RE.sub("[REDACTED_SSN]", result)
    result = _MEMBER_RE.sub("[REDACTED_MEMBER_ID]", result)
    return result


def install_redacting_log_filter(
    canaries: Iterable[str] | None = None,
    logger: logging.Logger | None = None,
) -> CanaryRedactingFilter:
    target = logger or logging.getLogger()
    filt = CanaryRedactingFilter(canaries=canaries)
    # Avoid duplicate installs.
    for existing in target.filters:
        if isinstance(existing, CanaryRedactingFilter):
            return existing
    target.addFilter(filt)
    for handler in target.handlers:
        handler.addFilter(filt)
    return filt
