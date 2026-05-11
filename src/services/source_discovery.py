"""Source discovery service."""

from __future__ import annotations

from pathlib import Path

from src.contracts import SourceBundle
from src.execution import discover_source_bundle


def discover_sources(source_path: Path | str) -> SourceBundle:
    return discover_source_bundle(source_path)


__all__ = ["discover_sources"]
