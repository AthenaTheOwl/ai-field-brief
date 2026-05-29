"""Chaos test suite for validate_run_evidence.py.

The cross-checks in scripts/validate_run_evidence.py (Round 3's Run+
ledger agreement checks, Round 2's typed event payload validation via
the event.schema.json oneOf branches, and the required-for-done field
gate) are load-bearing: they are the proof that a published Run is
actually replay-equivalent to the recorded ledger. If any of those
checks regress to a no-op, the validator would silently let bad runs
through and nobody would notice until a replay drift surfaced months
later.

This module mutates a copy of the canonical sample Run + ledger pair
once per mutation class, runs the validator against the mutated
artifacts, and asserts the validator exits non-zero. One mutation per
class. Seven classes total, covering the cross-checks, the typed
payload schema, and the required-for-done gate.

The canonical sample lives on disk under ops/run-records/ and
ops/event-ledger/; the tests copy it into tmp_path and mutate the
copy. The disk-resident sample is never touched.
"""

from __future__ import annotations

import copy
import json
import pathlib
import shutil
import subprocess
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"

# Canonical sample on disk. The Run is status=done with all four
# required-for-done fields populated, a pipeline.start carrying both
# snapshot hashes, twelve gate.check.passed events, a pipeline.complete
# cloning the gate summary, and a closing gate.run.evidence_recorded.
# Every mutation in this module starts from a deep copy of this pair.
CANONICAL_RUN_ID = "run-d74d787e6756"
CANONICAL_RUN_PATH = ROOT / "ops" / "run-records" / f"{CANONICAL_RUN_ID}.json"
CANONICAL_LEDGER_PATH = (
    ROOT / "ops" / "event-ledger" / f"{CANONICAL_RUN_ID}.jsonl"
)


# ---------------------------------------------------------------- helpers


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


