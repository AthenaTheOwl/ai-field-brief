"""End-to-end tests for the run-evidence CLIs.

- backfill_run_records.py produces validated Run + ledger for an
  existing brief (we exercise W22 because it is the canonical sample).
- finalize_run.py produces validated Run + ledger when called with a
  brief directory and an explicit gates string.
- validate_run_evidence.py exits 0 on the records both CLIs emit.
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"


def _run_python(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )


def test_backfill_produces_validated_records_for_w22(
    tmp_path: pathlib.Path,
) -> None:
    """backfill_run_records synthesizes a conformant Run + ledger for W22.

    Covers: R-PUB-004, R-PUB-005, R-PUB-007, R-PUB-009.
    """
    ledger_dir = tmp_path / "event-ledger"
    records_dir = tmp_path / "run-records"
    result = _run_python(
        [
            str(SCRIPTS / "backfill_run_records.py"),
            "--week",
            "2026-W22",
            "--event-ledger-dir",
            str(ledger_dir),
            "--run-records-dir",
            str(records_dir),
        ]
    )
    assert result.returncode == 0, (
        f"backfill failed: stdout={result.stdout!r} stderr={result.stderr!r}"
    )
    records = list(records_dir.glob("*.json"))
    ledgers = list(ledger_dir.glob("*.jsonl"))
    assert len(records) == 1
    assert len(ledgers) == 1

    run = json.loads(records[0].read_text(encoding="utf-8"))
    assert run["status"] == "done"
    assert run["spec_id"] == "specs/0007-publishing/"
    assert "prompt_snapshot_hash" in run
    assert "tool_schemas_snapshot_hash" in run
    assert "sandbox_image_ref" in run
    assert run["gate_results_summary"]["all_passed"] is True

    lines = [
        json.loads(line)
        for line in ledgers[0].read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    types = {line["type"] for line in lines}
    assert "pipeline.start" in types
    assert "pipeline.complete" in types
    assert "gate.run.evidence_recorded" in types


def test_backfill_all_briefs(tmp_path: pathlib.Path) -> None:
    ledger_dir = tmp_path / "event-ledger"
    records_dir = tmp_path / "run-records"
    result = _run_python(
        [
            str(SCRIPTS / "backfill_run_records.py"),
            "--all",
            "--event-ledger-dir",
            str(ledger_dir),
            "--run-records-dir",
            str(records_dir),
        ]
    )
    assert result.returncode == 0, (
        f"backfill --all failed: stdout={result.stdout!r} stderr={result.stderr!r}"
    )
    expected = len(
        [
            path
            for path in (ROOT / "briefs").iterdir()
            if path.is_dir() and path.name[:4].isdigit()
        ]
    )
    records = list(records_dir.glob("*.json"))
    ledgers = list(ledger_dir.glob("*.jsonl"))
    assert len(records) == expected
    assert len(ledgers) == expected


def test_finalize_run_emits_validated_records(tmp_path: pathlib.Path) -> None:
    """finalize_run is the publish-time CLI that lands Run + ledger.

    Covers: R-PUB-004, R-PUB-006, R-PUB-008.
    """
    ledger_dir = tmp_path / "event-ledger"
    records_dir = tmp_path / "run-records"
    result = _run_python(
        [
            str(SCRIPTS / "finalize_run.py"),
            "--brief",
            str(ROOT / "briefs" / "2026-W22"),
            "--gates",
            "voice_lint:passed,spec_check:passed,check_no_bom:passed",
            "--event-ledger-dir",
            str(ledger_dir),
            "--run-records-dir",
            str(records_dir),
        ]
    )
    assert result.returncode == 0, (
        f"finalize_run failed: stdout={result.stdout!r} stderr={result.stderr!r}"
    )
    records = list(records_dir.glob("*.json"))
    ledgers = list(ledger_dir.glob("*.jsonl"))
    assert len(records) == 1
    assert len(ledgers) == 1
    run = json.loads(records[0].read_text(encoding="utf-8"))
    assert run["status"] == "done"
    assert run["gate_results_summary"]["gates_passed"] == [
        "voice_lint",
        "spec_check",
        "check_no_bom",
    ]


def test_validate_run_evidence_passes_on_emitted_records(
    tmp_path: pathlib.Path,
) -> None:
    """validate_run_evidence accepts records emitted by the canonical CLIs.

    Covers: R-PUB-010, R-PUB-022, R-PUB-023.
    """
    ledger_dir = tmp_path / "event-ledger"
    records_dir = tmp_path / "run-records"
    backfill = _run_python(
        [
            str(SCRIPTS / "backfill_run_records.py"),
            "--week",
            "2026-W22",
            "--event-ledger-dir",
            str(ledger_dir),
            "--run-records-dir",
            str(records_dir),
        ]
    )
    assert backfill.returncode == 0

    validate = _run_python(
        [
            str(SCRIPTS / "validate_run_evidence.py"),
            "--event-ledger-dir",
            str(ledger_dir),
            "--run-records-dir",
            str(records_dir),
        ]
    )
    assert validate.returncode == 0, (
        f"validate_run_evidence failed on clean records: "
        f"stdout={validate.stdout!r} stderr={validate.stderr!r}"
    )


def test_validate_run_evidence_catches_bad_record(tmp_path: pathlib.Path) -> None:
    """validate_run_evidence flags non-conformant Run records.

    Covers: R-PUB-010, R-PUB-024, R-PUB-025.
    """
    records_dir = tmp_path / "run-records"
    records_dir.mkdir()
    bad = records_dir / "run-bad.json"
    bad.write_text(json.dumps({"id": "run-bad"}), encoding="utf-8")
    validate = _run_python(
        [
            str(SCRIPTS / "validate_run_evidence.py"),
            "--event-ledger-dir",
            str(tmp_path / "event-ledger"),
            "--run-records-dir",
            str(records_dir),
        ]
    )
    assert validate.returncode == 1
    assert "violation" in (validate.stdout + validate.stderr).lower()
