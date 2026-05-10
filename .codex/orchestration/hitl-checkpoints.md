# Human-in-the-Loop Checkpoints

Stop for human approval before:

- changing instruction precedence or removing governance boundaries
- adding a new framework, service, persistence layer, or hosted dependency
- changing authoritative state ownership or write authority
- broad refactors across multiple ownership boundaries
- destructive filesystem or Git operations
- security, secret-handling, authentication, or authorization changes
- unresolved ambiguity in human-owned intent

When a checkpoint is reached, provide:

1. decision needed
2. options and trade-offs
3. recommended minimal path
4. risks of proceeding without input
