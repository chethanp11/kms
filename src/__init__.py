"""KMS implementation scaffold.

The package exposes early, deterministic contracts for the governed knowledge
maintenance system described in `design/`.
"""

from src.components import ComponentRegistry, ComponentSpec, build_base_registry
from src.contracts import KnowledgePage, SourceFile, ValidationError

__all__ = [
    "ComponentRegistry",
    "ComponentSpec",
    "KnowledgePage",
    "SourceFile",
    "ValidationError",
    "build_base_registry",
]