def _load_canonical_pair() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Deep-copy the canonical Run + ledger from disk.

    Returns a (run, events) tuple. Both are freshly-parsed dicts so the
    caller can mutate them without affecting other tests in the module.
    """
    run = json.loads(CANONICAL_RUN_PATH.read_text(encoding="utf-8"))
    events: list[dict[str, Any]] = []
    for line in CANONICAL_LEDGER_PATH.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        events.append(json.loads(stripped))
    return run, events


def _write_pair(
    tmp_path: pathlib.Path,
    run: dict[str, Any],
    events: list[dict[str, Any]],
) -> tuple[pathlib.Path, pathlib.Path]:
    """Write Run + ledger into tmp_path/run-records and tmp_path/event-ledger."""
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


def _assert_chaos_caught(
    result: subprocess.CompletedProcess[str],
    *,
    mutation: str,
    expect_in_output: list[str],
) -> None:
    """Assert the validator exited non-zero and named the expected check.

    A zero exit code on a mutation is a real validator gap. The
    assertion message includes the mutation label so any future
    regression surfaces with a clear pointer at the missing check.
    """
    output = result.stdout + result.stderr
    assert result.returncode != 0, (
        f"chaos mutation {mutation!r}: validator returned 0 (silent pass); "
        f"this is a real validator gap. stdout={result.stdout!r} "
        f"stderr={result.stderr!r}"
    )
    for needle in expect_in_output:
        assert needle in output, (
            f"chaos mutation {mutation!r}: expected {needle!r} in validator "
            f"output but got: {output!r}"
        )


# ---------------------------------------------------------------- baseline


def test_canonical_sample_passes_validator(tmp_path: pathlib.Path) -> None:
    """Sanity: the unmutated canonical pair passes the validator.

    Every chaos test below starts from this pair and mutates one field;
    if the baseline does not pass, the mutation results are meaningless.
    """
    run, events = _load_canonical_pair()
    ledger_dir, records_dir = _write_pair(tmp_path, run, events)
    result = _run_validate(ledger_dir, records_dir)
    assert result.returncode == 0, (
        f"canonical sample failed baseline validation: "
        f"stdout={result.stdout!r} stderr={result.stderr!r}"
    )


# ---------------------------------------------------------------- mutations


def test_m1_mutate_run_prompt_snapshot_hash_caught(
    tmp_path: pathlib.Path,
) -> None:
    """M1: flip Run.prompt_snapshot_hash to a different valid-shaped hash.

    Cross-check #1 (Run.prompt_snapshot_hash == pipeline.start payload
    field) should fire. The validator names the run_id and the
    pipeline.start surface in the violation message.
    """
    run, events = _load_canonical_pair()
    run["prompt_snapshot_hash"] = "d" * 64
    ledger_dir, records_dir = _write_pair(tmp_path, run, events)
    result = _run_validate(ledger_dir, records_dir)
    _assert_chaos_caught(
        result,
        mutation="M1: Run.prompt_snapshot_hash mutated",
        expect_in_output=[
            CANONICAL_RUN_ID,
            "prompt_snapshot_hash",
            "pipeline.start",
        ],
    )


def test_m2_mutate_run_tool_schemas_snapshot_hash_caught(
    tmp_path: pathlib.Path,
) -> None:
    """M2: flip Run.tool_schemas_snapshot_hash to a different hash.

    Cross-check #2 (Run.tool_schemas_snapshot_hash == pipeline.start
    payload field) should fire.
    """
    run, events = _load_canonical_pair()
    run["tool_schemas_snapshot_hash"] = "e" * 64
    ledger_dir, records_dir = _write_pair(tmp_path, run, events)
    result = _run_validate(ledger_dir, records_dir)
    _assert_chaos_caught(
        result,
        mutation="M2: Run.tool_schemas_snapshot_hash mutated",
        expect_in_output=[
            CANONICAL_RUN_ID,
            "tool_schemas_snapshot_hash",
            "pipeline.start",
        ],
    )


def test_m3_add_phantom_gate_to_run_summary_caught(
    tmp_path: pathlib.Path,
) -> None:
    """M3: add a phantom gate name to Run.gate_results_summary.gates_passed.

    Cross-check #4 (Run.gate_results_summary matches the ledger gate
    rollup) should fire. The ledger has no gate.check.passed event
    naming the phantom gate, so the sorted lists diverge.
    """
    run, events = _load_canonical_pair()
    run["gate_results_summary"]["gates_passed"] = sorted(
        run["gate_results_summary"]["gates_passed"] + ["phantom_gate"]
    )
    ledger_dir, records_dir = _write_pair(tmp_path, run, events)
    result = _run_validate(ledger_dir, records_dir)
    _assert_chaos_caught(
        result,
        mutation="M3: phantom gate added to Run.gate_results_summary",
        expect_in_output=[
            CANONICAL_RUN_ID,
            "gate_results_summary",
            "gates_passed",
        ],
    )


def test_m4_drop_terminal_evidence_recorded_event_caught(
    tmp_path: pathlib.Path,
) -> None:
    """M4: drop the terminal gate.run.evidence_recorded event.

    The required-terminal-event check should fire. Without the
    closing event the Run record cannot prove which fields were
    declared populated at emit time.
    """
    run, events = _load_canonical_pair()
    events = [
        e for e in events if e.get("type") != "gate.run.evidence_recorded"
    ]
    ledger_dir, records_dir = _write_pair(tmp_path, run, events)
    result = _run_validate(ledger_dir, records_dir)
    _assert_chaos_caught(
        result,
        mutation="M4: terminal gate.run.evidence_recorded event dropped",
        expect_in_output=[
            CANONICAL_RUN_ID,
            "gate.run.evidence_recorded",
        ],
    )


def test_m5_drop_prompt_hash_from_pipeline_start_payload_caught(
    tmp_path: pathlib.Path,
) -> None:
    """M5: drop prompt_snapshot_hash from pipeline.start payload.

    The typed-event-payload validation (Round 2's oneOf discriminator
    in event.schema.json) requires prompt_snapshot_hash on the
    pipeline.start branch. Removing it knocks the event off every
    oneOf branch and the schema validator fires.
    """
    run, events = _load_canonical_pair()
    new_events: list[dict[str, Any]] = []
    for event in events:
        if event.get("type") == "pipeline.start":
            mutated = copy.deepcopy(event)
            mutated["payload"].pop("prompt_snapshot_hash", None)
            new_events.append(mutated)
        else:
            new_events.append(event)
    ledger_dir, records_dir = _write_pair(tmp_path, run, new_events)
    result = _run_validate(ledger_dir, records_dir)
    _assert_chaos_caught(
        result,
        mutation="M5: pipeline.start payload missing prompt_snapshot_hash",
        expect_in_output=["pipeline.start"],
    )


def test_m6_mutate_evidence_recorded_fields_populated_caught(
    tmp_path: pathlib.Path,
) -> None:
    """M6: claim a replay-equivalence field that is not populated on Run.

    The Run carries four populated replay-equivalence fields
    (prompt_snapshot_hash, tool_schemas_snapshot_hash,
    sandbox_image_ref, gate_results_summary). The mutation claims a
    fifth (`determinism`, which is not populated). Cross-check #3
    should fire because the sorted claimed list no longer equals the
    sorted populated subset on the Run.
    """
    run, events = _load_canonical_pair()
    new_events: list[dict[str, Any]] = []
    for event in events:
        if event.get("type") == "gate.run.evidence_recorded":
            mutated = copy.deepcopy(event)
            payload = mutated.setdefault("payload", {})
            populated = list(payload.get("fields_populated") or [])
            payload["fields_populated"] = sorted(populated + ["determinism"])
            new_events.append(mutated)
        else:
            new_events.append(event)
    ledger_dir, records_dir = _write_pair(tmp_path, run, new_events)
    result = _run_validate(ledger_dir, records_dir)
    _assert_chaos_caught(
        result,
        mutation="M6: gate.run.evidence_recorded.fields_populated overclaims",
        expect_in_output=[
            CANONICAL_RUN_ID,
            "fields_populated",
        ],
    )


def test_m7_done_run_missing_sandbox_image_ref_caught(
    tmp_path: pathlib.Path,
) -> None:
    """M7: Run.status='done' but sandbox_image_ref dropped.

    The required-for-done gate should fire. Every Run claiming done
    must carry the four replay-equivalence fields ai-field-brief
    populates; sandbox_image_ref is one of them.
    """
    run, events = _load_canonical_pair()
    assert run.get("status") == "done", (
        "canonical sample is expected to be a done Run; chaos M7 only "
        "makes sense on a done Run"
    )
    run.pop("sandbox_image_ref", None)
    ledger_dir, records_dir = _write_pair(tmp_path, run, events)
    result = _run_validate(ledger_dir, records_dir)
    _assert_chaos_caught(
        result,
        mutation="M7: done Run missing sandbox_image_ref",
        expect_in_output=[
            CANONICAL_RUN_ID,
            "sandbox_image_ref",
        ],
    )


# ---------------------------------------------------------------- canonical-sample guard


def test_canonical_sample_on_disk_is_not_modified() -> None:
    """Guard: the disk-resident canonical sample is byte-identical.

    Every chaos test above copies the canonical pair into tmp_path
    before mutating. If a future test mutates the on-disk source by
    mistake, this guard fires.
    """
    run = json.loads(CANONICAL_RUN_PATH.read_text(encoding="utf-8"))
    assert run.get("id") == CANONICAL_RUN_ID
    assert run.get("status") == "done"
    assert run.get("prompt_snapshot_hash"), (
        "canonical sample lost its prompt_snapshot_hash; a test mutated "
        "the disk-resident sample"
    )
    assert run.get("sandbox_image_ref"), (
        "canonical sample lost its sandbox_image_ref; a test mutated "
        "the disk-resident sample"
    )
