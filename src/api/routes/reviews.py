"""Review API routes."""
from __future__ import annotations
from src.api.dependencies import get_runtime
def get_diff(revision_id: str) -> dict[str, object] | None:
    revision = get_runtime().metadata.revisions.get(revision_id)
    return None if revision is None else {"revision_id": revision_id, "diff_summary": revision.diff_summary, "status": revision.status.value}
__all__ = ["get_diff"]
