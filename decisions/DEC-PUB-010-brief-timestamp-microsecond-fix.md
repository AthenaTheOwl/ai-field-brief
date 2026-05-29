---
id: DEC-PUB-010-brief-timestamp-microsecond-fix
spec: specs/0007-publishing/
requirement: R-PUB-026
date: 2026-05-29
status: approved
reversible: true
amends: DEC-PUB-009-ai-field-brief-ci-enforces-run-evidence-chain
decision: |
  ai-field-brief's `scripts/replay_run.py` uses microsecond-resolution
  timestamps for the per-replay event-ledger filename
  (`ops/event-ledger/replay-<run-id>-YYYY-MM-DDTHHMMSS.<micros>Z.jsonl`).
  This closes the latent per-second collision bug flagged by the
  Workflow B-Recovery cross-portfolio audit: the legacy form derived
  the filename timestamp from `run_evidence.now_iso()`, which carries
  only second precision, so two replays of the same Run inside one
  wall-clock second wrote to the same ledger filename and the second
  replay's event silently appended to the first replay's ledger.

  The fix is a local helper, `_now_filename_iso()`, inside
  `replay_run.py`. It reads `datetime.now(timezone.utc)` once and
  returns `YYYY-MM-DDTHH:MM:SS.<micros>Z`; the calling site strips
  colons for filesystem safety on Windows. The shared
  `run_evidence.now_iso()` stays at second precision because the
  in-event `created_at` and the Run record's `started_at` /
  `finished_at` fields use the canonical RFC 3339 second shape that
  every downstream consumer (validator, packet generator, event-
  ledger replay) already reads. The microsecond resolution is
  filename-local; the event payload's `created_at` continues to
  carry the unsanitized second-precision value.
alternatives:
  - label: append the replay_event_id (UUID) to the filename instead
      of upgrading the timestamp resolution (the chip-supply-chain-map
      pattern)
    rejected_because: |
      Two of the three Python repos that ship `replay_run.py`
      (supplier-risk-rag-agent via DEC-EVL-011 and
      procurement-negotiation-lab via DEC-FACTORY-013) already closed
      this bug with microsecond resolution. Picking the same shape
      here keeps the three Python implementations aligned so a future
      contributor reading the ledger-filename grammar sees one
      pattern across the portfolio, not two. The UUID-suffix
      alternative is fine in isolation but would diverge from the
      sibling repos for no semantic gain.
  - label: upgrade `run_evidence.now_iso()` itself to microsecond
      resolution so every event timestamp carries microseconds
    rejected_because: |
      `now_iso()` is the source-of-truth timestamp for the in-event
      `created_at` field, the Run record's `started_at` /
      `finished_at` fields, and the iso-week-to-started-at backfill
      anchor. Changing its return shape would ripple into every
      committed Run record and event ledger; downstream consumers
      (the validator, the trace-to-eval-harness packet generator,
      the per-week brief anchor) all read the second-precision shape
      and would need lock-step updates. The collision bug is
      filename-local; the fix should be filename-local too. A second
      helper inside `replay_run.py` carries the microsecond shape
      without touching the schema-validated event timestamps.
  - label: leave the bug alone because replay is invoked manually,
      not in tight loops, and the collision window is small in
      production
    rejected_because: |
      The cross-portfolio audit already named this as a contract
      gap. A determinism check or a rerun harness (the same shape
      that exposed the bug in supplier-risk and procurement-lab)
      would surface it immediately. Closing the gap now keeps the
      three Python repos at parity and removes a known sharp edge
      before the next replay-determinism gate lands.
rationale: |
  Workflow B-Recovery's cross-portfolio audit found the same
  per-second-collision bug in three Python repos that ship
  `scripts/replay_run.py`: supplier-risk-rag-agent (closed via
  DEC-EVL-011), procurement-negotiation-lab (closed via
  DEC-FACTORY-013), and ai-field-brief (this DEC). The bug is
  structural: the replay ledger filename was
  `replay-<run-id>-<ISO>.jsonl` where `<ISO>` came from a
  second-precision `now_iso()`, so any pair of replays of the same
  Run inside one second wrote to the same filename and the second
  event silently appended to the first ledger.

  The fix is the smallest possible change that matches the sibling
  repos. `_now_filename_iso()` is a four-line helper that reads
  the clock once and formats microseconds into the trailing field.
  The colons get stripped by the existing
  `safe_timestamp = ....replace(":", "")` line so the Windows
  filesystem stays happy. The dot separator before the microseconds
  is filesystem-safe on both Windows and POSIX.

  Keeping `run_evidence.now_iso()` at second precision is
  deliberate. The Run schema's `date-time` format accepts both
  shapes, so there is no schema-level pressure to upgrade. The
  collision bug is filename-local; widening the source-of-truth
  timestamp would touch every committed Run record without
  changing the failure mode. The local helper is the smaller blast
  radius.
evidence:
  - kind: decision
    ref: decisions/DEC-PUB-009-ai-field-brief-ci-enforces-run-evidence-chain.md
  - kind: decision
    ref: decisions/DEC-PUB-007-brief-replay-command.md
  - kind: code
    ref: scripts/replay_run.py
  - kind: code
    ref: tests/scripts/test_replay_run.py
  - kind: spec
    ref: specs/0007-publishing/requirements.md
  - kind: spec
    ref: specs/0007-publishing/acceptance.md
  - kind: spec
    ref: specs/0007-publishing/design.md
