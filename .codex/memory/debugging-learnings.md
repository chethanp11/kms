# Debugging Learnings

Reusable failure patterns after validation or debugging.

## Failure Pattern: project-specific terms in reusable support files

- Symptom: a reusable support file accidentally contains project-specific terms.
- Root cause classification: design defect.
- Minimal fix: Move domain-specific wording into `.codex/project-context.md`; keep reusable support files generic.
- Validation: Rerun the relevant doc or contract check.
- Prevention: Only `.codex/project-context.md` should need project-specific edits for a new application.

## Failure Pattern: stale support path references

- Symptom: Documentation points to deleted or duplicated support paths.
- Root cause classification: test defect or design defect depending on source artifact.
- Minimal fix: Remove references to deleted support folders and normalize the remaining paths.
- Validation: Rerun targeted grep or the relevant doc check.
- Prevention: Keep support folder references accurate and minimal.

## Rule

Do not record one-off speculation. Keep only lessons that help future debugging.
