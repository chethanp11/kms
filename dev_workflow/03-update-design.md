# Step 03 Prompt: Update Design

## Use This Prompt When

Use this prompt after planning when `REQ-*` work exists or when behavior must be defined before tests and implementation can proceed safely.

## Workflow Position

- Input step: approved plan
- Output step: current high-level and detailed design baseline

## Objective

Apply approved design changes to the correct design artifacts so tests and implementation follow an explicit, reviewable design instead of implicit assumptions.

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

Produce design artifacts that:

- reflect approved `REQ-*` scope
- align with current intent and high-level context
- are specific enough for test updates and implementation
- make acceptance expectations, boundaries, and gates explicit

## Procedure

1. Apply each `REQ-*` item to the correct design artifact instead of blending concerns.
2. Update `.codex/project-context.md` before or alongside detailed design when the high-level behavior, operating model, or workflow summary changes.
3. Keep the four canonical design files complementary:
   - `system-design` for system behavior
   - `architecture` for structure and major components
   - `ux-flows` for user and operator journeys
   - `acceptance-criteria` for correctness and gates
4. Preserve distinctions from intent and plan. Do not simplify away approval gates, failure behavior, edge cases, or security-relevant constraints.
5. Resolve drift at the design layer instead of normalizing it later in code.
6. If a design ambiguity remains, record it explicitly so tests and implementation do not guess.
7. Keep design docs human-readable. Use `REQ-*`, `DEV-*`, and `TEST-*` only as comments when needed, not as primary numbering.

## Guardrails

- Do not implement code changes in this step unless they are inseparable from the design artifact itself.
- Do not invent behavior absent from intent or plan.
- Do not leave acceptance or approval behavior implied.
- Do not allow design files to contradict `.codex/project-context.md`.

## Exit Criteria

- Relevant design artifacts are updated and internally consistent.
- `.codex/project-context.md` and `design/*` agree at the right level of abstraction.
- Step `04` can derive tests directly from the design without guessing.
