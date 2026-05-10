"""Unit coverage for foundational KMS component primitives."""

from __future__ import annotations

import unittest

from src.components import ComponentAuthority, ComponentLayer, ComponentRegistry, ComponentSpec, build_base_registry
from src.contracts import ApprovalDecision, ApprovalRecord, KnowledgePage, MaintenanceRun, ValidationError
from src.governance import validate_page_candidate
from src.ports import MetadataRepository, ProjectionRepository, WikiRepository
from src.storage import InMemoryMetadataStore, InMemoryProjectionStore, InMemoryWikiStore


class ComponentRegistryTests(unittest.TestCase):
    def test_base_registry_contains_authority_components(self) -> None:
        registry = build_base_registry()

        self.assertEqual(registry.get("wiki-store").authority, ComponentAuthority.AUTHORITATIVE)
        self.assertEqual(registry.get("publisher").authority, ComponentAuthority.GOVERNED_WRITE_PATH)
        self.assertEqual(registry.get("infopedia-projection").authority, ComponentAuthority.DERIVED_PROJECTION)
        self.assertIn("policy-gate", registry.names())

    def test_registry_rejects_duplicate_or_missing_dependencies(self) -> None:
        spec = ComponentSpec(
            name="custom",
            layer=ComponentLayer.METADATA_RUNTIME,
            authority=ComponentAuthority.SUPPORTING,
            responsibility="custom support component",
        )
        registry = ComponentRegistry([spec])

        with self.assertRaises(ValidationError):
            registry.register(spec)

        with self.assertRaises(ValidationError):
            registry.register(
                ComponentSpec(
                    name="dependent",
                    layer=ComponentLayer.METADATA_RUNTIME,
                    authority=ComponentAuthority.SUPPORTING,
                    responsibility="dependent support component",
                    dependencies=("missing",),
                )
            )

    def test_read_only_or_projection_components_cannot_write_wiki(self) -> None:
        with self.assertRaises(ValidationError):
            ComponentSpec(
                name="bad-projection",
                layer=ComponentLayer.KNOWLEDGE_NAVIGATION,
                authority=ComponentAuthority.DERIVED_PROJECTION,
                responsibility="bad projection",
                writes=("/wiki",),
            )


class FoundationalStoreTests(unittest.TestCase):
    def test_in_memory_stores_satisfy_ports(self) -> None:
        self.assertIsInstance(InMemoryMetadataStore(), MetadataRepository)
        self.assertIsInstance(InMemoryWikiStore(), WikiRepository)
        self.assertIsInstance(InMemoryProjectionStore(), ProjectionRepository)

    def test_metadata_store_persists_run_and_approval_evidence(self) -> None:
        store = InMemoryMetadataStore()
        run = MaintenanceRun(run_id="run-1", source_path="/raw/source")
        approval = ApprovalRecord("approval-1", "revision-1", ApprovalDecision.APPROVED, "manager")

        store.save_run(run)
        store.save_approval(approval)

        self.assertEqual(store.get_run("run-1"), run)
        self.assertEqual(store.approvals["approval-1"], approval)

    def test_wiki_store_requires_approval_and_passing_qa(self) -> None:
        store = InMemoryWikiStore()
        page = KnowledgePage(
            page_type="metric",
            path="metrics/revenue.md",
            title="Revenue",
            body="## Summary\nRevenue.\n\n## Source Trace\n- source.md",
        )
        qa_report = validate_page_candidate(page)

        with self.assertRaises(ValidationError):
            store.write_page(page, approved=False, qa_report=qa_report)

        store.write_page(page, approved=True, qa_report=qa_report)

        self.assertEqual(store.read_page("metrics/revenue.md"), page)

    def test_projection_store_is_rebuildable_from_wiki_pages(self) -> None:
        projection = InMemoryProjectionStore()
        pages = (
            KnowledgePage("metric", "metrics/revenue.md", "Revenue", "## Source Trace\n- a"),
            KnowledgePage("process", "process/monthly-close.md", "Monthly Close", "## Source Trace\n- b"),
        )

        projection.rebuild_from_wiki(pages)
        projection.rebuild_from_wiki(tuple(reversed(pages)))

        self.assertEqual(list(projection.nodes), ["metrics/revenue.md", "process/monthly-close.md"])
        self.assertEqual(projection.nodes["metrics/revenue.md"], "Revenue")


if __name__ == "__main__":
    unittest.main()
