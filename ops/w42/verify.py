"""Run the W42 editorial gates and retain their actual outcomes.

The committed ops/w42/validation-results.json is dated evidence. A replay
writes to the ignored .tmp/w42/ directory unless --out names another file,
and cadence_check runs as of the W42 through-date, not the system clock.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
GATES = [
    "voice_lint", "check_no_bom", "spec_check", "validate_schemas",
    "validate_registry", "validate_decisions", "validate_roles", "validate_tools",
    "validate_policies", "validate_brief_fields", "validate_matrix_cells",
    "validate_skills", "validate_dreams", "check_schema_cache_freshness",
    "validate_run_evidence", "validate_sensitive_disclosures", "cadence_check",
]
GATE_ARGS = {"cadence_check": ["--today", "2026-10-18"]}
DEFAULT_OUT = ROOT / ".tmp" / "w42" / "validation-results.json"


def run_gate(name):
    result = subprocess.run([sys.executable, "-X", "utf8", f"scripts/{name}.py", *GATE_ARGS.get(name, [])], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return {"gate": name, "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="results file (default: .tmp/w42/validation-results.json)")
    out = parser.parse_args().out
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(run_gate, GATES))
    output = {"checked_at": datetime.now(timezone.utc).isoformat(), "gate_args": GATE_ARGS, "results": results}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for result in results:
        print(result["gate"], result["exit_code"], (result["stdout"] + result["stderr"])[-1200:])
    sys.exit(int(any(result["exit_code"] != 0 for result in results)))
