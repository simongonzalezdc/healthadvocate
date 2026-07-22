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


class InMemoryKeyStore:
    """Test double. Never use for real cases."""

    def __init__(self, key: Optional[bytes] = None) -> None:
        self._key = key

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

    def rotate_key(self) -> bytes:
        self._key = secrets.token_bytes(32)
        return self._key


class KeyringKeyStore:
    """macOS Keychain / system keyring backed store."""

    def __init__(
        self,
        service: str = SERVICE_NAME,
        username: str = KEY_NAME,
    ) -> None:
        self.service = service
        self.username = username

    def _keyring(self):
        try:
            import keyring
        except ImportError as exc:
            raise KeyStoreError(
                "keyring package is required for OS credential store access"
            ) from exc
        return keyring

    def get_key(self) -> bytes:
        raw = self._keyring().get_password(self.service, self.username)
        if not raw:
            raise KeyStoreError("encryption key is missing from credential store")
        try:
            return bytes.fromhex(raw)
        except ValueError as exc:
            raise KeyStoreError("encryption key is malformed") from exc

    def get_or_create_key(self) -> bytes:
        try:
            return self.get_key()
        except KeyStoreError:
            key = secrets.token_bytes(32)
            self._keyring().set_password(self.service, self.username, key.hex())
            return key

    def delete_key(self) -> None:
        try:
            self._keyring().delete_password(self.service, self.username)
        except Exception:
            # Missing item is fine for delete.
            pass

    def rotate_key(self) -> bytes:
        key = secrets.token_bytes(32)
        self._keyring().set_password(self.service, self.username, key.hex())
        return key


def default_data_dir() -> str:
    override = os.environ.get("HEALTHADVOCATE_CASE_DIR")
    if override:
        return override
    home = os.path.expanduser("~")
    return os.path.join(home, "Library", "Application Support", "HealthAdvocate", "cases")
