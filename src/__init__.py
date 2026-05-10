"""KMS implementation scaffold.

The package exposes early, deterministic contracts for the governed knowledge
maintenance system described in `design/`.
"""

from src.components import COMPONENT_SCAFFOLDS, ComponentScaffold, component_registry
from src.contracts import KnowledgePage, SourceFile, ValidationError

__all__ = [
    "COMPONENT_SCAFFOLDS",
    "ComponentScaffold",
    "KnowledgePage",
    "SourceFile",
    "ValidationError",
    "component_registry",
]
