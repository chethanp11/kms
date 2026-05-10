"""Scaffold anchor for the KMS approval finalization service component."""

from src.components import component_registry

COMPONENT_NAME = "approval_finalization_service"
SCAFFOLD = component_registry()[COMPONENT_NAME]

__all__ = ["COMPONENT_NAME", "SCAFFOLD"]
