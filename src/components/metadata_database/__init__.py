"""Scaffold anchor for the KMS metadata database component."""

from src.components import component_registry

COMPONENT_NAME = "metadata_database"
SCAFFOLD = component_registry()[COMPONENT_NAME]

__all__ = ["COMPONENT_NAME", "SCAFFOLD"]
