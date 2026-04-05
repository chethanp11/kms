#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PYTHONPATH="${ROOT}/packages/domain/src:${ROOT}/packages/shared/src:${ROOT}/packages/config/src:${ROOT}/apps/worker/src"
export KMS_RAW_PATH="${KMS_RAW_PATH:-${ROOT}/raw}"
export KMS_WIKI_PATH="${KMS_WIKI_PATH:-${ROOT}/wiki}"
export KMS_METADATA_DB_URL="${KMS_METADATA_DB_URL:-sqlite:///${ROOT}/.kms-metadata.db}"
export KMS_SEARCH_INDEX_URL="${KMS_SEARCH_INDEX_URL:-http://localhost:7700}"

exec python -m kms_worker.main
