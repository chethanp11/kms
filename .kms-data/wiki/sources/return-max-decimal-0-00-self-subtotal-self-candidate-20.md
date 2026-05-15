---
candidate_id: candidate-20
source_ref: codes/python/order_service.py
title: return max Decimal 0 00 self subtotal self
type: metric
---

# return max Decimal 0 00 self subtotal self

## Summary
def total(self) -> Decimal: return max(Decimal("0.00"), self.subtotal() - self.discount)

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
