# Codex Skill Index

Skills are optional, task-specific context packs. Load only the one that matches the current job, and only add a second if the task is still blocked.

## Load order

1. Read `AGENTS.md`.
2. Read `.codex/project-context.md`.
3. Open one relevant skill file.
4. Expand only when the task needs a second perspective.

## Available skills

### Universal baseline

| Skill | Use when |
| --- | --- |
| `repo-orientation` | Mapping the repository, runtime entrypoints, contracts, and validation path. |
| `large-codebase-analysis` | Tracing request flow and narrowing the edit surface in unfamiliar repos. |
| `execution-planning` | Turning a request into a short bounded step plan with stop conditions. |
| `change-verification` | Proving a change with the smallest deterministic checks. |
| `governance-review` | Checking traceability, provenance, approval boundaries, and bypass risks. |
| `feedback-synthesis` | Converting feedback into concrete actions and artifact updates. |
| `documentation-maintenance` | Keeping docs aligned with implementation and validation evidence. |
| `long-horizon-work` | Managing durable objectives across multiple turns. |

### Reusable workflow capture

| Skill | Use when |
| --- | --- |
| `repeatable-workflows` | Capturing repeated work as a reusable skill, CLI, or scripted procedure. |

### Specialized review skills

| Skill | Use when |
| --- | --- |
| `architecture-review` | Reviewing boundaries, interfaces, provenance, persistence, or observability. |
| `feedback-triage` | Routing stakeholder or reviewer feedback into the right artifact class. |
| `prompt-contract-review` | Checking prompt inputs, outputs, tool policy, fallback behavior, and safety. |
| `test-repair` | Repairing stale, broken, or missing regression coverage. |
| `ai-eval-review` | Checking evaluation grounding, hallucination risk, and tool assumptions. |

## Rule

Do not bulk-load all skills. Read only the smallest skill file that advances the task.
