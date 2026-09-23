"""Governance receipts for opt-in policy-audited deidentification (Wave 2a).

HA-E78 ledger lineage (same evidence family as the license-provenance gate):
every opt-in policy run leaves a receipt under ``build/receipts/policy-audit``
following the existing receipt file shapes (JSON, ``indent=2``,
``sort_keys=True``, trailing newline — see gate.write_receipts).

No raw text, no canaries, ever: a receipt carries only the permitted policy
name, the audit reproducibility hash, the verification result, a one-way
16-hex digest of the run's assembled input (failure-volume evidence, never
reversible to text), and build metadata. Unknown requested policy names are
never echoed — only a SHA-256 digest of the requested string is recorded,
for correlation without content. This contract is enforced at the ledger
boundary: ``write_policy_audit_receipt`` sanitizes every free-form field
(permitted policy names, canonical ``sha256:<64 hex>`` hashes, the error-code
vocabulary, hex digests) and derives ``result`` from ``verification_result``
so contradictory evidence cannot be written, whatever the calling path.

The ledger is append-once and idempotent: the filename is derived from the
verification event's identity (policy, outcome, reproducibility hash, error
code, run input digest), so recording the same event for the same input
twice leaves exactly one unchanged file. CONSEQUENCE, stated plainly:
repeated IDENTICAL failing runs (same policy, same error code, same input
digest) collapse into that one receipt — the ledger evidences failure
VOLUME across distinct runs (distinct inputs, policies, or outcomes each
get their own file), not repetition count of a single identical event.
Wall-clock ``generated_at`` and ``build_revision`` are metadata recorded at
first write and never rewrite an existing receipt.

Writes are atomic (temp file + fsync + ``os.replace``), so a crash can never
leave a truncated receipt; and the append-once check treats only a PARSEABLE
existing file as recorded — an unparseable file (external corruption,
partial write by an older non-atomic writer) is rewritten cleanly instead of
sticking forever.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
from dataclasses import asdict, dataclass, replace
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

# Ledger-field contracts (ADV-008): anything not matching is replaced with ""
# before serialization — an unvalidated, possibly attacker-controlled value
# must never reach the ledger file, whatever the calling path.
_REPRO_HASH_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_ERROR_CODE_RE = re.compile(r"^[a-z0-9_]*$")
_REQUESTED_DIGEST_RE = re.compile(r"^[0-9a-f]{16}$")
_RUN_DIGEST_RE = re.compile(r"^[0-9a-f]{16}$")


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
    result: str  # "pass" | "fail" — derived from verification_result at write
    policy: str  # permitted canonical name; "" when the request was unknown
    reproducibility_hash: str
    verification_result: bool
    error_code: str = ""
    requested_policy_digest: str = ""
    run_input_digest: str = ""  # 16-hex sha256 of the assembled input
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
        """Stable digest of the verification event (excludes timestamps).

        Includes the run input digest so distinct failing runs over distinct
        documents each leave their own receipt (failure-volume evidence);
        identical events on identical inputs still collapse to one file.
        """
        identity = {
            "evidence_id": self.evidence_id,
            "result": self.result,
            "policy": self.policy,
            "reproducibility_hash": self.reproducibility_hash,
            "verification_result": self.verification_result,
            "error_code": self.error_code,
            "requested_policy_digest": self.requested_policy_digest,
            "run_input_digest": self.run_input_digest,
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


def _sanitize_receipt(receipt: PolicyAuditReceipt) -> PolicyAuditReceipt:
    """Return a copy whose free-form fields are provenance-safe.

    Only permitted policy names, canonical-format hashes, our error-code
    vocabulary, and hex digests may appear in a ledger file; every other
    value is blanked (ADV-008: no raw text, no canaries, ever — enforced at
    the ledger boundary, not just at the caller). ``result`` is DERIVED from
    ``verification_result`` so the pair can never contradict.
    """
    return replace(
        receipt,
        result="pass" if receipt.verification_result else "fail",
        policy=receipt.policy if receipt.policy in PERMITTED_POLICY_PROFILES else "",
        reproducibility_hash=(
            receipt.reproducibility_hash
            if _REPRO_HASH_RE.match(receipt.reproducibility_hash or "")
            else ""
        ),
        error_code=(
            receipt.error_code if _ERROR_CODE_RE.match(receipt.error_code or "") else ""
        ),
        requested_policy_digest=(
            receipt.requested_policy_digest
            if _REQUESTED_DIGEST_RE.match(receipt.requested_policy_digest or "")
            else ""
        ),
        run_input_digest=(
            receipt.run_input_digest
            if _RUN_DIGEST_RE.match(receipt.run_input_digest or "")
            else ""
        ),
        evidence_id="HA-E78",
        tool_version=TOOL_VERSION,
        reviewer=REVIEWER,
        stop_rule=STOP_RULE,
        contains_real_phi=False,
    )


def _receipt_intact(path: Path) -> bool:
    """A recorded receipt is a PARSEABLE file; corruption is not 'recorded'."""
    try:
        json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return True


def write_policy_audit_receipt(
    receipt: PolicyAuditReceipt,
    output_dir: Path,
) -> Path:
    """Write one append-once receipt; identical events never rewrite it.

    Atomic (temp file + fsync + ``os.replace``) so a crash mid-write cannot
    leave a truncated entry; an existing but UNPARSEABLE file at the target
    name is rewritten cleanly (self-heal) instead of sticking forever.
    """
    receipt = _sanitize_receipt(receipt)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / receipt.filename()
    if path.exists() and _receipt_intact(path):
        return path
    payload = json.dumps(receipt.to_dict(), indent=2, sort_keys=True) + "\n"
    fd, tmp_name = tempfile.mkstemp(
        dir=output_dir, prefix=".receipt-", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    except BaseException:
        Path(tmp_name).unlink(missing_ok=True)
        raise
    return path


def record_policy_audit(
    *,
    policy: str,
    verified: bool,
    repro_hash: str = "",
    error_code: str = "",
    requested_policy_digest: str = "",
    run_input_digest: str = "",
    receipts_dir: Path | None = None,
    project_root: Path | None = None,
) -> Path:
    """Build and write one policy-audit receipt; returns its path.

    ``policy`` must be a permitted canonical name; pass ``""`` with
    ``requested_policy_digest`` for unknown-policy failures so the requested
    string is never echoed into the ledger. ``run_input_digest`` is the
    16-hex sha256 of the run's assembled input (failure-volume evidence;
    a digest, never text). Raises on filesystem errors — callers decide
    whether that must fail the run closed.
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
        run_input_digest=run_input_digest,
    )
    return write_policy_audit_receipt(receipt, receipts_dir or default_receipts_dir())
