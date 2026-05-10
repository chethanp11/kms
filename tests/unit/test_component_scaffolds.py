"""Unit coverage for all KMS design component scaffolds."""

from __future__ import annotations

import importlib
import unittest

from src.components import COMPONENT_SCAFFOLDS, ComponentAuthority, component_registry


EXPECTED_COMPONENTS = {
    "kmi_application",
    "infopedia_application",
    "api_service",
    "run_orchestration_service",
    "source_discovery_parsing_service",
    "source_analysis_service",
    "wiki_drafting_refresh_service",
    "policy_validation_service",
    "contradiction_handling_service",
    "approval_finalization_service",
    "search_index_service",
    "infopedia_projection_refresh_service",
    "raw_source_store",
    "wiki_store",
    "metadata_database",
    "search_index",
    "artifact_storage",
}


class ComponentScaffoldTests(unittest.TestCase):
    def test_registry_covers_all_design_components(self) -> None:
        registry = component_registry()

        self.assertEqual(set(registry), EXPECTED_COMPONENTS)
        self.assertEqual(len(COMPONENT_SCAFFOLDS), len(EXPECTED_COMPONENTS))

    def test_each_component_package_exports_matching_scaffold(self) -> None:
        registry = component_registry()
        for component_name in sorted(EXPECTED_COMPONENTS):
            module = importlib.import_module(f"src.components.{component_name}")
            self.assertEqual(module.COMPONENT_NAME, component_name)
            self.assertEqual(module.SCAFFOLD, registry[component_name])

    def test_authority_boundaries_are_preserved(self) -> None:
        registry = component_registry()

        self.assertEqual(registry["wiki_store"].authority, ComponentAuthority.AUTHORITATIVE)
        self.assertEqual(registry["approval_finalization_service"].authority, ComponentAuthority.GOVERNED_WRITE_PATH)
        self.assertEqual(registry["infopedia_application"].writes, ())
        self.assertNotIn("/wiki", registry["infopedia_projection_refresh_service"].writes)
        self.assertNotIn("/wiki", registry["search_index"].writes)


if __name__ == "__main__":
    unittest.main()
