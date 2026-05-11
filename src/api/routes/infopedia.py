"""Infopedia read-only API routes."""
from __future__ import annotations
from src.api.dependencies import get_runtime
from src.services.infopedia_projection import build_tree
def tree() -> list[dict[str, object]]:
    return [node.__dict__ for node in build_tree(get_runtime().wiki)]
def search(query: str) -> list[dict[str, object]]:
    return [doc.__dict__ for doc in get_runtime().search.search(query)]
__all__ = ["search", "tree"]
