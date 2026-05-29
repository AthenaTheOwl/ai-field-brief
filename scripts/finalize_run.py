"""Finalize a live brief-generation run and emit run-evidence artifacts.

The playbook at ``playbook/run-weekly-brief.md`` calls this CLI at the
publish step (between voice-lint and commit). It reads the brief's
``meta.yaml``, computes the replay-equivalence hashes, writes a final
Run record under ``ops/run-records/<run-id>.json``, and appends closing
events to ``ops/event-ledger/<run-id>.jsonl``.

Typical invocation::

    python scripts/finalize_run.py \
        --brief briefs/2026-W23/ \
        --gates "voice_lint:passed,spec_check:passed,check_no_bom:passed"

Use ``--run-id`` to supply a stable id when the agent kicked off the
run earlier and recorded a ``pipeline.start`` event with the same id.
Without ``--run-id`` the CLI mints a fresh one.

The CLI is offline: it talks only to the local filesystem and ``git``.
"""

from __future__ import annotations

import argparse
import datetime as dt_module
import sys
from datetime import timezone
from pathlib import Path
from typing import Any

# Make the sibling library importable when invoked as a script.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import run_evidence  # noqa: E402


def _load_meta(brief_dir: Path) -> dict[str, Any]:
    meta_path = brief_dir / "meta.yaml"
    if not meta_path.is_file():
        raise SystemExit(
            f"finalize_run: meta.yaml missing under {brief_dir}. "
            f"Write the meta log before finalizing."
        )
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError as exc:
        raise SystemExit(
            "finalize_run: PyYAML is required. "
            "Install with `pip install pyyaml>=6.0`."
        ) from exc
    data = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(
            f"finalize_run: meta.yaml under {brief_dir} did not parse as a mapping"
        )
    return data


def _agent_id_from_meta(meta: dict[str, Any]) -> str:
    """Pick the model id off ``generated_by`` (e.g. ``claude-opus-4-7 (manual playbook run)``)."""
    raw = meta.get("generated_by")
    if not isinstance(raw, str) or not raw.strip():
        return run_evidence.DEFAULT_LLM_IDENTIFIER
    head = raw.split("(", 1)[0].strip()
    return head or run_evidence.DEFAULT_LLM_IDENTIFIER


