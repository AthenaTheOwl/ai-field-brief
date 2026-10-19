"""Run the W42 editorial gates and retain their actual outcomes."""
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
    "validate_run_evidence", "validate_sensitive_disclosures",
]


def run_gate(name):
    result = subprocess.run([sys.executable, "-X", "utf8", f"scripts/{name}.py"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return {"gate": name, "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr}


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(run_gate, GATES))
    output = {"checked_at": datetime.now(timezone.utc).isoformat(), "results": results}
    (Path(__file__).parent / "validation-results.json").write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for result in results:
        print(result["gate"], result["exit_code"], (result["stdout"] + result["stderr"])[-1200:])
    sys.exit(int(any(result["exit_code"] != 0 for result in results)))
