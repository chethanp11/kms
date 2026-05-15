# Candidate: order Order ord 1001 cust 42 add item

- Type: `metric`
- Proposal only: `true`
- Source: `codes/python/order_service.py`
- Relevance: `0.82`
- Confidence: `0.68`

## Extracted Evidence
order = Order("ord-1001", "cust-42") add_item(order, "widget alpha", "12.50", 2) add_item(order, "service plan", "4.75", 1) order.discount = Decimal("1.25")

## Governance Boundary
This draft is an inspectable intermediate artifact. It is not canonical wiki truth and is not publishable without deterministic validation, Knowledge Manager review, and approval.
