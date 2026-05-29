"""Tests for the run-evidence emitter library.

Covers the library surface in ``scripts/run_evidence.py``:

- canonicalize_prompt is stable across calls with same input.
- canonicalize_tool_surface is stable.
- compute_sha256 produces 64-char lowercase hex.
- emit_event writes valid JSONL conformant to event.schema.json.
- emit_run writes valid JSON conformant to run.schema.json (with the
  new replay-equivalence fields).
- aggregate_gate_results handles event and plain-mapping shapes.
- parse_gates_arg parses the CLI-style string.

End-to-end coverage that exercises the CLIs lives in
``tests/scripts/test_run_evidence_cli.py``.
"""

from __future__ import annotations

import json
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"

sys.path.insert(0, str(SCRIPTS))

import run_evidence  # noqa: E402


def test_canonicalize_prompt_is_stable() -> None:
    a = run_evidence.canonicalize_prompt("hello", ["e1"], ["s1"])
    b = run_evidence.canonicalize_prompt("hello", ["e1"], ["s1"])
    assert a == b
    c = run_evidence.canonicalize_prompt("hello", ["e1"], ["s2"])
    assert a != c


def test_canonicalize_tool_surface_is_stable() -> None:
    a = run_evidence.canonicalize_tool_surface(
        "version: 1\n", "claude-opus-4-7", {"k": 1}
    )
    b = run_evidence.canonicalize_tool_surface(
        "version: 1\n", "claude-opus-4-7", {"k": 1}
    )
    assert a == b
    c = run_evidence.canonicalize_tool_surface(
        "version: 1\n", "claude-opus-4-7", {"k": 2}
    )
    assert a != c


def test_compute_sha256_shape() -> None:
    digest = run_evidence.compute_sha256("anything")
    assert len(digest) == 64
    assert all(ch in "0123456789abcdef" for ch in digest)


def test_emit_event_writes_valid_jsonl(tmp_path: pathlib.Path) -> None:
    ledger = tmp_path / "ledger" / "run-abc.jsonl"
    # The cross-repo event schema enforces typed payloads on
    # pipeline.start (prompt_snapshot_hash + tool_schemas_snapshot_hash
    # are required); we pass real-shaped hashes so the writer's
    # schema-validation step accepts the record.
    event = run_evidence.make_event(
        event_type="pipeline.start",
        actor_kind="role",
        actor_id="product.brief-author",
        payload={
            "brief": "2026-W22",
            "prompt_snapshot_hash": "a" * 64,
            "tool_schemas_snapshot_hash": "b" * 64,
        },
        run_id="run-abcabcabcabc",
        spec_id="specs/0007-publishing/",
    )
    run_evidence.emit_event(event, ledger)
    text = ledger.read_text(encoding="utf-8")
    assert text.endswith("\n")
    line = text.rstrip("\n")
    parsed = json.loads(line)
    assert parsed["type"] == "pipeline.start"
    assert parsed["run_id"] == "run-abcabcabcabc"
    assert parsed["payload"]["brief"] == "2026-W22"


def test_emit_run_writes_valid_record(tmp_path: pathlib.Path) -> None:
    record_path = tmp_path / "run-xyz.json"
    fields = run_evidence.build_run_evidence_fields(
        head_sha="0" * 40,
        gates=[
            {"name": "voice_lint", "status": "passed"},
            {"name": "spec_check", "status": "passed"},
        ],
    )
    run = run_evidence.assemble_run_record(
        run_id="run-deadbeefdead",
        spec_id="specs/0007-publishing/",
        agent_id="claude-opus-4-7",
        runtime="claude-code-cli",
        workspace_id="ai-field-brief",
        started_at="2026-05-25T15:00:00Z",
        finished_at="2026-05-25T16:00:00Z",
        status="done",
        inputs=[{"kind": "playbook", "ref": "playbook/run-weekly-brief.md"}],
        outputs=[{"artifact_id": "briefs/2026-W22/brief.md"}],
        evidence_fields=fields.fields,
    )
    run_evidence.emit_run(run, record_path)
    parsed = json.loads(record_path.read_text(encoding="utf-8"))
    assert parsed["id"] == "run-deadbeefdead"
    assert parsed["status"] == "done"
    assert "prompt_snapshot_hash" in parsed
    assert "tool_schemas_snapshot_hash" in parsed
    assert "sandbox_image_ref" in parsed
    # DEC-CDCP-014 portable URI: derive_sandbox_image_ref now emits
    # repo://ai-field-brief@<sha>/ rather than the legacy <abs-path>@<sha>.
    assert parsed["sandbox_image_ref"].startswith("repo://ai-field-brief@")
    assert parsed["sandbox_image_ref"].endswith("/")
    assert parsed["gate_results_summary"]["all_passed"] is True


def test_emit_run_rejects_bad_record(tmp_path: pathlib.Path) -> None:
    bad = {
        "id": "run-x",
        # missing required spec_id and other fields
        "agent_id": "claude-opus-4-7",
    }
    with pytest.raises(ValueError):
        run_evidence.emit_run(bad, tmp_path / "bad.json")


