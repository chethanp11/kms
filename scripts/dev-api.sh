#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="${ROOT}/packages/domain/src:${ROOT}/packages/shared/src:${ROOT}/packages/config/src:${ROOT}/apps/api/src"
export KMS_RAW_PATH="${KMS_RAW_PATH:-${ROOT}/raw}"
export KMS_WIKI_PATH="${KMS_WIKI_PATH:-${ROOT}/wiki}"
export KMS_METADATA_DB_URL="${KMS_METADATA_DB_URL:-sqlite:///${ROOT}/.kms-metadata.db}"
export KMS_SEARCH_INDEX_URL="${KMS_SEARCH_INDEX_URL:-http://localhost:7700}"
export KMS_API_HOST="${KMS_API_HOST:-127.0.0.1}"
export KMS_API_PORT="${KMS_API_PORT:-8010}"

exec python -m kms_api.main
