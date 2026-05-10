"""KMS design component scaffolds.

This package contains metadata-only scaffold anchors for every major component
listed in `design/architecture.md`. Scaffolds do not grant runtime authority;
they document boundaries for later implementations.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping

from src.contracts import ValidationError


class ComponentLayer(str, Enum):
    RAW_SOURCE_INPUT = "Raw Source Input Layer"
    KNOWLEDGE_MAINTENANCE = "Knowledge Maintenance Layer"
    FINALIZED_KNOWLEDGE = "Finalized Knowledge Layer"
    KNOWLEDGE_NAVIGATION = "Knowledge Navigation Layer"
    METADATA_RUNTIME = "Metadata and Runtime Services Layer"


class ComponentAuthority(str, Enum):
    AUTHORITATIVE = "authoritative"
    GOVERNED_WRITE_PATH = "governed write path"
    SUPPORTING = "supporting"
    SUPPORTING_INPUT = "supporting input"
    SUPPORTING_PROJECTION = "supporting projection"
    READ_ONLY = "read-only"


@dataclass(frozen=True)
class ComponentScaffold:
    """Metadata-only scaffold contract for a KMS component."""

    name: str
    layer: ComponentLayer
    authority: ComponentAuthority
    responsibility: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    reads: tuple[str, ...]
    writes: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValidationError("component scaffold name is required")
        if not self.responsibility.strip():
            raise ValidationError("component scaffold responsibility is required")
        if self.authority in {ComponentAuthority.READ_ONLY, ComponentAuthority.SUPPORTING_PROJECTION} and "/wiki" in self.writes:
            raise ValidationError("read-only/projection components must not write /wiki")
        if self.layer is ComponentLayer.FINALIZED_KNOWLEDGE and self.authority is not ComponentAuthority.AUTHORITATIVE:
            raise ValidationError("finalized knowledge layer scaffold must be authoritative")


COMPONENT_SCAFFOLDS: tuple[ComponentScaffold, ...] = (
    ComponentScaffold("kmi_application", ComponentLayer.KNOWLEDGE_MAINTENANCE, ComponentAuthority.SUPPORTING, "Govern maintenance, review, contradiction handling, approval, and publication.", ("source path", "run status", "validation output", "contradictions", "proposals", "metadata state"), ("run initiation", "review actions", "approval decisions", "governed publication requests"), ("operational state",), ("workflow decisions", "approval actions")),
    ComponentScaffold("infopedia_application", ComponentLayer.KNOWLEDGE_NAVIGATION, ComponentAuthority.READ_ONLY, "Render and navigate finalized knowledge in a browse-first experience.", ("finalized /wiki content", "indexing metadata", "page structure", "search metadata"), ("read-only page views", "navigation paths", "search results"), ("/wiki", "indexes"), ()),
    ComponentScaffold("api_service", ComponentLayer.METADATA_RUNTIME, ComponentAuthority.SUPPORTING, "Provide the application-facing service boundary for KMI and Infopedia.", ("UI requests", "authentication context", "run commands", "browse requests"), ("workflow responses", "status", "page data", "search results", "metadata lookups"), ("metadata", "/wiki", "indexes"), ("metadata",)),
    ComponentScaffold("run_orchestration_service", ComponentLayer.KNOWLEDGE_MAINTENANCE, ComponentAuthority.SUPPORTING, "Coordinate the lifecycle of a maintenance run from input to publication decision.", ("source path", "existing wiki content", "policy rules", "orchestration directives"), ("run state transitions", "task dispatch", "step completion status", "failure signals"), ("raw sources", "/wiki", "metadata"), ("metadata",)),
    ComponentScaffold("source_discovery_parsing_service", ComponentLayer.KNOWLEDGE_MAINTENANCE, ComponentAuthority.SUPPORTING, "Discover source artifacts and normalize them into processable representations.", ("raw source folder contents", "source path configuration"), ("discovered files", "parsed text", "normalized source records", "extraction artifacts"), ("raw sources",), ("metadata", "artifacts")),
    ComponentScaffold("source_analysis_service", ComponentLayer.KNOWLEDGE_MAINTENANCE, ComponentAuthority.SUPPORTING, "Analyze normalized source material against current knowledge and rules.", ("parsed source content", "current /wiki pages", "rules", "validation context"), ("proposed knowledge deltas", "contradiction signals", "confidence indicators", "refresh recommendations"), ("artifacts", "/wiki", "rules"), ("metadata",)),
    ComponentScaffold("wiki_drafting_refresh_service", ComponentLayer.KNOWLEDGE_MAINTENANCE, ComponentAuthority.SUPPORTING, "Produce or update finalized markdown candidates for publication.", ("approved proposals", "structured page model", "source trace", "refresh directives"), ("candidate markdown files", "page refresh artifacts", "publication-ready outputs"), ("/wiki", "metadata", "templates"), ("staged revisions", "artifacts")),
    ComponentScaffold("policy_validation_service", ComponentLayer.METADATA_RUNTIME, ComponentAuthority.SUPPORTING, "Enforce structural, freshness, traceability, and governance rules.", ("proposals", "source trace", "page structure", "policy rules"), ("validation pass/fail", "rule violations", "review requirements"), ("rules", "metadata", "staged revisions"), ("QA reports", "validation events")),
    ComponentScaffold("contradiction_handling_service", ComponentLayer.METADATA_RUNTIME, ComponentAuthority.SUPPORTING, "Detect, classify, and retain unresolved conflicts in a visible state.", ("source conflicts", "existing knowledge", "policy constraints"), ("contradiction records", "resolution candidates", "unresolved issue states"), ("sources", "/wiki", "metadata"), ("contradiction records",)),
    ComponentScaffold("approval_finalization_service", ComponentLayer.KNOWLEDGE_MAINTENANCE, ComponentAuthority.GOVERNED_WRITE_PATH, "Apply Knowledge Manager decisions and publish approved knowledge.", ("approval actions", "reviewed proposals", "validated publication candidates"), ("finalized markdown", "publication records", "revision markers"), ("metadata", "staged revisions"), ("/wiki", "publication metadata")),
    ComponentScaffold("search_index_service", ComponentLayer.METADATA_RUNTIME, ComponentAuthority.SUPPORTING_PROJECTION, "Build and serve searchable structures for KMI and Infopedia.", ("finalized wiki content", "page metadata", "operational records"), ("search indexes", "browse indexes", "retrieval metadata"), ("/wiki", "metadata"), ("search index",)),
    ComponentScaffold("infopedia_projection_refresh_service", ComponentLayer.KNOWLEDGE_NAVIGATION, ComponentAuthority.SUPPORTING_PROJECTION, "Transform finalized wiki content into a browse-ready projection.", ("finalized markdown pages", "page relationships", "search metadata"), ("browse views", "navigation structures", "presentation metadata"), ("/wiki", "metadata", "search index"), ("projection cache",)),
    ComponentScaffold("raw_source_store", ComponentLayer.RAW_SOURCE_INPUT, ComponentAuthority.SUPPORTING_INPUT, "Store immutable upstream source inputs.", ("external exports", "documents", "notes", "extracts"), ("readable source files"), ("raw sources",), ()),
    ComponentScaffold("wiki_store", ComponentLayer.FINALIZED_KNOWLEDGE, ComponentAuthority.AUTHORITATIVE, "Persist finalized markdown knowledge.", ("approved publication outputs"), ("authoritative finalized pages"), ("/wiki",), ("/wiki",)),
    ComponentScaffold("metadata_database", ComponentLayer.METADATA_RUNTIME, ComponentAuthority.SUPPORTING, "Persist operational run state, approvals, contradictions, revisions, and QA records.", ("workflow events", "service outputs"), ("queryable operational state", "history"), ("metadata",), ("metadata",)),
    ComponentScaffold("search_index", ComponentLayer.METADATA_RUNTIME, ComponentAuthority.SUPPORTING_PROJECTION, "Support search and browse experiences over finalized knowledge and operational metadata.", ("finalized wiki content", "metadata"), ("searchable structures", "query responses"), ("/wiki", "metadata"), ("search index",)),
    ComponentScaffold("artifact_storage", ComponentLayer.METADATA_RUNTIME, ComponentAuthority.SUPPORTING, "Retain transient or derived artifacts from maintenance and analysis.", ("parsed text", "analysis outputs", "generated candidates"), ("recoverable artifacts"), ("artifacts",), ("artifacts",)),
)


def component_registry() -> Mapping[str, ComponentScaffold]:
    """Return a deterministic name-to-scaffold mapping."""

    return {component.name: component for component in COMPONENT_SCAFFOLDS}


__all__ = [
    "COMPONENT_SCAFFOLDS",
    "ComponentAuthority",
    "ComponentLayer",
    "ComponentScaffold",
    "component_registry",
]
