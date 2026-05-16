"""Contradiction API routes."""
from __future__ import annotations
from src.api.dependencies import get_runtime
def get_contradiction(contradiction_id: str) -> dict[str, object] | None:
    record = get_runtime().metadata.contradictions.get(contradiction_id)
    return None if record is None else {
        **record.__dict__,
        "severity": record.severity.value,
        "status": record.status.value,
    }
__all__ = ["get_contradiction"]
