"""Coverage Case domain: aggregate root, provenance, and lifecycle invariants."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional
from uuid import uuid4


class CaseLifecycle(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    NEEDS_REVIEW = "needs-review"
    BLOCKED = "blocked"
    CLOSED = "closed"


_ALLOWED_TRANSITIONS: dict[CaseLifecycle, frozenset[CaseLifecycle]] = {
    CaseLifecycle.DRAFT: frozenset({CaseLifecycle.ACTIVE, CaseLifecycle.CLOSED}),
    CaseLifecycle.ACTIVE: frozenset(
        {CaseLifecycle.NEEDS_REVIEW, CaseLifecycle.BLOCKED, CaseLifecycle.CLOSED}
    ),
    CaseLifecycle.NEEDS_REVIEW: frozenset(
        {CaseLifecycle.ACTIVE, CaseLifecycle.BLOCKED, CaseLifecycle.CLOSED}
    ),
    CaseLifecycle.BLOCKED: frozenset(
        {CaseLifecycle.NEEDS_REVIEW, CaseLifecycle.ACTIVE, CaseLifecycle.CLOSED}
    ),
    CaseLifecycle.CLOSED: frozenset(),
}


class FactStatus(str, Enum):
    VERIFIED = "verified"
    USER_REPORTED = "user-reported"
    INFERRED = "inferred"
    UNKNOWN = "unknown"
    STALE = "stale"
    CONFLICTED = "conflicted"


class ClaimClass(str, Enum):
    OFFICIAL_SOURCE = "official_source"
    USER_REPORTED = "user_reported"
    DERIVED = "derived"
    MODEL_DRAFT = "model_draft"
    UNKNOWN = "unknown"
    CONFLICTED = "conflicted"
    STALE = "stale"


class ContinuityTargetKind(str, Enum):
    PROVIDER = "provider"
    MEDICATION = "medication"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:12]}"


@dataclass
class MaterialFact:
    fact_id: str
    label: str
    value: str
    status: FactStatus
    claim_class: ClaimClass
    provenance: str
    observed_at: str
    retrieved_at: str
    freshness_policy: str = "manual"
    source_evidence_id: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        data["claim_class"] = self.claim_class.value
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MaterialFact":
        return cls(
            fact_id=data["fact_id"],
            label=data["label"],
            value=data["value"],
            status=FactStatus(data["status"]),
            claim_class=ClaimClass(data["claim_class"]),
            provenance=data["provenance"],
            observed_at=data["observed_at"],
            retrieved_at=data["retrieved_at"],
            freshness_policy=data.get("freshness_policy", "manual"),
            source_evidence_id=data.get("source_evidence_id"),
        )


@dataclass(frozen=True)
class EvidenceItem:
    """Immutable dated evidence. Never mutate after creation."""

    evidence_id: str
    title: str
    source: str
    observed_at: str
    retrieved_at: str
    checksum: str
    claim_class: ClaimClass
    summary: str
    raw_ref: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "title": self.title,
            "source": self.source,
            "observed_at": self.observed_at,
            "retrieved_at": self.retrieved_at,
            "checksum": self.checksum,
            "claim_class": self.claim_class.value,
            "summary": self.summary,
            "raw_ref": self.raw_ref,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EvidenceItem":
        return cls(
            evidence_id=data["evidence_id"],
            title=data["title"],
            source=data["source"],
            observed_at=data["observed_at"],
            retrieved_at=data["retrieved_at"],
            checksum=data["checksum"],
            claim_class=ClaimClass(data["claim_class"]),
            summary=data["summary"],
            raw_ref=data.get("raw_ref", ""),
        )


@dataclass(frozen=True)
class ContactEvent:
    """Append-only timeline entry."""

    event_id: str
    occurred_at: str
    channel: str
    party: str
    summary: str
    outcome: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ContactEvent":
        return cls(
            event_id=data["event_id"],
            occurred_at=data["occurred_at"],
            channel=data["channel"],
            party=data["party"],
            summary=data["summary"],
            outcome=data.get("outcome", ""),
        )


@dataclass
class ContinuityTarget:
    target_id: str
    kind: ContinuityTargetKind
    name: str
    facts: list[MaterialFact] = field(default_factory=list)
    risk_notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_id": self.target_id,
            "kind": self.kind.value,
            "name": self.name,
            "facts": [f.to_dict() for f in self.facts],
            "risk_notes": self.risk_notes,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ContinuityTarget":
        return cls(
            target_id=data["target_id"],
            kind=ContinuityTargetKind(data["kind"]),
            name=data["name"],
            facts=[MaterialFact.from_dict(f) for f in data.get("facts", [])],
            risk_notes=data.get("risk_notes", ""),
        )


@dataclass
class CoverageCase:
    case_id: str
    title: str
    lifecycle: CaseLifecycle
    created_at: str
    updated_at: str
    next_action: str
    deadlines: list[dict[str, str]] = field(default_factory=list)
    targets: list[ContinuityTarget] = field(default_factory=list)
    evidence: list[EvidenceItem] = field(default_factory=list)
    contacts: list[ContactEvent] = field(default_factory=list)
    facts: list[MaterialFact] = field(default_factory=list)
    synthetic: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "title": self.title,
            "lifecycle": self.lifecycle.value,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "next_action": self.next_action,
            "deadlines": list(self.deadlines),
            "targets": [t.to_dict() for t in self.targets],
            "evidence": [e.to_dict() for e in self.evidence],
            "contacts": [c.to_dict() for c in self.contacts],
            "facts": [f.to_dict() for f in self.facts],
            "synthetic": self.synthetic,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CoverageCase":
        return cls(
            case_id=data["case_id"],
            title=data["title"],
            lifecycle=CaseLifecycle(data["lifecycle"]),
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            next_action=data["next_action"],
            deadlines=list(data.get("deadlines") or []),
            targets=[ContinuityTarget.from_dict(t) for t in data.get("targets", [])],
            evidence=[EvidenceItem.from_dict(e) for e in data.get("evidence", [])],
            contacts=[ContactEvent.from_dict(c) for c in data.get("contacts", [])],
            facts=[MaterialFact.from_dict(f) for f in data.get("facts", [])],
            synthetic=bool(data.get("synthetic", True)),
        )

    def transition(self, new_state: CaseLifecycle) -> None:
        allowed = _ALLOWED_TRANSITIONS[self.lifecycle]
        if new_state not in allowed:
            raise ValueError(
                f"illegal lifecycle transition {self.lifecycle.value} -> {new_state.value}"
            )
        self.lifecycle = new_state
        self.updated_at = utc_now_iso()

    def add_evidence(self, item: EvidenceItem) -> None:
        # Immutability: only append; never replace by id.
        if any(e.evidence_id == item.evidence_id for e in self.evidence):
            raise ValueError("Evidence Items are immutable; duplicate id rejected")
        self.evidence.append(item)
        self.updated_at = utc_now_iso()

    def add_contact(self, event: ContactEvent) -> None:
        if any(c.event_id == event.event_id for c in self.contacts):
            raise ValueError("Contact Events are append-only; duplicate id rejected")
        self.contacts.append(event)
        self.updated_at = utc_now_iso()

    def replace_evidence(self, item: EvidenceItem) -> None:
        raise RuntimeError("Evidence Items are immutable")

    def update_contact(self, event: ContactEvent) -> None:
        raise RuntimeError("Contact Events are append-only")
