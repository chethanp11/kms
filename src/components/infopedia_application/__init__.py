"""Scaffold anchor for the KMS infopedia application component."""

from src.components import component_registry

COMPONENT_NAME = "infopedia_application"
SCAFFOLD = component_registry()[COMPONENT_NAME]

__all__ = ["COMPONENT_NAME", "SCAFFOLD"]
