"""Scaffold anchor for the KMS search index component."""

from src.components import component_registry

COMPONENT_NAME = "search_index"
SCAFFOLD = component_registry()[COMPONENT_NAME]

__all__ = ["COMPONENT_NAME", "SCAFFOLD"]
