"""Approval API routes."""
from __future__ import annotations
from src.api.dependencies import get_runtime
from src.contracts import ApprovalDecision
from src.services.approval import create_approval
def submit_approval(revision_id: str, payload: dict[str, object]) -> dict[str, str]:
    approval = create_approval(revision_id, str(payload.get("reviewer_id", "knowledge-manager")), ApprovalDecision(str(payload.get("decision", "approved"))), reason=str(payload.get("reason", "")))
    get_runtime().metadata.save_approval(approval)
    return {"revision_id": revision_id, "decision": approval.decision.value}
__all__ = ["submit_approval"]
