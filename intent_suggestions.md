# KMS Intent Suggestions

Run these one by one in `mode: app`. Each prompt should complete one AppFlow cycle before the next prompt is started.

## 1. Normalize current plans and scaffold boundary

```text
Review the current KMS plan, design, tests, and src scaffold. Update plan/design/test artifacts so they reflect the current app state. Do not add new src components unless the current design proves they are necessary. Record any scaffold drift as gaps or corrective work.
```

## 2. Define core domain contracts completely

```text
Complete the core KMS domain contracts for runs, source files, source documents, wiki pages, revisions, approvals, contradictions, QA reports, lint findings, Infopedia nodes, and search documents based on design/architecture.md. Update plan, design, tests, and src contracts only as needed.
```

## 3. Implement source intake pipeline

```text
Implement the source intake pipeline for path validation, deterministic discovery, registration, file classification, parsing placeholders, source-note output, warnings, and failure states. Keep writes out of /wiki. Update design and tests if the implementation reveals missing details.
```

## 4. Implement metadata repository layer

```text
Implement the metadata repository interfaces and deterministic in-memory repository behavior for runs, source records, revisions, approvals, contradictions, QA reports, and lint findings. Keep metadata supporting-only and not authoritative for knowledge truth.
```

## 5. Implement wiki draft and publish boundary

```text
Implement wiki draft generation and governed publish boundary so only approved and validated markdown can be written to /wiki. Add tests for blocked writes, approved writes, source trace, and audit evidence.
```

## 6. Implement governance and validation rules

```text
Implement governance validation for required wiki frontmatter, required body sections, source trace, confidence, freshness, links, duplicate canonical pages, contradictions, and approval gates. Update acceptance criteria and tests before code where rules are underspecified.
```

## 7. Implement contradiction and open-question workflow

```text
Implement contradiction records, severity/status handling, open-question creation support, and blocking behavior for unresolved contradictions. Preserve Knowledge Manager authority for final resolution.
```

## 8. Implement API service contracts

```text
Implement API service contracts for run creation/status/artifacts, review diff, approval submission, wiki page read, Infopedia tree/search, contradiction detail, and health findings. Keep UI clients behind API contracts and away from direct storage access.
```

## 9. Implement KMI HTML/CSS/JS shell

```text
Implement the initial KMI HTML/CSS/JavaScript shell for dashboard, intake, run detail, diff review, contradictions, approvals, and maintenance health using API contract stubs. Do not add frontend frameworks.
```

## 10. Implement Infopedia HTML/CSS/JS shell

```text
Implement the initial read-only Infopedia HTML/CSS/JavaScript shell for navigation tree, page view, search, related pages, and freshness/status indicators. Ensure it cannot mutate finalized knowledge.
```

## 11. Implement search and projection layer

```text
Implement rebuildable Infopedia projection and search document generation from /wiki plus supporting metadata. Ensure projections are derived and never authoritative.
```

## 12. Add end-to-end workflow tests

```text
Add end-to-end tests for source intake through draft, validation, approval, publish, Infopedia projection rebuild, and read-only browse. Keep tests deterministic and fixture-based.
```

## 13. Add operational observability and audit evidence

```text
Implement structured audit events, validation summaries, publish summaries, run status visibility, and health findings for the KMS workflow. Update UX and acceptance criteria if observability expectations are incomplete.
```

## 14. Harden failure handling and recovery

```text
Harden failure handling for invalid paths, empty source folders, unsupported files, parser failures, validation failures, rejected approvals, wiki write failures, metadata failures, and projection rebuild failures. Add regression tests for each failure path.
```

## 15. Complete release closeout

```text
Run a full design, test, code, validation, and log audit for KMS. Fix any drift between intent, plan, design, tests, src, and dev_log. Produce final validation evidence and next-cycle gaps only if evidence-backed gaps remain.
```
