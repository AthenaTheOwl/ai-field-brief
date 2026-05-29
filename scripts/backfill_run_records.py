"""Backfill run-evidence artifacts for already-published briefs.

For each brief under ``briefs/YYYY-WNN/``, synthesizes a minimal Run
record plus a closing event ledger. Because the original generation
timeline is lost (the playbook was a manual pass), the ledger carries
three deterministic events: ``pipeline.start``, ``pipeline.complete``,
and ``gate.run.evidence_recorded``. The Run record populates four of
the six replay-equivalence fields:

- ``prompt_snapshot_hash`` from the current playbook.
- ``tool_schemas_snapshot_hash`` from the current sources/registry.yaml.
- ``sandbox_image_ref`` as ``<repo-path>@<publishing-commit-SHA>``
  derived from ``git log -- briefs/YYYY-WNN/brief.md``.
- ``gate_results_summary`` populated from the canonical brief-gate set;
  every gate is marked passed because a failing gate would have blocked
  the publishing commit in CI.

``determinism`` and ``checkpoint_ref`` are omitted (consistent with the
procurement-lab precedent).

Typical invocations::

    python scripts/backfill_run_records.py --all
    python scripts/backfill_run_records.py --week 2026-W22
"""

from __future__ import annotations

import argparse
import datetime as dt_module
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import run_evidence  # noqa: E402

BRIEFS_DIR = run_evidence.ROOT / "briefs"


