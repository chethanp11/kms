# Agentic Application Development Workflow

This folder defines the canonical AppFlow 11-step workflow. Every development prompt should automatically enter this workflow unless the user explicitly asks for an answer-only or planning-only response.

The workflow is artifact-driven, not chat-driven: each step reads specific upstream artifacts, produces specific downstream artifacts, and must respect the repo contract before moving forward.

## Mode Gate

Before using this workflow, read `.devmode/mode.yaml`. Execute these app workflow steps only when `mode: app`. When `mode: framework`, do not run this lifecycle to fix application artifacts; edit workflow/framework files directly only if the prompt asks for framework changes.

## Automatic Prompt Routing

For ordinary development prompts such as "Improve the UI", "Fix the failing test", or "Add export support", the agent should not wait for the user to invoke workflow files manually.

Default behavior:

1. Treat the prompt as AppFlow input.
2. Start at `.codex/dev_workflow/00-create-intent.md`.
3. Read `.devmode/mode.yaml`, the selected `.devmode/*` entry point, `.codex/project-context.md`, and `.codex/tech-stack.md`.
4. Execute steps `00` through `10` as far as the task can safely proceed.
5. Use `.codex/agents/`, `.codex/skills/`, `.codex/orchestration/`, and `.codex/tools/` as support when the step needs them.
6. Stop only at completion, explicit user boundary, or a genuine blocker/HITL checkpoint.

## Core Operating Model

```mermaid
flowchart LR
    A[User prompt] --> B[00 Create Intent]
    B --> C[01 Read Intent]
    C --> D[02 Create Plan]
    D --> E[03 Update Design]
    E --> F[04 Update Tests]
    F --> G[05 Implement Code]
    G --> H[06 Run Validation]
    H --> I[07 Fix Failures]
    I --> H
    H --> J[08 Update Logs]
    J --> K[09 Detect Gaps]
    K --> L[10 Iteration Review]
```

The agent is not supposed to improvise outside this chain. It converts the prompt into current-turn intent, reconciles that intent with project context and relevant artifacts, plans work, updates design and validation expectations, implements approved behavior, proves the result, records what happened, and feeds evidence-backed gaps into the next loop.

## Workflow Principles

| Principle | Exact rule | Prevents |
| --- | --- | --- |
| Prompt to intent | Convert the user prompt into current-turn intent first | Coding directly from chat text |
| Contract first | Read `.devmode/mode.yaml`, the selected `.devmode/*` entry point, and project context before substantial work | Local edits that violate repo policy |
| Context first | Reconcile current-turn intent with project context before planning | Hidden scope drift |
| Plan before downstream edits | Translate intent into `plan/*` before changing design, tests, or code | Untracked assumptions |
| Design before code | If behavior changes, update design/contracts before implementation | Code inventing behavior |
| Tests before code | Update validation expectations before implementation | Post hoc testing |
| Validation before closeout | Every meaningful change ends with explicit validation | Unproven completion claims |
| Logs record reality | `dev_log/*` records actual changes and validation | Fake progress tracking |
| Gaps feed the next loop | Evidence-backed gaps go into `intent/gaps.md` | Rediscovering known issues |

## Source of Truth Order

| Priority | Artifact layer | Role |
| --- | --- | --- |
| 1 | user prompt and current-turn intent | Immediate task input |
| 2 | `.codex/project-context.md` and `.codex/tech-stack.md` | Project context, constraints, and stack |
| 3 | `plan/*` | Active iteration interpretation of prompt-derived intent |
| 4 | `design/*` | Detailed behavior, architecture, flows, and correctness |
| 5 | `tests/*` | Validation design and coverage plan |
| 6 | implementation source | Implementation artifacts |
| 7 | `dev_log/*` | Evidence and history |

## Prompt Navigation

