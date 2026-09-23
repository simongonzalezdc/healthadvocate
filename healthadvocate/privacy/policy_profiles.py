"""Pinned allowlist of openmed de-identification policy profiles (Wave 2a).

RALPLAN row 4 / docs/OPENMED-UPSTREAM-LEVERAGE-2026-09-17.md line 116:
policy-aware de-identification is OPT-IN. The default engine path passes no
policy and stays byte-identical to the pre-wave call; a policy can only add
redaction posture and audit evidence, never remove any.

The names below are PINNED CONSTANTS enumerated from the installed openmed
2.5.0 package (``openmed/core/policy.py`` class ``PolicyName`` — 20 canonical
values, cross-checked 2026-09-22 against ``CANONICAL_POLICY_NAMES`` and the
bundled ``openmed/core/policies/`` data files). Pinned means an openmed
upgrade can never silently expand what HA accepts: a new upstream profile
becomes usable only through an explicit change to this module.

Deliberately NOT permitted (fail closed):
- aliases (upstream ``POLICY_ALIASES``: "gdpr", "pipeda", "uk_ico", ...)
- case variants ("HIPAA_SAFE_HARBOR")
- bundled non-canonical data profiles ("fhir_hipaa_safe_harbor",
  "omop_research_limited_dataset")
- anything else unknown to this allowlist
"""

from __future__ import annotations

import re

# Version of the installed openmed package the constants were enumerated from.
OPENMED_POLICY_SOURCE_VERSION = "2.5.0"

# Canonical openmed hash format (audit.stable_hash/hash_text -> _sha256_bytes,
# "sha256:<64 lowercase hex>"). Anything else is not a hash we produced and is
# never echoed into the governance ledger (ADV-008).
_REPRO_HASH_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")

HIPAA_SAFE_HARBOR = "hipaa_safe_harbor"
HIPAA_EXPERT_REVIEW_ASSIST = "hipaa_expert_review_assist"
GDPR_PSEUDONYMIZATION = "gdpr_pseudonymization"
GDPR_ART9_HEALTH = "gdpr_art9_health"
RESEARCH_LIMITED_DATASET = "research_limited_dataset"
STRICT_NO_LEAK = "strict_no_leak"
CLINICAL_MINIMAL_REDACTION = "clinical_minimal_redaction"
CLINICAL_PRESERVE = "clinical_preserve"
CANADA_PIPEDA = "canada_pipeda"
UK_ICO_ANONYMISATION = "uk_ico_anonymisation"
AUSTRALIA_PRIVACY_ACT = "australia_privacy_act"
CHINA_PIPL = "china_pipl"
INDIA_DPDP_ACT = "india_dpdp_act"
AFRICA_MALABO_BASELINE = "africa_malabo_baseline"
ZA_POPIA = "za_popia"
NG_NDPA = "ng_ndpa"
KENYA_DPA = "ke_dpa"
INDIA_HEALTH_ID = "india_health_id"
EG_PDPL = "eg_pdpl"
MA_LAW_09_08 = "ma_law_09_08"

PERMITTED_POLICY_PROFILES: frozenset[str] = frozenset(
    {
        HIPAA_SAFE_HARBOR,
        HIPAA_EXPERT_REVIEW_ASSIST,
        GDPR_PSEUDONYMIZATION,
        GDPR_ART9_HEALTH,
        RESEARCH_LIMITED_DATASET,
        STRICT_NO_LEAK,
        CLINICAL_MINIMAL_REDACTION,
        CLINICAL_PRESERVE,
        CANADA_PIPEDA,
        UK_ICO_ANONYMISATION,
        AUSTRALIA_PRIVACY_ACT,
        CHINA_PIPL,
        INDIA_DPDP_ACT,
        AFRICA_MALABO_BASELINE,
        ZA_POPIA,
        NG_NDPA,
        KENYA_DPA,
        INDIA_HEALTH_ID,
        EG_PDPL,
        MA_LAW_09_08,
    }
)


def resolve_permitted_policy(policy: str | None) -> str | None:
    """Return the canonical profile name iff HA permits it, else ``None``.

    Exact match against the pinned allowlist only: no aliases, no case
    folding, no upstream lookup. ``None`` (or anything unknown) means the
    caller must fail closed — the name is never handed to openmed.
    """
    if not isinstance(policy, str):
        return None
    return policy if policy in PERMITTED_POLICY_PROFILES else None


