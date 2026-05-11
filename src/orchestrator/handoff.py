"""Handoff summaries between KMS service stages."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Handoff:
    from_stage: str
    to_stage: str
    summary: str
    artifact_refs: tuple[str, ...] = ()


def create_handoff(from_stage: str, to_stage: str, summary: str, artifact_refs: tuple[str, ...] = ()) -> Handoff:
    return Handoff(from_stage, to_stage, summary, tuple(artifact_refs))


__all__ = ["Handoff", "create_handoff"]
