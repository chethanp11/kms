#!/usr/bin/env bash
set -euo pipefail

API_URL="${API_URL:-http://127.0.0.1:8000}"

curl --fail --silent --show-error "${API_URL}/health" >/dev/null
curl --fail --silent --show-error "${API_URL}/api/health/findings" >/dev/null
echo "ok"
