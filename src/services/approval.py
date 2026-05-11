"""Approval decision service."""

from __future__ import annotations

from src.contracts import ApprovalDecision, ApprovalRecord


def create_approval(revision_id: str, reviewer_id: str, decision: ApprovalDecision, *, reason: str = "") -> ApprovalRecord:
    return ApprovalRecord(approval_id=f"approval-{revision_id}", revision_id=revision_id, decision=decision, reviewer_id=reviewer_id, reason=reason)


def approval_allows_publish(approval: ApprovalRecord | None) -> bool:
    return approval is not None and approval.decision is ApprovalDecision.APPROVED


__all__ = ["approval_allows_publish", "create_approval"]
