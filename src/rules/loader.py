"""Load simple policy rule files without mandatory third-party YAML dependencies."""
from __future__ import annotations
from pathlib import Path
from src.rules.schema import validate_rule

def load_policy_rules(path: Path | str) -> list[dict[str, object]]:
    text = Path(path).read_text(encoding="utf-8")
    rules: list[dict[str, object]] = []
    current: dict[str, object] = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("-") and current:
            rules.append(validate_rule(current)); current = {}
            line = line[1:].strip()
        if ":" in line and not line.startswith("-"):
            key, value = line.split(":", 1)
            current[key.strip()] = value.strip() or {}
    if current:
        rules.append(validate_rule(current))
    return rules
__all__ = ["load_policy_rules"]
