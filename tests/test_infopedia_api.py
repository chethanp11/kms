from __future__ import annotations

from fastapi.testclient import TestClient

from kms_api.app_factory import create_app


def test_infopedia_tree_search_and_page_are_read_only() -> None:
    client = TestClient(create_app(seed_demo_data=True))

    tree_response = client.get("/api/infopedia/tree")
    assert tree_response.status_code == 200
    tree = tree_response.json()
    assert tree["summary"]["page_count"] >= 1
    assert tree["domains"]
    assert any(domain["count"] >= 1 for domain in tree["domains"])

    search_response = client.get("/api/infopedia/search", params={"q": "Net Revenue Retention"})
    assert search_response.status_code == 200
    search = search_response.json()
    assert search["total"] >= 1
    assert search["items"]
    assert search["facets"]["page_types"]

    metric_item = next(item for item in search["items"] if item["page_type"] == "metric")
    page_response = client.get(f"/api/infopedia/pages/{metric_item['slug']}")
    assert page_response.status_code == 200
    page = page_response.json()
    assert page["page"]["slug"] == metric_item["slug"]
    assert page["page"]["status"] == "finalized"
    assert page["content_markdown"]
    assert isinstance(page["related_pages"], list)
    assert isinstance(page["backlinks"], list)
    assert isinstance(page["source_trace_summary"], list)
    assert page["breadcrumbs"][0]["title"] == "Infopedia"

    filtered_search = client.get(
        "/api/infopedia/search",
        params={"page_type": "metric", "status": "finalized", "freshness": "current"},
    )
    assert filtered_search.status_code == 200
    filtered = filtered_search.json()
    assert all(item["page_type"] == "metric" for item in filtered["items"])
    assert all(item["status"] == "finalized" for item in filtered["items"])
