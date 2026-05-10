"""KMS implementation scaffold.

The package exposes early, deterministic contracts for the governed knowledge
maintenance system described in `design/`.
"""

from src.contracts import KnowledgePage, SourceFile, ValidationError

__all__ = ["KnowledgePage", "SourceFile", "ValidationError"]
