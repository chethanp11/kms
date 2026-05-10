# State

Temporary resumable state for active long-running Codex tasks.

Do not store permanent decisions here. Move completed outcomes into `dev_log/*`, `design/*`, `.codex/memory/*`, or workflow docs as appropriate.

## App mode use

- `current-intent.md` is the prompt-derived intent for the current app-mode turn only.
- `appflow-current.json` is active lifecycle evidence for the current app-mode run only.
- Inactive state must not contain stale completed-step evidence.
