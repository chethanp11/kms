# Candidate: cloud agent supports MCP tools but not MCP

- Type: `contradiction`
- Proposal only: `true`
- Source: `Github_elite.md`
- Relevance: `0.97`
- Confidence: `0.72`

## Extracted Evidence
A few things are still partial or asymmetric. VS Code custom agents support `handoffs`, `argument-hint`, subagent controls, and agent-scoped hooks, but GitHub cloud agent currently ignores some IDE-only agent properties such as `argument-hint` and `handoffs`. MCP support in cloud agent is also narrower than in the IDE:

## Governance Boundary
This draft is an inspectable intermediate artifact. It is not canonical wiki truth and is not publishable without deterministic validation, Knowledge Manager review, and approval.
