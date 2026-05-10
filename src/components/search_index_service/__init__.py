"""Scaffold anchor for the KMS search index service component."""

from src.components import component_registry

COMPONENT_NAME = "search_index_service"
SCAFFOLD = component_registry()[COMPONENT_NAME]

__all__ = ["COMPONENT_NAME", "SCAFFOLD"]