def _started_at_from_meta(meta: dict[str, Any], brief_dir: Path) -> str:
    raw = meta.get("generated_at")
    if isinstance(raw, str) and raw.strip():
        return raw.strip()
    if isinstance(raw, dt_module.datetime):
        if raw.tzinfo is None:
            raw = raw.replace(tzinfo=timezone.utc)
        return raw.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return run_evidence.iso_week_dir_to_started_at(brief_dir.name)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="finalize_run",
        description="emit run-evidence for a published brief",
    )
    parser.add_argument(
        "--brief",
        type=Path,
        required=True,
        help="path to briefs/YYYY-WNN/ for the run being finalized",
    )
    parser.add_argument(
        "--run-id",
        default=None,
        help="explicit run_id; defaults to a freshly minted run-<12hex>",
    )
    parser.add_argument(
        "--gates",
        default=None,
        help=(
            "comma-separated gate results: voice_lint:passed,spec_check:passed,..."
            " defaults to BRIEF_GATES_CANONICAL all passed"
        ),
    )
    parser.add_argument(
        "--llm",
        default=None,
        help="LLM identifier (default: parsed from meta.generated_by or claude-opus-4-7)",
    )
    parser.add_argument(
        "--head-sha",
        default=None,
        help="override repo HEAD SHA (default: derived from `git rev-parse HEAD`)",
    )
    parser.add_argument(
        "--sandbox-pending",
        action="store_true",
        help=(
            "write sandbox_image_ref as repo://ai-field-brief@PENDING/ so "
            "scripts/finalize_sandbox_ref.py can rewrite to the actual "
            "sample-containing commit SHA after the records land "
            "(closes the emit-time HEAD off-by-one; see DEC-PUB-008)"
        ),
    )
    parser.add_argument(
        "--event-ledger-dir",
        type=Path,
        default=run_evidence.EVENT_LEDGER_DIR,
        help="override the event ledger directory (default: ops/event-ledger/)",
    )
    parser.add_argument(
        "--run-records-dir",
        type=Path,
        default=run_evidence.RUN_RECORDS_DIR,
        help="override the run records directory (default: ops/run-records/)",
    )
    args = parser.parse_args(argv)

    brief_dir: Path = args.brief.resolve()
    if not brief_dir.is_dir():
        print(
            f"finalize_run: brief directory not found: {brief_dir}",
            file=sys.stderr,
        )
        return 1

    meta = _load_meta(brief_dir)
    llm_identifier = args.llm or _agent_id_from_meta(meta)
    started_at = _started_at_from_meta(meta, brief_dir)
    finished_at = run_evidence.now_iso()
    run_id = args.run_id or run_evidence.new_run_id()
    spec_id = "specs/0007-publishing/"
    workspace_id = run_evidence.ROOT.name

    gates_spec = run_evidence.parse_gates_arg(args.gates)
    if not gates_spec:
        gates_spec = [
            {"name": name, "status": "passed"}
            for name in run_evidence.BRIEF_GATES_CANONICAL
        ]

    head_sha = args.head_sha or run_evidence.current_head_sha()

    evidence = run_evidence.build_run_evidence_fields(
        head_sha=head_sha,
        gates=gates_spec,
        llm_identifier=llm_identifier,
        sandbox_sha_pending=args.sandbox_pending,
    )

    ledger_path: Path = args.event_ledger_dir / f"{run_id}.jsonl"
    record_path: Path = args.run_records_dir / f"{run_id}.json"

    # Opening events. We re-emit pipeline.start with the canonical
    # hashes so the ledger is self-contained even if the live agent did
    # not write a start event earlier.
    start_event = run_evidence.make_event(
        event_type="pipeline.start",
        actor_kind=run_evidence.BRIEF_ACTOR_KIND,
        actor_id=run_evidence.BRIEF_ACTOR_ID,
        run_id=run_id,
        spec_id=spec_id,
        payload={
            "brief": brief_dir.name,
            "iso_week": meta.get("iso_week"),
            "title": meta.get("title"),
            "prompt_snapshot_hash": evidence.fields["prompt_snapshot_hash"],
            "tool_schemas_snapshot_hash": evidence.fields[
                "tool_schemas_snapshot_hash"
            ],
            "llm": llm_identifier,
        },
        created_at=started_at,
    )
    run_evidence.emit_event(start_event, ledger_path)

    for gate in gates_spec:
        passed = gate.get("status", "passed").lower() in {
            "passed",
            "pass",
            "ok",
            "true",
        }
        gate_payload: dict[str, Any] = {"gate_name": gate["name"]}
        if not passed:
            # The schema requires `reason` on gate.check.failed; the CLI
            # gates string does not carry one, so we name the missing
            # context rather than fabricating it.
            gate_payload["reason"] = gate.get("reason") or (
                "gate marked failed via --gates argument"
            )
        gate_event = run_evidence.make_event(
            event_type="gate.check.passed" if passed else "gate.check.failed",
            actor_kind="system",
            actor_id="ci.gate-runner",
            run_id=run_id,
            spec_id=spec_id,
            payload=gate_payload,
        )
        run_evidence.emit_event(gate_event, ledger_path)

    # The pipeline.complete payload carries the typed `status` field
    # required by event.schema.json (one of done|failed|cancelled). A
    # finalize call only fires on a successful publish, so status is
    # always "done" here; live failures stop short of finalize. We also
    # clone gate_results_summary into the closing event so the consumer
    # can cross-check the Run record's claimed rollup against the ledger
    # without re-aggregating gate events.
    complete_payload: dict[str, Any] = {
        "brief": brief_dir.name,
        "status": "done",
    }
    summary = evidence.fields.get("gate_results_summary")
    if isinstance(summary, dict):
        complete_payload["gate_results_summary"] = summary
    complete_event = run_evidence.make_event(
        event_type="pipeline.complete",
        actor_kind=run_evidence.BRIEF_ACTOR_KIND,
        actor_id=run_evidence.BRIEF_ACTOR_ID,
        run_id=run_id,
        spec_id=spec_id,
        payload=complete_payload,
        parent_event_id=start_event["event_id"],
        created_at=finished_at,
    )
    run_evidence.emit_event(complete_event, ledger_path)

    # repo:// URIs per DEC-CDCP-014. The SHA tracks
    # ``sandbox_image_ref``: when ``--sandbox-pending`` is in effect
    # every URI carries the PENDING placeholder and
    # ``scripts/finalize_sandbox_ref.py`` rewrites them in lockstep
    # after the records-containing commit lands.
    if args.sandbox_pending:
        uri_sha = run_evidence.SANDBOX_SHA_PENDING
    else:
        uri_sha = (
            head_sha
            if head_sha and head_sha.strip()
            else run_evidence.SANDBOX_SHA_PENDING
        )
    record = run_evidence.assemble_run_record(
        run_id=run_id,
        spec_id=spec_id,
        agent_id=llm_identifier,
        runtime="claude-code-cli",
        workspace_id=workspace_id,
        started_at=started_at,
        finished_at=finished_at,
        status="done",
        inputs=[
            {
                "kind": "playbook",
                "ref": run_evidence.compose_repo_uri(
                    "playbook/run-weekly-brief.md", uri_sha
                ),
            },
            {
                "kind": "source-registry",
                "ref": run_evidence.compose_repo_uri(
                    "sources/registry.yaml", uri_sha
                ),
            },
            {
                "kind": "meta",
                "ref": run_evidence.compose_repo_uri(
                    f"briefs/{brief_dir.name}/meta.yaml", uri_sha
                ),
            },
        ],
        outputs=[
            {
                "artifact_id": run_evidence.compose_repo_uri(
                    f"briefs/{brief_dir.name}/brief.md", uri_sha
                ),
                "type": "brief",
            },
            {
                "artifact_id": run_evidence.compose_repo_uri(
                    f"briefs/{brief_dir.name}/meta.yaml", uri_sha
                ),
                "type": "meta",
            },
        ],
        evidence_fields=evidence.fields,
    )
    run_evidence.emit_run(record, record_path)

    evidence_event = run_evidence.make_event(
        event_type="gate.run.evidence_recorded",
        actor_kind="system",
        actor_id="ci.run-evidence",
        run_id=run_id,
        spec_id=spec_id,
        payload={"run_id": run_id, "fields_populated": evidence.populated},
        parent_event_id=complete_event["event_id"],
    )
    run_evidence.emit_event(evidence_event, ledger_path)

    try:
        rel_record = record_path.relative_to(run_evidence.ROOT).as_posix()
    except ValueError:
        rel_record = record_path.as_posix()
    try:
        rel_ledger = ledger_path.relative_to(run_evidence.ROOT).as_posix()
    except ValueError:
        rel_ledger = ledger_path.as_posix()
    print(
        f"finalize_run OK: run_id={run_id} brief={brief_dir.name} "
        f"record={rel_record} ledger={rel_ledger}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
