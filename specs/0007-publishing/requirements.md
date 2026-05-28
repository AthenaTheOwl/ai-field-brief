# requirements: publishing

### R-PUB-001: public feed routes

The public site publishes RSS, Atom, and JSON Feed routes from the
same build-time brief snapshot used by the archive.

Acceptance:

- `/feed.xml`, `/atom.xml`, and `/feed.json` render without dynamic
  database access.
- Each feed links to the canonical brief URL for every published week.
- Feed dates come from `meta.yaml` when present.

### R-PUB-002: weekly email digest

The public site accepts subscriber emails and can send the latest
brief as a weekly Resend broadcast.

Acceptance:

- `/api/subscribe` adds a valid email to the configured Resend
  segment.
- `/api/cron/weekly-digest?dry_run=1` previews the current digest
  without sending email.
- The scheduled cron path sends only when the cron bearer secret is
  present and valid.
- The digest body links to the canonical brief and includes the
  Resend unsubscribe token.

### R-PUB-003: subscriber operations readiness

The public site exposes a credential-safe operator page for the weekly
email surface.

Acceptance:

- The page shows the latest digest week, subject, and preview text.
- The page reports whether the required Resend and cron environment
  keys are configured without printing secret values.
- The page links to the subscriber capture, dry-run, RSS, and JSON
  Feed endpoints.
- Tests cover the readiness model for missing and configured
  environments.

### R-PUB-004: brief generation emits an event ledger

Every weekly brief generation cycle (live runs and backfills both)
writes a conformant Event ledger to `ops/event-ledger/<run-id>.jsonl`.

Acceptance:

- The ledger file is append-only JSONL; every line conforms to
  `ops/schemas-cache/event.schema.json`.
- The ledger carries at least `pipeline.start`, `pipeline.complete`,
  and `gate.run.evidence_recorded` for every Run.
- Both live runs and backfills carry one `gate.check.passed` or
  `gate.check.failed` event per gate. Live runs derive the timeline
  from the gate runner; backfills synthesize a `gate.check.passed`
  per canonical brief gate (the publishing commit landed on main, so
  CI required every canonical gate to pass).
- The `pipeline.complete` payload carries the typed `status` field
  (one of `done`, `failed`, `cancelled`) plus an optional
  `gate_results_summary` cloned from the Run record.

### R-PUB-005: brief generation emits a run record

Every weekly brief generation cycle writes a conformant Run record to
`ops/run-records/<run-id>.json`.

Acceptance:

- The record conforms to the amended
  `ops/schemas-cache/run.schema.json` (with the six replay-equivalence
  fields).
- `id`, `spec_id`, `agent_id`, `runtime`, `workspace_id`,
  `started_at`, `status`, `inputs`, and `outputs` are populated.
- `events` is empty by design — the source-of-truth timeline lives in
  the JSONL ledger keyed by `run_id`.

### R-PUB-006: prompt and tool hashes are always populated

`prompt_snapshot_hash` and `tool_schemas_snapshot_hash` are populated
on every emitted Run record.

Acceptance:

- `prompt_snapshot_hash` is the SHA-256 of canonicalized playbook
  content plus active extraction and synthesis prompts.
- `tool_schemas_snapshot_hash` is the SHA-256 of the canonicalized
  source registry plus the LLM identifier plus the extraction schema.
- Both fields match `^[a-f0-9]{64}$`.

### R-PUB-007: sandbox image ref names the repo HEAD or publishing SHA

`sandbox_image_ref` is populated on every emitted Run record as
`<repo-path>@<HEAD-SHA>`.

Acceptance:

- Live runs use the current `git rev-parse HEAD` of the ai-field-brief
  workspace.
- Backfills use the SHA of the commit that first introduced the brief
  under `briefs/YYYY-WNN/brief.md`.
- The field is omitted (not set to a partial value) when no SHA is
  derivable.

### R-PUB-008: gate results summary is populated from gates

`gate_results_summary` is populated on every emitted Run record,
splitting names into `gates_passed`, `gates_failed`, and `all_passed`.

Acceptance:

- Live runs aggregate names from `gate.check.passed` and
  `gate.check.failed` events.
- Backfills populate the summary from the canonical brief-gate set
  (every CI gate the publishing commit must have passed).
- `all_passed` is `true` iff `gates_failed` is empty.

### R-PUB-009: validate_run_evidence gates the repo

`scripts/validate_run_evidence.py` runs on every push to `main` and
exits non-zero on schema violations.

Acceptance:

- The script validates every `ops/event-ledger/*.jsonl` line against
  `event.schema.json` and every `ops/run-records/*.json` against
  `run.schema.json`.
- The script cross-checks that every `run_id` carrying a terminal
  event (`pipeline.complete` or `gate.run.evidence_recorded`) has a
  matching Run record file.
- The script is wired into `.github/workflows/ci.yml` next to the
  other `validate_*.py` gates.

### R-PUB-010: required-for-done fields gate every published Run

