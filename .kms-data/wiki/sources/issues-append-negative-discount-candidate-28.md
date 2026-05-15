---
candidate_id: candidate-28
source_ref: codes/python/order_service.py
title: issues append negative discount
type: metric
---

# issues append negative discount

## Summary
if order.discount < Decimal("0.00"): issues.append("negative discount")

## Candidate Type
metric

## Review Status
Approved by Knowledge Manager through KMI candidate review.

## Source Trace
- codes/python/order_service.py

## Confidence
- Relevance: 0.86
- Confidence: 0.80

## Rationale
metric candidate extracted by semantic decomposition with deterministic relevance and confidence scoring.
