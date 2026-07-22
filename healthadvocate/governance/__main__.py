"""CLI: python -m healthadvocate.governance [--out DIR] [--project-root DIR]."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from healthadvocate.governance.gate import evaluate_shipped_build, write_receipts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate four separate artifact inventories and fail closed on "
            "unknown or incompatible licenses/provenance."
        )
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root (default: cwd)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("build/receipts/license"),
        help="Directory for inventories and attribution receipts",
    )
    parser.add_argument(
        "--registry",
        type=Path,
        default=None,
        help="Optional path to artifact_registry.json",
    )
    args = parser.parse_args(argv)

    project_root = args.project_root.resolve()
    report = evaluate_shipped_build(
        project_root=project_root,
        registry_path=args.registry,
    )
    out_dir = args.out
    if not out_dir.is_absolute():
        out_dir = project_root / out_dir
    paths = write_receipts(report, out_dir)

    print(f"evidence_id={report.evidence_id}")
    print(f"build_revision={report.build_revision}")
    print(f"result={'pass' if report.passed else 'fail'}")
    print(f"receipts={out_dir}")
    for label, path in paths.items():
        print(f"  {label}: {path.name}")
    if report.failures:
        print("failures:")
        for failure in report.failures:
            print(f"  - {failure}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
