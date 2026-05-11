#!/usr/bin/env python3
"""Create and validate lightweight AppFlow lifecycle state.

This tool does not replace agent judgment. It records whether the canonical
11-step workflow has evidence for the current turn so closeout can be checked
deterministically.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional


ROOT = Path(__file__).resolve().parents[2]
STATE_PATH = ROOT / ".codex" / "state" / "appflow-current.json"
PRODUCT_INTENT_PATH = ROOT / "intent" / "product-intent.md"
FEEDBACK_INTENT_PATH = ROOT / "intent" / "feedback-intent.md"
GAPS_PATH = ROOT / "intent" / "gaps.md"
CURRENT_INTENT_PATH = ROOT / ".codex" / "state" / "current-intent.md"
PLAN_FILES = [
    ROOT / "plan" / "design-update.md",
    ROOT / "plan" / "code-update.md",
    ROOT / "plan" / "test-update.md",
]

CURRENT_INTENT_TEMPLATE = """# Current Intent

This file is populated at AppFlow step `00` from the current app-mode prompt and cleared at closeout.

## Current-cycle intent

- None.
"""

PRODUCT_INTENT_TEMPLATE = """# Product Intent

This file is populated at AppFlow step `00` from the current app-mode prompt when the prompt requests product, design, test, code, documentation, or behavior changes.

## Current-cycle product intent

- None.
"""

FEEDBACK_INTENT_TEMPLATE = """# Feedback Intent

This file is populated at AppFlow step `00` from the current app-mode prompt when the prompt contains manual feedback, review observations, corrections, complaints, or user-reported issues.

## Current-cycle feedback

- None.
"""

EMPTY_GAPS_TEMPLATE = """# Gaps

This file is system-generated at AppFlow step `09` from logs, validation results, and workflow evidence. It should contain only next-cycle gaps.

## Current gaps

