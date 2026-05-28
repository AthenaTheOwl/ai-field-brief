"""Validate run-evidence artifacts emitted by ai-field-brief.

Walks two directories and validates each record against the cross-repo
schemas mirrored in ``ops/schemas-cache/``:

- ``ops/event-ledger/<run-id>.jsonl`` — append-only event ledger files;
  every line must be a JSON object conforming to ``event.schema.json``.
- ``ops/run-records/<run-id>.json`` — final Run records; each file must
  conform to the amended ``run.schema.json`` carrying the six
  replay-equivalence fields.

Cross-check: every ``run_id`` referenced by an event in the ledger must
either have a matching Run record file or be in-progress (no terminal
event observed). A terminal event is ``pipeline.complete`` or
``gate.run.evidence_recorded``; observing one without a matching
``ops/run-records/<run_id>.json`` is a violation.

Exit codes: ``0`` OK, ``1`` violations found. Violation detail is
written to stderr in the same shape as ``scripts/validate_decisions.py``.
This validator follows the offline-first pattern used by the other
``validate_*.py`` scripts: it loads the cached schema, never talks to
the network, and treats a missing schema cache file as a hard error.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
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
) -> tuple[list[str], dict[str, list[str]], set[str]]:
    """Walk every JSONL ledger file and validate every line."""
    violations: list[str] = []
    run_to_types: dict[str, list[str]] = {}
    run_ids: set[str] = set()
    if not ledger_dir.is_dir():
        return violations, run_to_types, run_ids
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
    return violations, run_to_types, run_ids


def validate_run_records(
    validator: Any, records_dir: Path
) -> tuple[list[str], set[str]]:
    """Walk every Run record file and validate the JSON body."""
    violations: list[str] = []
    recorded: set[str] = set()
    if not records_dir.is_dir():
        return violations, recorded
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
    return violations, recorded


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

    event_violations, run_to_types, run_ids_in_events = validate_event_ledger(
        event_validator, args.event_ledger_dir
    )
    record_violations, recorded_ids = validate_run_records(
        run_validator, args.run_records_dir
    )
    cross_violations = cross_check(run_to_types, run_ids_in_events, recorded_ids)

    all_violations = event_violations + record_violations + cross_violations
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
