from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass
class SecretRef:
    name: str
    env_var: str


@dataclass
class RuntimeConfig:
    raw_path: str = "./raw"
    wiki_path: str = "./wiki"
    metadata_db_url: str = "sqlite:///./.kms-metadata.db"
    search_index_url: str = "http://localhost:7700"
    secret_refs: list[SecretRef] = field(
        default_factory=lambda: [
            SecretRef(name="openai", env_var="OPENAI_API_KEY"),
            SecretRef(name="github", env_var="GITHUB_TOKEN"),
        ]
    )


def load_runtime_config() -> RuntimeConfig:
    return RuntimeConfig(
        raw_path=os.getenv("KMS_RAW_PATH", "./raw"),
        wiki_path=os.getenv("KMS_WIKI_PATH", "./wiki"),
        metadata_db_url=os.getenv("KMS_METADATA_DB_URL", "sqlite:///./.kms-metadata.db"),
        search_index_url=os.getenv("KMS_SEARCH_INDEX_URL", "http://localhost:7700"),
    )
