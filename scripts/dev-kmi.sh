#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export KMS_API_URL="${KMS_API_URL:-http://127.0.0.1:8010}"
export VITE_API_BASE_URL="${VITE_API_BASE_URL:-http://127.0.0.1:8010/api}"
exec npm --prefix "${ROOT}/apps/kmi" run dev
