"""Tests for the Round 3 cross-checks in validate_run_evidence.py.

The validator enforces, on every Run whose status is "done":

- Required-for-done fields: prompt_snapshot_hash, tool_schemas_snapshot_hash,
  sandbox_image_ref, gate_results_summary.
- Required terminal event: at least one gate.run.evidence_recorded.
- Four ledger/Run cross-checks: prompt-hash match against pipeline.start,
  tool-hash match against pipeline.start, fields_populated equals the
  populated replay-equivalence fields on the Run, and gate_results_summary
  matches the ledger gate.check.* aggregate.

This test module covers one positive end-to-end case and one focused
negative case per check. Each negative case constructs a minimum-viable
Run + ledger pair, mutates one field, and asserts the validator exits 1
with a clear message naming the run_id and the failing check.
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"


# ---------------------------------------------------------------- fixtures


def _run_validate(
    ledger_dir: pathlib.Path, records_dir: pathlib.Path
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "validate_run_evidence.py"),
            "--event-ledger-dir",
            str(ledger_dir),
            "--run-records-dir",
            str(records_dir),
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )


_PROMPT_HASH = "a" * 64
_TOOL_HASH = "b" * 64
_RUN_ID = "run-crosscheck0001"
_SPEC_ID = "specs/0007-publishing/"
_GATES = ["voice_lint", "spec_check", "check_no_bom"]


def _well_formed_pair() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Return a Run + ledger pair that passes every check.

    The fixture mirrors what backfill_run_records.py produces on a
    clean weekly brief: prompt + tool hashes on pipeline.start, one
    gate.check.passed per canonical gate, a pipeline.complete with
    status=done and the cloned gate summary, and a closing
    gate.run.evidence_recorded event whose fields_populated matches
    the populated replay-equivalence fields on the Run.
    """
    gate_summary = {
        "gates_passed": sorted(_GATES),
        "gates_failed": [],
        "all_passed": True,
    }
    run: dict[str, Any] = {
        "id": _RUN_ID,
        "spec_id": _SPEC_ID,
        "agent_id": "claude-opus-4-7",
        "runtime": "claude-code-cli",
        "workspace_id": "ai-field-brief",
        "started_at": "2026-05-25T15:00:00Z",
        "finished_at": "2026-05-25T16:00:00Z",
        "status": "done",
        "inputs": [{"kind": "playbook", "ref": "playbook/run-weekly-brief.md"}],
        "outputs": [{"artifact_id": "briefs/2026-W22/brief.md", "type": "brief"}],
        "events": [],
        "prompt_snapshot_hash": _PROMPT_HASH,
        "tool_schemas_snapshot_hash": _TOOL_HASH,
        "sandbox_image_ref": "ai-field-brief@" + ("c" * 40),
        "gate_results_summary": gate_summary,
    }
    events: list[dict[str, Any]] = [
        {
            "event_id": "11111111-1111-4111-8111-111111111111",
            "type": "pipeline.start",
            "created_at": "2026-05-25T15:00:00Z",
            "actor": {"kind": "role", "id": "product.brief-author"},
            "payload": {
                "brief": "2026-W22",
                "prompt_snapshot_hash": _PROMPT_HASH,
                "tool_schemas_snapshot_hash": _TOOL_HASH,
            },
            "run_id": _RUN_ID,
            "spec_id": _SPEC_ID,
        },
    ]
    for idx, gate in enumerate(_GATES):
        events.append(
            {
                "event_id": f"22222222-2222-4222-8222-{idx:012d}",
                "type": "gate.check.passed",
                "created_at": "2026-05-25T15:30:00Z",
                "actor": {"kind": "system", "id": "ci.gate-runner"},
                "payload": {"gate_name": gate},
                "run_id": _RUN_ID,
                "spec_id": _SPEC_ID,
            }
        )
    events.append(
        {
            "event_id": "33333333-3333-4333-8333-333333333333",
            "type": "pipeline.complete",
            "created_at": "2026-05-25T16:00:00Z",
            "actor": {"kind": "role", "id": "product.brief-author"},
            "payload": {
                "brief": "2026-W22",
                "status": "done",
                "gate_results_summary": gate_summary,
            },
            "run_id": _RUN_ID,
            "spec_id": _SPEC_ID,
            "parent_event_id": "11111111-1111-4111-8111-111111111111",
        }
    )
    events.append(
        {
            "event_id": "44444444-4444-4444-8444-444444444444",
            "type": "gate.run.evidence_recorded",
            "created_at": "2026-05-25T16:00:01Z",
            "actor": {"kind": "system", "id": "ci.run-evidence"},
            "payload": {
                "run_id": _RUN_ID,
                "fields_populated": [
                    "prompt_snapshot_hash",
                    "tool_schemas_snapshot_hash",
                    "sandbox_image_ref",
                    "gate_results_summary",
                ],
            },
            "run_id": _RUN_ID,
            "spec_id": _SPEC_ID,
            "parent_event_id": "33333333-3333-4333-8333-333333333333",
        }
    )
    return run, events


