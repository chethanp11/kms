"""Scaffold anchor for the KMS api service component."""

from src.components import component_registry

COMPONENT_NAME = "api_service"
SCAFFOLD = component_registry()[COMPONENT_NAME]

__all__ = ["COMPONENT_NAME", "SCAFFOLD"]