- None.
"""

STEPS = [
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

STEP_ALIASES = {step: step for step in STEPS}
STEP_ALIASES.update({step[:2]: step for step in STEPS})
STEP_ALIASES.update({str(int(step[:2])): step for step in STEPS})


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        raise SystemExit(
            f"Missing AppFlow state: {STATE_PATH.relative_to(ROOT)}. "
            "Run appflow_run.py init first."
        )
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def load_optional_state() -> Optional[dict[str, Any]]:
    if not STATE_PATH.exists():
        return None
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def write_state(state: dict[str, Any]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def init(args: argparse.Namespace) -> None:
    state = {
        "schema": "appflow-run-state-v1",
        "objective": args.objective,
        "created_at": now(),
        "updated_at": now(),
        "status": "active",
        "steps": {
            step: {
                "status": "pending",
                "evidence": "",
                "updated_at": "",
            }
            for step in STEPS
        },
        "validation": {
            "commands": [],
            "result": "",
        },
        "risks": [],
        "follow_up": [],
    }
    write_state(state)
    print(f"Initialized {STATE_PATH.relative_to(ROOT)}")


def normalize_step(step: str) -> str:
    try:
        return STEP_ALIASES[step]
    except KeyError:
        expected = ", ".join(STEPS)
        aliases = ", ".join(step[:2] for step in STEPS)
        raise SystemExit(f"Unknown step {step!r}. Expected one of: {expected}. Numeric aliases: {aliases}")


def mark(args: argparse.Namespace) -> None:
    state = load_state()
    step = normalize_step(args.step)
    state["steps"][step] = {
        "status": args.status,
        "evidence": args.evidence,
        "updated_at": now(),
    }
    state["updated_at"] = now()
    write_state(state)
    print(f"Marked {step} as {args.status}")


def add_validation(args: argparse.Namespace) -> None:
    state = load_state()
    state["validation"]["commands"].append(args.command)
    state["validation"]["result"] = args.result
    state["updated_at"] = now()
    write_state(state)
    print("Recorded validation evidence")


def closeout_intake(args: argparse.Namespace) -> None:
    """Clear consumed prompt intake artifacts at cycle closeout.

    Product intent and feedback intent are always current-cycle inputs, so they
    reset to empty templates. Gaps are next-cycle input; preserve the current
    step-09 gap record unless the caller explicitly requests an empty gap file.
    """

    PRODUCT_INTENT_PATH.parent.mkdir(parents=True, exist_ok=True)
    PRODUCT_INTENT_PATH.write_text(PRODUCT_INTENT_TEMPLATE, encoding="utf-8")
    FEEDBACK_INTENT_PATH.write_text(FEEDBACK_INTENT_TEMPLATE, encoding="utf-8")
    CURRENT_INTENT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CURRENT_INTENT_PATH.write_text(CURRENT_INTENT_TEMPLATE, encoding="utf-8")
    if args.empty_gaps or not GAPS_PATH.exists():
        GAPS_PATH.write_text(EMPTY_GAPS_TEMPLATE, encoding="utf-8")
    print("Cleared consumed AppFlow intake artifacts")


def file_has_non_template_content(path: Path, empty_template: Optional[str] = None) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return False
    if empty_template is not None and text == empty_template.strip():
        return False
    return True


def step_groups(state: dict[str, Any]) -> dict[str, list[str]]:
    steps = state.get("steps", {})
    return {
        "completed": [step for step in STEPS if steps.get(step, {}).get("status") == "completed"],
        "skipped": [step for step in STEPS if steps.get(step, {}).get("status") == "skipped"],
        "blocked": [step for step in STEPS if steps.get(step, {}).get("status") == "blocked"],
        "pending": [step for step in STEPS if steps.get(step, {}).get("status") == "pending"],
        "incomplete": [step for step in STEPS if steps.get(step, {}).get("status") not in {"completed", "skipped"}],
    }


def validation_errors(state: dict[str, Any], *, require_complete: bool = False, enforce_lifecycle: bool = False) -> list[str]:
    errors: list[str] = []
    if state.get("schema") != "appflow-run-state-v1":
        errors.append("schema must be appflow-run-state-v1")
    if not state.get("objective", "").strip():
        errors.append("objective is required")

    steps = state.get("steps", {})
    for step in STEPS:
        entry = steps.get(step)
        if not entry:
            errors.append(f"missing step {step}")
            continue
        status_value = entry.get("status")
        evidence = entry.get("evidence", "").strip()
        if status_value not in {"pending", "completed", "skipped", "blocked"}:
            errors.append(f"{step} has invalid status {status_value!r}")
        if status_value in {"completed", "skipped", "blocked"} and not evidence:
            errors.append(f"{step} must include evidence when status is {status_value}")

    groups = step_groups(state)
    validation = state.get("validation", {})
    if require_complete:
        if groups["incomplete"]:
            errors.append("incomplete steps: " + ", ".join(groups["incomplete"]))
        if not validation.get("commands"):
            errors.append("validation commands are required for complete closeout")
        if validation.get("result") not in {"pass", "partial", "fail"}:
            errors.append("validation result must be pass, partial, or fail")

    if enforce_lifecycle:
        lifecycle_status = state.get("status")
        if lifecycle_status not in {"inactive", "active", "complete", "blocked"}:
            errors.append("AppFlow state status must be inactive, active, complete, or blocked")
        if lifecycle_status == "active" and not groups["incomplete"]:
            errors.append("active AppFlow state cannot have every step completed or skipped; run appflow_run.py complete")
        if lifecycle_status == "complete":
            if groups["incomplete"]:
                errors.append("complete AppFlow state cannot have incomplete steps")
            if not validation.get("commands") or validation.get("result") not in {"pass", "partial", "fail"}:
                errors.append("complete AppFlow state requires validation evidence")
        if lifecycle_status == "inactive":
            for step in STEPS:
                entry = steps.get(step, {})
                if entry.get("status") != "pending":
                    errors.append(f"inactive AppFlow state must not retain completed evidence for {step}")
                if entry.get("evidence"):
                    errors.append(f"inactive AppFlow state must not retain stale evidence for {step}")
    return errors


def print_state_summary(state: Optional[dict[str, Any]]) -> None:
    if state is None:
        print("AppFlow state: missing")
        print("Next action: run appflow_run.py init before substantial app-mode file changes")
        return
    groups = step_groups(state)
    validation = state.get("validation", {})
    print(f"AppFlow state: {state.get('status', 'unknown')}")
    print(f"Objective: {state.get('objective', '')}")
    print(
        "Steps: "
        f"completed={len(groups['completed'])} "
        f"skipped={len(groups['skipped'])} "
        f"blocked={len(groups['blocked'])} "
        f"pending={len(groups['pending'])}"
    )
    print("Incomplete steps: " + (", ".join(groups["incomplete"]) if groups["incomplete"] else "none"))
    print("Blocked steps: " + (", ".join(groups["blocked"]) if groups["blocked"] else "none"))
    print(f"Validation result: {validation.get('result') or 'none'}")
    print(f"Validation commands: {len(validation.get('commands', []))}")


def print_intake_summary(state: Optional[dict[str, Any]]) -> None:
    current_intent_has_content = file_has_non_template_content(CURRENT_INTENT_PATH, CURRENT_INTENT_TEMPLATE)
    product_intent_has_content = file_has_non_template_content(PRODUCT_INTENT_PATH, PRODUCT_INTENT_TEMPLATE)
    feedback_intent_has_content = file_has_non_template_content(FEEDBACK_INTENT_PATH, FEEDBACK_INTENT_TEMPLATE)
    gaps_has_content = file_has_non_template_content(GAPS_PATH, EMPTY_GAPS_TEMPLATE)
    state_status = state.get("status") if state else "missing"
    stale_current_intent = current_intent_has_content and state_status != "active"
    stale_prompt_intake = (product_intent_has_content or feedback_intent_has_content) and state_status != "active"
    print(f"Current-intent content: {'yes' if current_intent_has_content else 'no'}")
    print(f"Prompt intake content: product={'yes' if product_intent_has_content else 'no'} feedback={'yes' if feedback_intent_has_content else 'no'}")
    print(f"Next-cycle gaps content: {'yes' if gaps_has_content else 'no'}")
    print(f"Stale current-intent warning: {'yes' if stale_current_intent else 'no'}")
    print(f"Stale prompt-intake warning: {'yes' if stale_prompt_intake else 'no'}")


def mode_text() -> str:
    path = ROOT / ".devmode" / "mode.yaml"
    return path.read_text(encoding="utf-8").strip() if path.exists() else "missing"


def preflight(args: argparse.Namespace) -> None:
    """Print preflight checks before an app-mode AppFlow cycle."""

    state = load_optional_state()
    print(f"Mode: {mode_text()}")
    print_state_summary(state)
    print_intake_summary(state)
    missing_plan_files = [str(path.relative_to(ROOT)) for path in PLAN_FILES if not path.is_file()]
    print("Required plan files: " + ("present" if not missing_plan_files else "missing " + ", ".join(missing_plan_files)))
    tech_stack = ROOT / ".codex" / "tech-stack.md"
    tests_plan = ROOT / "tests" / "test-plan.md"
    validation_sources = [str(path.relative_to(ROOT)) for path in [tech_stack, tests_plan] if path.exists()]
    print("Likely validation sources: " + (", ".join(validation_sources) if validation_sources else "none found"))
    if state and state.get("status") == "active" and not step_groups(state)["incomplete"]:
        print("Preflight warning: active run has no incomplete steps; run appflow_run.py complete or start a fresh run")


def status(args: argparse.Namespace) -> None:
    """Print a non-mutating summary of AppFlow lifecycle state."""

    state = load_optional_state()
    print_state_summary(state)
    print_intake_summary(state)


def complete(args: argparse.Namespace) -> None:
    """Mark a fully validated AppFlow run complete and clear current intent."""

    state = load_state()
    errors = validation_errors(state, require_complete=True)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        raise SystemExit(1)
    state["status"] = "complete"
    state["updated_at"] = now()
    write_state(state)
    CURRENT_INTENT_PATH.parent.mkdir(parents=True, exist_ok=True)
    CURRENT_INTENT_PATH.write_text(CURRENT_INTENT_TEMPLATE, encoding="utf-8")
    print("Marked AppFlow run as complete")



def validate_state(args: argparse.Namespace) -> None:
    state = load_state()
    errors = validation_errors(state, require_complete=args.require_complete)

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        raise SystemExit(1)

    print("PASS: AppFlow run state is valid")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(required=True)

    init_parser = sub.add_parser("init", help="start a new AppFlow run state")
    init_parser.add_argument("--objective", required=True)
    init_parser.set_defaults(func=init)

    mark_parser = sub.add_parser("mark", help="mark a lifecycle step")
    mark_parser.add_argument("step_arg", nargs="?", help="step name or numeric alias, for example 02 or 02-create-plan")
    mark_parser.add_argument("status_arg", nargs="?", choices=["pending", "completed", "skipped", "blocked"], help="step status")
    mark_parser.add_argument("--step", dest="step_option", help="step name or numeric alias")
    mark_parser.add_argument(
        "--status",
        dest="status_option",
        choices=["pending", "completed", "skipped", "blocked"],
        help="step status",
    )
    mark_parser.add_argument("--evidence", required=True)
    mark_parser.set_defaults(func=mark)

    validation_parser = sub.add_parser("validation", help="record validation evidence")
    validation_parser.add_argument("--command", required=True)
    validation_parser.add_argument("--result", choices=["pass", "partial", "fail"], required=True)
    validation_parser.set_defaults(func=add_validation)

    preflight_parser = sub.add_parser("preflight", help="print non-mutating mode, state, intake, plan, and validation preflight")
    preflight_parser.set_defaults(func=preflight)

    status_parser = sub.add_parser("status", help="print non-mutating AppFlow state and stale-intake summary")
    status_parser.set_defaults(func=status)

    closeout_parser = sub.add_parser(
        "closeout-intake",
        help="clear consumed product/feedback intent after step 09 has written next-cycle gaps",
    )
    closeout_parser.add_argument(
        "--empty-gaps",
        action="store_true",
        help="also reset intent/gaps.md to an explicit empty next-cycle gap record",
    )
    closeout_parser.set_defaults(func=closeout_intake)

    complete_parser = sub.add_parser("complete", help="validate closeout, mark state complete, and clear current-intent")
    complete_parser.set_defaults(func=complete)

    validate_parser = sub.add_parser("validate", help="validate current AppFlow state")
    validate_parser.add_argument("--require-complete", action="store_true")
    validate_parser.set_defaults(func=validate_state)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    if getattr(args, "func", None) is mark:
        args.step = args.step_option or args.step_arg
        args.status = args.status_option or args.status_arg
        if not args.step:
            raise SystemExit("mark requires a step via positional STEP or --step")
        if not args.status:
            raise SystemExit("mark requires a status via positional STATUS or --status")
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