def test_aggregate_gate_results_event_shape() -> None:
    events = [
        {
            "type": "gate.check.passed",
            "payload": {"gate_name": "voice_lint"},
        },
        {
            "type": "gate.check.failed",
            "payload": {"gate_name": "spec_check"},
        },
        {"type": "other.event", "payload": {}},
    ]
    summary = run_evidence.aggregate_gate_results(events)
    assert summary is not None
    assert summary["gates_passed"] == ["voice_lint"]
    assert summary["gates_failed"] == ["spec_check"]
    assert summary["all_passed"] is False


def test_aggregate_gate_results_empty_returns_none() -> None:
    assert run_evidence.aggregate_gate_results([]) is None


def test_parse_gates_arg() -> None:
    gates = run_evidence.parse_gates_arg(
        "voice_lint:passed,spec_check:passed,check_no_bom"
    )
    names = [g["name"] for g in gates]
    assert names == ["voice_lint", "spec_check", "check_no_bom"]
    assert gates[2]["status"] == "passed"


# ----------------------------------------------------------------- DEC-CDCP-014 URIs


def test_compose_repo_uri_round_trip() -> None:
    """compose_repo_uri emits the DEC-CDCP-014 grammar exactly."""
    sha = "a" * 40
    uri = run_evidence.compose_repo_uri("playbook/run-weekly-brief.md", sha)
    assert uri == f"repo://ai-field-brief@{sha}/playbook/run-weekly-brief.md"


def test_compose_repo_uri_strips_leading_slash() -> None:
    sha = "a" * 40
    uri = run_evidence.compose_repo_uri("/playbook/run-weekly-brief.md", sha)
    assert uri == f"repo://ai-field-brief@{sha}/playbook/run-weekly-brief.md"


def test_compose_repo_uri_accepts_pending_placeholder() -> None:
    uri = run_evidence.compose_repo_uri("briefs/2026-W22/brief.md", "PENDING")
    assert uri == "repo://ai-field-brief@PENDING/briefs/2026-W22/brief.md"


def test_compose_artifact_uri_round_trip() -> None:
    uri = run_evidence.compose_artifact_uri("watchlist-packet@run-abc")
    assert uri == "artifact://ai-field-brief/watchlist-packet@run-abc"


def test_resolve_uri_repo_form() -> None:
    sha = "f" * 40
    uri = f"repo://ai-field-brief@{sha}/playbook/run-weekly-brief.md"
    resolved = run_evidence.resolve_uri(
        uri, portfolio_root=pathlib.Path("/tmp/portfolio")
    )
    assert resolved == pathlib.Path(
        "/tmp/portfolio/ai-field-brief/playbook/run-weekly-brief.md"
    )


def test_resolve_uri_artifact_form_returns_none() -> None:
    uri = "artifact://ai-field-brief/watchlist-packet@run-abc"
    assert (
        run_evidence.resolve_uri(uri, portfolio_root=pathlib.Path("/tmp/portfolio"))
        is None
    )


def test_resolve_uri_legacy_path_returned_unchanged() -> None:
    legacy = "briefs/2026-W22/brief.md"
    resolved = run_evidence.resolve_uri(
        legacy, portfolio_root=pathlib.Path("/tmp/portfolio")
    )
    assert resolved == pathlib.Path(legacy)


def test_resolve_uri_malformed_treated_as_legacy() -> None:
    bogus = "repo://not-a-real-uri-without-sha"
    resolved = run_evidence.resolve_uri(
        bogus, portfolio_root=pathlib.Path("/tmp/portfolio")
    )
    # Does not match either scheme; treated as legacy Path.
    assert resolved == pathlib.Path(bogus)


def test_derive_sandbox_image_ref_uses_portable_uri() -> None:
    sha = "c" * 40
    ref = run_evidence.derive_sandbox_image_ref(head_sha=sha)
    assert ref == f"repo://ai-field-brief@{sha}/"


def test_parse_sandbox_sha_handles_both_forms() -> None:
    sha = "9" * 40
    legacy = f"E:/claude_code/random-apps/ai-field-brief@{sha}"
    portable = f"repo://ai-field-brief@{sha}/"
    assert run_evidence.parse_sandbox_sha(legacy) == sha
    assert run_evidence.parse_sandbox_sha(portable) == sha
    assert (
        run_evidence.parse_sandbox_sha("repo://ai-field-brief@PENDING/")
        == "PENDING"
    )


def test_build_run_evidence_fields_pending_placeholder() -> None:
    """sandbox_sha_pending mode emits the PENDING placeholder URI."""
    fields = run_evidence.build_run_evidence_fields(
        gates=[{"name": "voice_lint", "status": "passed"}],
        sandbox_sha_pending=True,
    )
    assert fields.fields["sandbox_image_ref"] == "repo://ai-field-brief@PENDING/"
