"""Scaffold anchor for the KMS source discovery parsing service component."""

from src.components import component_registry

COMPONENT_NAME = "source_discovery_parsing_service"
SCAFFOLD = component_registry()[COMPONENT_NAME]

__all__ = ["COMPONENT_NAME", "SCAFFOLD"]
