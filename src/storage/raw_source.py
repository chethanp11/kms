"""Raw source storage access; raw files are read-only evidence."""

from __future__ import annotations

from pathlib import Path

from src.execution import discover_source_bundle
from src.contracts import SourceBundle


class RawSourceStore:
    def discover(self, root: Path | str) -> SourceBundle:
        return discover_source_bundle(root)


__all__ = ["RawSourceStore"]
