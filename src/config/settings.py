"""Runtime settings for the stdlib KMS application slice."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import os


@dataclass(frozen=True)
class KMSSettings:
    raw_root: Path
    wiki_root: Path
    artifact_root: Path
    metadata_path: Path | None = None
    policy_version: str = "policy.example.v1"
    ai_enabled: bool = False
    ai_model: str = "gpt-4o"
    ai_timeout_seconds: float = 30.0
    openai_api_key: str = field(default="", repr=False)
    allow_auto_approve: bool = False

    @classmethod
    def from_env(cls) -> "KMSSettings":
        env = _merged_local_env()
        base = Path(env.get("KMS_DATA_ROOT", "data-storage")).expanduser().resolve()
        api_key = env.get("OPEN_AI_KEY", "")
        enabled_value = env.get("KMS_AI_ENABLED")
        ai_enabled = _env_bool(enabled_value, default=bool(api_key))
        return cls(
            raw_root=Path(env.get("KMS_RAW_ROOT", str(base / "raw"))).expanduser().resolve(),
            wiki_root=Path(env.get("KMS_WIKI_ROOT", str(base / "wiki"))).expanduser().resolve(),
            artifact_root=Path(env.get("KMS_ARTIFACT_ROOT", str(base / "artifacts"))).expanduser().resolve(),
            metadata_path=Path(env["KMS_METADATA_PATH"]).expanduser().resolve() if "KMS_METADATA_PATH" in env else None,
            ai_enabled=ai_enabled,
            ai_model=env.get("KMS_AI_MODEL", "gpt-4o"),
            ai_timeout_seconds=float(env.get("KMS_AI_TIMEOUT_SECONDS", "30")),
            openai_api_key=api_key,
            allow_auto_approve=_env_bool(env.get("KMS_ALLOW_AUTO_APPROVE"), default=False),
        )

    def ensure_directories(self) -> None:
        self.raw_root.mkdir(parents=True, exist_ok=True)
        self.wiki_root.mkdir(parents=True, exist_ok=True)
        self.artifact_root.mkdir(parents=True, exist_ok=True)


def default_settings() -> KMSSettings:
    return KMSSettings.from_env()


def _merged_local_env() -> dict[str, str]:
    values = dict(os.environ)
    for path in (Path(".env"), Path("config/.env")):
        if path.exists():
            for key, value in _read_env_file(path).items():
                values.setdefault(key, value)
    return values


def _read_env_file(path: Path) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            parsed[key] = value
    return parsed


def _env_bool(value: str | None, *, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().casefold() in {"1", "true", "yes", "on"}


__all__ = ["KMSSettings", "default_settings"]
