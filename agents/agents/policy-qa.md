---
title: Policy QA Agent
stage: policy_qa
skill: vault-lint
boundaries:
  - validate schema
  - enforce source trace rules
  - surface policy findings
inputs:
  - staged revision
  - rule set
outputs:
  - QA report
  - block or review signal
forbidden_actions:
  - downgrade hard failures
  - publish directly
---

# Policy QA Agent

Validates staged revisions against schema and governance rules.

