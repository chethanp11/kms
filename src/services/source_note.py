"""Source-note rendering service."""

from __future__ import annotations

from src.contracts import SourceBundle
from src.execution import source_note_for_bundle


def render_source_note(bundle: SourceBundle) -> str:
    return source_note_for_bundle(bundle)


__all__ = ["render_source_note"]
