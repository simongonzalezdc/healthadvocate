"""OpenMed model management and inference wrapper."""

from __future__ import annotations

import hashlib
import time
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

from healthadvocate.governance.policy_audit import record_policy_audit
from healthadvocate.privacy.boundary import (
    DEIDENTIFICATION_FAILED_PLACEHOLDER,
    DeidentificationResult,
    DeidentificationStatus,
    PrivacyBoundary,
)
from healthadvocate.privacy.policy_profiles import (
    resolve_permitted_policy,
    verify_policy_audit_report,
)

import openmed
from openmed import ModelLoader, OpenMedConfig


@dataclass
class EntityMatch:
    text: str
    label: str
    confidence: float
    start: int
    end: int
    category: str


@dataclass
class AnalysisResult:
    entities: list[EntityMatch] = field(default_factory=list)
    model_used: str = ""
    processing_time: float = 0.0
    error: str = ""


def _extract_entities(raw_result: object, category: str) -> list[EntityMatch]:
    """Extract EntityMatch list from an openmed PredictionResult or dict."""
    entities: list[EntityMatch] = []

    # PredictionResult has .entities attribute
    if hasattr(raw_result, "entities"):
        items = raw_result.entities
    elif isinstance(raw_result, dict):
        items = raw_result.get("entities", [])
        if not items:
            items = raw_result.get("predictions", [])
    elif isinstance(raw_result, list):
        items = raw_result
    else:
        return entities

    for item in items:
        if isinstance(item, dict):
            entities.append(EntityMatch(
                text=item.get("text", item.get("word", "")),
                label=item.get("label", item.get("entity_group", item.get("entity", ""))),
                confidence=float(item.get("confidence", item.get("score", 0.0))),
                start=int(item.get("start", 0)),
                end=int(item.get("end", 0)),
                category=category,
            ))
        elif hasattr(item, "text"):
            entities.append(EntityMatch(
                text=item.text,
                label=getattr(item, "label", getattr(item, "entity_group", "")),
                confidence=float(getattr(item, "confidence", getattr(item, "score", 0.0))),
                start=int(getattr(item, "start", 0)),
                end=int(getattr(item, "end", 0)),
                category=category,
            ))
    return entities


