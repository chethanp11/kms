---
name: workflow-drift-repair
description: Repair stale or inconsistent AppFlow framework references across `.devmode`, `.codex/dev_workflow`, `.codex/tools`, `.codex/state`, bootstrap templates, and validators. Use when copied templates, renamed files, or lifecycle docs drift.
---

# Workflow Drift Repair

## Purpose
Find and repair framework drift so copied AppFlow repositories keep one coherent workflow contract.

## Read
- `AGENTS.md` and `.devmode/*`
- `.codex/README.md`, `.codex/dev_workflow/*`, `.codex/tools/*`, and `.codex/state/*`
- `.codex/tools/bootstrap_appflow.py` templates
- `.codex/tools/validate_codex_contract.py`
- Current grep/search results for stale paths, retired terms, or missing step references

## Do
1. Identify stale paths, retired workflow names, missing step references, or contradictory instructions.
2. Repair the smallest synchronized set of framework docs, tools, bootstrap templates, and validator checks.
3. Preserve existing public commands and file names unless the prompt explicitly changes them.
4. Update validator coverage whenever a drift class should be prevented in future.
5. Run targeted framework validation after repair.

## Outputs
- Repaired framework references or a clear blocked finding.
- Validator or bootstrap updates that prevent recurrence.
- Validation commands and results.

## Rules
- Do not rewrite application plan/design/test/source/log artifacts during framework drift repair.
- Do not create duplicate policy sources when one canonical file can own the rule.
- Do not leave bootstrap templates less strict than the live framework contract.
