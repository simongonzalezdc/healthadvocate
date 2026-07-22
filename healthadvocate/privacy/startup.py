"""Startup policy checks that do not require heavy ML imports."""

from __future__ import annotations

import os

from healthadvocate.privacy.endpoint_policy import (
    EndpointPolicyError,
    assert_loopback_bind_host,
    default_app_bind_host,
)


def validate_startup_bind_policy(
    env: dict[str, str] | None = None,
) -> str:
    """Validate loopback bind policy. Returns the approved bind host.

    Raises SystemExit on policy violation so process startup fails closed.
    """
    source = env if env is not None else os.environ
    bind_host = source.get("HEALTHADVOCATE_BIND_HOST", default_app_bind_host())
    try:
        approved = assert_loopback_bind_host(bind_host)
    except EndpointPolicyError as exc:
        raise SystemExit(
            "HealthAdvocate default profile requires a loopback bind host "
            f"(127.0.0.1 or ::1). Refusing to start: {exc}"
        ) from exc

    allow_non_loopback = source.get("HEALTHADVOCATE_ALLOW_NON_LOOPBACK", "").strip() in {
        "1",
        "true",
        "True",
        "yes",
    }
    if allow_non_loopback:
        auth = source.get("HEALTHADVOCATE_DEPLOYMENT_AUTH", "").strip()
        if not auth:
            raise SystemExit(
                "Non-loopback deployment requested without "
                "HEALTHADVOCATE_DEPLOYMENT_AUTH; refusing to start."
            )
    return approved
