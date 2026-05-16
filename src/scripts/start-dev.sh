#!/bin/bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$SRC_DIR/.." && pwd)"
export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"

pids_for_port() {
  local port="$1"
  lsof -tiTCP:"$port" -sTCP:LISTEN 2>/dev/null | sort -u || true
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
      echo "Port $port still busy; will use a fallback port. Busy PIDs: $pids"
    fi
  fi
}

is_free_port() {
  local port="$1"
  [ -z "$(pids_for_port "$port")" ]
}

choose_port() {
  local preferred="$1"
  local port="$preferred"
  while ! is_free_port "$port"; do
    port=$((port + 1))
  done
  echo "$port"
}

write_if_changed() {
  local path="$1"
  local content="$2"
  if [ ! -f "$path" ] || [ "$(cat "$path")" != "$content" ]; then
    printf '%s\n' "$content" > "$path"
  fi
}

cd "$REPO_ROOT" || exit 1

stop_port 8000
stop_port 3000
stop_port 3001
sleep 1

API_PORT="$(choose_port 8000)"
KMI_PORT="$(choose_port 3000)"
INFOPEDIA_PORT="$(choose_port 3001)"
if [ "$INFOPEDIA_PORT" = "$KMI_PORT" ]; then
  INFOPEDIA_PORT="$(choose_port $((KMI_PORT + 1)))"
fi

DEMO_RAW="/private/tmp/kms-demo/raw"
mkdir -p "$DEMO_RAW"
if [ ! -f "$DEMO_RAW/overview.md" ]; then
  cat > "$DEMO_RAW/overview.md" <<'DEMO'
Revenue is governed knowledge maintained through KMS.
DEMO
fi

write_if_changed "$SRC_DIR/kmi/config.js" "window.KMS_API_BASE = 'http://127.0.0.1:$API_PORT';"
write_if_changed "$SRC_DIR/infopedia/config.js" "window.KMS_API_BASE = 'http://127.0.0.1:$API_PORT';"

echo "Starting API on http://127.0.0.1:$API_PORT ..."
uvicorn src.api.main:app --host 127.0.0.1 --port "$API_PORT" &

echo "Starting KMI on http://127.0.0.1:$KMI_PORT ..."
python3 -m http.server "$KMI_PORT" --bind 127.0.0.1 --directory "$SRC_DIR/kmi" &

echo "Starting Infopedia on http://127.0.0.1:$INFOPEDIA_PORT ..."
python3 -m http.server "$INFOPEDIA_PORT" --bind 127.0.0.1 --directory "$SRC_DIR/infopedia" &

echo "Starting Worker..."
python3 - <<'WORKER' &
from src.worker.main import run_intake
print("Worker module loaded; use run_intake(source_path, run_id=..., auto_approve=...) for intake jobs.")
WORKER

echo "KMS started"
echo "KMI: http://127.0.0.1:$KMI_PORT"
echo "Infopedia: http://127.0.0.1:$INFOPEDIA_PORT"
echo "API: http://127.0.0.1:$API_PORT"
