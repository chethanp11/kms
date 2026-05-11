# Codex Tools

Deterministic helper scripts for validating repository-visible Codex infrastructure.

## Available

- `validate_codex_contract.py`: checks required Codex-native support files, instruction references, framework skills, bootstrap synchronization, tool docs, and non-empty purpose docs.
- `bootstrap_appflow.py`: creates starter project-specific AppFlow artifacts when `.codex/` is copied into a new repository; `--dry-run` previews create/skip actions without writing files.
- `appflow_run.py`: records and validates per-turn AppFlow lifecycle evidence; `preflight` reports mode, intake, plan-file, validation-source, and active-run readiness; `status` prints incomplete steps, validation state, and stale-intake warnings; `complete` marks a fully validated run complete and clears current intent; `closeout-intake` clears consumed product/feedback intent after step `09` writes next-cycle gaps. Step marking accepts canonical IDs such as `02-create-plan` and numeric aliases such as `02` or `2`.

## Workflow use

- App mode uses `appflow_run.py` for substantial file-changing lifecycle evidence and intake closeout cleanup.
- Framework mode and control-plane changes use `validate_codex_contract.py` for deterministic structure validation.
- Bootstrap uses `bootstrap_appflow.py` only to create missing starter artifacts; it must not overwrite project-specific files.

## AppFlow state command examples

```bash
python3 .codex/tools/appflow_run.py preflight
python3 .codex/tools/appflow_run.py init --objective "..."
python3 .codex/tools/appflow_run.py mark 02 completed --evidence "Plan files refreshed"
python3 .codex/tools/appflow_run.py mark --step 03-update-design --status skipped --evidence "No design change required"
python3 .codex/tools/appflow_run.py validation --command "python3 -m unittest ..." --result pass
python3 .codex/tools/appflow_run.py status
python3 .codex/tools/appflow_run.py closeout-intake
python3 .codex/tools/appflow_run.py validate --require-complete
python3 .codex/tools/appflow_run.py complete
```

## Bootstrap preview

```bash
python3 .codex/tools/bootstrap_appflow.py --dry-run
```
