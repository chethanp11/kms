# Candidate: lines append f item sku x item quantity

- Type: `concept`
- Proposal only: `true`
- Source: `codes/python/order_service.py`
- Relevance: `0.60`
- Confidence: `0.68`

## Extracted Evidence
for item in order.items: lines.append(f"- {item.sku} x{item.quantity} @ {item.unit_price}")

## Governance Boundary
This draft is an inspectable intermediate artifact. It is not canonical wiki truth and is not publishable without deterministic validation, Knowledge Manager review, and approval.
