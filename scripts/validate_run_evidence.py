"""Validate run-evidence artifacts emitted by ai-field-brief.

Walks two directories and validates each record against the cross-repo
schemas mirrored in ``ops/schemas-cache/``:

- ``ops/event-ledger/<run-id>.jsonl`` — append-only event ledger files;
  every line must be a JSON object conforming to ``event.schema.json``.
- ``ops/run-records/<run-id>.json`` — final Run records; each file must
  conform to the amended ``run.schema.json`` carrying the six
  replay-equivalence fields.

Envelope cross-check: every ``run_id`` referenced by an event in the
ledger must either have a matching Run record file or be in-progress
(no terminal event observed). A terminal event is ``pipeline.complete``
or ``gate.run.evidence_recorded``; observing one without a matching
``ops/run-records/<run_id>.json`` is a violation.

Run-level required-for-done fields: when a Run record carries
``status == "done"`` the validator enforces that the following fields
are present and non-empty:

- ``prompt_snapshot_hash``
- ``tool_schemas_snapshot_hash``
- ``sandbox_image_ref``
- ``gate_results_summary``

The ledger for a done Run must additionally carry at least one
``gate.run.evidence_recorded`` event.

Four ledger/Run cross-checks per done Run:

1. ``Run.prompt_snapshot_hash`` == the matching pipeline.start payload
   field.
2. ``Run.tool_schemas_snapshot_hash`` == the matching pipeline.start
   payload field.
3. ``gate.run.evidence_recorded`` event's ``fields_populated`` list
   equals the set of replay-equivalence fields actually populated on
   the Run record (compared as sorted sets).
4. ``Run.gate_results_summary`` matches what scanning the ledger for
   ``gate.check.passed`` / ``gate.check.failed`` events produces:
   ``gates_passed`` is the sorted list of names from passed events,
   ``gates_failed`` is the sorted list of names from failed events, and
   ``all_passed`` is ``len(gates_failed) == 0``.

Exit codes: ``0`` OK, ``1`` violations found. Violation detail is
written to stderr in the same shape as ``scripts/validate_decisions.py``.
This validator follows the offline-first pattern used by the other
``validate_*.py`` scripts: it loads the cached schema, never talks to
the network, and treats a missing schema cache file as a hard error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

# Portable URI grammar (DEC-CDCP-014). The validator does not currently
# open files from inputs[].ref or outputs[].artifact_id values (it only
# enforces schema + cross-checks), but it ships ``resolve_uri`` for
# consumers that walk Run records through this module, and for the
# Round 7 file-existence gate that follows.
_REPO_URI_RE = re.compile(
    r"^repo://(?P<repo>[a-z][a-z0-9-]*)@(?P<sha>[a-f0-9]{40}|PENDING)/(?P<path>.*)$"
)
_ARTIFACT_URI_RE = re.compile(
    r"^artifact://(?P<repo>[a-z][a-z0-9-]*)/(?P<id>.+)$"
)


def resolve_uri(uri: str, portfolio_root: Path | None = None) -> Path | None:
    """Resolve a repo:// URI to a local path.

    Mirrors ``run_evidence.resolve_uri``. ``repo://<repo>@<sha>/<path>``
    resolves to ``<portfolio_root>/<repo>/<path>``;
    ``artifact://<repo>/<id>`` returns ``None``; anything else is
    treated as a legacy local path and returned as a ``Path``.
    """
    if portfolio_root is None:
        portfolio_root = Path("e:/claude_code/random-apps")
    repo_match = _REPO_URI_RE.match(uri)
    if repo_match:
        return portfolio_root / repo_match["repo"] / repo_match["path"]
    artifact_match = _ARTIFACT_URI_RE.match(uri)
    if artifact_match:
        return None
    return Path(uri)
CACHE_DIR = ROOT / "ops" / "schemas-cache"
DEFAULT_EVENT_LEDGER_DIR = ROOT / "ops" / "event-ledger"
DEFAULT_RUN_RECORDS_DIR = ROOT / "ops" / "run-records"

EVENT_SCHEMA_PATH = CACHE_DIR / "event.schema.json"
RUN_SCHEMA_PATH = CACHE_DIR / "run.schema.json"

# Terminal event types. Presence in a ledger means the run is no longer
# in-progress; a missing Run record alongside any of these is a
# violation.
TERMINAL_EVENT_TYPES = frozenset(
    {"gate.run.evidence_recorded", "pipeline.complete", "pipeline.done"}
)

# Required-for-done Run-record fields. Each must be present and
# non-empty when Run.status == "done".
REQUIRED_FOR_DONE_FIELDS: tuple[str, ...] = (
    "prompt_snapshot_hash",
    "tool_schemas_snapshot_hash",
    "sandbox_image_ref",
    "gate_results_summary",
)

# Names of the six replay-equivalence fields. The
# gate.run.evidence_recorded.payload.fields_populated list must equal
# the subset of these actually populated on the Run record.
REPLAY_EQUIVALENCE_FIELDS: tuple[str, ...] = (
    "prompt_snapshot_hash",
    "tool_schemas_snapshot_hash",
    "determinism",
    "checkpoint_ref",
    "sandbox_image_ref",
    "gate_results_summary",
)


def _load_schema(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise SystemExit(
            f"validate_run_evidence: cached schema missing at "
            f"{path.relative_to(ROOT).as_posix()}. Re-cache from athena-site."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def _validator_for(schema: dict[str, Any]) -> Any:
    try:
        import jsonschema  # type: ignore[import-untyped]
    except ImportError as exc:
        raise SystemExit(
            "validate_run_evidence: jsonschema is required. "
            "Install with `pip install jsonschema>=4.21`."
        ) from exc
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    return validator_cls(schema)


def _format_errors(prefix: str, errors: list[Any]) -> list[str]:
    out: list[str] = []
    for err in errors:
        location = "/".join(str(part) for part in err.path) or "<root>"
        out.append(f"{prefix}: {location}: {err.message}")
    return out


def _safe_rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def validate_event_ledger(
    validator: Any, ledger_dir: Path
) -> tuple[list[str], dict[str, list[str]], dict[str, list[dict[str, Any]]], set[str]]:
    """Walk every JSONL ledger file and validate every line.

    Returns four artifacts:

    - ``violations``: list of formatted error strings for the caller to
      print and exit non-zero on.
    - ``run_to_types``: mapping run_id -> list of event type strings, in
      ledger order; used by the envelope cross-check that terminal
      events have a matching Run record.
    - ``run_to_events``: mapping run_id -> list of fully-parsed event
      dicts in ledger order; used by the Run-level cross-checks that
      compare hashes, gate aggregates, and fields_populated against the
      Run record.
    - ``run_ids``: set of every run_id seen in the ledger.
    """
    violations: list[str] = []
    run_to_types: dict[str, list[str]] = {}
    run_to_events: dict[str, list[dict[str, Any]]] = {}
    run_ids: set[str] = set()
    if not ledger_dir.is_dir():
        return violations, run_to_types, run_to_events, run_ids
    for ledger in sorted(ledger_dir.glob("*.jsonl")):
        rel = _safe_rel(ledger)
        text = ledger.read_text(encoding="utf-8")
        for line_no, raw in enumerate(text.splitlines(), start=1):
            stripped = raw.strip()
            if not stripped:
                continue
            try:
                event = json.loads(stripped)
            except json.JSONDecodeError as exc:
                violations.append(f"{rel}:{line_no}: invalid JSON: {exc}")
                continue
            if not isinstance(event, dict):
                violations.append(
                    f"{rel}:{line_no}: top-level value must be a JSON object"
                )
                continue
            errs = sorted(validator.iter_errors(event), key=lambda e: list(e.path))
            violations.extend(_format_errors(f"{rel}:{line_no}", errs))
            run_id = event.get("run_id")
            if isinstance(run_id, str) and run_id:
                run_ids.add(run_id)
                run_to_types.setdefault(run_id, []).append(
                    str(event.get("type", ""))
                )
                run_to_events.setdefault(run_id, []).append(event)
    return violations, run_to_types, run_to_events, run_ids


def validate_run_records(
    validator: Any, records_dir: Path
) -> tuple[list[str], set[str], dict[str, dict[str, Any]], dict[str, str]]:
    """Walk every Run record file and validate the JSON body.

    Returns four artifacts:

    - ``violations``: list of formatted error strings.
    - ``recorded``: set of run_ids with a parsed record file.
    - ``run_by_id``: mapping run_id -> parsed Run dict; used by the
      Run-level required-for-done check and the cross-checks.
    - ``rel_by_id``: mapping run_id -> the relative ledger path string
      used to label per-Run cross-check violations.
    """
    violations: list[str] = []
    recorded: set[str] = set()
    run_by_id: dict[str, dict[str, Any]] = {}
    rel_by_id: dict[str, str] = {}
    if not records_dir.is_dir():
        return violations, recorded, run_by_id, rel_by_id
    for record in sorted(records_dir.glob("*.json")):
        rel = _safe_rel(record)
        try:
            run = json.loads(record.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            violations.append(f"{rel}: invalid JSON: {exc}")
            continue
        if not isinstance(run, dict):
            violations.append(f"{rel}: top-level value must be a JSON object")
            continue
        errs = sorted(validator.iter_errors(run), key=lambda e: list(e.path))
        violations.extend(_format_errors(rel, errs))
        run_id = run.get("id")
        if isinstance(run_id, str) and run_id:
            recorded.add(run_id)
            run_by_id[run_id] = run
            rel_by_id[run_id] = rel
    return violations, recorded, run_by_id, rel_by_id


def cross_check(
    run_to_event_types: dict[str, list[str]],
    run_ids_in_events: set[str],
    run_ids_recorded: set[str],
) -> list[str]:
    """Cross-check that terminal events have matching Run records."""
    violations: list[str] = []
    for run_id in sorted(run_ids_in_events):
        types = set(run_to_event_types.get(run_id, []))
        if types & TERMINAL_EVENT_TYPES and run_id not in run_ids_recorded:
            violations.append(
                f"run_id {run_id!r}: ledger carries terminal event "
                f"({sorted(types & TERMINAL_EVENT_TYPES)}) but no matching "
                f"ops/run-records/{run_id}.json"
            )
    return violations


def _first_event_of_type(
    events: list[dict[str, Any]], event_type: str
) -> dict[str, Any] | None:
    """Return the first event of ``event_type`` from a run's ledger slice."""
    for event in events:
        if event.get("type") == event_type:
            return event
    return None


