---
candidate_id: candidate-19
source_ref: codes/python/order_service.py
title: return sum item extended price for item in
type: metric
---

# return sum item extended price for item in

## Summary
def subtotal(self) -> Decimal: return sum((item.extended_price() for item in self.items), Decimal("0.00"))

## Candidate Type
metric

## Review Status
Approved by Knowledge Manager through KMI candidate review.

## Source Trace
- codes/python/order_service.py

## Confidence
- Relevance: 0.90
- Confidence: 0.80

## Rationale
metric candidate extracted by semantic decomposition with deterministic relevance and confidence scoring.
