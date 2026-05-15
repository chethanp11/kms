---
candidate_id: candidate-38
source_ref: codes/python/order_service.py
title: order Order ord 1001 cust 42 add item
type: metric
---

# order Order ord 1001 cust 42 add item

## Summary
order = Order("ord-1001", "cust-42") add_item(order, "widget alpha", "12.50", 2) add_item(order, "service plan", "4.75", 1) order.discount = Decimal("1.25")

## Candidate Type
metric

## Review Status
Approved by Knowledge Manager through KMI candidate review.

## Source Trace
- codes/python/order_service.py

## Confidence
- Relevance: 0.82
- Confidence: 0.68

## Rationale
metric candidate extracted by semantic decomposition with deterministic relevance and confidence scoring.