def _populated_replay_fields(run: dict[str, Any]) -> list[str]:
    """Return the sorted list of replay-equivalence fields populated on Run.

    "Populated" means present and non-empty (a present-but-empty string
    or dict does not count as populated, mirroring the build-side rule
    in run_evidence.build_run_evidence_fields).
    """
    populated: list[str] = []
    for name in REPLAY_EQUIVALENCE_FIELDS:
        value = run.get(name)
        if value is None:
            continue
        if isinstance(value, (str, list, dict)) and len(value) == 0:
            continue
        populated.append(name)
    return sorted(populated)


def _aggregate_summary_from_events(
    events: list[dict[str, Any]],
) -> dict[str, Any]:
    """Build the canonical gate_results_summary by scanning ledger events.

    Walks ``gate.check.passed`` and ``gate.check.failed`` events and
    returns the sorted-set rollup the validator compares against the
    Run record's claimed summary.
    """
    passed: list[str] = []
    failed: list[str] = []
    for event in events:
        event_type = event.get("type")
        payload = event.get("payload") or {}
        name = payload.get("gate_name") if isinstance(payload, dict) else None
        if not isinstance(name, str) or not name:
            continue
        if event_type == "gate.check.passed":
            passed.append(name)
        elif event_type == "gate.check.failed":
            failed.append(name)
    passed_sorted = sorted(passed)
    failed_sorted = sorted(failed)
    return {
        "gates_passed": passed_sorted,
        "gates_failed": failed_sorted,
        "all_passed": len(failed_sorted) == 0,
    }


