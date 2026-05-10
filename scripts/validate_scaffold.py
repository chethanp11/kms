#!/usr/bin/env python3
"""Validate the staged KMS application scaffold.

This project script checks application scaffold shape only. It does not validate
AppFlow control-plane files and it does not run product behavior tests.
"""

from __future__ import annotations

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]


COMPONENT_SCAFFOLD_DIRS = [
    "src/components/kmi_application",
    "src/components/infopedia_application",
    "src/components/api_service",
    "src/components/run_orchestration_service",
    "src/components/source_discovery_parsing_service",
    "src/components/source_analysis_service",
    "src/components/wiki_drafting_refresh_service",
    "src/components/policy_validation_service",
    "src/components/contradiction_handling_service",
    "src/components/approval_finalization_service",
    "src/components/search_index_service",
    "src/components/infopedia_projection_refresh_service",
    "src/components/raw_source_store",
    "src/components/wiki_store",
    "src/components/metadata_database",
    "src/components/search_index",
    "src/components/artifact_storage",
]

REQUIRED_DIRS = [
    "src",
    "src/agents",
    "src/app",
    "src/context",
    "src/contracts",
    "src/execution",
    "src/governance",
    "src/observability",
    "src/orchestrator",
    "src/components",
    *COMPONENT_SCAFFOLD_DIRS,
    "scripts",
    "tests/unit",
    "design",
    "plan",
    "dev_log",
    "intent",
]

REQUIRED_FILES = [
    "src/__init__.py",
    "src/agents/__init__.py",
    "src/app/__init__.py",
    "src/context/__init__.py",
    "src/contracts/__init__.py",
    "src/execution/__init__.py",
    "src/governance/__init__.py",
    "src/observability/__init__.py",
    "src/orchestrator/__init__.py",
    "src/components/__init__.py",
    *(f"{component}/__init__.py" for component in COMPONENT_SCAFFOLD_DIRS),
    "scripts/README.md",
    "scripts/__init__.py",
    "scripts/validate_scaffold.py",
    "tests/test-plan.md",
    "tests/design-traceability.md",
    "design/architecture.md",
    "design/system-design.md",
    "design/acceptance-criteria.md",
    "design/ux-flows.md",
    "plan/design-update.md",
    "plan/code-update.md",
    "plan/test-update.md",
]

DISALLOWED_SRC_FAMILIES = [
    "src/ports",
    "src/storage",
]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def validate_scaffold(root: Path = ROOT) -> None:
    for rel in REQUIRED_DIRS:
        if not (root / rel).is_dir():
            fail(f"missing required directory: {rel}")
    for rel in REQUIRED_FILES:
        path = root / rel
        if not path.is_file():
            fail(f"missing required file: {rel}")
        if not path.read_text(encoding="utf-8").strip():
            fail(f"required file is empty: {rel}")
    for rel in DISALLOWED_SRC_FAMILIES:
        if (root / rel).exists():
            fail(f"unplanned src component family exists: {rel}")


def main() -> int:
    validate_scaffold()
    print("PASS: KMS application scaffold validation succeeded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
