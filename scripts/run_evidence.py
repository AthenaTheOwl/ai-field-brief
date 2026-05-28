"""Run-evidence emitter for ai-field-brief weekly brief generation.

A Run in ai-field-brief is one brief-generation cycle: source sweep,
extraction, synthesis, and publish, producing one weekly brief at
``briefs/YYYY-WNN/``. The orchestrator is typically an agent following
``playbook/run-weekly-brief.md`` rather than a fully automated Python
pipeline, so this module ships in three forms:

- This library: emitter helpers + Run and Event constructors.
- ``scripts/finalize_run.py``: CLI the playbook calls at publish time.
- ``scripts/backfill_run_records.py``: backfill already-published briefs.

Both records conform to the cross-repo CDCP schemas mirrored under
``ops/schemas-cache/event.schema.json`` and
``ops/schemas-cache/run.schema.json``. The amended Run schema carries six
replay-equivalence fields: ``prompt_snapshot_hash``,
``tool_schemas_snapshot_hash``, ``determinism``, ``checkpoint_ref``,
``sandbox_image_ref``, and ``gate_results_summary``.

Field-population rules followed here:

- ``prompt_snapshot_hash``: SHA-256 of canonicalized playbook content
  plus active extraction prompts plus active synthesis prompts.
- ``tool_schemas_snapshot_hash``: SHA-256 of canonicalized source
  registry, extraction schema reference, and the LLM identifier.
- ``determinism``: omitted; brief generation calls an LLM without
  pinned sampler knobs.
- ``checkpoint_ref``: omitted; no managed brief-run checkpoint store.
- ``sandbox_image_ref``: ``<repo-path>@<HEAD-sha>`` derived from the
  ai-field-brief repo HEAD at finalize time, or the publishing commit
  SHA for backfills.
- ``gate_results_summary``: aggregated from ``gate.check.*`` events on
  live runs; populated from the canonical brief-gate list on backfills
  (the brief was committed, so every required gate must have passed).

This module is the source-of-truth shape; the gate at
``scripts/validate_run_evidence.py`` walks both directories and checks
every record against the cached schemas.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import uuid
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ----------------------------------------------------------------- repo layout

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "ops" / "schemas-cache"
EVENT_LEDGER_DIR = ROOT / "ops" / "event-ledger"
RUN_RECORDS_DIR = ROOT / "ops" / "run-records"
PLAYBOOK_PATH = ROOT / "playbook" / "run-weekly-brief.md"
SOURCES_REGISTRY_PATH = ROOT / "sources" / "registry.yaml"
TEMPLATE_PATH = ROOT / "templates" / "weekly-brief.md"

# The brief author currently runs as a single Claude or Codex agent
# following the playbook end-to-end. The LLM identifier is the canonical
# tool surface label; treating it as part of the tool-schema hash means a
# model swap (or an OpenAI Codex run vs Claude run) produces a different
# tool-surface fingerprint.
DEFAULT_LLM_IDENTIFIER = "claude-opus-4-7"

# Canonical brief-gate set. The CI workflow under .github/workflows/ci.yml
# runs these in the gates job; a brief commit means each one passed in
# CI history. The backfill uses this list to populate gate_results_summary
# in the absence of a live timeline.
BRIEF_GATES_CANONICAL: tuple[str, ...] = (
    "voice_lint",
    "spec_check",
    "check_no_bom",
    "validate_schemas",
    "validate_registry",
    "validate_decisions",
    "validate_roles",
    "validate_tools",
    "validate_policies",
    "validate_skills",
    "validate_dreams",
    "check_schema_cache_freshness",
)

# Actor for emitted events. The brief author is a role acting under the
# playbook contract; the consumer dispatches on event.type so the actor
# id is mostly metadata.
BRIEF_ACTOR_KIND = "role"
BRIEF_ACTOR_ID = "product.brief-author"


# ----------------------------------------------------------------- canonical hashing


def canonicalize_prompt(
    playbook_text: str,
    extraction_prompts: Sequence[str] | None = None,
    synthesis_prompts: Sequence[str] | None = None,
) -> str:
    """Return a stable canonical form of the prompt surface for a brief run.

    The output is a JSON-serialized mapping with sorted keys so byte-equal
    inputs always produce byte-equal canonical strings. The result is the
    input to :func:`compute_sha256` for ``prompt_snapshot_hash``.

    Newlines in the playbook are preserved as-is; line-ending
    normalization is the caller's responsibility (strip CRLFs before
    hashing if cross-platform reproducibility matters).
    """
    payload: dict[str, Any] = {
        "playbook": playbook_text or "",
        "extraction_prompts": list(extraction_prompts or []),
        "synthesis_prompts": list(synthesis_prompts or []),
    }
    return json.dumps(payload, sort_keys=True, ensure_ascii=False)


def canonicalize_tool_surface(
    source_registry_yaml: str,
    llm_identifier: str,
    extraction_schema: Mapping[str, Any] | None = None,
) -> str:
    """Return a stable canonical form of the tool/data surface.

    The source registry is the data input the agent reads to drive a
    sweep; the LLM identifier is the model that synthesizes the brief;
    the extraction schema is the typed shape the agent extracts to.
    Hashing the three together gives a fingerprint that changes when any
    of: a source is added or dropped, the model swaps, or the extraction
    contract moves.
    """
    payload: dict[str, Any] = {
        "source_registry": source_registry_yaml or "",
        "llm": llm_identifier,
        "extraction_schema": extraction_schema or {},
    }
    return json.dumps(payload, sort_keys=True, ensure_ascii=False)


def compute_sha256(canonical: str) -> str:
    """Return the lowercase hex SHA-256 digest of ``canonical``.

    The Run schema requires hashes to match ``^[a-f0-9]{64}$`` so the
    digest is returned without the ``sha256:`` prefix.
    """
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# ----------------------------------------------------------------- repo refs


def derive_sandbox_image_ref(
    repo_path: Path | None = None,
    head_sha: str | None = None,
) -> str | None:
    """Return ``<repo-path>@<head-sha>`` for the ai-field-brief workspace.

    The repo path defaults to the ai-field-brief root inferred from this
    module location. The head SHA is supplied by the caller (the
    finalize CLI reads ``git rev-parse HEAD``; the backfill reads the
    publishing commit SHA per brief). Returns ``None`` when the SHA is
    missing so the caller omits the field instead of writing a partial
    ref.
    """
    if head_sha is None or not head_sha.strip():
        return None
    base = (repo_path or ROOT).resolve()
    return f"{base.as_posix()}@{head_sha.strip()}"


def current_head_sha(repo_path: Path | None = None) -> str | None:
    """Return ``git rev-parse HEAD`` for the repo, or None if unavailable."""
    base = (repo_path or ROOT).resolve()
    try:
        result = subprocess.run(  # noqa: S603 - args fixed, no shell
            ["git", "-C", str(base), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    head = result.stdout.strip()
    if result.returncode != 0 or not head:
        return None
    return head


def publishing_commit_sha(
    brief_path: Path, repo_path: Path | None = None
) -> str | None:
    """Return the SHA of the commit that first introduced the brief.

    Reads ``git log --diff-filter=A --format=%H -- briefs/.../brief.md``
    and returns the oldest matching SHA. Used by the backfill to set
    ``sandbox_image_ref`` for already-published briefs.
    """
    base = (repo_path or ROOT).resolve()
    brief_md = brief_path / "brief.md" if brief_path.is_dir() else brief_path
    try:
        result = subprocess.run(  # noqa: S603 - args fixed, no shell
            [
                "git",
                "-C",
                str(base),
                "log",
                "--diff-filter=A",
                "--format=%H",
                "--",
                str(brief_md.relative_to(base).as_posix()),
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired, ValueError):
        return None
    if result.returncode != 0:
        return None
    shas = [line.strip() for line in result.stdout.splitlines() if line.strip()]
    if not shas:
        # Fall back to the most recent touching commit if no add was
        # found (the brief may have been moved or renamed).
        try:
            fallback = subprocess.run(  # noqa: S603
                [
                    "git",
                    "-C",
                    str(base),
                    "log",
                    "-1",
                    "--format=%H",
                    "--",
                    str(brief_md.relative_to(base).as_posix()),
                ],
                capture_output=True,
                text=True,
                check=False,
                timeout=10,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired, ValueError):
            return None
        return fallback.stdout.strip() or None
    return shas[-1]


# ----------------------------------------------------------------- schema cache


_SCHEMA_CACHE: dict[str, Mapping[str, Any]] = {}


def _load_schema(name: str) -> Mapping[str, Any]:
    cached = _SCHEMA_CACHE.get(name)
    if cached is not None:
        return cached
    path = SCHEMAS_DIR / name
    if not path.is_file():
        raise FileNotFoundError(
            f"schema cache missing: {path}. "
            f"Run scripts/check_schema_cache_freshness.py to refresh."
        )
    schema = json.loads(path.read_text(encoding="utf-8"))
    _SCHEMA_CACHE[name] = schema
    return schema  # type: ignore[no-any-return]


def _validate(record: Mapping[str, Any], schema_name: str) -> None:
    try:
        import jsonschema  # type: ignore[import-untyped]
    except ImportError as exc:
        raise SystemExit(
            "run_evidence: jsonschema is required. "
            "Install with `pip install jsonschema>=4.21`."
        ) from exc
    schema = _load_schema(schema_name)
    validator_cls = jsonschema.validators.validator_for(schema)
    validator = validator_cls(schema)
    errors = sorted(validator.iter_errors(record), key=lambda e: list(e.path))
    if errors:
        details = "; ".join(
            f"{'/'.join(str(p) for p in err.path) or '<root>'}: {err.message}"
            for err in errors
        )
        raise ValueError(
            f"run_evidence record does not validate against {schema_name}: {details}"
        )


# ----------------------------------------------------------------- emitters


def emit_event(event: Mapping[str, Any], ledger_path: Path) -> None:
    """Append-only writer for one Event record.

    Validates ``event`` against ``event.schema.json`` before writing.
    Writes a single canonical JSON line followed by a newline so the
    file remains valid JSONL.
    """
    _validate(event, "event.schema.json")
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event, sort_keys=True, ensure_ascii=False)
    with ledger_path.open("a", encoding="utf-8") as handle:
        handle.write(line)
        handle.write("\n")


def emit_run(run: Mapping[str, Any], record_path: Path) -> None:
    """Final Run record writer.

    Validates ``run`` against ``run.schema.json`` (with the amended
    replay-equivalence fields) before writing. Writes pretty-printed
    JSON with sorted keys so the file is diff-friendly across runs.
    """
    _validate(run, "run.schema.json")
    record_path.parent.mkdir(parents=True, exist_ok=True)
    record_path.write_text(
        json.dumps(run, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


# ----------------------------------------------------------------- event factory


def now_iso() -> str:
    """Return the current UTC timestamp in RFC 3339 form (second precision)."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def new_event_id() -> str:
    """Return a fresh UUIDv4 string for use as an event_id."""
    return str(uuid.uuid4())


