---
name: appflow-framework-audit
description: Audit the reusable AppFlow framework for mode routing, workflow consistency, bootstrap drift, state conventions, validator coverage, and project-agnostic reusable files. Use after framework changes or when AppFlow behavior may have drifted.
---

# AppFlow Framework Audit

## Purpose
Audit the AppFlow control plane itself, not application artifacts.

## Read
- `.devmode/mode.yaml`, `AGENTS.md`, and `.devmode/*`
- `.codex/README.md` and `.codex/dev_workflow/README.md`
- `.codex/tools/appflow_run.py`, `.codex/tools/bootstrap_appflow.py`, and `.codex/tools/validate_codex_contract.py`
- `.codex/state/README.md` and `.codex/state/appflow-closeout-checklist.md`
- Relevant `.codex/agents/*`, `.codex/skills/*/SKILL.md`, and `.codex/orchestration/*`

## Do
1. Confirm mode routing is authoritative and selected-mode instructions are first-class.
2. Check workflow step references, lifecycle evidence rules, preflight guidance, skip rules, and interrupted-run recovery guidance.
3. Compare bootstrap templates against live router and mode contracts for drift.
4. Verify validators cover required framework folders, skills, tools, state docs, and bootstrap synchronization.
5. Confirm reusable framework files stay project-agnostic outside approved project extension points.

## Outputs
- Framework audit result: `pass`, `partial`, or `fail`.
- Findings grouped by routing, workflow, skills, tools, state, bootstrap, validation, or project-specific leakage.
- Minimal repair recommendations and validation commands.

## Rules
- Do not inspect or modify application artifacts unless the prompt explicitly changes mode or grants project-specific scope.
- Do not treat passing application tests as framework validation.
- Do not add framework surface area unless it is wired into docs and validators.