def run_policy_deidentify(
    text: str,
    *,
    method: str,
    policy: str,
    loader: object,
) -> object:
    """Deidentify with a permitted policy AND audit evidence attached.

    The stock top-level ``openmed.deidentify`` cannot return text and audit
    evidence together in 2.5.0: it attaches ``result.audit_report`` only
    under ``audit=True`` (openmed/core/pii.py:2338-2341) and then returns the
    BARE ``AuditReport`` instead of the result object (pii.py:2866-2867).
    This helper mirrors the EXACT Pipeline construction the top-level
    function performs for this kwarg set (pii.py:2822-2846 — verified against
    the installed 2.5.0: every omitted constructor kwarg defaults to the
    value the top-level passes explicitly), requests ``run(..., audit=True)``,
    and returns ``PipelineResult.deidentification_result`` — the full result
    carrying ``deidentified_text``, ``mapping``, and ``audit_report``. This
    is the extension shape upstream's own doctest documents (it patches
    ``openmed.core.pipeline.Pipeline``).

    Raises whatever the pipeline raises; callers fail closed on exception.
    """
    from openmed.core.custom_recognizer import (
        abdm_mode_enabled,
        with_abdm_recognizer,
    )
    from openmed.core.pipeline import Pipeline
    from openmed.core.pii import _DEFAULT_EN_MODEL

    recognizer_config = None
    indian_multi_id_enabled = abdm_mode_enabled(
        None,
        policy=policy,
        lang="en",
        locale=None,
    )
    if indian_multi_id_enabled:
        recognizer_config = with_abdm_recognizer(recognizer_config)

    pipeline = Pipeline(
        model_name=_DEFAULT_EN_MODEL,
        loader=loader,
        policy=policy,
        custom_recognizer=recognizer_config,
        indian_multi_id=indian_multi_id_enabled,
    )
    run_result = pipeline.run(text, method=method, keep_mapping=True, audit=True)
    return run_result.deidentification_result


def verify_policy_audit_report(
    report: object,
    *,
    expected_policy: str,
    input_text: str,
    deidentified_text: str,
) -> tuple[bool, str, str]:
    """Validate an openmed ``AuditReport`` as evidence for THIS run.

    Returns ``(verified, reproducibility_hash, error_code)`` — the hash is
    returned only when it is well-formed (``sha256:<64 hex>``), so an
    attacker-controlled value is never echoed into the ledger (ADV-008).

    Binding checks, in order (each fails closed with its own error code):
    1. shape — must be a real ``openmed.core.audit.AuditReport`` instance;
       dicts and lookalikes self-verify upstream via ``from_dict`` and are
       not acceptable evidence (ADV-009).
    2. format — the stored reproducibility hash must match the canonical
       openmed hash format.
    3. self-consistency — ``openmed.core.audit.verify_repro_hash`` (the
       module-level checker over ``AuditReport.repro_hash_matches``,
       audit.py:1343): the stored hash must match the hash recomputed from
       the report's own payload. This catches post-construction tampering;
       it CANNOT catch a clean rebuild, which is internally consistent by
       construction (``__post_init__`` recomputes over whatever the report
       was built under) — hence the binding checks below.
    4. policy binding — ``report.policy`` must equal the requested (resolved)
       policy, so a report rebuilt under a different profile can never be
       certified as the requested one (ADV-004).
    5. input binding — ``report.input_hash`` must equal ``hash_text`` of the
       assembled input actually deidentified (ADV-005).
    6. output binding — ``report.deidentified_text_hash`` must equal
       ``hash_text`` of the text openmed actually returned (ADV-005).

    ``AuditReport.verify(...)`` is NOT used: it requires a non-empty HMAC
    release key and a signed report, and HA holds no key material (no
    secrets). Any exception during verification fails closed.
    """
    try:
        from openmed.core.audit import AuditReport, hash_text, verify_repro_hash
    except Exception:  # noqa: BLE001 — missing upstream surface fails closed
        return False, "", "policy_audit_invalid_report"

    if not isinstance(report, AuditReport):
        return False, "", "policy_audit_invalid_report"

    repro_hash = str(getattr(report, "repro_hash", "") or "")
    if not _REPRO_HASH_PATTERN.match(repro_hash):
        # Unvalidated (possibly attacker-controlled) value: never return it.
        return False, "", "policy_audit_invalid_report"

    try:
        if not verify_repro_hash(report):
            return False, repro_hash, "policy_audit_verification_failed"
        if str(getattr(report, "policy", "") or "") != expected_policy:
            return False, repro_hash, "policy_audit_policy_mismatch"
        if str(getattr(report, "input_hash", "") or "") != hash_text(input_text):
            return False, repro_hash, "policy_audit_input_mismatch"
        if (
            str(getattr(report, "deidentified_text_hash", "") or "")
            != hash_text(deidentified_text)
        ):
            return False, repro_hash, "policy_audit_output_mismatch"
    except Exception:  # noqa: BLE001 — verification must fail closed
        return False, repro_hash, "policy_audit_verification_failed"
    return True, repro_hash, ""
