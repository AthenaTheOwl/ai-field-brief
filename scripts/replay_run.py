"""Equivalence replay for a published brief Run.

Live LLM-agent re-execution of brief generation is not reproducible
(model state + wall-clock time + sampler nondeterminism), and the
backfilled samples have no live LLM call to re-make. Replay here
verifies that the recorded preconditions still hold at the recorded SHA
and that the brief artifacts exist + match their hashes if recorded.

What this CLI does:

1. Loads ``ops/run-records/<run-id>.json`` and the matching
   ``ops/event-ledger/<run-id>.jsonl``. Both must exist.
2. Reads ``sandbox_image_ref`` and extracts the recorded SHA. Compares
   to ``git rev-parse HEAD``. On any mismatch the CLI exits 1 with a
   ``git checkout <sha>`` instruction so the operator can re-run at the
   correct point.
3. Re-computes ``prompt_snapshot_hash`` against the current playbook +
   prompts using the same canonicalization the emitter uses
   (``scripts/run_evidence.py``). Compares to the recorded value.
4. Re-computes ``tool_schemas_snapshot_hash`` against the current
   source registry + extraction schema + active LLM identifier. Compares
   to the recorded value.
5. For each output in ``Run.outputs[]`` verifies the artifact file
   exists at the recorded path. If the Run carries recorded artifact
   hashes (it may not — backfills did not record per-artifact hashes),
   hashes the current file and compares.
6. Aggregates a verdict. The run is ``replay_equivalent: true`` iff
   every check above passes; any divergence flips the verdict false and
   carries the details into the replay report.
7. Appends a ``run.evidence.replayed`` event to a NEW per-replay
   ledger file ``ops/event-ledger/replay-<run-id>-<ISO>.jsonl`` and
   writes the full replay report at
   ``ops/replay-records/<run-id>/<replay-event-id>.json``.
8. Prints a one-line summary and exits 0 on equivalent, 1 on divergence.

What this CLI does NOT do:

- Re-call the LLM. Brief generation is an LLM-agent-driven playbook
  pass, not a programmatic pipeline, and the LLM state is not pinned;
  byte-replay of the brief output is out of scope. The ``replay_method``
  is recorded as ``equivalence`` to keep that boundary honest.
- Re-run the gate suite. Replay reads what the recorded ledger says
  about the gate rollup; gate enforcement remains the job of
  ``scripts/validate_run_evidence.py``.

Typical invocation::

    python scripts/replay_run.py --run-id run-874c5e341e13
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

# Make the sibling library importable when invoked as a script.
sys.path.insert(0, str(Path(__file__).resolve().parent))

import run_evidence  # noqa: E402


REPLAY_RECORDS_DIR = run_evidence.ROOT / "ops" / "replay-records"


# ----------------------------------------------------------------- loaders


def _relative_to_or_self(path: Path, root: Path) -> Path:
    """Return ``path`` relative to ``root`` when possible, else as-is.

    Replay tests run under tmp directories that sit outside the repo
    root; the helper keeps error messages readable in both shapes.
    """
    try:
        return path.relative_to(root)
    except ValueError:
        return path


def _load_run_record(records_dir: Path, run_id: str) -> dict[str, Any]:
    path = records_dir / f"{run_id}.json"
    if not path.is_file():
        raise SystemExit(
            f"replay_run: Run record not found at "
            f"{_relative_to_or_self(path, run_evidence.ROOT)}. "
            f"Run records live under ops/run-records/<run-id>.json; "
            f"check the --run-id value and the --run-records-dir override."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def _load_ledger_lines(ledger_dir: Path, run_id: str) -> list[dict[str, Any]]:
    path = ledger_dir / f"{run_id}.jsonl"
    if not path.is_file():
        raise SystemExit(
            f"replay_run: event ledger not found at "
            f"{_relative_to_or_self(path, run_evidence.ROOT)}. "
            f"Every Run must carry a matching JSONL ledger; see "
            f"scripts/finalize_run.py for the emitter shape."
        )
    out: list[dict[str, Any]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        try:
            out.append(json.loads(raw))
        except json.JSONDecodeError as exc:
            raise SystemExit(
                f"replay_run: ledger line is not valid JSON in {path}: {exc}"
            ) from exc
    return out


# ----------------------------------------------------------------- helpers


def _split_sandbox_ref(value: str) -> tuple[str, str]:
    """Split ``<repo>@<sha>`` into the two parts.

    Returns ``(repo, sha)``. Raises ``SystemExit`` if the shape is not
    parseable so the operator sees a clear error instead of a silent
    mismatch later.
    """
    if "@" not in value:
        raise SystemExit(
            f"replay_run: sandbox_image_ref does not match <repo>@<sha>: "
            f"{value!r}. The emitter writes this field as "
            f"derive_sandbox_image_ref(); a malformed value blocks replay."
        )
    repo, sha = value.rsplit("@", 1)
    return repo, sha.strip()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _output_recorded_hash(output: Mapping[str, Any]) -> str | None:
    """Return a recorded artifact hash if the Run output carries one.

    Run outputs do not currently carry hashes (the W20/W21/W22 backfills
    omit per-artifact hashes), but the replay tolerates both shapes:
    when ``hash`` or ``content_sha256`` is present, we cross-check it
    against the current file. When absent, we verify existence only and
    report ``hash_recorded: false`` for that output.
    """
    for key in ("content_sha256", "hash", "sha256"):
        candidate = output.get(key)
        if isinstance(candidate, str) and candidate.strip():
            return candidate.strip().lower().removeprefix("sha256:")
    return None


def _resolve_output_path(artifact_id: str, repo_root: Path) -> Path:
    """Resolve a Run output artifact_id into a filesystem path.

    Run outputs in this repo carry ``artifact_id`` values like
    ``briefs/2026-W22/brief.md`` (repo-relative POSIX paths). We resolve
    them under ``repo_root`` so the check works regardless of the caller's
    cwd.
    """
    return repo_root / artifact_id


# ----------------------------------------------------------------- main check


def _check_head(record: Mapping[str, Any], repo_root: Path) -> tuple[bool, str, str]:
    """Return (matches, recorded_sha, current_head_sha)."""
    sandbox_ref = record.get("sandbox_image_ref")
    if not isinstance(sandbox_ref, str) or not sandbox_ref.strip():
        raise SystemExit(
            f"replay_run: Run {record.get('id')!r} has no sandbox_image_ref; "
            f"strict HEAD verification is impossible without a recorded SHA."
        )
    _, recorded_sha = _split_sandbox_ref(sandbox_ref)
    current = run_evidence.current_head_sha(repo_path=repo_root) or ""
    return (current == recorded_sha and bool(recorded_sha)), recorded_sha, current


def _recompute_hashes(repo_root: Path, llm_identifier: str) -> tuple[str, str]:
    """Recompute prompt + tool schemas hashes against the current tree."""
    playbook_text = run_evidence.read_repo_text(
        repo_root / "playbook" / "run-weekly-brief.md"
    )
    prompt_hash = run_evidence.compute_sha256(
        run_evidence.canonicalize_prompt(playbook_text, [], [])
    )
    registry_text = run_evidence.read_repo_text(
        repo_root / "sources" / "registry.yaml"
    )
    tool_hash = run_evidence.compute_sha256(
        run_evidence.canonicalize_tool_surface(registry_text, llm_identifier, {})
    )
    return prompt_hash, tool_hash


def _check_outputs(
    record: Mapping[str, Any], repo_root: Path
) -> tuple[bool, list[dict[str, Any]]]:
    """Walk Run.outputs[]; verify existence + hash agreement when recorded."""
    outputs = record.get("outputs") or []
    if not isinstance(outputs, list):
        outputs = []
    all_ok = True
    details: list[dict[str, Any]] = []
    for output in outputs:
        if not isinstance(output, Mapping):
            continue
        artifact_id = output.get("artifact_id")
        if not isinstance(artifact_id, str) or not artifact_id.strip():
            continue
        path = _resolve_output_path(artifact_id, repo_root)
        exists = path.is_file()
        recorded_hash = _output_recorded_hash(output)
        item: dict[str, Any] = {
            "artifact_id": artifact_id,
            "exists": exists,
            "hash_recorded": recorded_hash is not None,
        }
        if not exists:
            all_ok = False
            item["divergence"] = "artifact missing at recorded path"
            details.append(item)
            continue
        if recorded_hash is not None:
            current_hash = _sha256_file(path)
            item["recorded_hash"] = recorded_hash
            item["current_hash"] = current_hash
            if current_hash != recorded_hash:
                all_ok = False
                item["divergence"] = "artifact hash mismatch"
        details.append(item)
    return all_ok, details


# ----------------------------------------------------------------- assemble + emit


def _llm_from_record(record: Mapping[str, Any]) -> str:
    agent = record.get("agent_id")
    if isinstance(agent, str) and agent.strip():
        return agent.strip()
    return run_evidence.DEFAULT_LLM_IDENTIFIER


def _build_replay_report(
    *,
    run_id: str,
    record: Mapping[str, Any],
    head_match: bool,
    recorded_sha: str,
    current_head: str,
    prompt_recorded: Any,
    prompt_current: str,
    tool_recorded: Any,
    tool_current: str,
    outputs_ok: bool,
    outputs_details: list[dict[str, Any]],
    replay_equivalent: bool,
    replay_event_id: str,
    replay_timestamp: str,
    packet_ref: str,
) -> dict[str, Any]:
    divergences: list[str] = []
    if not head_match:
        divergences.append("HEAD does not match recorded sandbox SHA")
    if prompt_recorded != prompt_current:
        divergences.append("prompt_snapshot_hash diverged from recorded")
    if tool_recorded != tool_current:
        divergences.append("tool_schemas_snapshot_hash diverged from recorded")
    if not outputs_ok:
        divergences.append("one or more outputs missing or hash-mismatched")
    return {
        "replay_event_id": replay_event_id,
        "replay_timestamp": replay_timestamp,
        "run_id": run_id,
        "replay_method": "equivalence",
        "replay_equivalent": replay_equivalent,
        "head_check": {
            "recorded_sha": recorded_sha,
            "current_head": current_head,
            "match": head_match,
        },
        "prompt_snapshot_hash_check": {
            "recorded": prompt_recorded,
            "current": prompt_current,
            "match": prompt_recorded == prompt_current,
        },
        "tool_schemas_snapshot_hash_check": {
            "recorded": tool_recorded,
            "current": tool_current,
            "match": tool_recorded == tool_current,
        },
        "outputs_check": {
            "all_ok": outputs_ok,
            "details": outputs_details,
        },
        "spec_id": record.get("spec_id"),
        "packet_ref": packet_ref,
        "divergences": divergences,
    }


def _emit_replay_event(
    *,
    run_id: str,
    spec_id: str | None,
    replay_event_id: str,
    replay_timestamp: str,
    replay_equivalent: bool,
    packet_ref: str,
    ledger_path: Path,
) -> None:
    payload: dict[str, Any] = {
        "run_id": run_id,
        "packet_ref": packet_ref,
        "replay_equivalent": replay_equivalent,
        "replay_method": "equivalence",
    }
    event: dict[str, Any] = {
        "event_id": replay_event_id,
        "type": "run.evidence.replayed",
        "created_at": replay_timestamp,
        "actor": {"kind": "system", "id": "ci.replay-runner"},
        "payload": payload,
        "run_id": run_id,
    }
    if spec_id:
        event["spec_id"] = spec_id
    run_evidence.emit_event(event, ledger_path)


# ----------------------------------------------------------------- CLI


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="replay_run",
        description=(
            "equivalence replay for a published ai-field-brief Run "
            "(verifies preconditions + artifacts; does not re-call the LLM)"
        ),
    )
    parser.add_argument("--run-id", required=True, help="run-<12hex> identifier")
    parser.add_argument(
        "--run-records-dir",
        type=Path,
        default=run_evidence.RUN_RECORDS_DIR,
        help="override the run-records directory (default: ops/run-records/)",
    )
    parser.add_argument(
        "--event-ledger-dir",
        type=Path,
        default=run_evidence.EVENT_LEDGER_DIR,
        help="override the event-ledger directory (default: ops/event-ledger/)",
    )
    parser.add_argument(
        "--replay-records-dir",
        type=Path,
        default=REPLAY_RECORDS_DIR,
        help="override the replay-records directory (default: ops/replay-records/)",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=run_evidence.ROOT,
        help="repo root used to resolve playbook + registry + outputs",
    )
    parser.add_argument(
        "--llm",
        default=None,
        help=(
            "LLM identifier for the tool-schema hash (default: Run.agent_id "
            "or claude-opus-4-7)"
        ),
    )
    args = parser.parse_args(argv)

    run_id: str = args.run_id
    repo_root: Path = args.repo_root.resolve()

    record = _load_run_record(args.run_records_dir, run_id)
    _load_ledger_lines(args.event_ledger_dir, run_id)  # presence-check the ledger

    llm_identifier = args.llm or _llm_from_record(record)

    # Step 4: strict HEAD verification. The check runs first so a wrong
    # checkout fails fast with an actionable message before we spend
    # cycles hashing the wrong tree.
    head_match, recorded_sha, current_head = _check_head(record, repo_root)
    if not head_match:
        print(
            f"replay_run: HEAD mismatch for {run_id}. "
            f"Recorded sandbox SHA: {recorded_sha}. "
            f"Current HEAD: {current_head or '<unknown>'}. "
            f"Run `git checkout {recorded_sha}` and re-invoke.",
            file=sys.stderr,
        )
        return 1

    # Step 5 + 6: re-compute the two snapshot hashes against the current
    # tree and compare to the recorded values.
    prompt_current, tool_current = _recompute_hashes(repo_root, llm_identifier)
    prompt_recorded = record.get("prompt_snapshot_hash")
    tool_recorded = record.get("tool_schemas_snapshot_hash")

    # Step 7: artifact existence + optional hash check.
    outputs_ok, outputs_details = _check_outputs(record, repo_root)

    # Step 8: aggregate verdict.
    replay_equivalent = (
        head_match
        and prompt_recorded == prompt_current
        and tool_recorded == tool_current
        and outputs_ok
    )

    replay_event_id = run_evidence.new_event_id()
    replay_timestamp = run_evidence.now_iso()

    # The packet_ref points at the replay report we are about to write;
    # the event schema requires the field, and the report is the
    # downstream artifact a consumer would inspect.
    replay_report_path = (
        args.replay_records_dir / run_id / f"{replay_event_id}.json"
    )
    try:
        packet_ref = replay_report_path.relative_to(repo_root).as_posix()
    except ValueError:
        packet_ref = replay_report_path.as_posix()

    report = _build_replay_report(
        run_id=run_id,
        record=record,
        head_match=head_match,
        recorded_sha=recorded_sha,
        current_head=current_head,
        prompt_recorded=prompt_recorded,
        prompt_current=prompt_current,
        tool_recorded=tool_recorded,
        tool_current=tool_current,
        outputs_ok=outputs_ok,
        outputs_details=outputs_details,
        replay_equivalent=replay_equivalent,
        replay_event_id=replay_event_id,
        replay_timestamp=replay_timestamp,
        packet_ref=packet_ref,
    )

    replay_report_path.parent.mkdir(parents=True, exist_ok=True)
    replay_report_path.write_text(
        json.dumps(report, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    # Step 9 + 10: append the replay event to a NEW per-replay JSONL
    # file so the source-of-truth ledger stays immutable. The ISO
    # timestamp is sanitized for filesystem-safe form (Windows rejects
    # ":" in filenames); the in-event created_at keeps the canonical
    # RFC 3339 shape so downstream consumers see the unsanitized value.
    safe_timestamp = replay_timestamp.replace(":", "")
    replay_ledger_path = (
        args.event_ledger_dir / f"replay-{run_id}-{safe_timestamp}.jsonl"
    )
    _emit_replay_event(
        run_id=run_id,
        spec_id=record.get("spec_id") if isinstance(record.get("spec_id"), str) else None,
        replay_event_id=replay_event_id,
        replay_timestamp=replay_timestamp,
        replay_equivalent=replay_equivalent,
        packet_ref=packet_ref,
        ledger_path=replay_ledger_path,
    )

    try:
        rel_replay = replay_ledger_path.relative_to(repo_root).as_posix()
    except ValueError:
        rel_replay = replay_ledger_path.as_posix()
    verdict = "equivalent" if replay_equivalent else "diverged"
    extra = (
        ""
        if replay_equivalent
        else f" divergences={'; '.join(report['divergences'])}"
    )
    print(
        f"replay_run {verdict}: run_id={run_id} "
        f"replay_event={replay_event_id} report={packet_ref} "
        f"ledger={rel_replay}{extra}"
    )
    return 0 if replay_equivalent else 1


if __name__ == "__main__":
    sys.exit(main())
