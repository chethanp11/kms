# Evaluation Plan

This file is system-generated from intent and iteration workflow. Do not edit directly.

## Purpose
Define how the copied project will be evaluated for correctness, safety, grounding quality, tool behavior, latency, and cost.

## Intent sources
- `intent/product-intent.md`
- `intent/constraints-intent.md`
- `intent/feedback-intent.md`
- `intent/iteration-intent.md`

## Evaluation goals
- `EVAL-001`: Confirm supported maintenance flows satisfy the mapped acceptance criteria.
- `EVAL-002`: Detect hallucinations, unsupported assertions, and unsafe overreach during contradiction handling.
- `EVAL-003`: Verify Infopedia browse behavior is read-only and correctly grounded in finalized wiki content.
- `EVAL-004`: Measure graceful handling of source, publication, or dependency failure against version expectations.
- `EVAL-005`: Capture manual-review findings that automated checks miss.

## Evaluation inventory
| ID | Scenario | Linked acceptance | Method | Pass condition | Notes |
| --- | --- | --- | --- | --- | --- |
| `EVAL-001` | Maintenance run over a valid local source bundle with an existing wiki snapshot | `ACC-001` | hybrid | Proposal output contains source trace, markdown diff, and run summary; nothing is finalized until review allows it | Use a representative source fixture and current wiki fixture |
| `EVAL-002` | Contradictory, incomplete, or policy-conflicting source input | `ACC-002` | manual or hybrid | System surfaces the contradiction, avoids automatic finalization, and requests review or escalation | Include at least one low-confidence case |
| `EVAL-003` | Infopedia browse/search/open flow over finalized wiki pages | `ACC-003` | automated and manual | Finalized content is readable and navigable, and no browse path can write or publish | Verify read-only separation explicitly |
| `EVAL-004` | Source discovery, markdown parsing, or publication dependency failure | `ACC-004` | hybrid | Run is halted or degraded safely, audit evidence remains intact, and no unauthorized wiki write occurs | Useful for partial source bundles and write conflicts |
| `EVAL-005` | Manual review sample set across approved, rejected, and escalated proposals | `ACC-004` | manual | Reviewer can trace source, decision, and publication outcome without ambiguity | Sample should include at least one rejected or escalated case |

## Evaluation dimensions
- Correctness of final answer or action
- Compliance with the prompt contract and schema
- Grounding accuracy and provenance
- Tool necessity and correctness
- Refusal, fallback, and uncertainty quality
- Latency and cost behavior
- Human-review burden

## Failure categories
- Hallucination: output contains unsupported or fabricated claims.
- Retrieval gap: the response relies on incorrect or missing source data.
- Prompt drift: the response exceeds the defined scope or contract.
- Safety violation: the response fails to respect guardrails.
- Performance issue: latency or cost exceeds acceptable thresholds.
- Tool misuse: the system used a tool unnecessarily or interpreted it incorrectly.
- Review gap: automated checks passed but manual review found a material issue.

## Test data and fixtures
- Eval dataset source: fixtures derived from representative source bundles and finalized wiki pages
- Coverage notes: includes happy path, contradiction path, browse-only path, and failure-path samples
- Refresh rule: update eval cases when source conventions, wiki conventions, or governance rules change

## Manual review loop
- Reviewer role: Knowledge Manager or designated reviewer
- Sample size or sampling rule: include every escalated case plus a rotating sample of approved and rejected cases
- Review rubric: provenance clarity, contradiction handling, publication correctness, and audit completeness
- Where to log findings: `dev_log/feedback-log.md` and `dev_log/validation-log.md`

## Release gates
- Required evals to ship this version: `EVAL-001`, `EVAL-002`, `EVAL-003`, `EVAL-004`, `EVAL-005`
- Blocking thresholds: zero uncontrolled publication events, zero critical provenance gaps, and no unresolved audit failures
- Non-blocking observations: style issues, minor wording cleanup, and backlog improvements that do not affect truth ownership
