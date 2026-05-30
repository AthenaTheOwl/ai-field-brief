"""Frontier-scout runner. Fetches sources, snapshots bytes, emits Run-evidence.

Producer side of the scout discipline captured in DEC-SRC-021. Walks the
``frontier-scout`` lane (or an explicit ``--source-ids`` subset) of
``sources/registry.yaml``, fetches each URL via stdlib ``urllib.request``,
records a SHA-256 over the response bytes, and writes:

- one snapshot file per source under ``ops/scout-snapshots/<run-id>/<source-id>.html``
- one sandbox manifest at ``ops/sandbox-manifests/<run-id>.json``
- one RunState checkpoint at ``ops/checkpoints/<run-id>.runstate.json`` carrying
  ``status=awaiting_lens_application`` so the downstream agent knows the
  artifact list is ready for lens application
- one Run record at ``ops/run-records/<run-id>.json`` and an event ledger at
  ``ops/event-ledger/<run-id>.jsonl`` via the existing ``run_evidence``
  emitter helpers

This runner is deterministic at the fetch + hash layer only. It does NOT
apply scout lenses (an agentic step) and it does NOT produce Action
packets (Phase 3). Lens application reads the snapshot bytes the runner
froze plus the lens prompts under ``prompts/lenses/`` to emit those
artifacts in a separate pass.

Usage::

    python scripts/scout_runner.py --lane frontier-scout
    python scripts/scout_runner.py --source-ids e2b-github,pydantic-ai-github,mastra-github

Source failures (404, anti-bot blocks, timeouts) are logged and recorded
in the Run record's ``failed_sources`` field on the ``pipeline.complete``
event payload so the next pass can decide whether to retry or drop the
source.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Make the sibling library importable when invoked as a script.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import run_evidence  # noqa: E402

ROOT = run_evidence.ROOT
SCOUT_SNAPSHOTS_DIR = ROOT / "ops" / "scout-snapshots"
SANDBOX_MANIFESTS_DIR = ROOT / "ops" / "sandbox-manifests"
CHECKPOINTS_DIR = ROOT / "ops" / "checkpoints"

RUNTIME_PROVIDER = "ai-field-brief-scout-runner"
MANIFEST_VERSION = "1.0"
USER_AGENT = "ai-field-brief-scout-runner/1.0 (+https://github.com/anthropics)"
DEFAULT_LANE = "frontier-scout"
DEFAULT_LENS_IDS = ("source_arbitrage", "repo_project_scan", "action_packet")
SCOUT_SPEC_ID = "specs/0002-source-registry/"
SCOUT_ACTOR_KIND = "role"
SCOUT_ACTOR_ID = "scout.runner"
FETCH_TIMEOUT_SECONDS = 30


def now_iso_micro() -> str:
    """Return current UTC time with microsecond resolution per portfolio convention."""
    return datetime.now(timezone.utc).isoformat()


def new_scout_run_id() -> str:
    """Return a fresh scout run id of the shape ``run-scout-<12hex>``."""
    import uuid

    return f"run-scout-{uuid.uuid4().hex[:12]}"


def sha256_bytes(data: bytes) -> str:
    """Return lowercase hex SHA-256 digest of ``data``."""
    return hashlib.sha256(data).hexdigest()


def parse_source_ids(spec: str | None) -> list[str]:
    """Parse a comma-separated source-ids argument into a deduplicated list."""
    if not spec:
        return []
    out: list[str] = []
    seen: set[str] = set()
    for token in spec.split(","):
        sid = token.strip()
        if not sid or sid in seen:
            continue
        seen.add(sid)
        out.append(sid)
    return out


def load_registry(registry_path: Path) -> dict[str, Any]:
    """Load the source registry YAML and return its parsed mapping."""
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError as exc:
        raise SystemExit(
            "scout_runner: PyYAML is required. Install with `pip install pyyaml>=6.0`."
        ) from exc
    data = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(
            f"scout_runner: registry at {registry_path} did not parse as a mapping"
        )
    return data


def select_sources(
    registry: dict[str, Any],
    *,
    lane: str | None,
    source_ids: list[str],
) -> list[dict[str, Any]]:
    """Filter sources by lane or explicit ids; preserve registry order."""
    all_sources = registry.get("sources") or []
    if not isinstance(all_sources, list):
        raise SystemExit("scout_runner: registry.sources is not a list")
    if source_ids:
        wanted = set(source_ids)
        return [s for s in all_sources if isinstance(s, dict) and s.get("id") in wanted]
    if lane:
        return [s for s in all_sources if isinstance(s, dict) and s.get("lane") == lane]
    return []


def fetch_source(
    url: str, *, timeout: int = FETCH_TIMEOUT_SECONDS
) -> tuple[bytes, int | None, str | None]:
    """Fetch ``url`` returning (body, http_status, error_message_or_none).

    Returns ``(b"", status_or_none, error_message)`` on failure so the
    caller can record the failure in the Run record without an exception
    abort. Anti-bot blocks (403, 429) and transient 5xx errors all map
    to the failure tuple shape; status is preserved when available.
    """
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(  # noqa: S310 - registry urls are vetted
            request, timeout=timeout
        ) as response:
            body = response.read()
            status = getattr(response, "status", None)
            return body, status, None
    except urllib.error.HTTPError as exc:
        return b"", exc.code, f"HTTPError {exc.code}: {exc.reason}"
    except urllib.error.URLError as exc:
        return b"", None, f"URLError: {exc.reason}"
    except (TimeoutError, ConnectionError, OSError) as exc:
        return b"", None, f"{type(exc).__name__}: {exc}"


def snapshot_source(
    source: dict[str, Any],
    *,
    snapshot_dir: Path,
    timeout: int = FETCH_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    """Fetch one source, write the snapshot file, return a record dict.

    The record carries either ``sha256`` + ``snapshot_path`` for a
    successful fetch or ``error`` + ``http_status`` for a failure. Either
    way the caller appends it to the per-source list emitted on the
    pipeline.complete event payload.
    """
    source_id = source.get("id") or ""
    url = source.get("url") or ""
    record: dict[str, Any] = {
        "source_id": source_id,
        "url": url,
        "fetched_at": now_iso_micro(),
    }
    if not source_id or not url:
        record["error"] = "missing id or url"
        return record
    body, status, error = fetch_source(url, timeout=timeout)
    if status is not None:
        record["http_status"] = status
    if error is not None or not body:
        record["error"] = error or "empty body"
        return record
    digest = sha256_bytes(body)
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    snapshot_path = snapshot_dir / f"{source_id}.html"
    snapshot_path.write_bytes(body)
    record["sha256"] = digest
    record["bytes"] = len(body)
    record["snapshot_path"] = snapshot_path.resolve().as_posix()
    return record


def build_sandbox_manifest(
    *,
    run_id: str,
    snapshot_dir: Path,
    source_ids: list[str],
) -> dict[str, Any]:
    """Assemble the sandbox manifest dict written under ops/sandbox-manifests/."""
    return {
        "manifest_version": MANIFEST_VERSION,
        "run_id": run_id,
        "runtime_provider": RUNTIME_PROVIDER,
        "model": None,
        "mounts": [
            {
                "kind": "snapshot-dir",
                "ref": snapshot_dir.resolve().as_posix(),
                "mode": "ro",
            }
        ],
        "env_refs": [],
        "tool_surface": [{"tool_name": "webfetch"}],
        "source_ids": source_ids,
        "emitted_at": now_iso_micro(),
    }


def build_checkpoint(
    *,
    run_id: str,
    fetched_sources: list[str],
    lens_ids: list[str],
    failed_sources: list[str],
) -> dict[str, Any]:
    """Assemble the RunState checkpoint dict (``awaiting_lens_application``)."""
    return {
        "run_id": run_id,
        "fetched_sources": fetched_sources,
        "failed_sources": failed_sources,
        "lens_ids": lens_ids,
        "status": "awaiting_lens_application",
        "emitted_at": now_iso_micro(),
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    """Write ``payload`` as pretty-printed sorted JSON with a trailing newline."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def emit_run_evidence(
    *,
    run_id: str,
    started_at: str,
    finished_at: str,
    fetched_records: list[dict[str, Any]],
    failed_records: list[dict[str, Any]],
    snapshot_dir: Path,
    manifest_path: Path,
    checkpoint_path: Path,
    lens_ids: list[str],
    head_sha: str | None,
) -> tuple[Path, Path]:
    """Emit the Run record + event ledger via the run_evidence helpers.

    Returns (record_path, ledger_path) so the caller can print them.
    """
    ledger_path = run_evidence.EVENT_LEDGER_DIR / f"{run_id}.jsonl"
    record_path = run_evidence.RUN_RECORDS_DIR / f"{run_id}.json"

    evidence = run_evidence.build_run_evidence_fields(
        head_sha=head_sha,
        gates=[],
        llm_identifier=run_evidence.DEFAULT_LLM_IDENTIFIER,
    )

    start_event = run_evidence.make_event(
        event_type="pipeline.start",
        actor_kind=SCOUT_ACTOR_KIND,
        actor_id=SCOUT_ACTOR_ID,
        run_id=run_id,
        spec_id=SCOUT_SPEC_ID,
        payload={
            "runner": RUNTIME_PROVIDER,
            "source_count": len(fetched_records) + len(failed_records),
            "prompt_snapshot_hash": evidence.fields["prompt_snapshot_hash"],
            "tool_schemas_snapshot_hash": evidence.fields["tool_schemas_snapshot_hash"],
            "lens_ids": lens_ids,
        },
        created_at=started_at,
    )
    run_evidence.emit_event(start_event, ledger_path)

    for rec in fetched_records:
        tool_event = run_evidence.make_event(
            event_type="tool.call.completed",
            actor_kind="system",
            actor_id=RUNTIME_PROVIDER,
            run_id=run_id,
            spec_id=SCOUT_SPEC_ID,
            payload={
                "tool_name": "webfetch",
                "status": "ok",
            },
        )
        run_evidence.emit_event(tool_event, ledger_path)

    for rec in failed_records:
        tool_event = run_evidence.make_event(
            event_type="tool.call.completed",
            actor_kind="system",
            actor_id=RUNTIME_PROVIDER,
            run_id=run_id,
            spec_id=SCOUT_SPEC_ID,
            payload={
                "tool_name": "webfetch",
                "status": "error",
                "error": str(rec.get("error") or "unknown"),
            },
        )
        run_evidence.emit_event(tool_event, ledger_path)

    complete_event = run_evidence.make_event(
        event_type="pipeline.complete",
        actor_kind=SCOUT_ACTOR_KIND,
        actor_id=SCOUT_ACTOR_ID,
        run_id=run_id,
        spec_id=SCOUT_SPEC_ID,
        payload={
            "status": "done",
            "fetched_sources": [r["source_id"] for r in fetched_records],
            "failed_sources": [r["source_id"] for r in failed_records],
        },
        parent_event_id=start_event["event_id"],
        created_at=finished_at,
    )
    run_evidence.emit_event(complete_event, ledger_path)

    uri_sha = head_sha if head_sha and head_sha.strip() else run_evidence.SANDBOX_SHA_PENDING

    inputs: list[dict[str, str]] = [
        {
            "kind": "source-registry",
            "ref": run_evidence.compose_repo_uri("sources/registry.yaml", uri_sha),
        }
    ]
    outputs: list[dict[str, str]] = []
    for rec in fetched_records:
        sid = rec["source_id"]
        rel = f"ops/scout-snapshots/{run_id}/{sid}.html"
        outputs.append(
            {
                "artifact_id": run_evidence.compose_repo_uri(rel, uri_sha),
                "type": "scout-snapshot",
            }
        )
    outputs.append(
        {
            "artifact_id": run_evidence.compose_repo_uri(
                f"ops/sandbox-manifests/{run_id}.json", uri_sha
            ),
            "type": "sandbox-manifest",
        }
    )
    outputs.append(
        {
            "artifact_id": run_evidence.compose_repo_uri(
                f"ops/checkpoints/{run_id}.runstate.json", uri_sha
            ),
            "type": "checkpoint",
        }
    )

    evidence_fields = dict(evidence.fields)
    evidence_fields["checkpoint_ref"] = checkpoint_path.resolve().as_posix()

    record = run_evidence.assemble_run_record(
        run_id=run_id,
        spec_id=SCOUT_SPEC_ID,
        agent_id=RUNTIME_PROVIDER,
        runtime=RUNTIME_PROVIDER,
        workspace_id=ROOT.name,
        started_at=started_at,
        finished_at=finished_at,
        status="needs_review",
        inputs=inputs,
        outputs=outputs,
        evidence_fields=evidence_fields,
    )
    run_evidence.emit_run(record, record_path)

    evidence_event = run_evidence.make_event(
        event_type="gate.run.evidence_recorded",
        actor_kind="system",
        actor_id="ci.run-evidence",
        run_id=run_id,
        spec_id=SCOUT_SPEC_ID,
        payload={"run_id": run_id, "fields_populated": evidence.populated},
        parent_event_id=complete_event["event_id"],
    )
    run_evidence.emit_event(evidence_event, ledger_path)

    return record_path, ledger_path


