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
- Live runs additionally carry `gate.check.passed` or
  `gate.check.failed` per gate; backfills omit per-gate events because
  the live timeline is lost.

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
