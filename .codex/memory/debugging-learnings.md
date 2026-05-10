# Debugging Learnings

Reusable failure patterns after validation or debugging.

## Failure Pattern: project-specific terms in reusable factory files

- Symptom: `.codex/tools/validate_codex_contract.py` fails with a project-specific term found in a reusable `.codex` file.
- Root cause classification: design defect.
- Minimal fix: Move domain-specific wording into root `AGENTS.md`, `.codex/project-context.md`, or `.codex/tech-stack.md`; keep other `.codex` files generic.
- Validation: Rerun `python .codex/tools/validate_codex_contract.py`.
- Prevention: The validator derives project-specific terms from root `AGENTS.md` and checks reusable markdown.

## Failure Pattern: stale workflow path references

- Symptom: Documentation points to root `dev_workflow/` or duplicated `.codex/.codex/dev_workflow/` paths after relocation.
- Root cause classification: test defect or design defect depending on source artifact.
- Minimal fix: Normalize references to `.codex/dev_workflow/`.
- Validation: Rerun `python .codex/tools/validate_codex_contract.py` and targeted grep for stale paths.
- Prevention: Keep canonical workflow path in `.codex/AGENTS.md`, `.codex/appflow.md`, and `.codex/project-context.md`.

## Template

```md
## Failure Pattern
- Symptom:
- Root cause classification:
- Minimal fix:
- Validation:
- Prevention:
```

## Rule

Do not record one-off speculation. Keep only lessons that help future debugging.
