"""Scaffold anchor for the KMS kmi application component."""

from src.components import component_registry

COMPONENT_NAME = "kmi_application"
SCAFFOLD = component_registry()[COMPONENT_NAME]

__all__ = ["COMPONENT_NAME", "SCAFFOLD"]
