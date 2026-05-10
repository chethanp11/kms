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
    "AGENTS.md": """# Repository Mode Router

Read `.devmode/mode.yaml` first.

If it contains:

```yaml
mode: app
```

then read and follow `.devmode/app.md`.

If it contains:

```yaml
mode: framework
```

then read and follow `.devmode/framework.md`.

If it contains:

```yaml
mode: override
```

then read and follow `.devmode/override.md`.

Do not apply app-mode workflow rules in framework mode. Do not apply framework-mode direct-edit rules in app mode. In override mode, follow the prompt directly without treating AppFlow or framework docs as workflows.
""",
    ".devmode/mode.yaml": "mode: app\n",
    ".devmode/app.md": """# App Mode

App mode uses AppFlow to create or change an application. Treat each user prompt as application intent and route work through the AppFlow lifecycle.

## Lifecycle

Prompt -> intent -> plan -> design/contracts -> validation expectations -> implementation -> validation -> repair -> evidence/logs -> gaps -> closeout.

## Project-Specific Files

Project-specific application context belongs in `.codex/project-context.md`. Project-specific stack and validation commands belong in `.codex/tech-stack.md`. Intent for each app-mode turn comes from the current user prompt, not from pre-filled files.

## Reusable Support

Use `.codex/agents/`, `.codex/dev_workflow/`, `.codex/skills/`, `.codex/orchestration/`, `.codex/memory/`, `.codex/tools/`, and `.codex/state/` as reusable AppFlow support infrastructure.
""",
    ".devmode/framework.md": """# Framework Mode

Framework mode improves the AppFlow framework directly from the prompt. Treat prompts as-is and do not run application workflow unless explicitly requested.

Framework mode must not modify application/product artifacts such as source, design, tests, plans, logs, or project-specific `.codex/project-context.md` and `.codex/tech-stack.md` unless explicitly requested.
""",
    ".devmode/override.md": """# Override Mode

Override mode follows the prompt directly. It is not AppFlow application workflow and it is not framework workflow.

Override mode may modify any repository file when the prompt requires it, while preserving normal safety, reviewability, and validation expectations.
""",
    ".codex/project-context.md": """# Project Context

Project-specific context for AppFlow. This file and `.codex/tech-stack.md` are the expected project-specific files for new application development.

## Product Identity

Describe what this application does, who uses it, and what outcomes it governs.

## Source of Truth and Precedence

Define the order for prompt-derived intent, project context, plan, design, validation, implementation, and evidence artifacts.

## Repository Map

List important folders and ownership boundaries.

## Architecture Boundaries

Define authoritative state, write paths, external integrations, AI/model/tool boundaries, and human approval requirements.

## Workflow Expectations

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
    "plan",
    "design",
    "src",
    "tests",
    "dev_log",
    ".devmode",
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
