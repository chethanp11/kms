---
name: change-verification
description: Verify code or doc changes with the smallest deterministic checks that prove the intended behavior.
---

# Change Verification

## Purpose
Prove that a change works without running broad, noisy validation.

## Read
- `AGENTS.md`
- project grounding file
- relevant implementation and tests
- relevant validation output

## Do
1. Pick the smallest test or smoke check that covers the change.
2. Run the targeted validation first.
3. Expand only if the first check passes and confidence still needs more evidence.
4. Record failures clearly and trace them back to the changed surface.
5. Stop when the requested scope is validated.

## Outputs
- Targeted validation commands
- Pass/fail evidence
- Remaining risks or follow-up checks

## Rules
- Do not weaken tests.
- Do not claim success without evidence.
- Do not substitute broad suites for a missing targeted check.