def new_run_id() -> str:
    """Return a fresh run id of the shape ``run-<12hex>``."""
    return f"run-{uuid.uuid4().hex[:12]}"


def make_event(
    *,
    event_type: str,
    actor_kind: str,
    actor_id: str,
    payload: Mapping[str, Any],
    run_id: str | None = None,
    spec_id: str | None = None,
    artifact_id: str | None = None,
    parent_event_id: str | None = None,
    created_at: str | None = None,
) -> dict[str, Any]:
    """Construct an Event dict conformant to ``event.schema.json``.

    Optional fields are included only when supplied so the resulting
    dict matches the schema's ``additionalProperties: false`` constraint.
    """
    event: dict[str, Any] = {
        "event_id": new_event_id(),
        "type": event_type,
        "created_at": created_at or now_iso(),
        "actor": {"kind": actor_kind, "id": actor_id},
        "payload": dict(payload),
    }
    if run_id is not None:
        event["run_id"] = run_id
    if spec_id is not None:
        event["spec_id"] = spec_id
    if artifact_id is not None:
        event["artifact_id"] = artifact_id
    if parent_event_id is not None:
        event["parent_event_id"] = parent_event_id
    return event


# ----------------------------------------------------------------- replay-fields builder


@dataclass(frozen=True)
class RunEvidenceFields:
    """The replay-equivalence fields plus the list of names populated."""

    fields: dict[str, Any]
    populated: list[str]


