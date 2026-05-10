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
    ".devmode/override.md",
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
    ".codex/memory/README.md",
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
    ".codex/memory",
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

STANDARD_FRONTMATTER = re.compile(
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


def validate_devmode() -> None:
    mode_text = read_text(ROOT / ".devmode" / "mode.yaml").strip()
    if mode_text not in {"mode: app", "mode: framework", "mode: override"}:
        fail(".devmode/mode.yaml must be exactly 'mode: app', 'mode: framework', or 'mode: override'")

    router = read_text(ROOT / "AGENTS.md")
    required_router_phrases = [
        ".devmode/mode.yaml` is mandatory and authoritative",
        "Never blend modes",
        "Never run `.codex/dev_workflow/*` in framework mode",
        "Never modify application artifacts in framework mode",
        "If `mode: override`, read and follow `.devmode/override.md`",
    ]
    for phrase in required_router_phrases:
        if phrase not in router:
            fail(f"AGENTS.md missing devmode enforcement phrase: {phrase}")

    framework = read_text(ROOT / ".devmode" / "framework.md")
    for phrase in ["Framework mode is control-plane-only", "report them as out-of-scope instead of fixing application code", "Files Framework Mode Must Not Modify"]:
        if phrase not in framework:
            fail(f".devmode/framework.md missing strict boundary phrase: {phrase}")

    override = read_text(ROOT / ".devmode" / "override.md")
    for phrase in ["Override mode", "may modify any repository file", "not AppFlow application workflow"]:
        if phrase not in override:
            fail(f".devmode/override.md missing override phrase: {phrase}")


def validate_skills() -> None:
    skills_dir = ROOT / ".codex" / "skills"
    skill_files = sorted(skills_dir.glob("*/SKILL.md"))
    if not skill_files:
        fail("no .codex skills found")

    for skill_file in skill_files:
        text = read_text(skill_file)
        match = STANDARD_FRONTMATTER.search(text)
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


def validate_agents() -> None:
    agents_dir = ROOT / ".codex" / "agents"
    agent_files = sorted(path for path in agents_dir.glob("*.md") if path.name != "README.md")
    if not agent_files:
        fail("no .codex agent role files found")

    for agent_file in agent_files:
        text = read_text(agent_file)
        match = STANDARD_FRONTMATTER.search(text)
        if not match:
            fail(f"agent missing required frontmatter: {agent_file.relative_to(ROOT)}")
        if match.group("name") != agent_file.stem:
            fail(
                "agent frontmatter name does not match file: "
                f"{agent_file.relative_to(ROOT)}"
            )
        if len(match.group("description").strip()) < 20:
            fail(f"agent description too short: {agent_file.relative_to(ROOT)}")


def validate_required_mentions() -> None:
    agents = read_text(ROOT / ".devmode" / "app.md")
    for required in [
        ".codex/agents/",
        ".codex/dev_workflow/",
        ".codex/skills/",
        ".codex/orchestration/",
        ".codex/memory/",
        ".codex/tools/",
        ".codex/state/",
    ]:
        if required not in agents:
            fail(f".devmode/app.md does not mention {required}")

    appflow = read_text(ROOT / ".devmode" / "app.md")
    for phrase in ["intent", "plan", "validation", "implementation", "evidence"]:
        if phrase not in appflow:
            fail(f".devmode/app.md missing lifecycle concept: {phrase}")
    for phrase in [
        "Step `02` must update `plan/design-update.md`",
        "Step `03` must update design artifacts when intent changes",
        "After initial scaffolding exists",
    ]:
        if phrase not in appflow:
            fail(f".devmode/app.md missing app-mode discipline phrase: {phrase}")
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

    plan_text = read_text(workflow_dir / "02-create-plan.md")
    for phrase in ["stale plan", "all three plan files", "new component family"]:
        if phrase not in plan_text:
            fail(f"02-create-plan.md missing planning discipline phrase: {phrase}")

    design_text = read_text(workflow_dir / "03-update-design.md")
    for phrase in ["design review", "no design file changes are required"]:
        if phrase not in design_text:
            fail(f"03-update-design.md missing design discipline phrase: {phrase}")

    implement_text = read_text(workflow_dir / "05-implement-code.md")
    for phrase in ["Once initial scaffolding exists", "absolutely necessary"]:
        if phrase not in implement_text:
            fail(f"05-implement-code.md missing scaffold discipline phrase: {phrase}")

    readme = read_text(workflow_dir / "README.md")
    for filename in expected_files[1:]:
        if f".codex/dev_workflow/{filename}" not in readme:
            fail(f"workflow README missing reference to {filename}")
    removed_workflows_path = ".codex/" + "workflows"
    if removed_workflows_path in readme:
        fail("workflow README references removed workflow-pattern path")


def validate_project_artifacts() -> None:
    """Check retired legacy paths without requiring app-specific artifacts."""

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
    if state.get("status") not in {"inactive", "active", "complete", "blocked"}:
        fail("AppFlow state status must be inactive, active, complete, or blocked")
    steps = state.get("steps", {})
    for step in expected_steps:
        if step not in steps:
            fail(f"AppFlow state missing step {step}")
        entry = steps[step]
        if entry.get("status") not in {"pending", "completed", "skipped", "blocked"}:
            fail(f"AppFlow state step {step} has invalid status")
        if state.get("status") == "inactive" and entry.get("status") != "pending":
            fail(f"inactive AppFlow state must not retain completed evidence for {step}")
        if state.get("status") == "inactive" and entry.get("evidence"):
            fail(f"inactive AppFlow state must not retain stale evidence for {step}")


def main() -> int:
    require_dirs()
    require_files()
    validate_devmode()
    validate_skills()
    validate_agents()
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
