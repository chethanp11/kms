#!/usr/bin/env python3
"""Validate the repository's Codex-native support contract.

This script intentionally uses only the Python standard library so it can run
before project runtime dependencies exist.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[2]
GENERIC_UPPERCASE_TERMS = {
    "AGENTS",
    "API",
    "CLI",
    "CRUD",
    "DEV",
    "HITL",
    "HTTP",
    "JSON",
    "README",
    "REQ",
    "REST",
    "SQL",
    "TEST",
    "TOML",
    "UI",
    "UTF",
    "YAML",
}

REQUIRED_FILES = [
    "AGENTS.md",
    ".devmode/mode.yaml",
    ".devmode/app.md",
    ".devmode/framework.md",
    ".codex/README.md",
    ".codex/project-context.md",
    ".codex/dev_workflow/README.md",
    ".codex/dev_workflow/00-create-intent.md",
    ".codex/dev_workflow/01-read-intent.md",
    ".codex/dev_workflow/02-create-plan.md",
    ".codex/dev_workflow/03-update-design.md",
    ".codex/dev_workflow/04-update-tests.md",
    ".codex/dev_workflow/05-implement-code.md",
    ".codex/dev_workflow/06-run-validation.md",
    ".codex/dev_workflow/07-fix-failures.md",
    ".codex/dev_workflow/08-update-logs.md",
    ".codex/dev_workflow/09-detect-gaps.md",
    ".codex/dev_workflow/10-iteration-review.md",
    ".codex/tech-stack.md",
    ".codex/agents/README.md",
    ".codex/orchestration/README.md",
    ".codex/context/README.md",
    ".codex/memory/README.md",
    ".codex/rules/README.md",
    ".codex/prompts/README.md",
    ".codex/tools/README.md",
    ".codex/tools/appflow_run.py",
    ".codex/tools/bootstrap_appflow.py",
    ".codex/tools/validate_codex_contract.py",
    ".codex/state/README.md",
    ".codex/state/appflow-closeout-checklist.md",
]

REQUIRED_DIRS = [
    ".devmode",
    ".codex/agents",
    ".codex/dev_workflow",
    ".codex/skills",
    ".codex/orchestration",
    ".codex/context",
    ".codex/memory",
    ".codex/rules",
    ".codex/prompts",
    ".codex/tools",
    ".codex/state",
]

RETIRED_REFERENCES = [
    "dev_log/change-log",
    "dev_log/decision-log",
    "dev_log/deviations-log",
    "dev_log/feedback-log",
    "dev_log/issue-log",
    "dev_log/validation-log",
    "dev_log/backlog",
    "dev_log/iteration-log",
    "dev_log/version-status",
    "dev_log/release-notes",
]

SKILL_FRONTMATTER = re.compile(
    r"^---\nname:\s*(?P<name>[a-z0-9-]+)\ndescription:\s*(?P<description>.+?)\n---",
    re.DOTALL,
)


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    sys.exit(1)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        fail(f"{path.relative_to(ROOT)} is not valid UTF-8: {exc}")


def require_files() -> None:
    for rel in REQUIRED_FILES:
        path = ROOT / rel
        if not path.is_file():
            fail(f"missing required file: {rel}")
        if not read_text(path).strip():
            fail(f"required file is empty: {rel}")


def require_dirs() -> None:
    for rel in REQUIRED_DIRS:
        path = ROOT / rel
        if not path.is_dir():
            fail(f"missing required directory: {rel}")


def validate_skills() -> None:
    skills_dir = ROOT / ".codex" / "skills"
    skill_files = sorted(skills_dir.glob("*/SKILL.md"))
    if not skill_files:
        fail("no .codex skills found")

    for skill_file in skill_files:
        text = read_text(skill_file)
        match = SKILL_FRONTMATTER.search(text)
        if not match:
            fail(f"skill missing required frontmatter: {skill_file.relative_to(ROOT)}")
        folder_name = skill_file.parent.name
        if match.group("name") != folder_name:
            fail(
                "skill frontmatter name does not match folder: "
                f"{skill_file.relative_to(ROOT)}"
            )
        if len(match.group("description").strip()) < 20:
            fail(f"skill description too short: {skill_file.relative_to(ROOT)}")


def validate_required_mentions() -> None:
    agents = read_text(ROOT / ".devmode" / "app.md")
    for required in [
        ".codex/agents/",
        ".codex/dev_workflow/",
        ".codex/skills/",
        ".codex/orchestration/",
        ".codex/context/",
        ".codex/memory/",
        ".codex/rules/",
        ".codex/tools/",
        ".codex/prompts/",
        ".codex/state/",
    ]:
        if required not in agents:
            fail(f".devmode/app.md does not mention {required}")

    appflow = read_text(ROOT / ".devmode" / "app.md")
    for phrase in ["intent", "plan", "validation", "implementation", "evidence"]:
        if phrase not in appflow:
            fail(f".devmode/app.md missing lifecycle concept: {phrase}")
    if "appflow_run.py" not in read_text(ROOT / ".codex" / "tools" / "README.md"):
        fail(".codex/tools/README.md does not mention appflow_run.py")


def validate_retired_references() -> None:
    search_roots = [ROOT / ".codex"]
    for root in search_roots:
        paths = [root] if root.is_file() else sorted(root.rglob("*.md"))
        for path in paths:
            text = read_text(path)
            for retired in RETIRED_REFERENCES:
                if retired in text:
                    fail(f"retired reference {retired!r} in {path.relative_to(ROOT)}")


def validate_no_retired_id_prefixes() -> None:
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        text = read_text(path)
        retired_prefix = "AC" + "C-"
        if retired_prefix in text:
            fail(f"retired traceability ID prefix found in {path.relative_to(ROOT)}")


def validate_factory_is_project_agnostic() -> None:
    """Keep reusable factory markdown out of known project extension points.

    The only expected project-specific files in .codex are project-context.md
    and tech-stack.md.
    """

    allowed = {
        ROOT / ".codex" / "project-context.md",
        ROOT / ".codex" / "tech-stack.md",
    }
    root_terms = []
    root_agents = ROOT / "AGENTS.md"
    if root_agents.exists():
        text = read_text(root_agents)
        # Uppercase product acronyms and slash-prefixed authority paths are
        # common project-coupling signals. Keep this heuristic conservative.
        root_terms.extend(
            sorted(
                term
                for term in set(re.findall(r"\b[A-Z]{3,}\b", text))
                if term not in GENERIC_UPPERCASE_TERMS
            )
        )
        root_terms.extend(sorted(set(re.findall(r"`(/[A-Za-z0-9_.-]+)`", text))))

    for path in sorted((ROOT / ".codex").rglob("*.md")):
        if path in allowed:
            continue
        text = read_text(path)
        for term in root_terms:
            if term in text:
                fail(
                    f"project-specific term {term!r} found in reusable factory file "
                    f"{path.relative_to(ROOT)}"
                )


def validate_workflow_semantics() -> None:
    workflow_dir = ROOT / ".codex" / "dev_workflow"
    expected_files = [
        "README.md",
        "00-create-intent.md",
        "01-read-intent.md",
        "02-create-plan.md",
        "03-update-design.md",
        "04-update-tests.md",
        "05-implement-code.md",
        "06-run-validation.md",
        "07-fix-failures.md",
        "08-update-logs.md",
        "09-detect-gaps.md",
        "10-iteration-review.md",
    ]
    for filename in expected_files:
        path = workflow_dir / filename
        if not path.is_file():
            fail(f"missing canonical workflow file: {path.relative_to(ROOT)}")
        text = read_text(path)
        if filename != "README.md":
            for heading in ["## Objective", "## Required Read Order", "## Allowed Writes", "## Exit Criteria"]:
                if heading not in text:
                    fail(f"{path.relative_to(ROOT)} missing heading {heading!r}")

    readme = read_text(workflow_dir / "README.md")
    for filename in expected_files[1:]:
        if f".codex/dev_workflow/{filename}" not in readme:
            fail(f"workflow README missing reference to {filename}")
    removed_workflows_path = ".codex/" + "workflows"
    if removed_workflows_path in readme:
        fail("workflow README references removed workflow-pattern path")


def validate_project_artifacts() -> None:
    required_project_files = [
        "intent/product-intent.md",
        "intent/feedback-intent.md",
        "intent/gaps.md",
        "plan/design-update.md",
        "plan/code-update.md",
        "plan/test-update.md",
        "design/system-design.md",
        "design/architecture.md",
        "design/ux-flows.md",
        "design/acceptance-criteria.md",
        "tests/test-plan.md",
        "tests/design-traceability.md",
        "dev_log/design-update-log.md",
        "dev_log/code-update-log.md",
        "dev_log/test-update-log.md",
        "dev_log/validation-results.md",
    ]
    for rel in required_project_files:
        path = ROOT / rel
        if not path.is_file():
            fail(f"missing project artifact: {rel}")
        if not read_text(path).strip():
            fail(f"project artifact is empty: {rel}")

    retired_root_dirs = ["dev_workflow", "governance", "observability", "workflows", "knowledge"]
    for rel in retired_root_dirs:
        if (ROOT / rel).exists():
            fail(f"retired root support path still exists: {rel}")

    retired_paths = [
        "km" + "s.md",
        ".codex/" + "workflows",
    ]
    for rel in retired_paths:
        if (ROOT / rel).exists():
            fail(f"retired support path still exists: {rel}")


def validate_optional_appflow_state() -> None:
    state_path = ROOT / ".codex" / "state" / "appflow-current.json"
    if not state_path.exists():
        return
    try:
        import json

        state = json.loads(state_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - validation should report any parse issue.
        fail(f"invalid AppFlow state JSON: {exc}")

    expected_steps = [
        "00-create-intent",
        "01-read-intent",
        "02-create-plan",
        "03-update-design",
        "04-update-tests",
        "05-implement-code",
        "06-run-validation",
        "07-fix-failures",
        "08-update-logs",
        "09-detect-gaps",
        "10-iteration-review",
    ]
    if state.get("schema") != "appflow-run-state-v1":
        fail("AppFlow state schema must be appflow-run-state-v1")
    steps = state.get("steps", {})
    for step in expected_steps:
        if step not in steps:
            fail(f"AppFlow state missing step {step}")


def main() -> int:
    require_dirs()
    require_files()
    validate_skills()
    validate_required_mentions()
    validate_retired_references()
    validate_no_retired_id_prefixes()
    validate_factory_is_project_agnostic()
    validate_workflow_semantics()
    validate_project_artifacts()
    validate_optional_appflow_state()
    print("PASS: Codex contract validation succeeded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
