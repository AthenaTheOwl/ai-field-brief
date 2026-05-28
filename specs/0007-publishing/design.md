# design: publishing

Publishing reads from the same `.briefs-snapshot` directory as the
public archive. That keeps the static archive, feeds, and email body on
one content source.

The feed routes are static. The subscriber and digest routes are
dynamic because they call Resend and read deployment secrets. The
Resend integration uses the REST API directly:

- `POST /contacts` for subscriber capture.
- `POST /broadcasts` with `send: true` for the weekly digest.

The cron path supports a dry-run query so CI and operators can inspect
the exact subject and preview text without sending mail.

## run-evidence emitter

Brief generation emits run-evidence in three forms:

- `scripts/run_evidence.py` (library) — canonical hashing
  (`canonicalize_prompt`, `canonicalize_tool_surface`, `compute_sha256`),
  Event + Run constructors (`make_event`, `assemble_run_record`),
  schema-validating writers (`emit_event`, `emit_run`), and the
  replay-fields builder (`build_run_evidence_fields`).
- `scripts/finalize_run.py` (live CLI) — the playbook calls this at
  the publish step. Reads `briefs/YYYY-WNN/meta.yaml`, computes hashes
  against the live playbook + registry + HEAD SHA, writes the Run
  record plus the closing event ledger
  (`pipeline.start` → per-gate `gate.check.*` → `pipeline.complete` →
  `gate.run.evidence_recorded`).
- `scripts/backfill_run_records.py` (backfill CLI) — synthesizes Run +
  ledger for already-published briefs. Populates four of six
  replay-equivalence fields (`prompt_snapshot_hash`,
  `tool_schemas_snapshot_hash`, `sandbox_image_ref`,
  `gate_results_summary`); `determinism` and `checkpoint_ref` are
  omitted because the brief author calls a model API without pinned
  sampler knobs and there is no managed checkpoint store yet. The
  backfill writes the same closing events as the live CLI plus one
  synthetic `gate.check.passed` per canonical brief gate (the
  publishing commit landed on main, so CI required every gate to
  pass — the timestamps are synthetic but the gate names are real).

The `pipeline.complete` payload carries the typed `status` field
(constant `done` from both CLIs because finalize and backfill only
fire on a successful publish) plus a `gate_results_summary` clone, so
the closing event re-states the rollup the Run record claims.

The validator gate `scripts/validate_run_evidence.py` walks both
directories on every push and exits non-zero on schema violations.
The gate is wired into `.github/workflows/ci.yml` next to the other
`validate_*.py` gates. Beyond envelope validation, the validator
enforces, for every Run with `status == "done"`:

- The four required-for-done fields are present and non-empty.
- The ledger carries at least one `gate.run.evidence_recorded` event.
- `Run.prompt_snapshot_hash` and `Run.tool_schemas_snapshot_hash`
  equal the matching `pipeline.start` payload fields.
- `gate.run.evidence_recorded.payload.fields_populated` equals the
  sorted set of replay-equivalence fields actually populated on the
  Run.
- `Run.gate_results_summary` matches what scanning the ledger's
  `gate.check.passed` / `gate.check.failed` events produces
  (sorted `gates_passed`, sorted `gates_failed`,
  `all_passed == len(gates_failed) == 0`).

The cross-checks bridge the per-record schema validations: a
syntactically valid Run + ledger pair can still drift (a claimed hash
the ledger does not corroborate, or a rollup the gate events do not
support), and the cross-checks fail loudly with a message naming the
run_id and the specific check.