rollback: |
  Revert the `_now_filename_iso()` helper and restore the prior
  `safe_timestamp = replay_timestamp.replace(":", "")` line in
  `scripts/replay_run.py`; drop the `R-PUB-026` row from
  `specs/0007-publishing/requirements.md`; drop the matching
  acceptance bullet from `specs/0007-publishing/acceptance.md`; drop
  the design.md microsecond note; delete this DEC. The replay CLI
  reverts to second-precision filenames and the per-second
  collision window re-opens, matching pre-fix behavior. No data
  migration is needed because existing replay-ledger filenames in
  `ops/event-ledger/replay-*.jsonl` still match the
  `replay-<run-id>-*.jsonl` glob.
owner: science.proof-gate-runner
---

## decision

ai-field-brief's `scripts/replay_run.py` uses microsecond-resolution
timestamps for the per-replay event-ledger filename
(`ops/event-ledger/replay-<run-id>-YYYY-MM-DDTHHMMSS.<micros>Z.jsonl`).
This closes the latent per-second collision bug flagged by the
Workflow B-Recovery cross-portfolio audit. The legacy form derived
the filename timestamp from `run_evidence.now_iso()`, which carries
only second precision, so two replays of the same Run inside one
wall-clock second wrote to the same ledger filename and the second
replay's event silently appended to the first replay's ledger.

The fix is a local helper, `_now_filename_iso()`, inside
`replay_run.py`. It reads `datetime.now(timezone.utc)` once and
returns `YYYY-MM-DDTHH:MM:SS.<micros>Z`; the calling site strips
colons for filesystem safety on Windows. The shared
`run_evidence.now_iso()` stays at second precision because the
in-event `created_at` and the Run record's `started_at` and
`finished_at` fields use the canonical RFC 3339 second shape that
every downstream consumer (validator, packet generator, event-ledger
replay) already reads. The microsecond resolution is filename-local;
the event payload's `created_at` continues to carry the unsanitized
second-precision value.

## alternatives

- Append the `replay_event_id` (UUID) to the filename instead of
  upgrading the timestamp resolution (the chip-supply-chain-map
  pattern). Rejected because two of the three Python repos that ship
  `replay_run.py` already closed this bug with microsecond
  resolution. Matching the sibling shape keeps the three
  implementations aligned so a contributor reading the ledger-
  filename grammar sees one pattern across the portfolio, not two.
- Upgrade `run_evidence.now_iso()` itself to microsecond resolution
  so every event timestamp carries microseconds. Rejected because
  `now_iso()` is the source-of-truth timestamp for the in-event
  `created_at`, the Run record's `started_at` and `finished_at`, and
  the iso-week-to-started-at backfill anchor. Changing its return
  shape would ripple into every committed Run record and ledger;
  the collision bug is filename-local and the fix should be too.
- Leave the bug alone because replay is invoked manually and the
  collision window is small in production. Rejected because the
  cross-portfolio audit already named this as a contract gap, and a
  determinism check would surface it immediately. Closing it now
  keeps the three Python repos at parity.

## rationale

Workflow B-Recovery's cross-portfolio audit found the same
per-second-collision bug in three Python repos that ship
`scripts/replay_run.py`: supplier-risk-rag-agent (closed via
DEC-EVL-011), procurement-negotiation-lab (closed via
DEC-FACTORY-013), and ai-field-brief (this DEC). The bug is
structural: the replay ledger filename was
`replay-<run-id>-<ISO>.jsonl` where `<ISO>` came from a
second-precision `now_iso()`, so any pair of replays of the same
Run inside one second wrote to the same filename and the second
event silently appended to the first ledger.

The fix is the smallest possible change that matches the sibling
repos. `_now_filename_iso()` is a small helper that reads the clock
once and formats microseconds into the trailing field. The colons
get stripped by the existing
`safe_timestamp = ....replace(":", "")` line so the Windows
filesystem stays happy. The dot separator before the microseconds
is filesystem-safe on both Windows and POSIX.

Keeping `run_evidence.now_iso()` at second precision is deliberate.
The Run schema's `date-time` format accepts both shapes, so there
is no schema-level pressure to upgrade. The collision bug is
filename-local; widening the source-of-truth timestamp would touch
every committed Run record without changing the failure mode. The
local helper is the smaller blast radius.

## rollback

Revert the `_now_filename_iso()` helper and restore the prior
`safe_timestamp = replay_timestamp.replace(":", "")` line in
`scripts/replay_run.py`; drop the `R-PUB-026` row from
`specs/0007-publishing/requirements.md`; drop the matching
acceptance bullet from `specs/0007-publishing/acceptance.md`; drop
the design.md microsecond note; delete this DEC. The replay CLI
reverts to second-precision filenames and the per-second collision
window re-opens, matching pre-fix behavior. No data migration is
needed because existing replay-ledger filenames in
`ops/event-ledger/replay-*.jsonl` still match the
`replay-<run-id>-*.jsonl` glob.

## coverage

This DEC resolves the following requirement added to
`specs/0007-publishing/requirements.md`:

- `R-PUB-026` the replay ledger filename written by
  `scripts/replay_run.py` carries microsecond resolution so two
  replays of the same Run inside one wall-clock second land on
  distinct files. Closes the latent per-second collision bug
  flagged by the Workflow B-Recovery cross-portfolio audit; same
  fix as supplier-risk-rag-agent (DEC-EVL-011) and
  procurement-negotiation-lab (DEC-FACTORY-013).
