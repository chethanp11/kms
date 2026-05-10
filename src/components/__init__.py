"""Foundational component model and registry for KMS.

Components describe the stable building blocks future services and UI/API
adapters depend on. They are metadata contracts, not executable permission
bypasses: write authority still comes from KMS governance boundaries.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Mapping

from src.contracts import ValidationError


class ComponentLayer(str, Enum):
    RAW_SOURCE = "raw_source_input"
    KNOWLEDGE_MAINTENANCE = "knowledge_maintenance"
    FINALIZED_KNOWLEDGE = "finalized_knowledge"
    KNOWLEDGE_NAVIGATION = "knowledge_navigation"
    METADATA_RUNTIME = "metadata_runtime_services"


class ComponentAuthority(str, Enum):
    AUTHORITATIVE = "authoritative"
    GOVERNED_WRITE_PATH = "governed_write_path"
    SUPPORTING = "supporting"
    DERIVED_PROJECTION = "derived_projection"
    READ_ONLY = "read_only"
    UPSTREAM_INPUT = "upstream_input"


@dataclass(frozen=True)
class ComponentSpec:
    """Design-aligned description of a KMS component."""

    name: str
    layer: ComponentLayer
    authority: ComponentAuthority
    responsibility: str
    inputs: tuple[str, ...] = ()
    outputs: tuple[str, ...] = ()
    reads: tuple[str, ...] = ()
    writes: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValidationError("component name is required")
        if not self.responsibility.strip():
            raise ValidationError("component responsibility is required")
        if self.authority in {ComponentAuthority.READ_ONLY, ComponentAuthority.DERIVED_PROJECTION} and "/wiki" in self.writes:
            raise ValidationError("read-only or derived components must not write /wiki")
        if self.layer is ComponentLayer.FINALIZED_KNOWLEDGE and self.authority is not ComponentAuthority.AUTHORITATIVE:
            raise ValidationError("finalized knowledge components must be authoritative")


class ComponentRegistry:
    """Deterministic registry used to assemble future components safely."""

    def __init__(self, specs: Iterable[ComponentSpec] = ()) -> None:
        self._specs: dict[str, ComponentSpec] = {}
        for spec in specs:
            self.register(spec)

    def register(self, spec: ComponentSpec) -> None:
        if spec.name in self._specs:
            raise ValidationError(f"duplicate component: {spec.name}")
        missing = [dependency for dependency in spec.dependencies if dependency not in self._specs]
        if missing:
            raise ValidationError(f"component {spec.name} has missing dependencies: {', '.join(missing)}")
        self._specs[spec.name] = spec

    def get(self, name: str) -> ComponentSpec:
        try:
            return self._specs[name]
        except KeyError as exc:
            raise ValidationError(f"unknown component: {name}") from exc

    def by_layer(self, layer: ComponentLayer) -> tuple[ComponentSpec, ...]:
        return tuple(spec for spec in self._specs.values() if spec.layer is layer)

    def names(self) -> tuple[str, ...]:
        return tuple(self._specs)

    def as_mapping(self) -> Mapping[str, ComponentSpec]:
        return dict(self._specs)


BASE_COMPONENT_SPECS: tuple[ComponentSpec, ...] = (
    ComponentSpec(
        name="raw-source-store",
        layer=ComponentLayer.RAW_SOURCE,
        authority=ComponentAuthority.UPSTREAM_INPUT,
        responsibility="Expose immutable upstream source files for governed intake.",
        outputs=("source files",),
        reads=("external source folder",),
    ),
    ComponentSpec(
        name="metadata-store",
        layer=ComponentLayer.METADATA_RUNTIME,
        authority=ComponentAuthority.SUPPORTING,
        responsibility="Persist operational run, approval, contradiction, validation, and projection metadata.",
        inputs=("workflow events",),
        outputs=("operational state",),
        reads=("metadata",),
        writes=("metadata",),
    ),
    ComponentSpec(
        name="wiki-store",
        layer=ComponentLayer.FINALIZED_KNOWLEDGE,
        authority=ComponentAuthority.AUTHORITATIVE,
        responsibility="Persist finalized markdown knowledge as the canonical truth substrate.",
        inputs=("approved markdown",),
        outputs=("finalized wiki pages",),
        reads=("/wiki",),
        writes=("/wiki",),
    ),
    ComponentSpec(
        name="policy-gate",
        layer=ComponentLayer.METADATA_RUNTIME,
        authority=ComponentAuthority.SUPPORTING,
        responsibility="Evaluate validation and governance rules before publication.",
        inputs=("candidate revisions", "rules"),
        outputs=("QA reports", "block or pass decisions"),
        reads=("metadata", "rules"),
        writes=("metadata",),
        dependencies=("metadata-store",),
    ),
    ComponentSpec(
        name="publisher",
        layer=ComponentLayer.KNOWLEDGE_MAINTENANCE,
        authority=ComponentAuthority.GOVERNED_WRITE_PATH,
        responsibility="Write approved and validated knowledge into /wiki through the governed publication path.",
        inputs=("approved revisions", "QA reports"),
        outputs=("published markdown", "publish summary"),
        reads=("metadata",),
        writes=("/wiki", "metadata"),
        dependencies=("metadata-store", "wiki-store", "policy-gate"),
    ),
    ComponentSpec(
        name="infopedia-projection",
        layer=ComponentLayer.KNOWLEDGE_NAVIGATION,
        authority=ComponentAuthority.DERIVED_PROJECTION,
        responsibility="Build read-only browse structures from finalized wiki content.",
        inputs=("finalized wiki pages",),
        outputs=("navigation nodes",),
        reads=("/wiki", "metadata"),
        writes=("projection",),
        dependencies=("wiki-store", "metadata-store"),
    ),
)


def build_base_registry() -> ComponentRegistry:
    return ComponentRegistry(BASE_COMPONENT_SPECS)


__all__ = [
    "BASE_COMPONENT_SPECS",
    "ComponentAuthority",
    "ComponentLayer",
    "ComponentRegistry",
    "ComponentSpec",
    "build_base_registry",
]
