"""Tests for ``scripts/finalize_sandbox_ref.py``.

The second-pass CLI rewrites every PENDING placeholder in a Run record
to the actual sample-containing commit SHA. The tests cover:

- A record carrying ``sandbox_image_ref`` and inputs/outputs URIs with
  ``@PENDING/`` placeholders gets all of them rewritten in one pass.
- A record carrying no PENDING markers is untouched (idempotent).
- The CLI refuses to write a non-40-char SHA value.
- ``--run-id`` and ``--all`` both target the right files.
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"


def _run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )


def _pending_record(run_id: str) -> dict[str, object]:
    return {
        "agent_id": "claude-opus-4-7",
        "events": [],
        "finished_at": "2026-05-25T16:00:00Z",
        "gate_results_summary": {
            "all_passed": True,
            "gates_failed": [],
            "gates_passed": ["voice_lint"],
        },
        "id": run_id,
        "inputs": [
            {
                "kind": "playbook",
                "ref": "repo://ai-field-brief@PENDING/playbook/run-weekly-brief.md",
            },
            {
                "kind": "source-registry",
                "ref": "repo://ai-field-brief@PENDING/sources/registry.yaml",
            },
        ],
        "outputs": [
            {
                "artifact_id": "repo://ai-field-brief@PENDING/briefs/2026-W22/brief.md",
                "type": "brief",
            },
        ],
        "prompt_snapshot_hash": "a" * 64,
        "runtime": "claude-code-cli",
        "sandbox_image_ref": "repo://ai-field-brief@PENDING/",
        "spec_id": "specs/0007-publishing/",
        "started_at": "2026-05-25T15:00:00Z",
        "status": "done",
        "tool_schemas_snapshot_hash": "b" * 64,
        "workspace_id": "ai-field-brief",
    }


def test_finalize_sandbox_ref_rewrites_pending(tmp_path: pathlib.Path) -> None:
    records_dir = tmp_path / "run-records"
    records_dir.mkdir()
    run_id = "run-pendingrewriter"
    record_path = records_dir / f"{run_id}.json"
    record_path.write_text(
        json.dumps(_pending_record(run_id), sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    sha = "0" * 40
    result = _run(
        [
            str(SCRIPTS / "finalize_sandbox_ref.py"),
            "--run-id",
            run_id,
            "--sha",
            sha,
            "--run-records-dir",
            str(records_dir),
        ]
    )
    assert result.returncode == 0, (
        f"finalize_sandbox_ref failed: stdout={result.stdout!r} stderr={result.stderr!r}"
    )
    rewritten = json.loads(record_path.read_text(encoding="utf-8"))
    assert rewritten["sandbox_image_ref"] == f"repo://ai-field-brief@{sha}/"
    for entry in rewritten["inputs"]:
        assert "@PENDING/" not in entry["ref"]
        assert f"@{sha}/" in entry["ref"]
    for entry in rewritten["outputs"]:
        assert "@PENDING/" not in entry["artifact_id"]
        assert f"@{sha}/" in entry["artifact_id"]


def test_finalize_sandbox_ref_idempotent(tmp_path: pathlib.Path) -> None:
    records_dir = tmp_path / "run-records"
    records_dir.mkdir()
    run_id = "run-noopcheck001"
    sha = "f" * 40
    # Build a record that already names the real SHA — no PENDING left.
    record = _pending_record(run_id)
    record["sandbox_image_ref"] = f"repo://ai-field-brief@{sha}/"
    for entry in record["inputs"]:  # type: ignore[union-attr]
        entry["ref"] = entry["ref"].replace("@PENDING/", f"@{sha}/")
    for entry in record["outputs"]:  # type: ignore[union-attr]
        entry["artifact_id"] = entry["artifact_id"].replace(
            "@PENDING/", f"@{sha}/"
        )
    record_path = records_dir / f"{run_id}.json"
    record_path.write_text(
        json.dumps(record, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    before = record_path.read_text(encoding="utf-8")
    result = _run(
        [
            str(SCRIPTS / "finalize_sandbox_ref.py"),
            "--all",
            "--sha",
            sha,
            "--run-records-dir",
            str(records_dir),
        ]
    )
    assert result.returncode == 0
    after = record_path.read_text(encoding="utf-8")
    assert before == after


def test_finalize_sandbox_ref_refuses_bad_sha(tmp_path: pathlib.Path) -> None:
    records_dir = tmp_path / "run-records"
    records_dir.mkdir()
    result = _run(
        [
            str(SCRIPTS / "finalize_sandbox_ref.py"),
            "--all",
            "--sha",
            "not-a-sha",
            "--run-records-dir",
            str(records_dir),
        ]
    )
    assert result.returncode == 1
    assert "non-SHA" in (result.stdout + result.stderr)
