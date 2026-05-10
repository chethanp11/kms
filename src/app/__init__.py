"""Application-facing API contract scaffold."""

from __future__ import annotations

REPRESENTATIVE_ENDPOINTS: tuple[tuple[str, str], ...] = (
    ("POST", "/api/runs"),
    ("GET", "/api/runs/{run_id}"),
    ("GET", "/api/runs/{run_id}/artifacts"),
    ("GET", "/api/reviews/{revision_id}/diff"),
    ("POST", "/api/approvals/{revision_id}"),
    ("GET", "/api/wiki/pages/{slug}"),
    ("GET", "/api/infopedia/tree"),
    ("GET", "/api/infopedia/search"),
    ("GET", "/api/contradictions/{id}"),
    ("GET", "/api/health/findings"),
)

__all__ = ["REPRESENTATIVE_ENDPOINTS"]
