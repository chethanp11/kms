from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from kms_api.app_factory import create_app


FIXTURE_ROOT = Path("tests/fixtures/source_intake/customer-revenue").resolve()


def test_kmi_api_surfaces_governed_workflow() -> None:
    client = TestClient(create_app(seed_demo_data=False))

    create_response = client.post(
        "/api/runs",
        json={
            "source_path": str(FIXTURE_ROOT),
            "initiated_by": "knowledge-manager",
            "domain_hint": "customer-revenue",
            "run_notes": "KMI smoke test",
        },
    )
    assert create_response.status_code == 200
    created = create_response.json()

    run = created["run"]
    run_id = run["run_id"]
    assert run["status"] == "blocked"
    assert run["current_stage"] == "approval"
    assert created["revisions"]
    assert created["contradictions"]

    run_detail = client.get(f"/api/runs/{run_id}")
    assert run_detail.status_code == 200
    detail = run_detail.json()
    assert detail["run"]["run_id"] == run_id
    assert detail["source_files"]
    assert detail["source_notes"]
    assert detail["run_events"]

    artifacts = client.get(f"/api/runs/{run_id}/artifacts")
    assert artifacts.status_code == 200
    artifact_payload = artifacts.json()
    assert artifact_payload["run"]["run_id"] == run_id
    assert artifact_payload["revisions"] == detail["revisions"]

    revision_id = detail["revisions"][0]["revision_id"]
    diff_response = client.get(f"/api/reviews/{revision_id}/diff")
    assert diff_response.status_code == 200
    diff = diff_response.json()
    assert diff["revision"]["revision_id"] == revision_id
    assert diff["source_trace_ids"]
    assert diff["rule_findings"]["summary"]

    contradiction_id = detail["contradictions"][0]["contradiction_id"]
    contradiction_response = client.get(f"/api/contradictions/{contradiction_id}")
    assert contradiction_response.status_code == 200
    contradiction = contradiction_response.json()
    assert contradiction["contradiction"]["contradiction_id"] == contradiction_id
    assert contradiction["run"]["run_id"] == run_id

    approval_response = client.post(
        f"/api/approvals/{revision_id}",
        json={
            "decision": "approved",
            "reviewer_id": "knowledge-manager",
            "policy_version": "governance.v1",
            "reason": "Approved through KMI.",
            "finalize": True,
        },
    )
    assert approval_response.status_code == 200
    approval = approval_response.json()
    assert approval["finalized"] is True
    assert approval["governance"]["publish_allowed"] is True

    slug = diff["revision"]["draft_slug"]
    wiki_response = client.get(f"/api/wiki/pages/{slug}")
    assert wiki_response.status_code == 200
    wiki = wiki_response.json()
    assert wiki["page"]["slug"] == slug
    assert wiki["content"]

    wiki_search_response = client.get("/api/search", params={"q": "Net Revenue Retention", "scope": "wiki"})
    assert wiki_search_response.status_code == 200
    wiki_search = wiki_search_response.json()
    assert wiki_search["total"] >= 1
    assert any(item["slug"] == slug for item in wiki_search["items"])

    operational_search_response = client.get("/api/search", params={"q": "Run", "scope": "operational"})
    assert operational_search_response.status_code == 200
    operational_search = operational_search_response.json()
    assert operational_search["total"] >= 1
    assert any(item["page_type"] == "" or item["page_type"] == "metric" for item in operational_search["items"])

    health_response = client.get("/api/health/findings")
    assert health_response.status_code == 200
    health = health_response.json()
    assert health["summary"]["contradiction_count"] >= 1
    assert health["summary"]["lint_finding_count"] >= 0


def test_kmi_api_allows_local_dev_cors_preflight() -> None:
    client = TestClient(create_app(seed_demo_data=False))

    response = client.options(
        "/api/runs",
        headers={
            "Origin": "http://127.0.0.1:4173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code in {200, 204}
    assert response.headers.get("access-control-allow-origin") == "http://127.0.0.1:4173"