| Step | Prompt file | What it controls |
| --- | --- | --- |
| `00` | `.codex/dev_workflow/00-create-intent.md` | Convert raw user prompt into current-turn intent |
| `01` | `.codex/dev_workflow/01-read-intent.md` | Reconcile current-turn intent with project context and repo constraints |
| `02` | `.codex/dev_workflow/02-create-plan.md` | Scope reconciliation and traceable work item creation |
| `03` | `.codex/dev_workflow/03-update-design.md` | High-level and detailed design updates |
| `04` | `.codex/dev_workflow/04-update-tests.md` | Criteria-driven validation preparation |
| `05` | `.codex/dev_workflow/05-implement-code.md` | Implementation aligned to plan, design, and tests |
| `06` | `.codex/dev_workflow/06-run-validation.md` | Execution of explicit proof |
| `07` | `.codex/dev_workflow/07-fix-failures.md` | Failure correction at the correct layer |
| `08` | `.codex/dev_workflow/08-update-logs.md` | Permanent logging of actual work and evidence |
| `09` | `.codex/dev_workflow/09-detect-gaps.md` | System-detected gap surfacing |
| `10` | `.codex/dev_workflow/10-iteration-review.md` | Closeout and next-loop readiness |

The 11 prompt files are intended to be execution-complete as a set. If followed in order, they should cover a full iteration using the current prompt and repository artifacts without relying on hidden workflow knowledge from chat history.

## Codex-Native Support

| Support area | Purpose |
| --- | --- |
| `.codex/agents/` | Bounded role contracts |
| `.codex/skills/` | Reusable specialized procedures |
| `.codex/orchestration/` | Long-horizon loops, task patterns, HITL checkpoints, and resumable-state guidance |
| `.codex/memory/` | Reviewable structured memory |
| `.codex/tools/` | Deterministic helper scripts |

## State and Tool Requirements

For substantial app-mode changes that edit files, record lifecycle evidence in `.codex/state/appflow-current.json` using `.codex/tools/appflow_run.py`. Step `00` initializes or refreshes the run state, each completed/skipped/blocked step records evidence, validation commands are recorded, and closeout runs `appflow_run.py validate --require-complete` when the full lifecycle is expected.

`.codex/state/current-intent.md` is only the current prompt-derived intent handoff from step `00` to later steps; it is not durable pre-filled intent.

## Agent and Skill Use

| Need | Use |
| --- | --- |
| Scope and sequencing | `.codex/agents/planner.md` |
| Architecture or boundary review | `.codex/agents/architecture.md` and matching architecture/review skills |
| Patch execution | `.codex/agents/implementer.md` |
| Validation selection and evidence | `.codex/agents/validator.md` and matching test/eval skills |
| Failure isolation | `.codex/agents/debugger.md` |
| Governance, traceability, or HITL checks | `.codex/agents/governance.md` and matching traceability/review skills |
| Documentation consistency | `.codex/agents/documentation.md` |
| Diff quality and closeout | `.codex/agents/reviewer.md` and release/design-audit skills |

Use skills only when their `SKILL.md` frontmatter description matches the current task. Agent role contracts guide workflow responsibilities; they do not grant authority beyond `.devmode/app.md` and the workflow step being executed.

## Step-by-Step Execution Semantics

| Step | Reads from | May update | Must achieve | Must not do |
| --- | --- | --- | --- | --- |
| `00` Create Intent | User prompt, selected `.devmode/*` entry point, `.codex/project-context.md` | `.codex/state/current-intent.md` | Current-turn intent exists before repo reconciliation | Start coding or edit project-owned requirements |
| `01` Read Intent | `.codex/state/current-intent.md`, selected `.devmode/*` entry point, `.codex/project-context.md`, `.codex/tech-stack.md`, relevant user-referenced artifacts | None | Scope, constraints, ambiguity, and context are clear | Start coding or plan from memory |
| `02` Create Plan | current-turn intent, project context, current repo state, active logs | `plan/*` | Explicit `REQ-*`, `DEV-*`, `TEST-*` work | Hide ambiguity or compress constraints |
| `03` Update Design | `plan/*`, `.codex/project-context.md`, `design/*` | `.codex/project-context.md` when needed, `design/*` | Design baseline for downstream work | Let code define behavior first |
| `04` Update Tests | `design/*`, correctness criteria, traceability | `tests/*` | Proving strategy and validation assets before code | Write tests from implementation convenience |
| `05` Implement Code | `plan/*`, `design/*`, `tests/*`, stack notes | `src/*` | Approved behavior implemented | Invent new requirements in code |
| `06` Run Validation | Changed artifacts, test plan, validation methods | No permanent logs yet | Real pass, fail, or partial evidence | Claim success without proof |
| `07` Fix Failures | Validation findings and implicated artifacts | The correct failing layer | Root cause fixed or explicitly deferred | Patch around upstream defects |
| `08` Update Logs | Final diff and final validation result | `dev_log/*` | Permanent factual execution record | Log intended work as completed |
| `09` Detect Gaps | `dev_log/*`, validation outcomes | project gap artifact defined by `.codex/project-context.md` | Evidence-backed next-loop gaps captured | Rewrite user intent or requirements |
| `10` Iteration Review | Outputs from all prior steps | Usually none beyond final workflow artifacts | Explicit closure status and next-loop readiness | Start new scope silently |

