"""Scaffold anchor for the KMS infopedia projection refresh service component."""

from src.components import component_registry

COMPONENT_NAME = "infopedia_projection_refresh_service"
SCAFFOLD = component_registry()[COMPONENT_NAME]

__all__ = ["COMPONENT_NAME", "SCAFFOLD"]
