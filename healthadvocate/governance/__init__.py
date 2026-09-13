"""Open license and provenance governance for shipped HealthAdvocate builds.

Inventories are deliberately separate:

1. application / runtime packages
2. model runtimes
3. model artifacts (weights, tokenizers, templates, conversions, quantizations)
4. datasets

Approval of one inventory never implies approval of another.
"""

from healthadvocate.governance.models import (
    ApprovalResult,
    ArtifactInventory,
    ArtifactKind,
    ArtifactRecord,
    GateReport,
)
from healthadvocate.governance.gate import (
    evaluate_shipped_build,
    generate_attribution,
    write_receipts,
)
from healthadvocate.governance.registry import load_registry

__all__ = [
    "ApprovalResult",
    "ArtifactInventory",
    "ArtifactKind",
    "ArtifactRecord",
    "GateReport",
    "evaluate_shipped_build",
    "generate_attribution",
    "load_registry",
    "write_receipts",
]
