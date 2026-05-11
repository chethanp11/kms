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
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
STATE_PATH = ROOT / ".codex" / "state" / "appflow-current.json"
PRODUCT_INTENT_PATH = ROOT / "intent" / "product-intent.md"
FEEDBACK_INTENT_PATH = ROOT / "intent" / "feedback-intent.md"
GAPS_PATH = ROOT / "intent" / "gaps.md"

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
    if args.empty_gaps or not GAPS_PATH.exists():
        GAPS_PATH.write_text(EMPTY_GAPS_TEMPLATE, encoding="utf-8")
    print("Cleared consumed AppFlow intake artifacts")


def validate_state(args: argparse.Namespace) -> None:
    state = load_state()
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
        status = entry.get("status")
        evidence = entry.get("evidence", "").strip()
        if status not in {"pending", "completed", "skipped", "blocked"}:
            errors.append(f"{step} has invalid status {status!r}")
        if status in {"completed", "skipped", "blocked"} and not evidence:
            errors.append(f"{step} must include evidence when status is {status}")

    if args.require_complete:
        incomplete = [
            step
            for step in STEPS
            if steps.get(step, {}).get("status") not in {"completed", "skipped"}
        ]
        if incomplete:
            errors.append("incomplete steps: " + ", ".join(incomplete))
        if not state.get("validation", {}).get("commands"):
            errors.append("validation commands are required for complete closeout")
        if state.get("validation", {}).get("result") not in {"pass", "partial", "fail"}:
            errors.append("validation result must be pass, partial, or fail")

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
