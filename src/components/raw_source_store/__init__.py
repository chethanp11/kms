"""Scaffold anchor for the KMS raw source store component."""

from src.components import component_registry

COMPONENT_NAME = "raw_source_store"
SCAFFOLD = component_registry()[COMPONENT_NAME]

__all__ = ["COMPONENT_NAME", "SCAFFOLD"]
