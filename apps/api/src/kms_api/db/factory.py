from __future__ import annotations

from pathlib import Path

from kms_config import RuntimeConfig
from kms_domain import MetadataStore

from .metadata_store import InMemoryMetadataStore
from .sqlite_metadata_store import SQLiteMetadataStore


def create_metadata_store(runtime_config: RuntimeConfig | None = None, *, use_memory: bool = False) -> MetadataStore:
    if use_memory:
        return InMemoryMetadataStore()
    config = runtime_config or RuntimeConfig()
    metadata_db_url = config.metadata_db_url.strip()
    if metadata_db_url.startswith("sqlite:///"):
        db_path = metadata_db_url[len("sqlite:///") :]
        if db_path == ":memory:":
            return SQLiteMetadataStore(Path(":memory:"))
        return SQLiteMetadataStore(Path(db_path))
    raise ValueError(
        "Unsupported metadata_db_url scheme. Supported local backend: sqlite:///path/to/db.sqlite3"
    )
