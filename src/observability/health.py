"""Runtime health helpers."""
from __future__ import annotations
def health_status() -> dict[str, str]:
    return {"status": "ok"}
__all__ = ["health_status"]
