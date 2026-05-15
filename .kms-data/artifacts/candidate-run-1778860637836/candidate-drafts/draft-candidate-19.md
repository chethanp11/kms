# Candidate: return sum item extended price for item in

- Type: `metric`
- Proposal only: `true`
- Source: `codes/python/order_service.py`
- Relevance: `0.90`
- Confidence: `0.80`

## Extracted Evidence
def subtotal(self) -> Decimal: return sum((item.extended_price() for item in self.items), Decimal("0.00"))

## Governance Boundary
This draft is an inspectable intermediate artifact. It is not canonical wiki truth and is not publishable without deterministic validation, Knowledge Manager review, and approval.
