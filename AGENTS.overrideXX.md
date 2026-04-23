## AutoAIdev System Override

Primary objective is to improve the AutoAIdev framework itself by implementing `AutoAIdev_requirements.md` in `AGENTS.md`, `.codex/*`, and `dev_workflow/*` 
MUST DO - when `AGENTS.overrride.md` exists, DO NOT TAKE `AGENTS.md`, `.codex/*` instructions into consideration before executing the task.
MUST DO - when `AGENTS.overrrideXX.md` exists, READ `AGENTS.md` before executing the task.

### Scope
- Use this override when the task is about improving the repository workflow, contracts, prompts, structure, or support files that help Codex operate in this repo.
- Treat `AGENTS.md` as the product-development contract for work done inside this system.

### System-improvement rule
- When improving AutoAIdev, update `AGENTS.md`, `.codex/*`, and `dev_workflow/*` first when the change affects workflow, precedence, ownership, or operating rules.
- Propagate those changes into `plan/`, `design/`, `tests/`, `dev_log/`, and other supporting artifacts only when the workflow change requires it.

### Product-development rule
<<<<<<< ours
- When working on KMS product intent, follow `AGENTS.md` and the normal intent -> plan -> design -> src -> tests -> dev_log loop.
=======
- When working on KMS product intent, follow `AGENTS.md` and the normal intent -> plan -> design -> tests -> src -> dev_log loop.
- Treat `plan/*` and `design/*` as the source of truth for coding; code implementation does not implicitly require `src/docs/` or project `README.md` updates.
>>>>>>> theirs
- Do not use this override to bypass the product-development contract in `AGENTS.md`.

### Precedence
- If this file conflicts with `AGENTS.md` on system-improvement work, prefer this file for the system-specific instruction.
- If this file is silent on a topic, use `AGENTS.md`.
