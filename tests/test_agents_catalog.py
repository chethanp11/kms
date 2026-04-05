from __future__ import annotations

from kms_api.orchestration.catalog import load_orchestration_catalog


def test_agent_and_skill_catalog_matches_design_tree() -> None:
    catalog = load_orchestration_catalog()

    assert sorted(catalog.agents) == [
        "contradiction_review",
        "lint",
        "orchestration",
        "policy_qa",
        "publisher",
        "source_analysis",
        "source_intake",
        "wiki_curator",
        "wiki_impact",
    ]
    assert sorted(catalog.skills) == [
        "contradiction-resolution",
        "infopedia-index-refresh",
        "source-intake",
        "source-summarization",
        "vault-lint",
        "wiki-impact-analysis",
        "wiki-refresh",
    ]
    assert catalog.agents["source_intake"].skill_name == "source-intake"
    assert catalog.agents["publisher"].skill_name is None
    assert catalog.skills["infopedia-index-refresh"].purpose == "refresh navigation and search projections"
    assert catalog.agent_specs()["approval"].agent_name == "Orchestrator Agent"
