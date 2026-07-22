"""Fail-closed loopback policy for application binds and model destinations."""

from __future__ import annotations

import ipaddress
import socket
from urllib.parse import urlparse


class EndpointPolicyError(ValueError):
    """Raised when a bind host or model URL is not an approved loopback target."""


_LOOPBACK_HOSTNAMES = frozenset({"localhost", "localhost."})


def _strip_brackets(host: str) -> str:
    cleaned = host.strip().lower()
    if cleaned.startswith("[") and cleaned.endswith("]"):
        return cleaned[1:-1]
    return cleaned


def is_loopback_ip(value: str) -> bool:
    try:
        addr = ipaddress.ip_address(_strip_brackets(value))
    except ValueError:
        return False
    return bool(addr.is_loopback)


def is_loopback_host(host: str) -> bool:
    """Return True only when host is a loopback name or literal IP."""
    if not host:
        return False
    cleaned = _strip_brackets(host).rstrip(".")
    if cleaned in _LOOPBACK_HOSTNAMES or cleaned == "localhost":
        return True
    if cleaned.startswith("::ffff:"):
        mapped = cleaned.split("::ffff:", 1)[1]
        return is_loopback_ip(mapped) or is_loopback_ip(cleaned)
    return is_loopback_ip(cleaned)


def _resolve_host(host: str) -> list[str]:
    cleaned = _strip_brackets(host).rstrip(".")
    if is_loopback_ip(cleaned):
        return [cleaned]
    try:
        infos = socket.getaddrinfo(cleaned, None, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise EndpointPolicyError(
            f"host {host!r} could not be resolved; failing closed"
        ) from exc
    addresses = [str(info[4][0]) for info in infos if info[4]]
    if not addresses:
        raise EndpointPolicyError(
            f"host {host!r} resolved to no addresses; failing closed"
        )
    return addresses


def assert_loopback_bind_host(host: str) -> str:
    """Validate an application/container bind host."""
    if host is None or not str(host).strip():
        raise EndpointPolicyError("bind host is required")
    cleaned = str(host).strip()
    if cleaned in {"0.0.0.0", "::", "[::]", "*"}:
        raise EndpointPolicyError(
            f"bind host {cleaned!r} exposes non-loopback interfaces; "
            "default profile requires 127.0.0.1 or ::1"
        )
    if is_loopback_host(cleaned):
        return cleaned
    for addr in _resolve_host(cleaned):
        if not is_loopback_ip(addr):
            raise EndpointPolicyError(
                f"bind host {cleaned!r} resolves to non-loopback address {addr}"
            )
    # Non-loopback hostname labels are rejected even if DNS currently points
    # at loopback, to reduce DNS-rebinding risk for bind configuration.
    raise EndpointPolicyError(
        f"bind host {cleaned!r} is not an approved loopback name or address"
    )


def assert_loopback_model_url(url: str, *, allow_redirects: bool = False) -> str:
    """Validate a model base URL. Redirects are never allowed by default."""
    if allow_redirects:
        raise EndpointPolicyError(
            "HTTP redirects are not permitted for model destinations"
        )
    if not url or not str(url).strip():
        raise EndpointPolicyError("model URL is required")
    raw = str(url).strip()
    parsed = urlparse(raw)
    if parsed.scheme not in {"http", "https"}:
        raise EndpointPolicyError(
            f"model URL scheme {parsed.scheme!r} is not allowed; use http(s) to loopback"
        )
    if not parsed.hostname:
        raise EndpointPolicyError("model URL is missing a host")
    if parsed.username is not None or parsed.password is not None:
        raise EndpointPolicyError(
            "model URL must not include credentials; failing closed"
        )
    host = parsed.hostname
    if is_loopback_host(host):
        return raw
    # For non-loopback labels, resolve and still reject to prevent rebinding.
    for addr in _resolve_host(host):
        if not is_loopback_ip(addr):
            raise EndpointPolicyError(
                f"model host {host!r} resolves to non-loopback address {addr}"
            )
    raise EndpointPolicyError(
        f"model host {host!r} is not an approved loopback name or address"
    )


def default_app_bind_host() -> str:
    return "127.0.0.1"


def default_model_base_url() -> str:
    # Ollama OpenAI-compatible default; optional and loopback-only.
    return "http://127.0.0.1:11434/v1"
