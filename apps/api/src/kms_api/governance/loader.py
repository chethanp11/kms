from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .models import GovernanceRule


@dataclass(frozen=True)
class LoadedRuleSet:
    rules: tuple[GovernanceRule, ...]


class GovernanceRuleLoader:
    def __init__(self, rules_root: Path | None = None) -> None:
        self._rules_root = rules_root or Path("rules")

    def load(self) -> LoadedRuleSet:
        rule_files = sorted(self._iter_rule_files())
        if not rule_files:
            raise ValueError(f"No governance rule files found in {self._rules_root}")

        rules: list[GovernanceRule] = []
        for path in rule_files:
            payload = yaml.safe_load(path.read_text(encoding="utf-8"))
            if payload is None:
                raise ValueError(f"Empty rule file: {path}")
            if isinstance(payload, dict) and "rules" in payload:
                entries = payload["rules"]
            elif isinstance(payload, list):
                entries = payload
            else:
                entries = [payload]
            if not isinstance(entries, list):
                raise ValueError(f"Invalid rule payload in {path}")
            for index, entry in enumerate(entries):
                rules.append(self._load_rule(entry, source_file=f"{path}:{index + 1}"))
        return LoadedRuleSet(rules=tuple(rules))

    def _iter_rule_files(self) -> list[Path]:
        if not self._rules_root.exists():
            return []
        return [*self._rules_root.glob("*.yaml"), *self._rules_root.glob("*.yml")]

    def _load_rule(self, payload: Any, *, source_file: str) -> GovernanceRule:
        if not isinstance(payload, dict):
            raise ValueError(f"Rule entry must be a mapping: {source_file}")

        required_fields = ("id", "description", "scope", "severity", "condition", "action")
        missing = [field for field in required_fields if field not in payload]
        if missing:
            raise ValueError(f"Rule entry missing required field(s) {missing}: {source_file}")

        scope = payload["scope"]
        if not isinstance(scope, dict):
            raise ValueError(f"Rule scope must be a mapping: {source_file}")
        page_types = scope.get("page_types", [])
        if page_types is None:
            page_types = []
        if not isinstance(page_types, list):
            raise ValueError(f"Rule scope.page_types must be a list: {source_file}")

        severity = payload["severity"]
        if severity not in {"error", "warning"}:
            raise ValueError(f"Invalid rule severity {severity!r}: {source_file}")

        action = payload["action"]
        if action not in {"block_publish", "escalate_review", "log_only"}:
            raise ValueError(f"Invalid rule action {action!r}: {source_file}")

        condition = payload["condition"]
        if not isinstance(condition, dict):
            raise ValueError(f"Rule condition must be a mapping: {source_file}")

        return GovernanceRule(
            rule_id=str(payload["id"]),
            description=str(payload["description"]),
            scope_page_types=tuple(str(page_type) for page_type in page_types),
            severity=severity,
            condition=condition,
            action=action,
            source_file=source_file,
        )