def read_repo_text(path: Path) -> str:
    """Read a UTF-8 file from the repo; return empty string if missing."""
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8")


def build_run_evidence_fields(
    *,
    brief_path: Path | None = None,
    head_sha: str | None = None,
    gates: Sequence[Mapping[str, Any]] | None = None,
    playbook_text: str | None = None,
    extraction_prompts: Sequence[str] | None = None,
    synthesis_prompts: Sequence[str] | None = None,
    source_registry_yaml: str | None = None,
    extraction_schema: Mapping[str, Any] | None = None,
    llm_identifier: str = DEFAULT_LLM_IDENTIFIER,
    repo_path: Path | None = None,
) -> RunEvidenceFields:
    """Compute the six replay-equivalence fields where derivable.

    All arguments are keyword-only so the call site reads as a manifest.
    Missing sources are read from disk: ``playbook_text`` defaults to the
    current ``playbook/run-weekly-brief.md`` and ``source_registry_yaml``
    defaults to the current ``sources/registry.yaml``. ``gates`` is an
    iterable of either Event records (with ``type`` matching
    ``gate.check.*``) or simple gate-result mappings carrying ``name``
    and ``status`` keys; the aggregator splits the names into the two
    summary lists either way.

    ``brief_path`` and ``head_sha`` together determine
    ``sandbox_image_ref``: pass the brief directory for backfill (the
    publishing commit SHA is derived from git log), or pass the explicit
    ``head_sha`` to override.
    """
    fields: dict[str, Any] = {}
    populated: list[str] = []

    playbook_body = (
        playbook_text if playbook_text is not None else read_repo_text(PLAYBOOK_PATH)
    )
    prompt_hash = compute_sha256(
        canonicalize_prompt(
            playbook_body,
            list(extraction_prompts or []),
            list(synthesis_prompts or []),
        )
    )
    fields["prompt_snapshot_hash"] = prompt_hash
    populated.append("prompt_snapshot_hash")

    registry_text = (
        source_registry_yaml
        if source_registry_yaml is not None
        else read_repo_text(SOURCES_REGISTRY_PATH)
    )
    tool_hash = compute_sha256(
        canonicalize_tool_surface(
            registry_text, llm_identifier, extraction_schema or {}
        )
    )
    fields["tool_schemas_snapshot_hash"] = tool_hash
    populated.append("tool_schemas_snapshot_hash")

    resolved_sha = head_sha
    if resolved_sha is None and brief_path is not None:
        resolved_sha = publishing_commit_sha(brief_path, repo_path=repo_path)
    if resolved_sha is None:
        resolved_sha = current_head_sha(repo_path=repo_path)
    sandbox_ref = derive_sandbox_image_ref(
        repo_path=repo_path, head_sha=resolved_sha
    )
    if sandbox_ref is not None:
        fields["sandbox_image_ref"] = sandbox_ref
        populated.append("sandbox_image_ref")

    summary = aggregate_gate_results(gates or [])
    if summary is not None:
        fields["gate_results_summary"] = summary
        populated.append("gate_results_summary")

    return RunEvidenceFields(fields=fields, populated=populated)


