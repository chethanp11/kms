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

`.devmode/mode.yaml` is mandatory and authoritative. Read it before any repository-specific instruction file or workflow file.

Valid modes:

```yaml
mode: app
```

```yaml
mode: framework
```

```yaml
mode: override
```

## Strict Routing

- If `mode: app`, read and follow `.devmode/app.md`.
- If `mode: framework`, read and follow `.devmode/framework.md`.
- If `mode: override`, read and follow `.devmode/override.md`.
- Treat the selected `.devmode/<mode>.md` file as the first-class instruction contract for the turn.
- If the file is missing, malformed, or contains any other mode, stop and report the configuration error.

## Mode Enforcement

- Never blend modes.
- Never run `.codex/dev_workflow/*` in framework mode unless the user explicitly asks to test or edit the workflow files themselves.
- Never modify application artifacts in framework mode, including implementation source, product design, tests, plans, logs, or app-specific project files, unless the user explicitly asks for application work after switching to app mode.
- Never modify framework/control-plane files in app mode unless the user prompt explicitly changes AppFlow behavior.
- When `mode: override`, do not run AppFlow or framework workflows automatically; modify any file only as directed by the prompt and normal repository safety rules.
- When uncertain whether a request is framework or application work, follow `.devmode/mode.yaml` and ask before crossing modes.
""",
    ".devmode/mode.yaml": "mode: app\n",
    ".devmode/app.md": """# App Mode

App mode uses AppFlow to create or change an application from the user's prompt.

## Core Rule

The current user prompt is the source of intent for the turn. Do not assume intent is pre-filled in repository files.

## Project-Specific Files

Project-specific application context belongs in `.codex/project-context.md`. Project-specific stack and validation commands belong in `.codex/tech-stack.md`.

## AppFlow Lifecycle

Prompt -> current-turn intent -> product/feedback intent plus current gaps -> plan -> design/contracts -> validation expectations -> implementation -> validation -> repair -> evidence/logs -> new gaps -> closeout cleanup.

## Reusable Support

Use `.codex/agents/`, `.codex/dev_workflow/`, `.codex/skills/`, `.codex/orchestration/`, `.codex/memory/`, `.codex/tools/`, and `.codex/state/` as reusable AppFlow support infrastructure.

## State and Tool Use

For substantial file-changing app-mode work, use `.codex/tools/appflow_run.py` to initialize state, mark lifecycle steps with evidence, record validation, and close out consumed intake.
""",
    ".devmode/framework.md": """# Framework Mode

Framework mode improves the AppFlow framework itself.

## Core Rule

Treat the current user prompt as-is. Do not convert it into application intent, do not run the application lifecycle, and do not assume application context unless the prompt explicitly requests application work.

## In-Scope Framework Work

Framework mode may change root router behavior, `.devmode/*`, `.codex/dev_workflow/*`, `.codex/agents/*`, `.codex/skills/*`, `.codex/orchestration/*`, `.codex/tools/*`, `.codex/state/*` conventions, validators, bootstrap templates, and reusable framework docs.

## Out-of-Scope Application Work

Framework mode is control-plane-only. Do not modify application/product artifacts such as source, design, tests, plans, logs, or project-specific `.codex/project-context.md` and `.codex/tech-stack.md` unless explicitly requested.

If validation exposes application failures while in framework mode, report them as out-of-scope instead of fixing application code.

## Files Framework Mode Must Not Modify

Framework mode must not modify application/product artifacts unless the current prompt explicitly asks for application work after switching to app mode or explicitly requests a bounded project-specific edit.
""",
    ".devmode/override.md": """# Override Mode

Override mode follows the user prompt directly. It is not AppFlow application workflow and it is not framework workflow.

Override mode may modify any repository file when the prompt requires it, including application artifacts, framework/control-plane files, mode contracts, workflow files, design, tests, source, plans, logs, and project-specific `.codex` files.

This is a permission mode, not a workflow. It does not erase normal safety rules: avoid destructive operations unless explicitly requested, preserve secrets, keep changes reviewable, and validate when practical.
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
    "intent/product-intent.md": "# Product Intent\n\nThis file is populated from the current app-mode prompt and cleared at closeout.\n\n## Current-cycle product intent\n\n- None.\n",
    "intent/feedback-intent.md": "# Feedback Intent\n\nThis file is populated from current app-mode feedback prompts and cleared at closeout.\n\n## Current-cycle feedback\n\n- None.\n",
    "intent/gaps.md": "# Gaps\n\nThis file is system-generated at step 09 and should contain only next-cycle gaps.\n\n## Current gaps\n\n- None.\n",
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
