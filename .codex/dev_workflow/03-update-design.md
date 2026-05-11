# Step 03 Prompt: Update Design

## Mode Guard

Use this workflow step only when `.devmode/mode.yaml` is `mode: app`. In framework mode, do not use this step to modify application artifacts. In override mode, follow `.devmode/override.md` instead of running AppFlow automatically.


## Use This Prompt When

Use this prompt after planning when `REQ-*` work exists, when behavior or structure must be defined before tests and implementation can proceed safely, or when the plan says design review is required.

## Workflow Position

- Input step: approved plan
- Output step: current high-level and detailed design baseline

## Objective

Apply approved design changes to the correct design artifacts so tests and implementation follow an explicit, reviewable design instead of implicit assumptions. If the current intent does not require a design change, verify and record that decision before tests or code proceed.

## Recommended Agent/Skills

- Recommended agent: `.codex/agents/architecture.md`.
- Recommended skill support: design-update; architecture-review when structure changes.
- Use `.codex/orchestration/implementation-review-validation.md` when this step is part of a larger multi-step change.

## Required Read Order

Read and use:

1. Step `01` intent brief
2. Step `02` plan outputs
3. `.codex/project-context.md`
4. Relevant `design/*`
5. Relevant traceability, validation, or architecture artifacts when they clarify design impact

## Allowed Writes

- `.codex/project-context.md` when high-level behavior or operating model changes
- `design/system-design.md`
- `design/architecture.md`
- `design/ux-flows.md`
- `design/acceptance-criteria.md`

Create missing canonical design files if they do not yet exist.

## Required Outputs

Produce design artifacts or an explicit no-change design decision that:

- reflect approved `REQ-*` scope
- align with current intent and high-level context
- are specific enough for test updates and implementation
- make correctness expectations, boundaries, and gates explicit
- document whether new scaffold/components are allowed, disallowed, or deferred for this cycle

## Procedure

1. Check the plan for required design work before touching tests or code.
2. Apply each `REQ-*` item to the correct design artifact instead of blending concerns.
3. Update `.codex/project-context.md` before or alongside detailed design when the high-level behavior, operating model, or workflow summary changes.
4. Keep the four canonical design files complementary:
   - `system-design` for system behavior
   - `architecture` for structure and major components
   - `ux-flows` for user and operator journeys
   - `acceptance-criteria` for correctness and gates
5. Preserve distinctions from intent and plan. Do not simplify away approval gates, failure behavior, edge cases, or security-relevant constraints.
6. Resolve drift at the design layer instead of normalizing it later in code.
7. If a design ambiguity remains, record it explicitly so tests and implementation do not guess.
8. If no design file changes are required, ensure `plan/design-update.md` says `none` with a reason tied to current intent.
9. Keep design docs human-readable. Use `REQ-*`, `DEV-*`, and `TEST-*` only as comments when needed, not as primary numbering.

## Skip Rules

- Mark this step `skipped` only when the user explicitly bounds the task or the step is genuinely not applicable.
- Skipped steps must include evidence in `.codex/state/appflow-current.json`.
- Do not skip this step to avoid uncertainty; record ambiguity or block instead.

## Guardrails

- Do not implement code changes in this step unless they are inseparable from the design artifact itself.
- Do not invent behavior absent from intent or plan.
- Do not leave acceptance or approval behavior implied.
- Do not allow design files to contradict `.codex/project-context.md`.
- Do not skip design review merely because implementation seems obvious.

## State Evidence Expectations

- Record completion, skip, or block status with `.codex/tools/appflow_run.py mark`.
- Evidence should name the artifacts read or changed and the reason this step can hand off safely.
- Before resuming interrupted work, inspect `.codex/tools/appflow_run.py status` or `preflight`.

## Exit Criteria

- Relevant design artifacts are updated and internally consistent.
- `.codex/project-context.md` and `design/*` agree at the right level of abstraction.
- Step `04` can derive tests directly from the design without guessing.
