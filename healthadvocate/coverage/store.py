"""Encrypted-at-rest Coverage Case store (AES-GCM over SQLite payload)."""

from __future__ import annotations

import json
import os
import sqlite3
import struct
from pathlib import Path
from typing import Optional

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from healthadvocate.coverage.domain import (
    CaseLifecycle,
    ClaimClass,
    ContactEvent,
    ContinuityTarget,
    ContinuityTargetKind,
    CoverageCase,
    EvidenceItem,
    FactStatus,
    MaterialFact,
    new_id,
    utc_now_iso,
)
from healthadvocate.coverage.keystore import InMemoryKeyStore, KeyStore, KeyStoreError

FILE_MAGIC = b"HAC1"  # HealthAdvocate Coverage v1
NONCE_SIZE = 12


class CaseStoreError(RuntimeError):
    pass


class CaseStore:
    """Persist Coverage Cases outside the repository as encrypted SQLite blobs."""

    def __init__(
        self,
        path: Path | str,
        keystore: KeyStore,
        *,
        create: bool = False,
    ) -> None:
        self.path = Path(path)
        self.keystore = keystore
        self._conn: Optional[sqlite3.Connection] = None
        if create or not self.path.exists():
            self._init_new()
        else:
            self._open_existing()

    def close(self) -> None:
        if self._conn is not None:
            self._persist()
            self._conn.close()
            self._conn = None

    def __enter__(self) -> "CaseStore":
        return self
    def __exit__(self, *exc) -> None:
        self.close()

    # -- crypto / open -----------------------------------------------------

    def _encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        nonce = os.urandom(NONCE_SIZE)
        aes = AESGCM(key)
        ciphertext = aes.encrypt(nonce, plaintext, FILE_MAGIC)
        return FILE_MAGIC + nonce + ciphertext

    def _decrypt(self, blob: bytes, key: bytes) -> bytes:
        if len(blob) < 4 + NONCE_SIZE + 16:
            raise CaseStoreError("case store file is truncated or corrupt")
        if blob[:4] != FILE_MAGIC:
            raise CaseStoreError("case store file has unknown format")
        nonce = blob[4 : 4 + NONCE_SIZE]
        ciphertext = blob[4 + NONCE_SIZE :]
        try:
            return AESGCM(key).decrypt(nonce, ciphertext, FILE_MAGIC)
        except Exception as exc:  # InvalidTag, etc.
            raise CaseStoreError(
                "unable to decrypt case store; key is missing or incorrect"
            ) from exc

    def _init_new(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        key = self.keystore.get_or_create_key()
        self._conn = sqlite3.connect(":memory:")
        self._conn.row_factory = sqlite3.Row
        self._create_schema()
        self._persist(key=key)

    def _open_existing(self) -> None:
        try:
            key = self.keystore.get_key()
        except KeyStoreError as exc:
            raise CaseStoreError(
                "unable to open case store; encryption key is missing"
            ) from exc
        blob = self.path.read_bytes()
        plaintext = self._decrypt(blob, key)
        self._conn = sqlite3.connect(":memory:")
        self._conn.row_factory = sqlite3.Row
        self._conn.deserialize(plaintext)
        # Fail closed: prove the key actually yields a readable schema.
        try:
            self._conn.execute("SELECT count(*) FROM coverage_cases").fetchone()
        except sqlite3.Error as exc:
            self._conn.close()
            self._conn = None
            raise CaseStoreError(
                "unable to open case store; key is incorrect or schema unreadable"
            ) from exc

    def _persist(self, key: Optional[bytes] = None) -> None:
        if self._conn is None:
            return
        use_key = key if key is not None else self.keystore.get_key()
        payload = self._conn.serialize()
        encrypted = self._encrypt(payload, use_key)
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_bytes(encrypted)
        os.replace(tmp, self.path)

    def _create_schema(self) -> None:
        assert self._conn is not None
        self._conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS coverage_cases (
                case_id TEXT PRIMARY KEY,
                payload_json TEXT NOT NULL,
                lifecycle TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                synthetic INTEGER NOT NULL DEFAULT 1
            );
            """
        )
        self._conn.commit()

    def _require_conn(self) -> sqlite3.Connection:
        if self._conn is None:
            raise CaseStoreError("case store is closed")
        return self._conn

    # -- CRUD --------------------------------------------------------------

    def create_case(
        self,
        title: str,
        *,
        next_action: str = "Review coverage situation and list deadlines",
        synthetic: bool = True,
    ) -> CoverageCase:
        if not synthetic:
            raise CaseStoreError(
                "real-case import is disabled; only synthetic cases may be created"
            )
        now = utc_now_iso()
        case = CoverageCase(
            case_id=new_id("case"),
            title=title,
            lifecycle=CaseLifecycle.DRAFT,
            created_at=now,
            updated_at=now,
            next_action=next_action,
            synthetic=True,
        )
        self._write_case(case)
        return case

    def _write_case(self, case: CoverageCase) -> None:
        conn = self._require_conn()
        conn.execute(
            """
            INSERT INTO coverage_cases(case_id, payload_json, lifecycle, updated_at, synthetic)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(case_id) DO UPDATE SET
                payload_json=excluded.payload_json,
                lifecycle=excluded.lifecycle,
                updated_at=excluded.updated_at,
                synthetic=excluded.synthetic
            """,
            (
                case.case_id,
                json.dumps(case.to_dict()),
                case.lifecycle.value,
                case.updated_at,
                1 if case.synthetic else 0,
            ),
        )
        conn.commit()
        self._persist()

    def get_case(self, case_id: str) -> CoverageCase:
        conn = self._require_conn()
        row = conn.execute(
            "SELECT payload_json FROM coverage_cases WHERE case_id = ?",
            (case_id,),
        ).fetchone()
        if row is None:
            raise CaseStoreError(f"case not found: {case_id}")
        return CoverageCase.from_dict(json.loads(row["payload_json"]))

    def list_cases(self) -> list[dict]:
        conn = self._require_conn()
        rows = conn.execute(
            "SELECT case_id, lifecycle, updated_at, synthetic, payload_json "
            "FROM coverage_cases ORDER BY updated_at DESC"
        ).fetchall()
        result = []
        for row in rows:
            payload = json.loads(row["payload_json"])
            result.append(
                {
                    "case_id": row["case_id"],
                    "title": payload.get("title", ""),
                    "lifecycle": row["lifecycle"],
                    "updated_at": row["updated_at"],
                    "next_action": payload.get("next_action", ""),
                    "synthetic": bool(row["synthetic"]),
                }
            )
        return result

    def save_case(self, case: CoverageCase) -> CoverageCase:
        case.updated_at = utc_now_iso()
        self._write_case(case)
        return case

    def update_case(
        self,
        case_id: str,
        *,
        title: Optional[str] = None,
        next_action: Optional[str] = None,
        lifecycle: Optional[str] = None,
        deadlines: Optional[list[dict[str, str]]] = None,
    ) -> CoverageCase:
        case = self.get_case(case_id)
        if title is not None:
            case.title = title
        if next_action is not None:
            case.next_action = next_action
        if deadlines is not None:
            case.deadlines = deadlines
        if lifecycle is not None:
            case.transition(CaseLifecycle(lifecycle))
        return self.save_case(case)

    def add_evidence(
        self,
        case_id: str,
        *,
        title: str,
        source: str,
        summary: str,
        claim_class: str = ClaimClass.USER_REPORTED.value,
        checksum: str = "",
        observed_at: Optional[str] = None,
        retrieved_at: Optional[str] = None,
    ) -> CoverageCase:
        case = self.get_case(case_id)
        now = utc_now_iso()
        item = EvidenceItem(
            evidence_id=new_id("ev"),
            title=title,
            source=source,
            observed_at=observed_at or now,
            retrieved_at=retrieved_at or now,
            checksum=checksum or "none",
            claim_class=ClaimClass(claim_class),
            summary=summary,
        )
        case.add_evidence(item)
        return self.save_case(case)

    def add_contact(
        self,
        case_id: str,
        *,
        channel: str,
        party: str,
        summary: str,
        outcome: str = "",
        occurred_at: Optional[str] = None,
    ) -> CoverageCase:
        case = self.get_case(case_id)
        event = ContactEvent(
            event_id=new_id("ce"),
            occurred_at=occurred_at or utc_now_iso(),
            channel=channel,
            party=party,
            summary=summary,
            outcome=outcome,
        )
        case.add_contact(event)
        return self.save_case(case)

    def add_target(
        self,
        case_id: str,
        *,
        kind: str,
        name: str,
        risk_notes: str = "",
    ) -> CoverageCase:
        case = self.get_case(case_id)
        case.targets.append(
            ContinuityTarget(
                target_id=new_id("tgt"),
                kind=ContinuityTargetKind(kind),
                name=name,
                risk_notes=risk_notes,
            )
        )
        return self.save_case(case)

    def add_fact(
        self,
        case_id: str,
        *,
        label: str,
        value: str,
        status: str = FactStatus.USER_REPORTED.value,
        claim_class: str = ClaimClass.USER_REPORTED.value,
        provenance: str = "user",
        observed_at: Optional[str] = None,
        retrieved_at: Optional[str] = None,
        source_evidence_id: Optional[str] = None,
    ) -> CoverageCase:
        case = self.get_case(case_id)
        now = utc_now_iso()
        case.facts.append(
            MaterialFact(
                fact_id=new_id("fact"),
                label=label,
                value=value,
                status=FactStatus(status),
                claim_class=ClaimClass(claim_class),
                provenance=provenance,
                observed_at=observed_at or now,
                retrieved_at=retrieved_at or now,
                source_evidence_id=source_evidence_id,
            )
        )
        return self.save_case(case)

    def raw_file_bytes(self) -> bytes:
        return self.path.read_bytes()
