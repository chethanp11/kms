#!/usr/bin/env python3
"""Bootstrap project-specific AppFlow artifacts around a copied .codex factory.

The script is intentionally conservative:
- it creates missing starter files only
- it never overwrites existing project files
- it uses only the Python standard library
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


FILES: dict[str, str] = {
    "AGENTS.md": """# Project Contract

This is the project-specific contract for this application. The reusable AppFlow factory contract lives in `.codex/AGENTS.md`.

## Project Identity

Describe the application, users, core value, and non-goals.

## Source-of-Truth Chain

Define the order for intent, plan, context, design, validation, implementation, and evidence artifacts.

## Architecture Boundaries

Define authoritative state, write paths, external integrations, AI/model/tool boundaries, and human approval requirements.

## Validation

Define the commands or review methods required before closeout.
""",
    ".codex/project-context.md": """# Project Context

Compact project-specific context for AppFlow.

## Purpose

Describe what this application does and why it exists.

## Repository Map

List important folders and ownership boundaries.

## Current Architecture

Summarize runtime entrypoints, major modules, data flow, and known constraints.

## Current Workflow

Summarize how planning, design, validation, implementation, and evidence are handled in this repository.
""",
    ".codex/tech-stack.md": """# Tech Stack

Project-specific technology, dependency, and validation commands.

## Runtime

- Languages:
- Frameworks:
- Package managers:
- Runtime services:

## Validation Commands

- Format:
- Lint:
- Typecheck:
- Unit tests:
- Integration tests:
- E2E tests:

## Dependency Rules

Document dependency boundaries and approval expectations.
""",
    "intent/product-intent.md": "# Product Intent\n\nHuman-owned product intent goes here.\n",
    "intent/feedback-intent.md": "# Feedback Intent\n\nHuman-owned feedback goes here.\n",
    "intent/gaps.md": "# Gaps\n\nSystem-detected evidence-backed gaps go here.\n",
    "plan/design-update.md": "# Design Update Plan\n\nCurrent design work items go here.\n",
    "plan/code-update.md": "# Code Update Plan\n\nCurrent implementation work items go here.\n",
    "plan/test-update.md": "# Test Update Plan\n\nCurrent validation work items go here.\n",
    "design/architecture.md": "# Architecture\n\nProject architecture goes here.\n",
    "design/system-design.md": "# System Design\n\nSystem behavior and operating model go here.\n",
    "design/acceptance-criteria.md": "# Acceptance Criteria\n\nAcceptance criteria go here.\n",
    "tests/test-plan.md": "# Test Plan\n\nValidation strategy goes here.\n",
    "tests/design-traceability.md": "# Design Traceability\n\nIntent/design/test mappings go here.\n",
    "dev_log/validation-results.md": "# Validation Results\n\nActual validation evidence goes here.\n",
}

DIRS = [
    "intent",
    "plan",
    "design",
    "src",
    "tests",
    "dev_log",
]


def main() -> int:
    created: list[str] = []
    skipped: list[str] = []

    for rel in DIRS:
        path = ROOT / rel
        if not path.exists():
            path.mkdir(parents=True)
            created.append(rel + "/")

    for rel, content in FILES.items():
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            skipped.append(rel)
            continue
        path.write_text(content, encoding="utf-8")
        created.append(rel)

    print("AppFlow bootstrap complete.")
    if created:
        print("Created:")
        for item in created:
            print(f"  - {item}")
    if skipped:
        print("Skipped existing:")
        for item in skipped:
            print(f"  - {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
