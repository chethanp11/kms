"""Runtime settings for the stdlib KMS application slice."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os


@dataclass(frozen=True)
class KMSSettings:
    raw_root: Path
    wiki_root: Path
    artifact_root: Path
    metadata_path: Path | None = None
    policy_version: str = "policy.example.v1"

    @classmethod
    def from_env(cls) -> "KMSSettings":
        base = Path(os.environ.get("KMS_DATA_ROOT", ".kms-data")).expanduser().resolve()
        return cls(
            raw_root=Path(os.environ.get("KMS_RAW_ROOT", base / "raw")).expanduser().resolve(),
            wiki_root=Path(os.environ.get("KMS_WIKI_ROOT", base / "wiki")).expanduser().resolve(),
            artifact_root=Path(os.environ.get("KMS_ARTIFACT_ROOT", base / "artifacts")).expanduser().resolve(),
            metadata_path=Path(os.environ["KMS_METADATA_PATH"]).expanduser().resolve() if "KMS_METADATA_PATH" in os.environ else None,
        )

    def ensure_directories(self) -> None:
        self.raw_root.mkdir(parents=True, exist_ok=True)
        self.wiki_root.mkdir(parents=True, exist_ok=True)
        self.artifact_root.mkdir(parents=True, exist_ok=True)


def default_settings() -> KMSSettings:
    return KMSSettings.from_env()


__all__ = ["KMSSettings", "default_settings"]
