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

## equivalence replay

`scripts/replay_run.py` is the per-Run replay command. It loads the
Run record and its event ledger, extracts the recorded SHA from
`sandbox_image_ref`, and exits 1 with a `git checkout <sha>`
instruction when `git rev-parse HEAD` does not match. At a matching
HEAD the CLI re-computes `prompt_snapshot_hash` and
`tool_schemas_snapshot_hash` against the current tree using the same
canonicalization the emitter uses (`scripts/run_evidence.py`), walks
every `Run.outputs[]` to verify the artifact exists at the recorded
path (hashing the file when the output carries a recorded hash), and
aggregates a verdict. `replay_equivalent` is true iff every check
matches; any divergence is named in the report's `divergences[]`
list.

The CLI writes two artifacts:

- `ops/event-ledger/replay-<run-id>-<ISO>.jsonl` is a new per-replay
  ledger carrying one `run.evidence.replayed` event with
  `replay_method: equivalence`. The source-of-truth ledger at
  `ops/event-ledger/<run-id>.jsonl` is not modified.
- `ops/replay-records/<run-id>/<replay-event-id>.json` carries the
  full verdict (per-check booleans plus aggregate
  `replay_equivalent` plus the recorded vs current value pairs).

The replay is equivalence-only because brief generation is an LLM-
agent playbook pass with no pinned model state; byte-replay is not
reachable. The `replay_method: equivalence` field on every emitted
event is the schema-level anchor for that boundary so a future
contributor reading the artifact does not conflate it with
deterministic replay.

For backfilled briefs, `sandbox_image_ref` records the SHA at which
the recorded snapshot hashes are reproducible (the records-
regeneration commit), not the brief-publishing commit. The publishing
commit stays recoverable via
`git log --diff-filter=A -- briefs/YYYY-WNN/brief.md`; the SHA the
replay verifies against is the one the Run record names. DEC-PUB-007
documents the semantic clarification.

## portable repo:// + artifact:// URIs

Round 6 (DEC-PUB-008) migrates ai-field-brief's run-evidence emitter
to the portable URI grammar defined in DEC-CDCP-014 (athena-site).
`sandbox_image_ref` becomes `repo://ai-field-brief@<sha>/`,
`inputs[].ref` becomes `repo://ai-field-brief@<sha>/<rel-path>`, and
`outputs[].artifact_id` becomes either `repo://ai-field-brief@<sha>/<rel-path>`
for path-shaped outputs or `artifact://ai-field-brief/<id>` for
logical artifact identifiers. `workspace_id` stays the bare repo
identifier (`ai-field-brief`) because it is an identity string, not a
file reference.

The validator and replay CLI ship a shared `resolve_uri(uri, portfolio_root)`
helper that accepts the new URI forms AND legacy local paths during the
interop window. The replay CLI's `parse_sandbox_sha` helper extracts
the SHA from both the new portable form and the legacy `<abs-path>@<sha>`
shape, so Run records produced under the previous emitter still replay.

## sandbox_image_ref off-by-one + two-pass protocol

The systemic off-by-one observed across four Round 5 agent reports:
the emitter reads `git rev-parse HEAD` BEFORE the regenerate commit
lands, so the recorded SHA names the PARENT of the commit that
actually contains the sample. DEC-PUB-008 closes this via a two-pass
protocol.

1. The emitter writes `repo://ai-field-brief@PENDING/` as a
   placeholder when called with `sandbox_sha_pending=True`. Every
   `inputs[].ref` and `outputs[].artifact_id` URI carries the same
   placeholder so the rewrite is one-shot.
   `scripts/backfill_run_records.py` always uses the placeholder;
   `scripts/finalize_run.py` accepts a `--sandbox-pending` flag for
   the same shape on live runs.

2. `scripts/finalize_sandbox_ref.py --all` (or `--run-id <id>`) reads
   the just-landed SHA via `git rev-parse HEAD` (or the `--sha`
   override) and rewrites every `@PENDING/` occurrence to `@<sha>/`
   in one or every Run record. The CLI is idempotent (no-op on
   records with no PENDING placeholders) and refuses to write a
   non-SHA value.

The regenerate workflow becomes: emit-with-placeholder → commit →
`finalize_sandbox_ref` → commit. The second commit's SHA is the SHA
the Run record names, so replay HEAD-strict succeeds at HEAD without
`git checkout` gymnastics. The Round 5 ad-hoc patches (hand-edit,
publishing-commit anchor, `--head-sha` override) are subsumed.
