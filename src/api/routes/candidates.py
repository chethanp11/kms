"""Candidate workflow API route functions."""

from __future__ import annotations

from src.api.dependencies import get_runtime
from src.contracts import KnowledgeCandidate, UploadedSourceFile


def create_candidates(payload: dict[str, object]) -> dict[str, object]:
    raw_source_files = payload.get("source_files", ())
    source_files = tuple(
        UploadedSourceFile(
            relative_path=str(item.get("relative_path", "")),
            content=str(item.get("content", "")),
            media_type=str(item.get("media_type", "text/plain")),
        )
        for item in raw_source_files
        if isinstance(item, dict)
    ) if isinstance(raw_source_files, list) else ()
    result = get_runtime().create_candidates(
        str(payload["source_path"]),
        run_id=str(payload.get("run_id", "run-1")),
        source_files=source_files,
    )
    return {
        "run_id": result.run.run_id,
        "state": result.run.state.value,
        "provider": result.provider,
        "fallback_used": result.fallback_used,
        "warning": result.warning,
        "summary_counts": dict(result.run.summary_counts),
        "candidates": [_candidate_response(candidate, approved=False, archived=False) for candidate in result.candidates],
    }


def list_candidates(run_id: str) -> list[dict[str, object]]:
    runtime = get_runtime()
    approved = runtime.metadata.approved_candidate_ids
    archived = runtime.metadata.archived_candidate_ids
    return [
        _candidate_response(candidate, approved=candidate.candidate_id in approved, archived=candidate.candidate_id in archived)
        for candidate in runtime.metadata.candidates_for_run(run_id)
    ]


def approve_candidates(run_id: str, payload: dict[str, object]) -> dict[str, object]:
    raw_ids = payload.get("candidate_ids", ())
    candidate_ids = tuple(str(item) for item in raw_ids) if isinstance(raw_ids, list) else ()
    raw_mods = payload.get("modifications", {})
    modifications = {str(key): str(value) for key, value in raw_mods.items()} if isinstance(raw_mods, dict) else {}
    if payload.get("decision") == "reject":
        result = get_runtime().reject_candidates(
            run_id,
            candidate_ids=candidate_ids,
            reason=str(payload.get("reason", "")),
        )
        return {
            "run_id": result.run_id,
            "approved_candidate_ids": list(result.approved_candidate_ids),
            "rejected_candidate_ids": list(result.rejected_candidate_ids),
        }
    result = get_runtime().approve_candidates(
        run_id,
        candidate_ids=candidate_ids,
        approve_all=bool(payload.get("approve_all", False)),
        modifications=modifications,
    )
    return {
        "run_id": result.run_id,
        "approved_candidate_ids": list(result.approved_candidate_ids),
        "rejected_candidate_ids": list(result.rejected_candidate_ids),
    }


def publish_approved_candidates(run_id: str, payload: dict[str, object] | None = None) -> dict[str, object]:
    payload = payload or {}
    result = get_runtime().publish_approved_candidates(
        run_id,
        reviewer_id=str(payload.get("reviewer_id", "knowledge-manager")),
    )
    return {
        "run_id": result.run.run_id,
        "state": result.run.state.value,
        "summary_counts": dict(result.run.summary_counts),
        "published": [item.page_path for item in result.published],
    }


def _candidate_response(candidate: KnowledgeCandidate, *, approved: bool, archived: bool) -> dict[str, object]:
    return {
        "candidate_id": candidate.candidate_id,
        "run_id": candidate.run_id,
        "type": candidate.candidate_type.value,
        "title": candidate.title,
        "excerpt": candidate.excerpt,
        "source_ref": candidate.source_ref,
        "relevance_score": candidate.relevance_score,
        "confidence_score": candidate.confidence_score,
        "rationale": candidate.rationale,
        "review_status": candidate.review_status.value,
        "duplicate_of": candidate.duplicate_of,
        "duplicate_rationale": candidate.duplicate_rationale,
        "modification_text": candidate.modification_text,
        "approved": approved,
        "rejected": candidate.candidate_id in get_runtime().metadata.rejected_candidate_ids,
        "archived": archived,
    }


__all__ = ["approve_candidates", "create_candidates", "list_candidates", "publish_approved_candidates"]
