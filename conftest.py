from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent
PYTHONPATHS = [
    REPO_ROOT,
    REPO_ROOT / "apps/api/src",
    REPO_ROOT / "apps/worker/src",
    REPO_ROOT / "packages/domain/src",
    REPO_ROOT / "packages/shared/src",
    REPO_ROOT / "packages/config/src",
]

for path in reversed(PYTHONPATHS):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)