def cross_check_done_runs(
    run_by_id: dict[str, dict[str, Any]],
    run_to_events: dict[str, list[dict[str, Any]]],
    rel_by_id: dict[str, str],
) -> list[str]:
    """Run-level cross-checks for every Run with status == "done".

    Enforces the required-for-done fields plus the four ledger/Run
    cross-checks documented in the module docstring. Each violation
    names the run_id and the specific check that failed.
    """
    violations: list[str] = []
    for run_id in sorted(run_by_id):
        run = run_by_id[run_id]
        if run.get("status") != "done":
            continue
        rel = rel_by_id.get(run_id, run_id)
        prefix = f"{rel}: run_id={run_id}"

        # Required-for-done fields. We check presence + non-emptiness;
        # the schema already checks the shape.
        for field in REQUIRED_FOR_DONE_FIELDS:
            value = run.get(field)
            if value is None or (
                isinstance(value, (str, list, dict)) and len(value) == 0
            ):
                violations.append(
                    f"{prefix}: required-for-done field missing or empty: "
                    f"{field}"
                )

        events = run_to_events.get(run_id, [])

        # Required terminal event: at least one
        # gate.run.evidence_recorded must exist for this run.
        if not any(
            e.get("type") == "gate.run.evidence_recorded" for e in events
        ):
            violations.append(
                f"{prefix}: required terminal event missing: "
                f"gate.run.evidence_recorded"
            )

        # Cross-check 1 + 2: hashes match between Run and pipeline.start.
        start_event = _first_event_of_type(events, "pipeline.start")
        start_payload = (
            start_event.get("payload") if isinstance(start_event, dict) else None
        )
        if not isinstance(start_payload, dict):
            violations.append(
                f"{prefix}: cross-check skipped: no pipeline.start event in "
                f"ledger to compare hashes against"
            )
        else:
            for field in (
                "prompt_snapshot_hash",
                "tool_schemas_snapshot_hash",
            ):
                run_value = run.get(field)
                event_value = start_payload.get(field)
                if run_value != event_value:
                    violations.append(
                        f"{prefix}: cross-check failed: Run.{field}="
                        f"{run_value!r} does not match pipeline.start."
                        f"payload.{field}={event_value!r}"
                    )

        # Cross-check 3: fields_populated on the
        # gate.run.evidence_recorded event matches the actually populated
        # replay-equivalence fields on the Run.
        evidence_event = _first_event_of_type(events, "gate.run.evidence_recorded")
        if isinstance(evidence_event, dict):
            evidence_payload = evidence_event.get("payload") or {}
            claimed = evidence_payload.get("fields_populated") if isinstance(
                evidence_payload, dict
            ) else None
            actual = _populated_replay_fields(run)
            if not isinstance(claimed, list):
                violations.append(
                    f"{prefix}: cross-check failed: gate.run.evidence_recorded."
                    f"payload.fields_populated must be an array, "
                    f"got {claimed!r}"
                )
            else:
                claimed_sorted = sorted(str(item) for item in claimed)
                if claimed_sorted != actual:
                    violations.append(
                        f"{prefix}: cross-check failed: "
                        f"gate.run.evidence_recorded.payload.fields_populated="
                        f"{claimed_sorted} does not match Run record's "
                        f"populated replay-equivalence fields={actual}"
                    )

        # Cross-check 4: Run.gate_results_summary matches what scanning
        # gate.check.* events in the ledger produces.
        ledger_summary = _aggregate_summary_from_events(events)
        run_summary = run.get("gate_results_summary")
        if not isinstance(run_summary, dict):
            # Already flagged by the required-for-done check; skip the
            # comparison to avoid a duplicate.
            continue
        run_passed = sorted(
            str(name) for name in (run_summary.get("gates_passed") or [])
        )
        run_failed = sorted(
            str(name) for name in (run_summary.get("gates_failed") or [])
        )
        run_all_passed = bool(run_summary.get("all_passed"))
        if run_passed != ledger_summary["gates_passed"]:
            violations.append(
                f"{prefix}: cross-check failed: Run.gate_results_summary."
                f"gates_passed={run_passed} does not match ledger "
                f"gate.check.passed events={ledger_summary['gates_passed']}"
            )
        if run_failed != ledger_summary["gates_failed"]:
            violations.append(
                f"{prefix}: cross-check failed: Run.gate_results_summary."
                f"gates_failed={run_failed} does not match ledger "
                f"gate.check.failed events={ledger_summary['gates_failed']}"
            )
        if run_all_passed != ledger_summary["all_passed"]:
            violations.append(
                f"{prefix}: cross-check failed: Run.gate_results_summary."
                f"all_passed={run_all_passed} does not match ledger-derived "
                f"all_passed={ledger_summary['all_passed']}"
            )
    return violations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="validate_run_evidence",
        description="validate ai-field-brief run-evidence artifacts",
    )
    parser.add_argument(
        "--event-ledger-dir",
        type=Path,
        default=DEFAULT_EVENT_LEDGER_DIR,
        help="override the event ledger directory (default: ops/event-ledger/)",
    )
    parser.add_argument(
        "--run-records-dir",
        type=Path,
        default=DEFAULT_RUN_RECORDS_DIR,
        help="override the run records directory (default: ops/run-records/)",
    )
    args = parser.parse_args(argv)

    event_schema = _load_schema(EVENT_SCHEMA_PATH)
    run_schema = _load_schema(RUN_SCHEMA_PATH)
    event_validator = _validator_for(event_schema)
    run_validator = _validator_for(run_schema)

    (
        event_violations,
        run_to_types,
        run_to_events,
        run_ids_in_events,
    ) = validate_event_ledger(event_validator, args.event_ledger_dir)
    (
        record_violations,
        recorded_ids,
        run_by_id,
        rel_by_id,
    ) = validate_run_records(run_validator, args.run_records_dir)
    cross_violations = cross_check(run_to_types, run_ids_in_events, recorded_ids)
    done_violations = cross_check_done_runs(run_by_id, run_to_events, rel_by_id)

    all_violations = (
        event_violations + record_violations + cross_violations + done_violations
    )
    if all_violations:
        for line in all_violations:
            print(line, file=sys.stderr)
        print(
            f"validate_run_evidence: {len(all_violations)} violation(s) found",
            file=sys.stderr,
        )
        return 1

    n_events = sum(len(v) for v in run_to_types.values())
    print(
        f"validate_run_evidence OK ("
        f"{n_events} event(s), "
        f"{len(recorded_ids)} run record(s), "
        f"{len(run_ids_in_events)} run_id(s) referenced)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
