# Repository Mode Router

`.devmode/mode.yaml` is mandatory and authoritative. Read it before any repository-specific instruction file or workflow file.

Valid modes:

```yaml
mode: app
```

```yaml
mode: framework
```

```yaml
mode: override
```

```yaml
mode: fix
```

## Strict Routing

- If `mode: app`, read and follow `.devmode/app.md`.
- If `mode: framework`, read and follow `.devmode/framework.md`.
- If `mode: override`, read and follow `.devmode/override.md`.
- If `mode: fix`, read and follow `.devmode/fix.md`.
- Treat the selected `.devmode/<mode>.md` file as the first-class instruction contract for the turn.
- If the file is missing, malformed, or contains any other mode, stop and report the configuration error.

## Mode Enforcement

- Never blend modes.
- Never run `.codex/dev_workflow/*` in framework mode unless the user explicitly asks to test or edit the workflow files themselves.
- Never modify application artifacts in framework mode, including implementation source, product design, tests, plans, logs, or app-specific project files, unless the user explicitly asks for application work after switching to app mode.
- Never modify framework/control-plane files in app mode unless the user prompt explicitly changes AppFlow behavior.
- When `mode: override`, do not run AppFlow or framework workflows automatically; modify any file only as directed by the prompt and normal repository safety rules.
- When `mode: fix`, run only the application repair loop for existing behavior; do not modify framework/control-plane files or add new features.
- When uncertain whether a request is framework or application work, follow `.devmode/mode.yaml` and ask before crossing modes.
- If you feel the mode is incorrent based on the prompt pause and ask user to change the mode.
