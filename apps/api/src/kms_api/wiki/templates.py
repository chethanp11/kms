from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11 compatibility
    import tomli as tomllib

from .conventions import CANONICAL_PAGE_TYPES
from .models import WikiPageBlueprint, SectionValue

PLACEHOLDER_PATTERN = re.compile(r"\{\{([^{}]+)\}\}")


@dataclass(frozen=True)
class TemplateCatalog:
    templates_root: Path
    frontmatter_order: tuple[str, ...]
    blueprints: dict[str, WikiPageBlueprint]

    @classmethod
    def load(cls, templates_root: Path) -> "TemplateCatalog":
        manifest_path = templates_root / "blueprints.toml"
        manifest = tomllib.loads(manifest_path.read_text(encoding="utf-8"))
        frontmatter_order = tuple(manifest["common"]["frontmatter_order"])
        blueprints: dict[str, WikiPageBlueprint] = {}
        for page_type in CANONICAL_PAGE_TYPES:
            page_manifest = manifest["pages"][page_type]
            blueprints[page_type] = WikiPageBlueprint(
                page_type=page_type,
                folder=page_manifest["folder"],
                template_file=page_manifest["template_file"],
                body_sections=tuple(page_manifest["body_sections"]),
            )
        return cls(templates_root=templates_root, frontmatter_order=frontmatter_order, blueprints=blueprints)

    def blueprint_for(self, page_type: str) -> WikiPageBlueprint:
        try:
            return self.blueprints[page_type]
        except KeyError as exc:
            raise ValueError(f"Unsupported wiki page type: {page_type}") from exc

    def template_text(self, page_type: str) -> str:
        blueprint = self.blueprint_for(page_type)
        return (self.templates_root / blueprint.template_file).read_text(encoding="utf-8")


def render_section(value: SectionValue | None) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "\n".join(f"- {item}" for item in value)
    return value


def render_frontmatter(
    frontmatter_order: tuple[str, ...],
    frontmatter: dict[str, Any],
) -> str:
    lines: list[str] = ["---"]
    for field_name in frontmatter_order:
        value = frontmatter[field_name]
        if isinstance(value, bool):
            lines.append(f"{field_name}: {'true' if value else 'false'}")
            continue
        if isinstance(value, list):
            lines.append(f"{field_name}:")
            for item in value:
                lines.append(f"  - {item}")
            continue
        lines.append(f"{field_name}: {value}")
    lines.append("---")
    return "\n".join(lines)


def render_template(
    template_text: str,
    context: dict[str, str],
    section_content: dict[str, SectionValue],
) -> str:
    def replace(match: re.Match[str]) -> str:
        token = match.group(1).strip()
        if token.startswith("section:"):
            section_name = token.split(":", 1)[1]
            return render_section(section_content.get(section_name))
        return context.get(token, "")

    return PLACEHOLDER_PATTERN.sub(replace, template_text)
