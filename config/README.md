# Config

This directory centralizes runtime configuration manifests, environment templates, and secret references for KMS.

Actual API keys and secret values must be injected at runtime and must not be committed to the repository.

Suggested layout:

- `runtime.env.example` for non-secret environment variables
- `secrets.example.yaml` for placeholder secret references
- `local/` for developer-only overrides that remain untracked

