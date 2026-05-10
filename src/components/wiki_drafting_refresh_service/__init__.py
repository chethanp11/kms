"""Scaffold anchor for the KMS wiki drafting refresh service component."""

from src.components import component_registry

COMPONENT_NAME = "wiki_drafting_refresh_service"
SCAFFOLD = component_registry()[COMPONENT_NAME]

__all__ = ["COMPONENT_NAME", "SCAFFOLD"]
