---
candidate_id: candidate-22
source_ref: codes/python/order_service.py
title: Order sku str price str quantity int Order
type: concept
---

# Order sku str price str quantity int Order

## Summary
def add_item(order: Order, sku: str, price: str, quantity: int) -> Order: order.items.append(LineItem(normalize_sku(sku), Decimal(price), quantity)) return order

## Candidate Type
concept

## Review Status
Approved by Knowledge Manager through KMI candidate review.

## Source Trace
- codes/python/order_service.py

## Confidence
- Relevance: 0.60
- Confidence: 0.68

## Rationale
concept candidate extracted by semantic decomposition with deterministic relevance and confidence scoring.
