from __future__ import annotations

import argparse
import signal
import sys
import time

from kms_config import load_runtime_config


def main() -> None:
    parser = argparse.ArgumentParser(description="KMS worker process")
    parser.add_argument("--once", action="store_true", help="Print startup config and exit")
    args = parser.parse_args()

    config = load_runtime_config()
    print(
        "kms worker ready "
        f"raw={config.raw_path} wiki={config.wiki_path} metadata_db={config.metadata_db_url}"
    )
    if args.once:
        return

    stop = False

    def _handle_stop(signum: int, frame: object) -> None:
        nonlocal stop
        stop = True

    signal.signal(signal.SIGTERM, _handle_stop)
    signal.signal(signal.SIGINT, _handle_stop)

    while not stop:
        time.sleep(1)


if __name__ == "__main__":
    main()