def build_arg_parser() -> argparse.ArgumentParser:
    """Construct the argparse parser. Factored for testability."""
    parser = argparse.ArgumentParser(
        prog="scout_runner",
        description="Fetch frontier-scout sources, snapshot bytes, emit run-evidence.",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--lane",
        default=None,
        help=f"lane id to sweep (default: {DEFAULT_LANE!r} when no --source-ids)",
    )
    group.add_argument(
        "--source-ids",
        default=None,
        help="comma-separated source ids (overrides --lane)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "ops" / "scout-runs",
        help="directory for the human-readable run summary (default: ops/scout-runs/)",
    )
    parser.add_argument(
        "--registry",
        type=Path,
        default=run_evidence.SOURCES_REGISTRY_PATH,
        help="path to sources/registry.yaml (default: repo registry)",
    )
    parser.add_argument(
        "--lens-ids",
        default=",".join(DEFAULT_LENS_IDS),
        help="comma-separated lens ids recorded on the checkpoint",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=FETCH_TIMEOUT_SECONDS,
        help="per-source fetch timeout in seconds",
    )
    parser.add_argument(
        "--head-sha",
        default=None,
        help="override repo HEAD SHA (default: `git rev-parse HEAD`)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    source_ids = parse_source_ids(args.source_ids)
    lane = args.lane if (args.lane or source_ids) else DEFAULT_LANE

    registry = load_registry(args.registry)
    selected = select_sources(registry, lane=lane, source_ids=source_ids)
    if not selected:
        print(
            "scout_runner: no sources selected "
            f"(lane={lane!r}, source_ids={source_ids!r})",
            file=sys.stderr,
        )
        return 1

    run_id = new_scout_run_id()
    started_at = now_iso_micro()
    snapshot_dir = SCOUT_SNAPSHOTS_DIR / run_id
    manifest_path = SANDBOX_MANIFESTS_DIR / f"{run_id}.json"
    checkpoint_path = CHECKPOINTS_DIR / f"{run_id}.runstate.json"

    fetched: list[dict[str, Any]] = []
    failed: list[dict[str, Any]] = []
    for source in selected:
        rec = snapshot_source(source, snapshot_dir=snapshot_dir, timeout=args.timeout)
        if "sha256" in rec:
            fetched.append(rec)
            print(
                f"scout_runner: fetched {rec['source_id']} sha256={rec['sha256'][:12]} "
                f"bytes={rec.get('bytes', 0)}"
            )
        else:
            failed.append(rec)
            print(
                f"scout_runner: FAILED {rec.get('source_id', '?')} "
                f"error={rec.get('error', 'unknown')}",
                file=sys.stderr,
            )

    finished_at = now_iso_micro()

    manifest = build_sandbox_manifest(
        run_id=run_id,
        snapshot_dir=snapshot_dir,
        source_ids=[r["source_id"] for r in fetched],
    )
    write_json(manifest_path, manifest)

    lens_ids = [s for s in (args.lens_ids or "").split(",") if s.strip()]
    checkpoint = build_checkpoint(
        run_id=run_id,
        fetched_sources=[r["source_id"] for r in fetched],
        lens_ids=lens_ids,
        failed_sources=[r["source_id"] for r in failed],
    )
    write_json(checkpoint_path, checkpoint)

    head_sha = args.head_sha or run_evidence.current_head_sha()

    record_path, ledger_path = emit_run_evidence(
        run_id=run_id,
        started_at=started_at,
        finished_at=finished_at,
        fetched_records=fetched,
        failed_records=failed,
        snapshot_dir=snapshot_dir,
        manifest_path=manifest_path,
        checkpoint_path=checkpoint_path,
        lens_ids=lens_ids,
        head_sha=head_sha,
    )

    summary = {
        "run_id": run_id,
        "lane": lane,
        "fetched": [r["source_id"] for r in fetched],
        "failed": [
            {"source_id": r.get("source_id"), "error": r.get("error")}
            for r in failed
        ],
        "snapshot_dir": snapshot_dir.resolve().as_posix(),
        "manifest_path": manifest_path.resolve().as_posix(),
        "checkpoint_path": checkpoint_path.resolve().as_posix(),
        "run_record": record_path.resolve().as_posix(),
        "event_ledger": ledger_path.resolve().as_posix(),
        "started_at": started_at,
        "finished_at": finished_at,
    }
    args.out.mkdir(parents=True, exist_ok=True)
    write_json(args.out / f"{run_id}.summary.json", summary)

    print(
        f"scout_runner OK: run_id={run_id} fetched={len(fetched)} failed={len(failed)} "
        f"snapshot_dir={snapshot_dir.resolve().as_posix()}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
