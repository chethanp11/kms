"""Identifier helpers."""
from __future__ import annotations
import re

def stable_id(prefix: str, value: int | str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.:-]+", "-", str(value)).strip("-") or "item"
    return f"{prefix}-{cleaned}"

__all__ = ["stable_id"]
