"""Scaffold anchor for the KMS run orchestration service component."""

from src.components import component_registry

COMPONENT_NAME = "run_orchestration_service"
SCAFFOLD = component_registry()[COMPONENT_NAME]

__all__ = ["COMPONENT_NAME", "SCAFFOLD"]
