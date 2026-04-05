#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cleanup() {
  if [[ -n "${API_PID:-}" ]]; then
    kill "${API_PID}" >/dev/null 2>&1 || true
  fi
  if [[ -n "${WORKER_PID:-}" ]]; then
    kill "${WORKER_PID}" >/dev/null 2>&1 || true
  fi
  if [[ -n "${KMI_PID:-}" ]]; then
    kill "${KMI_PID}" >/dev/null 2>&1 || true
  fi
  if [[ -n "${INFO_PID:-}" ]]; then
    kill "${INFO_PID}" >/dev/null 2>&1 || true
  fi
}

trap cleanup EXIT INT TERM

"${ROOT}/scripts/dev-api.sh" &
API_PID=$!
"${ROOT}/scripts/dev-worker.sh" &
WORKER_PID=$!
npm --prefix "${ROOT}/apps/kmi" run dev &
KMI_PID=$!
npm --prefix "${ROOT}/apps/infopedia" run dev &
INFO_PID=$!

wait "${API_PID}" "${WORKER_PID}" "${KMI_PID}" "${INFO_PID}"
