from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from .agents import AgentSpec


@dataclass(frozen=True)
class AgentDefinition:
    key: str
    title: str
    stage: str
    skill_name: str | None
    file_path: Path
    boundaries: list[str]
    inputs: list[str]
    outputs: list[str]
    forbidden_actions: list[str]

    def to_spec(self) -> AgentSpec:
        return AgentSpec(
            agent_name=self.title,
            skill_name=self.skill_name,
            stage=self.stage,
        )


@dataclass(frozen=True)
class SkillDefinition:
    name: str
    file_path: Path
    purpose: str
    used_by: list[str]
    hard_rules: list[str]


@dataclass(frozen=True)
class AgentCatalog:
    repo_root: Path
    agents: dict[str, AgentDefinition]
    skills: dict[str, SkillDefinition]

    def agent_specs(self) -> dict[str, AgentSpec]:
        specs = {definition.stage: definition.to_spec() for definition in self.agents.values()}
        if "orchestration" in specs and "approval" not in specs:
            specs["approval"] = specs["orchestration"]
        return specs


def load_orchestration_catalog(repo_root: Path | None = None) -> AgentCatalog:
    root = repo_root or _find_repo_root()
    agents_dir = root / "agents" / "agents"
    skills_dir = root / "agents" / "skills"

    agents: dict[str, AgentDefinition] = {}
    for file_path in sorted(agents_dir.glob("*.md")):
        payload = _read_frontmatter(file_path)
        definition = AgentDefinition(
            key=file_path.stem,
            title=str(payload["title"]),
            stage=str(payload["stage"]),
            skill_name=_optional_str(payload.get("skill")),
            file_path=file_path,
            boundaries=list(payload.get("boundaries", [])),
            inputs=list(payload.get("inputs", [])),
            outputs=list(payload.get("outputs", [])),
            forbidden_actions=list(payload.get("forbidden_actions", [])),
        )
        agents[definition.stage] = definition

    skills: dict[str, SkillDefinition] = {}
    for file_path in sorted(skills_dir.glob("*/SKILL.md")):
        payload = _read_frontmatter(file_path)
        definition = SkillDefinition(
            name=str(payload["name"]),
            file_path=file_path,
            purpose=str(payload["purpose"]),
            used_by=list(payload.get("used_by", [])),
            hard_rules=list(payload.get("hard_rules", [])),
        )
        skills[definition.name] = definition

    return AgentCatalog(repo_root=root, agents=agents, skills=skills)


def _find_repo_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "agents" / "AGENTS.md").exists():
            return candidate
    raise FileNotFoundError("Could not locate repository root from orchestration catalog")


def _read_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8").lstrip()
    if not text.startswith("---\n"):
        raise ValueError(f"Missing YAML frontmatter in {path}")
    _, frontmatter, _ = text.split("---\n", 2)
    return yaml.safe_load(frontmatter) or {}


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
