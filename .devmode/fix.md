# Fix Mode

Fix mode is the application repair workflow for existing behavior.

## Activation

Root `AGENTS.md` routes here when `.devmode/mode.yaml` contains:

```yaml
mode: fix
```

The normal user prompt to begin this workflow is:

```text
fix mode start
```

## Core Rule

Run the existing application against the repository's configured test inputs, mimic human testing, identify errors and logical gaps, fix only application defects, and repeat until the result is satisfactory or a blocker is clearly reported.

Fix mode is not AppFlow app-development mode and not framework mode. It does not add new product features and it must not change framework/control-plane behavior.

## Allowed Work

Fix mode may change application artifacts required to repair existing behavior, including:

- runtime implementation under `src/`
- application tests and fixtures under `tests/`
- app-specific runtime configuration examples when needed for local testing
- product documentation only when it directly describes an observed bug fix or test procedure

## Forbidden Work

Fix mode must not modify framework/control-plane files, including:

- `AGENTS.md`
- `.devmode/*`
- `.codex/dev_workflow/*`
- `.codex/fix_workflow/*`
- `.codex/agents/*`
- `.codex/skills/*`
- `.codex/orchestration/*`
- `.codex/tools/*`
- `.codex/state/*` conventions and schemas
- reusable `.codex/README.md` and `.codex/memory/*` framework docs

If a fix appears to require framework changes, stop and report the boundary instead of editing framework files.

## Execution Loop

When the prompt is `fix mode start`:

1. Inspect the application run/test instructions and current Git diff.
2. Use terminal commands to run the application or the smallest available runtime/API smoke path.
3. Use the configured test source path, defaulting to `tests/kmi-source` when the application supports source-path input.
4. Mimic human testing of the visible workflow: start a run, inspect outputs, review errors, and check generated artifacts.
5. Classify each finding as an implementation defect, test defect, environment issue, or logical gap in existing behavior.
6. Fix only bugs or gaps in existing behavior; do not add new features.
7. Re-run targeted validation after each fix.
8. Repeat until tests and smoke checks pass, or until a blocker is understood and reported.

## Validation

Prefer targeted application validation first, then broaden only as needed:

```bash
python3 -m unittest discover -s tests/unit -p 'test_*.py'
python3 -m compileall -q src
git diff --check
```

If a local server is available, test the run creation path using `tests/kmi-source` as source input.
