# Candidate: issues append negative discount

- Type: `metric`
- Proposal only: `true`
- Source: `codes/python/order_service.py`
- Relevance: `0.86`
- Confidence: `0.80`

## Extracted Evidence
if order.discount < Decimal("0.00"): issues.append("negative discount")

## Governance Boundary
This draft is an inspectable intermediate artifact. It is not canonical wiki truth and is not publishable without deterministic validation, Knowledge Manager review, and approval.
