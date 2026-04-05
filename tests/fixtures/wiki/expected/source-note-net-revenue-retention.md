---
title: Net Revenue Retention Source Note
slug: net-revenue-retention-source-note
type: source-note
domain: customer-revenue-analytics
status: finalized
source_refs:
  - raw:/sources/reports/nrr.csv
  - raw:/sources/notes/revenue-note.md
last_updated: 2026-04-05
confidence: medium
review_required: true
related:
  - metric/customer-revenue-analytics/net-revenue-retention
  - data-asset/customer-revenue-analytics/sales-orders-fact
tags:
  - source-note
  - revenue
  - retention
owners:
  - knowledge-manager:revenue-ops
---

# Net Revenue Retention Source Note

## Summary

NRR improved to 118% for enterprise accounts in Q4.

## Current Understanding

The note is an intake artifact that should be reconciled with the monthly close report.

## Source Details

Parsed from intake source files and the attached revenue note.

## Extracted Signals

- NRR
- enterprise accounts
- Q4 improvement

## Candidate Entities

- enterprise customer cohort

## Candidate Metrics

- Net Revenue Retention

## Candidate Processes

- monthly revenue close

## Candidate Impacts

- reconcile metric definition against the approved sales orders fact

## Source Trace

- Source reference: `/sources/reports/nrr.csv`
- Source reference: `/sources/notes/revenue-note.md`
