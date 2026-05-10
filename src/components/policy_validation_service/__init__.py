"""Scaffold anchor for the KMS policy validation service component."""

from src.components import component_registry

COMPONENT_NAME = "policy_validation_service"
SCAFFOLD = component_registry()[COMPONENT_NAME]

__all__ = ["COMPONENT_NAME", "SCAFFOLD"]
