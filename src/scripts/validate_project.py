"""Runtime project validation entrypoint."""
from __future__ import annotations
from src.api.main import create_app
from src.app import REPRESENTATIVE_ENDPOINTS
def validate() -> list[str]:
    findings: list[str] = []
    if ("POST", "/api/runs") not in REPRESENTATIVE_ENDPOINTS:
        findings.append("missing run endpoint")
    if create_app() is None:
        findings.append("api app did not initialize")
    return findings
def main() -> int:
    findings = validate()
    for finding in findings:
        print(finding)
    return 1 if findings else 0
if __name__ == "__main__":
    raise SystemExit(main())
