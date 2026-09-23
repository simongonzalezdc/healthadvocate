"""Governance receipts for opt-in policy-audited deidentification (Wave 2a).

HA-E78 ledger lineage (same evidence family as the license-provenance gate):
every opt-in policy run leaves a receipt under ``build/receipts/policy-audit``
following the existing receipt file shapes (JSON, ``indent=2``,
``sort_keys=True``, trailing newline — see gate.write_receipts).

No raw text, no canaries, ever: a receipt carries only the permitted policy
name, the audit reproducibility hash, the verification result, and build
metadata. Unknown requested policy names are never echoed — only a SHA-256
digest of the requested string is recorded, for correlation without content.

The ledger is append-once and idempotent: the filename is derived from the
verification event's identity (policy, outcome, reproducibility hash, error
code), so recording the same event twice leaves exactly one unchanged file.
Wall-clock ``generated_at`` and ``build_revision`` are metadata recorded at
first write and never rewrite an existing receipt.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from healthadvocate.governance.registry import TOOL_VERSION
from healthadvocate.privacy.policy_profiles import PERMITTED_POLICY_PROFILES

RECEIPTS_DIR = Path("build") / "receipts" / "policy-audit"

REVIEWER = "policy-audit"
STOP_RULE = (
    "A policy-audited deidentification run is evidenced only by a verified "
    "openmed AuditReport reproducibility hash; unknown policies, missing "
    "audit reports, and hash mismatches fail closed with a failure receipt."
)


@dataclass(frozen=True)
class PolicyAuditReceipt:
    """One policy-audit verification event in the HA-E78 ledger.

    Fields mirror the license-gate receipt envelope (evidence_id,
    build_revision, generated_at, tool_version, result, reviewer, stop_rule,
    contains_real_phi) plus the policy-audit specifics (policy,
    reproducibility_hash, verification_result, error_code,
    requested_policy_digest).
    """

    build_revision: str
    generated_at: str
    result: str  # "pass" | "fail" — verification outcome
    policy: str  # permitted canonical name; "" when the request was unknown
    reproducibility_hash: str
    verification_result: bool
    error_code: str = ""
    requested_policy_digest: str = ""
    evidence_id: str = "HA-E78"
    tool_version: str = TOOL_VERSION
    reviewer: str = REVIEWER
    stop_rule: str = STOP_RULE
    contains_real_phi: bool = False

    def to_dict(self) -> dict:
        data = asdict(self)
        data["verification_result"] = bool(self.verification_result)
        data["contains_real_phi"] = bool(self.contains_real_phi)
        return data

    def identity_digest(self) -> str:
        """Stable digest of the verification event (excludes timestamps)."""
        identity = {
            "evidence_id": self.evidence_id,
            "result": self.result,
            "policy": self.policy,
            "reproducibility_hash": self.reproducibility_hash,
            "verification_result": self.verification_result,
            "error_code": self.error_code,
            "requested_policy_digest": self.requested_policy_digest,
        }
        canonical = json.dumps(identity, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]

    def filename(self) -> str:
        slug = self.policy if self.policy in PERMITTED_POLICY_PROFILES else "unknown"
        return f"receipt-policy-{slug}-{self.identity_digest()}.json"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _git_revision(project_root: Path) -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=project_root,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip() or "unknown"
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def default_project_root() -> Path:
    """Repository root holding the ``build/receipts`` ledger (best effort)."""
    return Path(__file__).resolve().parents[2]


def default_receipts_dir() -> Path:
    return default_project_root() / RECEIPTS_DIR


def write_policy_audit_receipt(
    receipt: PolicyAuditReceipt,
    output_dir: Path,
) -> Path:
    """Write one append-once receipt; identical events never rewrite it."""
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / receipt.filename()
    if path.exists():
        return path
    payload = json.dumps(receipt.to_dict(), indent=2, sort_keys=True) + "\n"
    path.write_text(payload, encoding="utf-8")
    return path


def record_policy_audit(
    *,
    policy: str,
    verified: bool,
    repro_hash: str = "",
    error_code: str = "",
    requested_policy_digest: str = "",
    receipts_dir: Path | None = None,
    project_root: Path | None = None,
) -> Path:
    """Build and write one policy-audit receipt; returns its path.

    ``policy`` must be a permitted canonical name; pass ``""`` with
    ``requested_policy_digest`` for unknown-policy failures so the requested
    string is never echoed into the ledger. Raises on filesystem errors —
    callers decide whether that must fail the run closed.
    """
    root = project_root or default_project_root()
    receipt = PolicyAuditReceipt(
        build_revision=_git_revision(root),
        generated_at=_utc_now(),
        result="pass" if verified else "fail",
        policy=policy,
        reproducibility_hash=repro_hash,
        verification_result=verified,
        error_code=error_code,
        requested_policy_digest=requested_policy_digest,
    )
    return write_policy_audit_receipt(receipt, receipts_dir or default_receipts_dir())
