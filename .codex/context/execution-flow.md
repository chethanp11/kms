# Execution Flow Template

Use this template to document how work moves through an application and through the repository.

## Runtime Flow

Capture:

1. user or system trigger
2. entrypoint
3. orchestration path
4. domain/service calls
5. persistence or external calls
6. response/output
7. observability events
8. failure and retry behavior

## Development Flow

Recommended AppFlow sequence:

1. read project contract and context
2. interpret intent
3. plan scoped work
4. update design/contracts when needed
5. update validation expectations
6. implement
7. validate
8. repair failures
9. record evidence
10. close the iteration

## Long-Horizon Flow

For multi-phase work, use:

`plan → design/context update → implement → review → validate → log → closeout`
