# State

Temporary resumable state for active long-running Codex tasks.

Do not store permanent decisions here. Move completed outcomes into `dev_log/*`, `design/*`, `.codex/memory/*`, or workflow docs as appropriate.

## App mode use

- `current-intent.md` is the prompt-derived intent for the current app-mode turn only.
- `appflow-current.json` is active lifecycle evidence for the current app-mode run only.
- Inactive state must not contain stale completed-step evidence.

## Lifecycle commands

- `preflight`: inspect mode, stale intake, plan files, validation sources, and active run state before work.
- `status`: inspect incomplete steps, validation state, and stale intake warnings during work.
- `complete`: mark a fully validated run complete and clear current-turn intent after closeout.
