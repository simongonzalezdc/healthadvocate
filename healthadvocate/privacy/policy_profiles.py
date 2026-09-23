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

# Version of the installed openmed package the constants were enumerated from.
OPENMED_POLICY_SOURCE_VERSION = "2.5.0"

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


def verify_policy_audit_report(report: object) -> tuple[bool, str]:
    """Validate an openmed ``AuditReport`` and return ``(ok, repro_hash)``.

    Validation is ``openmed.core.audit.verify_repro_hash`` (the module-level
    checker over ``AuditReport.repro_hash_matches``, audit.py:1343): the
    stored reproducibility hash must match the hash recomputed from the
    report's canonical payload. ``AuditReport.verify(...)`` is NOT used: it
    requires a non-empty HMAC release key and a signed report, and HA holds
    no key material (no secrets). Any exception during verification — wrong
    shape, tampering artifacts, upstream changes — fails closed.
    """
    repro_hash = ""
    try:
        repro_hash = str(getattr(report, "repro_hash", "") or "")
        from openmed.core.audit import verify_repro_hash

        ok = bool(verify_repro_hash(report))
    except Exception:  # noqa: BLE001 — verification must fail closed
        return False, repro_hash
    return ok, repro_hash
