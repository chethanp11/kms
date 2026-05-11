"""Request schemas represented as stdlib dataclasses."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class CreateRunRequest:
    source_path: str
    run_id: str = "run-1"
    auto_approve: bool = False

@dataclass(frozen=True)
class ApprovalRequest:
    reviewer_id: str
    decision: str
    reason: str = ""

__all__ = ["ApprovalRequest", "CreateRunRequest"]