def aggregate_gate_results(
    gates: Iterable[Mapping[str, Any]],
) -> dict[str, Any] | None:
    """Aggregate gate results from events or plain gate mappings.

    Accepts two input shapes:

    - Event records: ``type`` matches ``gate.check.passed`` or
      ``gate.check.failed``; ``payload.gate_name`` carries the name.
    - Plain mappings: ``name`` plus ``status`` (``passed`` or
      ``failed``).

    Returns ``None`` if the iterable carries no recognizable gate
    results so the caller can omit ``gate_results_summary`` for runs
    that ran zero gates.
    """
    passed: list[str] = []
    failed: list[str] = []
    seen_any = False
    for entry in gates:
        if not isinstance(entry, Mapping):
            continue
        event_type = entry.get("type")
        if isinstance(event_type, str) and event_type.startswith("gate.check."):
            seen_any = True
            payload = entry.get("payload") or {}
            name = (
                payload.get("gate_name")
                if isinstance(payload, Mapping)
                else None
            )
            if not isinstance(name, str) or not name:
                name = event_type
            if event_type == "gate.check.passed":
                passed.append(name)
            elif event_type == "gate.check.failed":
                failed.append(name)
            continue
        name = entry.get("name")
        status = entry.get("status")
        if not isinstance(name, str) or not isinstance(status, str):
            continue
        seen_any = True
        status_lower = status.strip().lower()
        if status_lower in {"passed", "pass", "ok", "true"}:
            passed.append(name)
        elif status_lower in {"failed", "fail", "error", "false"}:
            failed.append(name)
    if not seen_any:
        return None
    return {
        "gates_passed": passed,
        "gates_failed": failed,
        "all_passed": not failed,
    }


