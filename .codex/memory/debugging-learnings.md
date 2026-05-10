# Debugging Learnings

Reusable failure patterns after validation or debugging.

## Failure Pattern: project-specific terms in reusable framework files

- Symptom: `.codex/tools/validate_codex_contract.py` fails with a project-specific term found in a reusable framework file.
- Root cause classification: design defect.
- Minimal fix: Move domain-specific wording into `.codex/project-context.md` or `.codex/tech-stack.md`; keep `.devmode/*` and other `.codex/*` files generic.
- Validation: Rerun `python .codex/tools/validate_codex_contract.py`.
- Prevention: Only `.codex/project-context.md` and `.codex/tech-stack.md` should need project-specific edits for a new application.

## Failure Pattern: stale workflow path references

- Symptom: Documentation points to root `dev_workflow/`, deleted `.codex/prompts/`, deleted `.codex/context/`, deleted `.codex/rules/`, or duplicated `.codex/.codex/dev_workflow/` paths.
- Root cause classification: test defect or design defect depending on source artifact.
- Minimal fix: Normalize lifecycle references to `.codex/dev_workflow/` and remove references to deleted support folders.
- Validation: Rerun `python .codex/tools/validate_codex_contract.py` and targeted grep for stale paths.
- Prevention: Keep canonical workflow and support-folder references in `.devmode/app.md`, `.codex/README.md`, `.codex/dev_workflow/README.md`, and the validator.

## Rule

Do not record one-off speculation. Keep only lessons that help future debugging.