For every Run record with `status == "done"`,
`scripts/validate_run_evidence.py` enforces that the four
replay-equivalence fields ai-field-brief populates are all present
and non-empty.

Acceptance:

- The required-for-done field set is `prompt_snapshot_hash`,
  `tool_schemas_snapshot_hash`, `sandbox_image_ref`, and
  `gate_results_summary`.
- A missing or empty value on any of the four fails the validator
  with a message naming the run_id and the missing field.
- The ledger for every done Run carries at least one
  `gate.run.evidence_recorded` event; a missing terminal event also
  fails the validator.

### R-PUB-011: hash agreement between Run and pipeline.start

`Run.prompt_snapshot_hash` and `Run.tool_schemas_snapshot_hash` must
each equal the matching `pipeline.start` event payload field.

Acceptance:

- The validator reads the first `pipeline.start` event from the
  Run's ledger and compares both hashes.
- Any mismatch fails the validator with a message naming the run_id,
  the field, the Run-side value, and the event-side value.

### R-PUB-012: fields_populated matches Run's populated fields

The closing `gate.run.evidence_recorded` event's
`payload.fields_populated` list must equal the sorted set of
replay-equivalence fields actually populated on the Run record.

Acceptance:

- The validator computes the sorted populated subset from the Run
  (over the six canonical field names) and compares against the
  sorted event payload list.
- Any mismatch fails the validator with a message naming the run_id,
  the claimed list, and the actual list.

### R-PUB-013: gate_results_summary matches ledger gate events

`Run.gate_results_summary` must match what scanning the ledger's
`gate.check.passed` and `gate.check.failed` events produces.

Acceptance:

- `gates_passed` equals the sorted list of `gate_name` from
  `gate.check.passed` events.
- `gates_failed` equals the sorted list of `gate_name` from
  `gate.check.failed` events.
- `all_passed` equals `len(gates_failed) == 0`.
- Any mismatch on any of the three fields fails the validator with a
  message naming the run_id, the field, the Run-side value, and the
  ledger-derived value.

### R-PUB-014: equivalence replay command per Run

ai-field-brief ships `scripts/replay_run.py` performing equivalence
replay against any backfilled or live brief Run record. The CLI is
HEAD-strict and does not re-call the LLM.

Acceptance:

- `python scripts/replay_run.py --run-id <id>` reads
  `ops/run-records/<id>.json` and `ops/event-ledger/<id>.jsonl`.
- The CLI extracts the recorded SHA from `sandbox_image_ref` and exits
  1 with a `git checkout <sha>` instruction when `git rev-parse HEAD`
  does not match.
- The emitted `run.evidence.replayed` event carries
  `replay_method: equivalence` so the boundary against deterministic
  replay is explicit on every event.
- A missing Run record exits 1 with a pointer to the records
  directory layout.

### R-PUB-015: replay re-computes both snapshot hashes

At a matching HEAD the replay CLI re-computes
`prompt_snapshot_hash` and `tool_schemas_snapshot_hash` against the
current tree and compares to the recorded Run-side values.

Acceptance:

- `prompt_snapshot_hash` is recomputed against the current playbook +
  extraction prompts + synthesis prompts using
  `run_evidence.canonicalize_prompt`.
- `tool_schemas_snapshot_hash` is recomputed against the current
  source registry + extraction schema + active LLM identifier using
  `run_evidence.canonicalize_tool_surface`.
- Any mismatch flips `replay_equivalent` to false and names the
  diverged field in `divergences[]` on the replay report.

### R-PUB-016: replay verifies every Run output

The replay CLI walks `Run.outputs[]`, verifies each named artifact
exists at the recorded path, and hashes the current file when the
output carries a recorded hash.

Acceptance:

- A missing output file flips `outputs_check.all_ok` to false and
  records `divergence: "artifact missing at recorded path"` for the
  output in `outputs_check.details`.
- When an output carries a recorded hash (`content_sha256`, `hash`,
  or `sha256`), the CLI hashes the current file and compares.
- When no hash is recorded on the output, the check is
  existence-only and the report records `hash_recorded: false` for
  that output (backfills currently take this path).

### R-PUB-017: replay emits a typed event and a verdict report

Each replay run appends one `run.evidence.replayed` event to a new
per-replay ledger file and writes the full verdict to a replay record.

Acceptance:

- The new per-replay ledger lands at
  `ops/event-ledger/replay-<run-id>-<ISO>.jsonl`; the source-of-truth
  ledger at `ops/event-ledger/<run-id>.jsonl` is not appended to.
- The verdict report lands at
  `ops/replay-records/<run-id>/<replay-event-id>.json` with the per-
  check booleans (`head_check`, `prompt_snapshot_hash_check`,
  `tool_schemas_snapshot_hash_check`, `outputs_check`), the
  aggregate `replay_equivalent` verdict, and the `divergences[]`
  list.
- The emitted event passes `event.schema.json` envelope validation
  under the typed `run.evidence.replayed` branch.
- The CLI exits 0 on equivalent and 1 on any divergence.
