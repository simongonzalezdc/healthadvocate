"""OS credential store interface for the Coverage Case encryption key."""

from __future__ import annotations

import os
import secrets
from typing import Optional, Protocol


SERVICE_NAME = "healthadvocate.coverage"
KEY_NAME = "case-store-master-key"


class KeyStoreError(RuntimeError):
    """Missing or unusable encryption key."""


class KeyStore(Protocol):
    def get_key(self) -> bytes: ...
    def get_or_create_key(self) -> bytes: ...
    def delete_key(self) -> None: ...
    def rotate_key(self) -> bytes: ...
    def candidate_keys(self) -> list[bytes]: ...
    def discard_previous_key(self) -> None: ...


class InMemoryKeyStore:
    """Test double. Never use for real cases."""

    def __init__(self, key: Optional[bytes] = None) -> None:
        self._key = key
        self._previous_key: Optional[bytes] = None

    def get_key(self) -> bytes:
        if not self._key:
            raise KeyStoreError("encryption key is missing")
        return self._key

    def get_or_create_key(self) -> bytes:
        if not self._key:
            self._key = secrets.token_bytes(32)
        return self._key

    def delete_key(self) -> None:
        self._key = None
        self._previous_key = None

    def rotate_key(self) -> bytes:
        self._previous_key = self._key
        self._key = secrets.token_bytes(32)
        return self._key

    def candidate_keys(self) -> list[bytes]:
        return [key for key in (self._key, self._previous_key) if key]

    def discard_previous_key(self) -> None:
        self._previous_key = None


class KeyringKeyStore:
    """macOS Keychain / system keyring backed store."""

    def __init__(
        self,
        service: str = SERVICE_NAME,
        username: str = KEY_NAME,
    ) -> None:
        self.service = service
        self.username = username
        self.previous_username = f"{username}.previous"

    def _keyring(self):
        try:
            import keyring
        except ImportError as exc:
            raise KeyStoreError(
                "keyring package is required for OS credential store access"
            ) from exc
        return keyring

    @staticmethod
    def _decode_key(raw: str, *, label: str = "encryption key") -> bytes:
        try:
            key = bytes.fromhex(raw)
        except ValueError as exc:
            raise KeyStoreError(f"{label} is malformed") from exc
        if len(key) != 32:
            raise KeyStoreError(f"{label} is malformed")
        return key

    def get_key(self) -> bytes:
        raw = self._keyring().get_password(self.service, self.username)
        if raw is None:
            raise KeyStoreError("encryption key is missing from credential store")
        return self._decode_key(raw)

    def get_or_create_key(self) -> bytes:
        keyring = self._keyring()
        raw = keyring.get_password(self.service, self.username)
        if raw is not None:
            return self._decode_key(raw)

        key = secrets.token_bytes(32)
        keyring.set_password(self.service, self.username, key.hex())
        return key

    def delete_key(self) -> None:
        for username in (self.username, self.previous_username):
            try:
                self._keyring().delete_password(self.service, username)
            except Exception:
                # Missing item is fine for delete.
                pass

    def rotate_key(self) -> bytes:
        old_key = self.get_key()
        key = secrets.token_bytes(32)
        keyring = self._keyring()
        # Retain the old key until the newly encrypted store is durably replaced.
        # A crash at any rotation stage therefore leaves at least one usable key.
        keyring.set_password(self.service, self.previous_username, old_key.hex())
        keyring.set_password(self.service, self.username, key.hex())
        return key

    def candidate_keys(self) -> list[bytes]:
        keys = [self.get_key()]
        raw = self._keyring().get_password(self.service, self.previous_username)
        if raw is not None:
            keys.append(self._decode_key(raw, label="previous encryption key"))
        return keys

    def discard_previous_key(self) -> None:
        try:
            self._keyring().delete_password(self.service, self.previous_username)
        except Exception:
            pass


def default_data_dir() -> str:
    override = os.environ.get("HEALTHADVOCATE_CASE_DIR")
    if override:
        return override
    home = os.path.expanduser("~")
    return os.path.join(home, "Library", "Application Support", "HealthAdvocate", "cases")
