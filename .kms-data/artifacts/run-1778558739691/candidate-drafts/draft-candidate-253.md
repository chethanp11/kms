# Candidate: setup runs first and can use network access

- Type: `concept`
- Proposal only: `true`
- Source: `codex_elite.md`
- Relevance: `0.60`
- Confidence: `0.68`

## Extracted Evidence
Cloud execution is architecturally different from local execution. Codex cloud uses isolated provider-managed containers and a two-phase runtime model: setup runs first and can use network access to install dependencies; then the agent phase runs offline by default unless internet access is enabled for that environment

## Governance Boundary
This draft is an inspectable intermediate artifact. It is not canonical wiki truth and is not publishable without deterministic validation, Knowledge Manager review, and approval.
