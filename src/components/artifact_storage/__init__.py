"""Scaffold anchor for the KMS artifact storage component."""

from src.components import component_registry

COMPONENT_NAME = "artifact_storage"
SCAFFOLD = component_registry()[COMPONENT_NAME]

__all__ = ["COMPONENT_NAME", "SCAFFOLD"]