def parse_gates_arg(spec: str | None) -> list[dict[str, str]]:
    """Parse a CLI gates string like ``voice_lint:passed,spec_check:passed``.

    Accepts comma- or whitespace-separated entries; each entry is
    ``name:status``. Returns a list of plain mappings ready to feed
    :func:`aggregate_gate_results`. An empty or ``None`` input returns
    an empty list so the caller can fall back to a default gate set.
    """
    if not spec:
        return []
    out: list[dict[str, str]] = []
    for token in re.split(r"[,\s]+", spec.strip()):
        if not token:
            continue
        if ":" not in token:
            out.append({"name": token, "status": "passed"})
            continue
        name, status = token.split(":", 1)
        if name.strip():
            out.append({"name": name.strip(), "status": status.strip() or "passed"})
    return out


# ----------------------------------------------------------------- assemblers


def assemble_run_record(
    *,
    run_id: str,
    spec_id: str,
    agent_id: str,
    runtime: str,
    workspace_id: str,
    started_at: str,
    finished_at: str | None,
    status: str,
    inputs: Sequence[Mapping[str, str]],
    outputs: Sequence[Mapping[str, str]],
    evidence_fields: Mapping[str, Any],
) -> dict[str, Any]:
    """Assemble the final Run record dict ready for :func:`emit_run`.

    Leaves ``events`` empty by design: the source-of-truth event timeline
    lives in the JSONL ledger keyed by run_id. Downstream consumers (for
    example the trace-to-eval-harness packet generator) read the ledger,
    not the Run.events array.
    """
    run: dict[str, Any] = {
        "id": run_id,
        "spec_id": spec_id,
        "agent_id": agent_id,
        "runtime": runtime,
        "workspace_id": workspace_id,
        "started_at": started_at,
        "status": status,
        "inputs": [dict(item) for item in inputs],
        "events": [],
        "outputs": [dict(item) for item in outputs],
    }
    if finished_at is not None:
        run["finished_at"] = finished_at
    for key, value in evidence_fields.items():
        run[key] = value
    return run


def iso_week_dir_to_started_at(brief_dir_name: str) -> str:
    """Best-effort started_at for backfilled briefs.

    Maps ``YYYY-WNN`` to the Monday 00:00:00 UTC of that ISO week. The
    real run was a manual playbook pass spanning Friday morning; this
    is the deterministic anchor used when the live timestamp is lost.
    """
    match = re.fullmatch(r"(\d{4})-W(\d{2})", brief_dir_name.strip())
    if not match:
        return now_iso()
    year = int(match.group(1))
    week = int(match.group(2))
    # ISO week: %G %V %u with %u=1 = Monday.
    try:
        dt = datetime.strptime(
            f"{year}-{week:02d}-1", "%G-%V-%u"
        ).replace(tzinfo=timezone.utc)
    except ValueError:
        return now_iso()
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
