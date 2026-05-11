"""Rule schema validation for policy YAML-like dictionaries."""
from __future__ import annotations
from src.contracts import ValidationError
REQUIRED_RULE_FIELDS = {"id", "description", "scope", "severity", "condition", "action"}
def validate_rule(rule: dict[str, object]) -> dict[str, object]:
    missing = sorted(REQUIRED_RULE_FIELDS - set(rule))
    if missing:
        raise ValidationError(f"rule missing required fields: {', '.join(missing)}")
    if rule["severity"] not in {"error", "warning"}:
        raise ValidationError("rule severity must be error or warning")
    if rule["action"] not in {"block_publish", "escalate_review", "log_only"}:
        raise ValidationError("rule action is not supported")
    return dict(rule)
__all__ = ["REQUIRED_RULE_FIELDS", "validate_rule"]
