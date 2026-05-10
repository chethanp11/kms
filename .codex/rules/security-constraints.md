# Security Constraints

- Do not commit secrets, credentials, tokens, private keys, or sensitive local paths beyond necessary repo-relative paths.
- Do not expose raw source content as finalized truth.
- Treat publication, authentication, authorization, and secret handling as high-risk changes requiring explicit design and validation.
- Prefer fail-closed behavior for missing governance rules, missing source trace, or invalid publication state.
