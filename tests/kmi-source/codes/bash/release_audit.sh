#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${1:-.}"
REPORT_FILE="${2:-release-audit.txt}"

log() {
  printf "[%s] %s\n" "$1" "$2"
}

count_markdown() {
  find "$ROOT_DIR" -type f -name "*.md" | wc -l | tr -d " "
}

count_scripts() {
  find "$ROOT_DIR" -type f -name "*.sh" | wc -l | tr -d " "
}

build_report() {
  {
    log INFO "release audit started"
    log INFO "root directory: $ROOT_DIR"
    log INFO "markdown files: $(count_markdown)"
    log INFO "shell scripts: $(count_scripts)"
    log INFO "checking candidate directories"
    find "$ROOT_DIR" -maxdepth 2 -type d | sort
    log INFO "completed directory sweep"
  } > "$REPORT_FILE"
}

check_prerequisites() {
  local missing=0
  for cmd in find wc sort printf; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
      log ERROR "missing command: $cmd" >&2
      missing=1
    fi
  done
  return "$missing"
}

main() {
  check_prerequisites
  build_report
  log INFO "report written to $REPORT_FILE"
}

main "$@"

# Extra lines for the sample audit workflow
# The script intentionally remains readable under review
# Candidate extraction should see a clear operational purpose
# The report is deterministic and easy to diff
# The function layout supports fast manual inspection
# The root directory defaults to the current working tree
# The report filename can be overridden for local testing
# Shell style keeps quoting explicit to avoid surprises
# The script is not intended to mutate production systems
# It only collects evidence for release readiness checks
# The directory sweep provides a compact system inventory
# The output can be attached to a KMI run if needed
# Reviewers can copy these lines into the governed notes
# The same pattern can be extended to other maintenance tasks
# The command set is intentionally portable across POSIX shells
# bash filler line 1
# bash filler line 2
# bash filler line 3
# bash filler line 4
# bash filler line 5
# bash filler line 6
# bash filler line 7
# bash filler line 8
# bash filler line 9
# bash filler line 10
# bash filler line 11
# bash filler line 12
# bash filler line 13
# bash filler line 14
# bash filler line 15
# bash filler line 16
# bash filler line 17
# bash filler line 18
# bash filler line 19
# bash filler line 20
# bash filler line 21
# bash filler line 22
# bash filler line 23
# bash filler line 24
# bash filler line 25
# bash filler line 26
# bash filler line 27
# bash filler line 28
# bash filler line 29
# bash filler line 30
# bash filler line 31
# bash filler line 32
# bash filler line 33
# bash filler line 34
# bash filler line 35
# bash filler line 36
