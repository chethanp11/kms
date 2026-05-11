"""Wiki read API routes."""
from __future__ import annotations
from src.api.dependencies import get_runtime
def get_page(slug: str) -> dict[str, str]:
    return {"slug": slug, "markdown": get_runtime().wiki.read_page(slug)}
__all__ = ["get_page"]
