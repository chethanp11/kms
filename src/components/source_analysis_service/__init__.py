"""Scaffold anchor for the KMS source analysis service component."""

from src.components import component_registry

COMPONENT_NAME = "source_analysis_service"
SCAFFOLD = component_registry()[COMPONENT_NAME]

__all__ = ["COMPONENT_NAME", "SCAFFOLD"]