def _write_pair(
    tmp_path: pathlib.Path,
    run: dict[str, Any],
    events: list[dict[str, Any]],
) -> tuple[pathlib.Path, pathlib.Path]:
    ledger_dir = tmp_path / "event-ledger"
    records_dir = tmp_path / "run-records"
    ledger_dir.mkdir(parents=True, exist_ok=True)
    records_dir.mkdir(parents=True, exist_ok=True)
    (records_dir / f"{run['id']}.json").write_text(
        json.dumps(run, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    ledger_path = ledger_dir / f"{run['id']}.jsonl"
    with ledger_path.open("w", encoding="utf-8") as fh:
        for event in events:
            fh.write(json.dumps(event, sort_keys=True) + "\n")
    return ledger_dir, records_dir


# ---------------------------------------------------------------- positive


def test_validate_passes_on_well_formed_pair(tmp_path: pathlib.Path) -> None:
    """Baseline: well-formed Run + ledger pair passes every Round 3 check.

    Covers: R-PUB-010, R-PUB-011.
    """
    run, events = _well_formed_pair()
    ledger_dir, records_dir = _write_pair(tmp_path, run, events)
    result = _run_validate(ledger_dir, records_dir)
    assert result.returncode == 0, (
        f"validator failed on well-formed pair: "
        f"stdout={result.stdout!r} stderr={result.stderr!r}"
    )


# ---------------------------------------------------------------- negatives


def test_missing_prompt_snapshot_hash_on_done_run_fails(
    tmp_path: pathlib.Path,
) -> None:
    run, events = _well_formed_pair()
    run.pop("prompt_snapshot_hash")
    ledger_dir, records_dir = _write_pair(tmp_path, run, events)
    result = _run_validate(ledger_dir, records_dir)
    assert result.returncode == 1
    output = result.stdout + result.stderr
    assert _RUN_ID in output
    assert "prompt_snapshot_hash" in output


def test_missing_terminal_evidence_recorded_event_fails(
    tmp_path: pathlib.Path,
) -> None:
    run, events = _well_formed_pair()
    events = [e for e in events if e.get("type") != "gate.run.evidence_recorded"]
    ledger_dir, records_dir = _write_pair(tmp_path, run, events)
    result = _run_validate(ledger_dir, records_dir)
    assert result.returncode == 1
    output = result.stdout + result.stderr
    assert _RUN_ID in output
    assert "gate.run.evidence_recorded" in output


def test_prompt_hash_mismatch_between_run_and_pipeline_start_fails(
    tmp_path: pathlib.Path,
) -> None:
    """Cross-check #1: Run.prompt_snapshot_hash must match pipeline.start payload.

    Covers: R-PUB-011.
    """
    run, events = _well_formed_pair()
    run["prompt_snapshot_hash"] = "d" * 64
    ledger_dir, records_dir = _write_pair(tmp_path, run, events)
    result = _run_validate(ledger_dir, records_dir)
    assert result.returncode == 1
    output = result.stdout + result.stderr
    assert _RUN_ID in output
    assert "prompt_snapshot_hash" in output
    assert "pipeline.start" in output


def test_tool_schemas_hash_mismatch_fails(tmp_path: pathlib.Path) -> None:
    """Cross-check #2: tool_schemas_snapshot_hash must match pipeline.start.

    Covers: R-PUB-012.
    """
    run, events = _well_formed_pair()
    run["tool_schemas_snapshot_hash"] = "e" * 64
    ledger_dir, records_dir = _write_pair(tmp_path, run, events)
    result = _run_validate(ledger_dir, records_dir)
    assert result.returncode == 1
    output = result.stdout + result.stderr
    assert _RUN_ID in output
    assert "tool_schemas_snapshot_hash" in output
    assert "pipeline.start" in output


def test_fields_populated_mismatch_fails(tmp_path: pathlib.Path) -> None:
    """Cross-check #3: gate.run.evidence_recorded.fields_populated must match Run.

    Covers: R-PUB-013.
    """
    run, events = _well_formed_pair()
    # The Run carries four populated replay-equivalence fields; claim
    # only three on the gate.run.evidence_recorded event.
    for event in events:
        if event.get("type") == "gate.run.evidence_recorded":
            event["payload"]["fields_populated"] = [
                "prompt_snapshot_hash",
                "tool_schemas_snapshot_hash",
                "sandbox_image_ref",
            ]
    ledger_dir, records_dir = _write_pair(tmp_path, run, events)
    result = _run_validate(ledger_dir, records_dir)
    assert result.returncode == 1
    output = result.stdout + result.stderr
    assert _RUN_ID in output
    assert "fields_populated" in output


def test_gate_results_summary_mismatch_with_events_fails(
    tmp_path: pathlib.Path,
) -> None:
    """Cross-check #4: Run.gate_results_summary must match ledger gate aggregate.

    Covers: R-PUB-013.
    """
    run, events = _well_formed_pair()
    # The Run claims three gates passed; emit only two events.
    new_events: list[dict[str, Any]] = []
    skipped_one = False
    for event in events:
        if (
            event.get("type") == "gate.check.passed"
            and not skipped_one
            and event.get("payload", {}).get("gate_name") == "check_no_bom"
        ):
            skipped_one = True
            continue
        new_events.append(event)
    ledger_dir, records_dir = _write_pair(tmp_path, run, new_events)
    result = _run_validate(ledger_dir, records_dir)
    assert result.returncode == 1
    output = result.stdout + result.stderr
    assert _RUN_ID in output
    assert "gate_results_summary" in output
    assert "gates_passed" in output
