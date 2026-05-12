# Framework Mode

Framework mode improves the AppFlow framework itself.

## Activation

Root `AGENTS.md` routes here when `.devmode/mode.yaml` contains:

```yaml
mode: framework
```

## Core Rule

Treat the current user prompt as-is. Do not convert it into application intent, do not run the application lifecycle, and do not assume application context unless the prompt explicitly requests application work.

## Framework Mission

Help evolve AppFlow as a reusable, copy/drop, AI-native engineering framework. Optimize for clear mode routing, prompt-derived app intent, deterministic workflow execution, strong validation, project-agnostic reusable files, and minimal project-specific extension points.

For new application development, the framework contract is that only these files normally need project-specific edits:

1. `.codex/project-context.md`
2. `.codex/tech-stack.md`

## In-Scope Framework Work

Framework mode may change:

- root router behavior in `AGENTS.md`
- mode contracts in `.devmode/app.md`, `.devmode/framework.md`, `.devmode/override.md`, and `.devmode/fix.md`
- lifecycle prompts under `.codex/dev_workflow/`
- fix-mode workflow guidance under `.codex/fix_workflow/`
- role contracts under `.codex/agents/`
- skill contracts under `.codex/skills/`
- orchestration guidance under `.codex/orchestration/`
- active state and evidence conventions under `.codex/state/`
- deterministic helpers under `.codex/tools/`
- framework README and reusable memory under `.codex/`
- validators, bootstrap templates, and structural checks

## Out-of-Scope Application Work

Framework mode is control-plane-only. Do not modify application artifacts, including:

- implementation source such as `src/`, `apps/`, `packages/`, runtime scripts, or product code
- product design, test, plan, intent, or dev-log artifacts
- `.codex/project-context.md` or `.codex/tech-stack.md` content for application behavior, except to preserve generic extension-point guidance when the prompt explicitly asks for framework structure changes

If validation exposes application failures while in framework mode, report them as out-of-scope instead of fixing application code.


## Files Framework Mode Must Not Modify

Framework mode must not modify application/product artifacts unless the current prompt explicitly asks for application work after switching to app mode or explicitly requests a bounded project-specific edit. Forbidden-by-default paths include:

- implementation source: `src/`, `apps/`, `packages/`, runtime `scripts/`, and product code
- product design and requirements: `design/`, `intent/`, product docs, and acceptance criteria
- product validation artifacts: `tests/` and app-specific test plans
- planning and evidence artifacts: `plan/` and `dev_log/`
- project-specific extension files `.codex/project-context.md` and `.codex/tech-stack.md`, except generic extension-point guidance or an explicit project-specific prompt
- product data/content folders such as `wiki/`, `raw/`, `templates/`, `rules/`, `config/`, and `docs/` when they contain application facts

If framework work appears to require these paths, report the boundary and ask for app or override mode unless the prompt already grants explicit scope.

## Execution Behavior

For framework-enhancement prompts:

1. Read `.devmode/mode.yaml`, `AGENTS.md`, the selected first-class `.devmode/<mode>.md` instruction file, sibling mode files needed for synchronization, and the relevant `.codex` framework files.
2. Identify whether the request changes routing, lifecycle, roles, skills, state, tools, validation, bootstrap, or documentation.
3. Inspect current references before editing; do not rename, remove, or add framework folders without updating references and validation.
4. Make minimal, reversible, project-agnostic changes.
5. Keep app-mode behavior synchronized when framework changes affect application workflow.
6. Update validators and bootstrap templates with structural changes.
7. Run targeted framework validation.
8. Report any application validation failures as out-of-scope unless the user explicitly switches to app work.

## Design Principles

- Mode routing is authoritative and must not be bypassed.
- App-mode intent comes from the current prompt, not pre-filled files.
- Reusable framework files must not contain application-specific domain facts.
- Framework behavior should be explicit, deterministic where possible, and easy to validate.
- Agents are role contracts, not permission grants.
- Skills are invoked only when their standard frontmatter description matches the task.
- State is temporary lifecycle evidence, not durable requirements or memory.
- Memory is factual and reviewable; it must not override source-of-truth artifacts.
- Prefer fewer, well-wired framework folders over unused template sprawl.

## Required Synchronization

When changing framework structure, check and update as needed:

- `AGENTS.md`
- `.devmode/app.md`
- `.devmode/framework.md`
- `.devmode/override.md`
- `.devmode/fix.md`
- `.codex/README.md`
- `.codex/dev_workflow/README.md`
- `.codex/fix_workflow/README.md`
- affected `.codex/dev_workflow/*` steps
- `.codex/tools/validate_codex_contract.py`
- `.codex/tools/bootstrap_appflow.py`
- `.codex/state/*` conventions
- `.codex/agents/*` and `.codex/skills/*/SKILL.md` contracts
- `.codex/memory/*` only when it would otherwise become factually stale

## Validation

For framework changes, run the smallest applicable set first:

```bash
python3 .codex/tools/validate_codex_contract.py
git diff --check
python3 -m py_compile .codex/tools/*.py
```

Do not run product tests to justify framework changes unless the prompt explicitly asks for application validation. If product tests are run and fail, do not repair application code in framework mode.

## Stop Conditions

Stop and surface the issue when:

- a requested change would mix framework and application modes
- a framework change would require project-specific facts outside `.codex/project-context.md` or `.codex/tech-stack.md`
- removing or renaming a framework file would leave references or validator gaps unresolved
- validation fails and the root cause is not understood
- application code changes appear necessary while still in framework mode

## Output Expectations

Framework-mode outputs should be concise and should state:

- framework files changed
- routing or lifecycle impact
- validator/bootstrap/state updates made, if any
- validation run and result
- application issues observed but intentionally left out-of-scope
