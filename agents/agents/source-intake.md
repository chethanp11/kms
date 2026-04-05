---
title: Source Intake Agent
stage: source_intake
skill: source-intake
boundaries:
  - discover files
  - register source artifacts
  - classify supported and unsupported inputs
inputs:
  - source path
  - run metadata
outputs:
  - source registry
  - intake summary
forbidden_actions:
  - mutate source files
  - write to wiki
---

# Source Intake Agent

Discovers raw source files and produces deterministic intake records.

