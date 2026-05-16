"""Health API routes."""
from __future__ import annotations
from src.api.dependencies import get_runtime
def findings() -> list[dict[str, object]]:
    return [
        {
            **finding.__dict__,
            "severity": finding.severity.value,
            "status": finding.status.value,
        }
        for finding in get_runtime().metadata.lint_findings.values()
    ]
def health() -> dict[str, str]:
    return {"status": "ok"}
__all__ = ["findings", "health"]
