"""Scaffold anchor for the KMS wiki store component."""

from src.components import component_registry

COMPONENT_NAME = "wiki_store"
SCAFFOLD = component_registry()[COMPONENT_NAME]

__all__ = ["COMPONENT_NAME", "SCAFFOLD"]
