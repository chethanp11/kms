# Candidate: str str return value strip upper replace

- Type: `concept`
- Proposal only: `true`
- Source: `codes/python/order_service.py`
- Relevance: `0.60`
- Confidence: `0.68`

## Extracted Evidence
def normalize_sku(value: str) -> str: return value.strip().upper().replace(" ", "-")

## Governance Boundary
This draft is an inspectable intermediate artifact. It is not canonical wiki truth and is not publishable without deterministic validation, Knowledge Manager review, and approval.
