# Step 03 Prompt: Update Design

## Use This Prompt When

Use this prompt after planning when `REQ-*` work exists or when intent changes require design clarification before implementation.

## Objective

Apply approved design changes to the correct design artifacts so implementation and tests follow an explicit design baseline.

## Required Inputs

Read and use:

1. Step `01` output
2. Step `02` plan outputs
3. `.codex/project-context.md`
4. Relevant `design/*`
5. Relevant traceability and validation artifacts when they clarify design implications

## Instructions

1. Apply each `REQ-*` item to the correct design artifact instead of blending concerns:
   - `design/system-design.md` for system behavior
   - `design/architecture.md` for structure and major components
   - `design/ux-flows.md` for user and operator journeys
   - `design/acceptance-criteria.md` for correctness and gates
2. Update `.codex/project-context.md` before or alongside detailed design when the high-level behavior, operating model, or workflow summary changes.
3. If the request changes workflow, precedence, ownership, or operating rules, update `AGENTS.md` and `.codex/project-context.md` first before finishing detailed design edits.
4. Keep design files complementary. Avoid repetition that blurs ownership.
5. Preserve the important distinctions from intent and plan. Do not simplify away edge cases or approval gates.
6. Keep design docs human-readable. Do not use `REQ-*`, `DEV-*`, or `TEST-*` as primary numbering in the design body.
7. Resolve drift at the design layer instead of normalizing it later in code.
8. If design is unclear or blocked, record the ambiguity explicitly so tests and implementation do not guess.

## Produce

Produce design artifacts that:

- reflect the approved `REQ-*` scope
- align with current intent and high-level context
- are specific enough for test updates and implementation
- make acceptance expectations clear

## Guardrails

- Do not implement code changes in this step unless they are inseparable from the design artifact itself.
- Do not invent behavior that is absent from intent or plan.
- Do not move design-only traceability IDs into primary in-document numbering.
- Do not leave downstream teams to infer acceptance behavior from vague wording.

## Exit Criteria

- Relevant design artifacts are updated and internally consistent.
- `.codex/project-context.md` and `design/*` agree at the right level of abstraction.
- The next test step can derive proving work from explicit acceptance-driven design.
