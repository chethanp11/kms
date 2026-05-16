"""Approval API routes."""
from __future__ import annotations
from src.api.dependencies import get_runtime
from src.contracts import ApprovalDecision, ValidationError
from src.services.approval import create_approval
def submit_approval(revision_id: str, payload: dict[str, object]) -> dict[str, str]:
    runtime = get_runtime()
    if revision_id not in runtime.metadata.revisions:
        raise ValidationError(f"revision not found: {revision_id}")
    approval = create_approval(revision_id, str(payload.get("reviewer_id", "knowledge-manager")), ApprovalDecision(str(payload.get("decision", "approved"))), reason=str(payload.get("reason", "")))
    runtime.metadata.save_approval(approval)
    return {"revision_id": revision_id, "decision": approval.decision.value}
__all__ = ["submit_approval"]
