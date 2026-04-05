from __future__ import annotations

from pathlib import Path

from kms_api.db.metadata_store import InMemoryMetadataStore
from kms_api.orchestration import OrchestrationRequest, RunOrchestrationService


FIXTURE_ROOT = Path("tests/fixtures/source_intake/customer-revenue").resolve()


def test_orchestration_blocks_without_approval(tmp_path: Path) -> None:
    store = InMemoryMetadataStore()
    service = RunOrchestrationService(
        store,
        wiki_root=tmp_path / "wiki",
        timestamp_provider=lambda: "2026-04-05T09:12:44Z",
    )

    result = service.orchestrate(
        OrchestrationRequest(
            source_root_path=str(FIXTURE_ROOT),
            initiated_by="knowledge-manager",
            domain_hint="customer-revenue",
            run_notes="monthly refresh",
        )
    )

    assert result.run_status == "blocked"
    assert result.blocked_reason == "Approval required before finalization."
    assert result.run_id
    assert result.current_stage == "approval"
    assert not (tmp_path / "wiki").exists()

    run_events = store.list_run_events(result.run_id)
    assert run_events[0].kind == "run_created"
    assert run_events[-1].kind == "stage_blocked"
    assert any(event.stage == "contradiction_review" for event in run_events)
    assert any(event.stage == "policy_qa" for event in run_events)
    assert any(event.stage == "wiki_impact" for event in run_events)

    executions = store.list_agent_executions(result.run_id)
    assert [execution.agent_name for execution in executions[:4]] == [
        "Source Intake Agent",
        "Source Analyst Agent",
        "Wiki Impact Analyst",
        "Wiki Curator",
    ]
    assert any(execution.agent_name == "Policy QA Agent" for execution in executions)


def test_orchestration_can_publish_after_approval(tmp_path: Path) -> None:
    store = InMemoryMetadataStore()
    service = RunOrchestrationService(
        store,
        wiki_root=tmp_path / "wiki",
        timestamp_provider=lambda: "2026-04-05T09:12:44Z",
    )

    result = service.orchestrate(
        OrchestrationRequest(
            source_root_path=str(FIXTURE_ROOT),
            initiated_by="knowledge-manager",
            domain_hint="customer-revenue",
            run_notes="monthly refresh",
            approval_decision="approved",
            approval_reviewer_id="knowledge-manager",
            approval_reason="Ready to finalize governed open questions.",
        )
    )

    assert result.run_status == "completed"
    assert result.current_stage == "completed"
    assert result.blocked_reason is None
    assert len(result.revision_ids) == 3
    assert result.lint_finding_ids == []

    wiki_root = tmp_path / "wiki"
    assert wiki_root.exists()
    assert len(list(wiki_root.rglob("*.md"))) == 3
    published_pages = store.list_wiki_pages()
    assert len(published_pages) == 3
    assert all(page.status == "finalized" for page in published_pages)

    run_events = store.list_run_events(result.run_id)
    assert run_events[-1].kind == "run_completed"
    assert any(event.stage == "publisher" for event in run_events)
    assert any(event.stage == "lint" for event in run_events)

    approvals = store.list_approvals()
    assert len(approvals) == 3
    assert all(approval.decision == "approved" for approval in approvals)

    contradictions = store.list_contradictions(run_id=result.run_id)
    assert len(contradictions) == 3
    assert all(record.severity == "warning" for record in contradictions)
    assert all(record.status in {"reviewing", "open"} for record in contradictions)
