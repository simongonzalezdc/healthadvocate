"""F1b — the share-safe pack: on-device PHI anonymization.

A patient should be able to hand a document to a new doctor, an insurer,
or a forum WITHOUT leaking every name, date, and phone number in it.
OpenMed's DocumentStreamDeidentifier runs IN-PROCESS (no network, ever);
this module wraps it with a lazy singleton so the first call pays the
model load and nothing after does.

Honesty contract: masking is deterministic and type-labeled ([first_name],
[date], [phone_number]...). We report exactly what was removed — counts per
type and the total — and never claim more safety than the masks deliver.
The replacement table stays in memory only for the life of the request.
"""
from __future__ import annotations

import logging
import threading
from typing import Any

logger = logging.getLogger(__name__)

_lock = threading.Lock()
_deidentifier: Any = None


def _get_deidentifier():
    """Lazy singleton; the PII model loads once per process."""
    global _deidentifier
    if _deidentifier is None:
        with _lock:
            if _deidentifier is None:
                from openmed import DocumentStreamDeidentifier

                logger.info("share-safe: loading PII deidentifier (first call)")
                _deidentifier = DocumentStreamDeidentifier(method="mask", lang="en")
    return _deidentifier


def make_share_safe(text: str) -> dict:
    """Return {clean_text, counts, total} for a piece of text.

    Deterministic masking, on-device. Empty input returns an empty result
    (0 removed) rather than an error — an empty document is already safe.
    """
    if not text or not text.strip():
        return {"clean_text": "", "counts": {}, "total": 0}

    result = _get_deidentifier().run(text)
    counts: dict[str, int] = {}
    for entity in getattr(result, "pii_entities", []) or []:
        label = getattr(entity, "label", None) or "unknown"
        counts[label] = counts.get(label, 0) + 1

    clean = getattr(result, "redacted_text", None)
    if clean is None:
        # method='mask' always produces redacted_text; guard anyway so the
        # endpoint can never silently return the ORIGINAL text as "safe"
        raise RuntimeError("deidentifier produced no redacted output — refusing to return unsafe text")

    return {
        "clean_text": clean,
        "counts": dict(sorted(counts.items())),
        "total": sum(counts.values()),
    }
