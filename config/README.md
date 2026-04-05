# Config

This directory centralizes runtime configuration manifests, environment templates, and secret references for KMS.

Actual API keys and secret values must be injected at runtime and must not be committed to the repository.

Suggested layout:

- `runtime.env.example` for non-secret environment variables
- `secrets.example.yaml` for placeholder secret references
- `local/` for developer-only overrides that remain untracked

Common local values:

- `KMS_RAW_PATH` should point at the immutable source mount
- `KMS_WIKI_PATH` should point at the canonical `/wiki` mount
- `KMS_METADATA_DB_URL` should target the metadata database used by the API and worker
- `KMS_SEARCH_INDEX_URL` should target the derived search/index service when present