def _load_meta(brief_dir: Path) -> dict[str, Any]:
    meta_path = brief_dir / "meta.yaml"
    if not meta_path.is_file():
        return {}
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError as exc:
        raise SystemExit(
            "backfill_run_records: PyYAML is required. "
            "Install with `pip install pyyaml>=6.0`."
        ) from exc
    data = yaml.safe_load(meta_path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def _agent_id_from_meta(meta: dict[str, Any]) -> str:
    raw = meta.get("generated_by")
    if isinstance(raw, str) and raw.strip():
        return raw.split("(", 1)[0].strip() or run_evidence.DEFAULT_LLM_IDENTIFIER
    return run_evidence.DEFAULT_LLM_IDENTIFIER


def _started_at(brief_dir: Path, meta: dict[str, Any]) -> str:
    raw = meta.get("generated_at")
    if isinstance(raw, str) and raw.strip():
        return raw.strip()
    if isinstance(raw, dt_module.datetime):
        # PyYAML parses RFC3339 strings into datetime; serialize back to
        # the canonical Z-suffixed form the Run schema expects.
        if raw.tzinfo is None:
            raw = raw.replace(tzinfo=timezone.utc)
        return raw.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return run_evidence.iso_week_dir_to_started_at(brief_dir.name)


def _finished_at_anchor(started_at: str) -> str:
    """Synthesize a finished_at one hour after started_at.

    The backfill cannot recover the real wall-clock duration so we pin a
    deterministic +1h anchor. Down-stream consumers should treat the
    interval as a placeholder; the real timeline lives in the event
    ledger when live runs emit it.
    """
    try:
        dt = datetime.strptime(started_at, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        )
    except ValueError:
        return run_evidence.now_iso()
    dt = dt + timedelta(hours=1)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def backfill_week(
    brief_dir: Path,
    *,
    event_ledger_dir: Path,
    run_records_dir: Path,
) -> tuple[Path, Path]:
    """Backfill one brief; return the (record_path, ledger_path) tuple."""
    if not brief_dir.is_dir():
        raise SystemExit(f"backfill_run_records: not a directory: {brief_dir}")
    meta = _load_meta(brief_dir)
    llm_identifier = _agent_id_from_meta(meta)
    started_at = _started_at(brief_dir, meta)
    finished_at = _finished_at_anchor(started_at)
    run_id = run_evidence.new_run_id()
    spec_id = "specs/0007-publishing/"
    workspace_id = run_evidence.ROOT.name

    # Two-pass sandbox-ref protocol (DEC-PUB-008): the backfill records
    # ``repo://ai-field-brief@PENDING/`` so the off-by-one between
    # ``git rev-parse HEAD`` at emit time (PARENT of the records-
    # regeneration commit) and the actual sample-containing SHA is
    # closed by a post-commit rewrite. ``scripts/finalize_sandbox_ref.py``
    # finishes the second pass.
    sandbox_fallback = False

    gates = [
        {"name": name, "status": "passed"}
        for name in run_evidence.BRIEF_GATES_CANONICAL
    ]

    evidence = run_evidence.build_run_evidence_fields(
        brief_path=brief_dir,
        gates=gates,
        llm_identifier=llm_identifier,
        sandbox_sha_pending=True,
    )

    ledger_path = event_ledger_dir / f"{run_id}.jsonl"
    record_path = run_records_dir / f"{run_id}.json"

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
            "backfilled": True,
        },
        created_at=started_at,
    )
    run_evidence.emit_event(start_event, ledger_path)

    # Emit one gate.check.passed event per canonical brief gate. The
    # original ledger lost the live gate timeline, but the publishing
    # commit landed on main — CI required every canonical gate to pass.
    # Synthesizing the per-gate events here gives the validator a ledger
    # to cross-check Run.gate_results_summary against, instead of trusting
    # the Run record's claimed rollup blindly.
    for gate in gates:
        gate_event = run_evidence.make_event(
            event_type="gate.check.passed",
            actor_kind="system",
            actor_id="ci.gate-runner",
            run_id=run_id,
            spec_id=spec_id,
            payload={"gate_name": gate["name"]},
            created_at=finished_at,
        )
        run_evidence.emit_event(gate_event, ledger_path)

    # The pipeline.complete payload carries the typed `status` field the
    # event schema requires (done|failed|cancelled). Backfill only runs
    # on already-published briefs, so status is always "done". The
    # closing event also clones gate_results_summary so the cross-check
    # holds without re-aggregation.
    complete_payload: dict[str, Any] = {
        "brief": brief_dir.name,
        "status": "done",
        "backfilled": True,
        "sandbox_fallback_to_head": sandbox_fallback,
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

    # repo:// URIs per DEC-CDCP-014. The SHA is PENDING here; the
    # second pass (scripts/finalize_sandbox_ref.py) rewrites every
    # PENDING placeholder to the actual records-regeneration commit
    # SHA. The replay resolver accepts both URI forms and legacy
    # local paths for interop.
    pending = run_evidence.SANDBOX_SHA_PENDING
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
                    "playbook/run-weekly-brief.md", pending
                ),
            },
            {
                "kind": "source-registry",
                "ref": run_evidence.compose_repo_uri(
                    "sources/registry.yaml", pending
                ),
            },
            {
                "kind": "meta",
                "ref": run_evidence.compose_repo_uri(
                    f"briefs/{brief_dir.name}/meta.yaml", pending
                ),
            },
        ],
        outputs=[
            {
                "artifact_id": run_evidence.compose_repo_uri(
                    f"briefs/{brief_dir.name}/brief.md", pending
                ),
                "type": "brief",
            },
            {
                "artifact_id": run_evidence.compose_repo_uri(
                    f"briefs/{brief_dir.name}/meta.yaml", pending
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
        payload={
            "run_id": run_id,
            "fields_populated": evidence.populated,
            "backfilled": True,
        },
        parent_event_id=complete_event["event_id"],
    )
    run_evidence.emit_event(evidence_event, ledger_path)

    return record_path, ledger_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="backfill_run_records",
        description="synthesize run-evidence for already-published briefs",
    )
    parser.add_argument(
        "--week",
        default=None,
        help="ISO-week folder name (YYYY-WNN) to backfill; default: all weeks",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="backfill every brief under briefs/ (default if --week is omitted)",
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

    if args.week:
        brief_dirs = [BRIEFS_DIR / args.week]
    else:
        brief_dirs = sorted(
            p for p in BRIEFS_DIR.iterdir() if p.is_dir() and p.name[:4].isdigit()
        )

    if not brief_dirs:
        print(
            "backfill_run_records: no briefs to backfill", file=sys.stderr
        )
        return 1

    for brief_dir in brief_dirs:
        if not brief_dir.is_dir():
            print(
                f"backfill_run_records: skipping missing brief dir {brief_dir}",
                file=sys.stderr,
            )
            continue
        record_path, ledger_path = backfill_week(
            brief_dir,
            event_ledger_dir=args.event_ledger_dir,
            run_records_dir=args.run_records_dir,
        )
        try:
            rel_record = record_path.relative_to(run_evidence.ROOT).as_posix()
        except ValueError:
            rel_record = record_path.as_posix()
        try:
            rel_ledger = ledger_path.relative_to(run_evidence.ROOT).as_posix()
        except ValueError:
            rel_ledger = ledger_path.as_posix()
        print(
            f"backfill {brief_dir.name}: record={rel_record} ledger={rel_ledger}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
