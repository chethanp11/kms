from __future__ import annotations

from pathlib import Path

import pytest

from kms_config import RuntimeConfig
from kms_domain import Run

from kms_api.db.factory import create_metadata_store


def test_sqlite_metadata_store_persists_between_instances(tmp_path: Path) -> None:
    db_path = tmp_path / "metadata.db"
    config = RuntimeConfig(
        raw_path=str(tmp_path / "raw"),
        wiki_path=str(tmp_path / "wiki"),
        metadata_db_url=f"sqlite:///{db_path}",
        search_index_url="http://localhost:7700",
    )

    store = create_metadata_store(config)
    store.create_run(
        Run(
            run_id="run_1",
            status="created",
            source_path="/tmp/source",
            created_at="2026-04-05T09:12:44Z",
            created_by="tester",
            current_stage="source_intake",
        )
    )

    reopened = create_metadata_store(config)
    run = reopened.get_run("run_1")
    assert run is not None
    assert run.source_path == "/tmp/source"
    assert run.current_stage == "source_intake"


def test_metadata_store_factory_rejects_unsupported_urls() -> None:
    config = RuntimeConfig(metadata_db_url="postgresql://localhost:5432/kms")

    with pytest.raises(ValueError, match="Unsupported metadata_db_url scheme"):
        create_metadata_store(config)
