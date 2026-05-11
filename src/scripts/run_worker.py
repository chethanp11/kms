"""CLI helper for running the worker."""
from __future__ import annotations
import argparse
from src.worker.main import main
def cli() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_path")
    parser.add_argument("--run-id", default="run-1")
    parser.add_argument("--auto-approve", action="store_true")
    args = parser.parse_args()
    return main(args.source_path, run_id=args.run_id, auto_approve=args.auto_approve)
if __name__ == "__main__":
    raise SystemExit(cli())