class HealthEngine:
    """Central OpenMed inference wrapper shared by all feature modules."""

    def __init__(self) -> None:
        self._loader: Optional[ModelLoader] = None
        # Optional override for the Wave-2a policy-audit ledger location
        # (build/receipts/policy-audit by default). Test/ops injection point.
        self.policy_audit_receipts_dir: Optional[Path] = None

    @property
    def loader(self) -> ModelLoader:
        if self._loader is None:
            self._loader = ModelLoader()
        return self._loader

    def preload(self) -> None:
        """Pre-warm the most commonly used models (call at startup)."""
        logger.info("Pre-loading OpenMed models...")
        start = time.time()
        # Trigger model loading by creating a pipeline for each key model
        for model_name in (
            "disease_detection_superclinical",
            "pharma_detection_superclinical",
            "anatomy_detection_electramed",
        ):
            try:
                self.loader.create_pipeline(
                    model_name,
                    task="token-classification",
                    aggregation_strategy="simple",
                )
                logger.info("  Loaded: %s", model_name)
            except Exception as exc:
                logger.warning("  Failed to preload %s: %s", model_name, exc)
        elapsed = time.time() - start
        logger.info("Model pre-loading complete (%.1fs)", elapsed)

    def analyze(
        self,
        text: str,
        model_name: str,
        confidence: float = 0.5,
        category: str = "unknown",
    ) -> AnalysisResult:
        """Run NER analysis and return normalized results."""
        start = time.time()
        try:
            raw = openmed.analyze_text(
                text,
                model_name,
                loader=self.loader,
                output_format="dict",
                confidence_threshold=confidence,
                group_entities=True,
            )
        except Exception as exc:
            logger.error("analyze_text failed with %s: %s", model_name, exc)
            return AnalysisResult(model_used=model_name, processing_time=0.0, error=str(exc))

        elapsed = time.time() - start
        entities = _extract_entities(raw, category)
        return AnalysisResult(
            entities=entities,
            model_used=model_name,
            processing_time=round(elapsed, 3),
        )

    def unload_models(self) -> dict:
        """Release cached OpenMed models for the dev loop (RAM win after
        battery/model-enabled runs; openmed>=2.5.0 loader API). Fail-open to a
        no-op receipt when the loader predates the unload API or is a test
        fake — unloading is maintenance, never a safety surface.
        """
        unload_all = getattr(self.loader, "unload_all_models", None)
        if not callable(unload_all):
            return {"models": 0, "tokenizers": 0, "pipelines": 0, "supported": False}
        released = dict(unload_all())
        released["supported"] = True
        logger.info(
            "engine.unload_models models=%s tokenizers=%s pipelines=%s",
            released.get("models", 0),
            released.get("tokenizers", 0),
            released.get("pipelines", 0),
        )
        return released

    def extract_diseases(self, text: str, confidence: float = 0.65) -> AnalysisResult:
        return self.analyze(text, "disease_detection_superclinical", confidence, "disease")

    def extract_drugs(self, text: str, confidence: float = 0.70) -> AnalysisResult:
        return self.analyze(text, "pharma_detection_superclinical", confidence, "drug")

    def extract_anatomy(self, text: str, confidence: float = 0.60) -> AnalysisResult:
        return self.analyze(text, "anatomy_detection_electramed", confidence, "anatomy")

    def extract_pii(self, text: str, lang: str = "en") -> AnalysisResult:
        start = time.time()
        try:
            raw = openmed.extract_pii(text, lang=lang, loader=self.loader)
        except Exception as exc:
            logger.error("extract_pii failed: %s", exc)
            return AnalysisResult(model_used="pii", processing_time=0.0, error=str(exc))

        elapsed = time.time() - start
        entities = _extract_entities(raw, "pii")
        return AnalysisResult(
            entities=entities,
            model_used="pii",
            processing_time=round(elapsed, 3),
        )

    def deidentify(self, text: str, method: str = "mask") -> str:
        try:
            result = openmed.deidentify(text, method=method, loader=self.loader)
            return result.deidentified_text
        except Exception as exc:
            # Fail closed: never return raw text when deidentification fails.
            logger.error("deidentify failed code=deidentify_exception type=%s", type(exc).__name__)
            return DEIDENTIFICATION_FAILED_PLACEHOLDER

    def deidentify_for_llm(self, text: str, method: str = "mask") -> tuple[str, dict[str, str]]:
        """Return (safe_text, mapping). Mapping includes status keys for callers.

        Status is explicit via `_deidentification_status`:
        success | no_pii_found | failed
        """
        result = self.deidentify_for_llm_result(text, method=method)
        mapping = dict(result.mapping)
        mapping["_deidentification_status"] = result.status.value
        if result.status == DeidentificationStatus.FAILED:
            mapping["_deidentification_failed"] = result.error_code or "failed"
        return result.safe_text, mapping

    def deidentify_for_llm_result(
        self,
        text: str,
        method: str = "mask",
        *,
        profile_context: str = "",
        evidence_metadata: str = "",
        notes: str = "",
        canaries: list[str] | None = None,
        policy: str | None = None,
    ) -> DeidentificationResult:
        """Deidentify the fully assembled model context through PrivacyBoundary.

        Wave 2a (RALPLAN row 4): ``policy`` is OPT-IN. ``None`` (default) keeps
        exactly the legacy openmed call and behavior. A permitted policy name
        (healthadvocate.privacy.policy_profiles allowlist) is threaded to
        ``openmed.deidentify(..., policy=...)`` and the run must be backed by a
        verifiable ``AuditReport`` on the result — unknown policies, missing
        audit reports, failed hash verification, or an unwritable governance
        ledger all fail closed through the existing deid-failure path. A policy
        can only add redaction/audit posture, never remove any.
        """

        def _record_audit(
            policy_name: str,
            *,
            verified: bool,
            repro_hash: str = "",
            error_code: str = "",
            requested_policy_digest: str = "",
        ) -> bool:
            """Write the HA-E78 policy-audit receipt; True iff recorded.

            Failure-leg callers ignore the result (the run is already closed);
            the pass leg treats False as a fail-closed condition.
            """
            try:
                record_policy_audit(
                    policy=policy_name,
                    verified=verified,
                    repro_hash=repro_hash,
                    error_code=error_code,
                    requested_policy_digest=requested_policy_digest,
                    receipts_dir=(
                        Path(self.policy_audit_receipts_dir)
                        if self.policy_audit_receipts_dir
                        else None
                    ),
                )
                return True
            except Exception as exc:  # noqa: BLE001 — logging must never leak text
                logger.error(
                    "policy_audit receipt write failed code=%s type=%s",
                    error_code or "policy_audit",
                    type(exc).__name__,
                )
                return False

        def _policy_failure(code: str) -> tuple[str, dict[str, str]]:
            logger.error("deidentify_for_llm failed code=%s", code)
            return DEIDENTIFICATION_FAILED_PLACEHOLDER, {
                "_deidentification_failed": code,
            }

        def _engine_deidentify(assembled: str) -> tuple[str, dict[str, str]]:
            # Default path: byte-identical to the pre-Wave-2a call — policy is
            # not threaded at all when unset.
            if policy is None:
                try:
                    raw = openmed.deidentify(
                        assembled,
                        method=method,
                        loader=self.loader,
                        keep_mapping=True,
                    )
                    pii_map = getattr(raw, "mapping", {}) or {}
                    return raw.deidentified_text, dict(pii_map)
                except Exception as exc:
                    logger.error(
                        "deidentify_for_llm failed code=deidentify_exception type=%s",
                        type(exc).__name__,
                    )
                    return DEIDENTIFICATION_FAILED_PLACEHOLDER, {
                        "_deidentification_failed": type(exc).__name__,
                    }

            resolved = resolve_permitted_policy(policy)
            if resolved is None:
                _record_audit(
                    "",
                    verified=False,
                    error_code="policy_unknown",
                    # Digest (never the raw string) lets the ledger correlate
                    # the rejected request without echoing attacker text.
                    requested_policy_digest=hashlib.sha256(
                        policy.encode("utf-8")
                    ).hexdigest()[:16],
                )
                return _policy_failure("policy_unknown")

            try:
                raw = openmed.deidentify(
                    assembled,
                    method=method,
                    loader=self.loader,
                    keep_mapping=True,
                    policy=resolved,
                )
            except Exception as exc:
                logger.error(
                    "deidentify_for_llm failed code=deidentify_exception type=%s",
                    type(exc).__name__,
                )
                return DEIDENTIFICATION_FAILED_PLACEHOLDER, {
                    "_deidentification_failed": type(exc).__name__,
                }

            audit_report = getattr(raw, "audit_report", None)
            if audit_report is None:
                _record_audit(
                    resolved,
                    verified=False,
                    error_code="policy_audit_missing",
                )
                return _policy_failure("policy_audit_missing")

            # The report must be verified AS EVIDENCE FOR THIS RUN: real
            # AuditReport instance, well-formed hash, self-consistent, built
            # under the requested policy, and bound to the assembled input
            # and the returned output (ADV-004/005/008/009).
            (
                verified,
                repro_hash,
                audit_error,
            ) = verify_policy_audit_report(
                audit_report,
                expected_policy=resolved,
                input_text=assembled,
                deidentified_text=raw.deidentified_text,
            )
            if not verified:
                error_code = audit_error or "policy_audit_verification_failed"
                _record_audit(
                    resolved,
                    verified=False,
                    repro_hash=repro_hash,
                    error_code=error_code,
                )
                return _policy_failure(error_code)

            # A pass without recorded governance evidence is a silent pass:
            # the receipt is required, not best-effort.
            if not _record_audit(
                resolved,
                verified=True,
                repro_hash=repro_hash,
            ):
                return _policy_failure("policy_audit_receipt_write_failed")

            pii_map = getattr(raw, "mapping", {}) or {}
            return raw.deidentified_text, dict(pii_map)

        boundary = PrivacyBoundary(
            deidentify_fn=_engine_deidentify,
            canaries=canaries or [],
        )
        return boundary.prepare_model_input(
            text,
            profile_context=profile_context,
            evidence_metadata=evidence_metadata,
            notes=notes,
        )

    def privacy_boundary(self, canaries: list[str] | None = None) -> PrivacyBoundary:
        def _engine_deidentify(assembled: str) -> tuple[str, dict[str, str]]:
            return self.deidentify_for_llm(assembled)[:2]

        return PrivacyBoundary(deidentify_fn=_engine_deidentify, canaries=canaries)


def format_entities_with_confidence(entities: list[EntityMatch]) -> str:
    if not entities:
        return "No medical entities detected by NER."
    parts = []
    for e in entities:
        if e.confidence >= 0.85:
            cert = "very high certainty"
        elif e.confidence >= 0.70:
            cert = "high certainty"
        elif e.confidence >= 0.50:
            cert = "moderate certainty, may need verification"
        else:
            cert = "low certainty, possibly incidental"
        parts.append(f"'{e.text}' ({e.label}, {e.confidence:.0%} confidence - {cert})")
    return "; ".join(parts)
