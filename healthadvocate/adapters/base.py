"""Shared adapter contracts and claim boundaries."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, FrozenSet


@dataclass(frozen=True)
class AdapterEvidence:
    source: str
    source_revision: str
    retrieved_at: str
    checksum: str
    claim_class: str
    permitted_claims: tuple[str, ...]
    forbidden_claims: tuple[str, ...]
    payload: dict[str, Any]
    attribution: str = ""
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "source": self.source,
            "source_revision": self.source_revision,
            "retrieved_at": self.retrieved_at,
            "checksum": self.checksum,
            "claim_class": self.claim_class,
            "permitted_claims": list(self.permitted_claims),
            "forbidden_claims": list(self.forbidden_claims),
            "payload": dict(self.payload),
            "attribution": self.attribution,
            "notes": self.notes,
        }


class ClaimContractError(ValueError):
    pass


def assert_no_forbidden_keys(payload: dict[str, Any], forbidden: FrozenSet[str]) -> None:
    for key in payload:
        if key in forbidden:
            raise ClaimContractError(f"forbidden claim key present: {key}")
