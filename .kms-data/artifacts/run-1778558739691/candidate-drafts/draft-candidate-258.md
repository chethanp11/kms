# Candidate: CLI flags and config overrides win first then

- Type: `metric`
- Proposal only: `true`
- Source: `codex_elite.md`
- Relevance: `0.90`
- Confidence: `0.80`

## Extracted Evidence
Codex’s configuration system is strong enough now that advanced usage should be designed around it, not worked around. The configuration precedence is clear: CLI flags and `--config` overrides win first, then named profiles, then project config files from `.codex/config.toml` ordered from repo root to current working d

## Governance Boundary
This draft is an inspectable intermediate artifact. It is not canonical wiki truth and is not publishable without deterministic validation, Knowledge Manager review, and approval.