## Guardrails

- Do not modify project-owned intent or requirements artifacts unless explicitly asked; only update the configured gap artifact for evidence-backed gaps.
- Do not use implementation behavior as the de facto design source.
- Do not invent tests without design linkage.
- Do not treat "looks correct" as validation.
- Do not write logs before the real result is known.
- Do not close out while validation, logs, or review are incomplete.

## Validation and Evidence Model

| Changed layer | Expected proof | Typical evidence destination |
| --- | --- | --- |
| Workflow docs or contract docs | Manual review, structural checks, `git diff --check` | `dev_log/validation-results.md` |
| Design | Manual review against intent, traceability, correctness, and architecture | `dev_log/validation-results.md` |
| Tests | Targeted test execution, checklist review, or artifact review | `dev_log/validation-results.md` |
| Code | Targeted unit, integration, e2e, regression, or smoke validation | `dev_log/validation-results.md` |

Validation must state the method, result, findings, failure classification if relevant, and follow-up.

## Failure Classification Model

| Classification | Meaning |
| --- | --- |
| `design defect` | Design is wrong, incomplete, or conflicting |
| `implementation defect` | Code does not follow intended design |
| `test defect` | Validation layer is weak, wrong, or missing |
| `eval gap` | Evidence is insufficient to prove behavior |
| `environment issue` | Tooling, runtime, infra, or dependency problem blocks progress |
| `backlog enhancement` | Useful but out-of-scope follow-on work |

## Decision Gates

| If this happens | The workflow must do this next |
| --- | --- |
| Prompt changes operating model or repo rules | Update the selected `.devmode/*` entry point and `.codex/project-context.md` before downstream artifacts |
| Behavior changes | Update design before code |
| Correctness criteria or workflows change | Update tests before code |
| Validation fails | Enter step `07`, classify root cause, fix the correct layer, rerun step `06` |
| Validation passes | Update logs, detect gaps, review iteration |
| Evidence reveals unresolved systemic follow-up | Record it in the project gap artifact defined by `.codex/project-context.md` |
| Work is out of scope | Defer it or update design first |

## Workflow Anti-Patterns

| Anti-pattern | Why it is wrong |
| --- | --- |
| Coding directly from the user prompt | Skips intent creation, reconciliation, planning, design, and validation preparation |
| Using code behavior to decide requirements | Reverses the source-of-truth order |
| Writing tests only after code exists | Breaks criteria-driven validation discipline |
| Logging planned work before execution | Corrupts the permanent record |
| Editing project-owned requirements to resolve ambiguity | Rewrites requirements instead of surfacing questions |
| Treating validation as optional for doc changes | Leaves workflow and contract drift unproven |
| Treating the project gap artifact as personal notes | Breaks the evidence-backed gap model |
| Closing without review | Hides residual risks, deferrals, or blockers |

## Start and Stop Conditions

| Condition | Meaning |
| --- | --- |
| Iteration start | A user prompt enters step `00` |
| Step handoff | A step completes only when its exit condition is met |
| Validation loop active | Steps `06` and `07` are repeating |
| Iteration complete | Validation outcome is recorded, logs are current, and review confirms closure |
| Next loop begins | Only after a new prompt, new feedback, or a surfaced gap requires another pass |
