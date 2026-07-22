"""Local Privacy Boundary: loopback policy, deidentification status, safe logging."""

from healthadvocate.privacy.boundary import (
    DeidentificationResult,
    DeidentificationStatus,
    PrivacyBoundary,
    PrivacyBoundaryError,
)
from healthadvocate.privacy.endpoint_policy import (
    EndpointPolicyError,
    assert_loopback_bind_host,
    assert_loopback_model_url,
    is_loopback_host,
)
from healthadvocate.privacy.logging_redaction import (
    CanaryRedactingFilter,
    install_redacting_log_filter,
)

__all__ = [
    "CanaryRedactingFilter",
    "DeidentificationResult",
    "DeidentificationStatus",
    "EndpointPolicyError",
    "PrivacyBoundary",
    "PrivacyBoundaryError",
    "assert_loopback_bind_host",
    "assert_loopback_model_url",
    "install_redacting_log_filter",
    "is_loopback_host",
]
