# Repository Conventions

- Markdown is the primary reviewable artifact format.
- Prefix IDs such as `REQ-*`, `DEV-*`, and `TEST-*` are used in planning, traceability, and logs.
- Detailed design files should remain human-readable and avoid unnecessary mechanical numbering.
- Validation evidence should include command/method, result, findings, classification, and follow-up.
- New folders require a README or purposeful first artifact.
- Substantial AppFlow turns should use `.codex/tools/appflow_run.py` or equivalent explicit closeout evidence.
- Reusable `.devmode/*` and `.codex/*` files must remain project-agnostic except `.codex/project-context.md` and `.codex/tech-stack.md`.

- Agent role files use standard `name` and `description` frontmatter; skill files use standard `SKILL.md` frontmatter.
