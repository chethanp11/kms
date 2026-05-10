"""Agent boundary names for future governed automation."""

AGENT_ROLES: tuple[str, ...] = (
    "orchestrator",
    "source-intake",
    "source-analyst",
    "wiki-curator",
    "policy-qa",
    "contradiction-reviewer",
    "publisher",
    "lint",
)

__all__ = ["AGENT_ROLES"]
