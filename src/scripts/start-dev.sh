#!/bin/bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$SRC_DIR/.." && pwd)"
export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"

pids_for_port() {
  local port="$1"
  {
    lsof -tiTCP:"$port" -sTCP:LISTEN 2>/dev/null || true
    lsof -tiTCP:"$port" 2>/dev/null || true
  } | sort -u
}

stop_port() {
  local port="$1"
  local pids
  pids="$(pids_for_port "$port")"
  if [ -n "$pids" ]; then
    echo "Stopping existing process on port $port: $pids"
    kill $pids 2>/dev/null || true
    sleep 1
    pids="$(pids_for_port "$port")"
    if [ -n "$pids" ]; then
      echo "Force stopping process on port $port: $pids"
      kill -9 $pids 2>/dev/null || true
    fi
  fi
}

require_free_port() {
  local port="$1"
  local pids
  pids="$(pids_for_port "$port")"
  if [ -n "$pids" ]; then
    echo "Port $port is still busy after cleanup: $pids" >&2
    echo "Stop it manually with: kill -9 $pids" >&2
    exit 1
  fi
}

cd "$REPO_ROOT" || exit 1

stop_port 8000
stop_port 3000
stop_port 3001
sleep 1
require_free_port 8000
require_free_port 3000
require_free_port 3001

echo "Starting API..."
uvicorn src.api.main:app --host 127.0.0.1 --port 8000 &

echo "Starting KMI..."
python3 -m http.server 3000 --bind 127.0.0.1 --directory "$SRC_DIR/kmi" &

echo "Starting Infopedia..."
python3 -m http.server 3001 --bind 127.0.0.1 --directory "$SRC_DIR/infopedia" &

echo "Starting Worker..."
python3 - <<'PY' &
from src.worker.main import run_intake
print("Worker module loaded; use run_intake(source_path, run_id=..., auto_approve=...) for intake jobs.")
PY

echo "KMS started"
