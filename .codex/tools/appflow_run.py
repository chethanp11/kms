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


def mark(args: argparse.Namespace) -> None:
    state = load_state()
    if args.step not in STEPS:
        raise SystemExit(f"Unknown step {args.step!r}. Expected one of: {', '.join(STEPS)}")
    state["steps"][args.step] = {
        "status": args.status,
        "evidence": args.evidence,
        "updated_at": now(),
    }
    state["updated_at"] = now()
    write_state(state)
    print(f"Marked {args.step} as {args.status}")


def add_validation(args: argparse.Namespace) -> None:
    state = load_state()
    state["validation"]["commands"].append(args.command)
    state["validation"]["result"] = args.result
    state["updated_at"] = now()
    write_state(state)
    print("Recorded validation evidence")


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
    mark_parser.add_argument("--step", required=True)
    mark_parser.add_argument(
        "--status",
        choices=["pending", "completed", "skipped", "blocked"],
        required=True,
    )
    mark_parser.add_argument("--evidence", required=True)
    mark_parser.set_defaults(func=mark)

    validation_parser = sub.add_parser("validation", help="record validation evidence")
    validation_parser.add_argument("--command", required=True)
    validation_parser.add_argument("--result", choices=["pass", "partial", "fail"], required=True)
    validation_parser.set_defaults(func=add_validation)

    validate_parser = sub.add_parser("validate", help="validate current AppFlow state")
    validate_parser.add_argument("--require-complete", action="store_true")
    validate_parser.set_defaults(func=validate_state)

    return parser


def main() -> int:
    args = build_parser().parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
