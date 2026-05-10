"""Scaffold anchor for the KMS contradiction handling service component."""

from src.components import component_registry

COMPONENT_NAME = "contradiction_handling_service"
SCAFFOLD = component_registry()[COMPONENT_NAME]

__all__ = ["COMPONENT_NAME", "SCAFFOLD"]
