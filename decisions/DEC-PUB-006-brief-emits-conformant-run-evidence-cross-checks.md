---
id: DEC-PUB-006-brief-emits-conformant-run-evidence-cross-checks
spec: specs/0007-publishing/
requirement: R-PUB-010
date: 2026-05-28
status: approved
reversible: true
amends: DEC-PUB-005-brief-emits-conformant-run-evidence
decision: |
  Brief generation's emitted run-evidence MUST satisfy four ledger/Run
  cross-checks plus a required-for-done field set, enforced by
  `scripts/validate_run_evidence.py`. For every Run with
  `status == "done"`, the validator fails when any of these conditions
  do not hold: `prompt_snapshot_hash`, `tool_schemas_snapshot_hash`,
  `sandbox_image_ref`, and `gate_results_summary` are all present and
  non-empty; the ledger carries at least one
  `gate.run.evidence_recorded` event; `Run.prompt_snapshot_hash` equals
  the matching `pipeline.start` payload field; `Run.tool_schemas_snapshot_hash`
  equals the matching `pipeline.start` payload field;
  `gate.run.evidence_recorded.payload.fields_populated` equals the
  sorted set of replay-equivalence fields populated on the
  Run; and `Run.gate_results_summary` matches what scanning the
  ledger's `gate.check.passed` / `gate.check.failed` events produces.
  The emitters (`scripts/finalize_run.py`,
  `scripts/backfill_run_records.py`) populate `pipeline.complete` with
  the typed `status` field plus a cloned `gate_results_summary`, and
  the backfill emits one `gate.check.passed` event per canonical brief
  gate so the rollup is verifiable.
alternatives:
  - label: validate only against the per-record schemas
    rejected_because: |
      The amended `event.schema.json` enforces the shape of every
      event-type payload, and `run.schema.json` enforces the Run record
      shape, but neither schema cross-checks the bridge between the
      two: a Run record could claim a prompt hash that disagrees with
      its `pipeline.start` event, or claim a gate rollup the ledger
      does not support, and both records would pass envelope
      validation. Codex's review of the Round 2 schema work named this
      gap explicitly; without cross-checks, the ledger and the Run
      drift independently and the consumer-side packet generator picks
      up the disagreement only when a packet replay fails.
  - label: enforce the cross-checks only on the consumer side
      (trace-to-eval-harness)
    rejected_because: |
      The consumer-side packet generator reads ai-field-brief's run
      records and ledger to produce review packets. Pushing the
      cross-check responsibility down-stream means every emitter in
      the portfolio re-implements the same checks in its own packet
      generator, and a malformed Run lands on `main` here before the
      consumer ever sees it. The emitter is the right place to fail
      fast — the same pattern procurement-lab's DEC-FACTORY-007 used
      for the schema-level checks.
  - label: drop per-gate events from backfills (keep the original
      "live timeline lost" shape)
    rejected_because: |
      Cross-check 4 requires the ledger to be the source-of-truth for
      `gate_results_summary`. If the backfill never emits gate.check.*
      events, the validator either lets the Run record claim any
      rollup it wants (no enforcement) or rejects every backfilled run
      (the existing shape). Emitting one `gate.check.passed` per
      canonical brief gate threads the needle: the gate timeline is
      synthetic (the live timestamps are lost) but the gate names are
      real (CI required every canonical gate to pass before the
      publishing commit landed). A future contributor reading the
      ledger sees the canonical-set anchor and not a vacuum.
rationale: |
  athena-site's DEC-CDCP-013 (commit bfc735a, Round 2 of the v2
  run-evidence engineering upgrade) amended `event.schema.json` to add
  typed per-event-type payloads, including a `status` field on
  `pipeline.complete` and an optional `gate_results_summary` clone.
  The amendment lets a downstream consumer read the closing event and
  trust the shape, but it does not enforce that the Run record's
  claimed rollup matches what the ledger says. Codex flagged
  this during the Round 2 review: schema typing closes the syntactic
  gap; cross-checks close the semantic one.

  This DEC amends DEC-PUB-005 with the cross-check enforcement that
  closes the semantic gap for ai-field-brief. The four cross-checks
  named in the decision body each turn a "the agent claimed X" Run
  field into a verifiable assertion against the ledger that the same
  Run produced.

  The cross-checks fail loudly with messages that name the run_id and
  the specific check, so a contributor inspecting a validator failure
  knows exactly which field on which Run to fix. The negative tests
  cover one mutation per check so a future refactor cannot silently
  weaken any of them.
evidence:
  - kind: decision
    ref: decisions/DEC-PUB-005-brief-emits-conformant-run-evidence.md
  - kind: decision
    ref: athena-site/decisions/DEC-CDCP-013-event-schema-typed-payloads.md
  - kind: code
    ref: scripts/validate_run_evidence.py
  - kind: code
    ref: scripts/finalize_run.py
  - kind: code
    ref: scripts/backfill_run_records.py
  - kind: code
    ref: tests/scripts/test_validate_run_evidence_cross_checks.py
  - kind: spec
    ref: specs/0007-publishing/requirements.md
rollback: |
  Revert the validator extension by restoring the pre-cross-check
  shape of `cross_check_done_runs` in
  `scripts/validate_run_evidence.py` (drop the function and its call
  site in `main`), revert the per-gate event emission in
  `scripts/backfill_run_records.py`, revert the `gate_results_summary`
  clone on `pipeline.complete` in `scripts/finalize_run.py` and
  `scripts/backfill_run_records.py`, delete
  `tests/scripts/test_validate_run_evidence_cross_checks.py`, drop the
  `R-PUB-010..R-PUB-013` rows from `specs/0007-publishing/`, and
  delete this DEC. The W20/W21/W22 sample records would then need to
  be regenerated under the pre-cross-check shape, or kept as-is (the
  envelope validation still passes). No data migration is needed
  because run records and ledgers are append-only audit trails with
  no fan-out.
owner: science.proof-gate-runner
---

## decision

Brief generation's emitted run-evidence MUST satisfy four ledger/Run
cross-checks plus a required-for-done field set, enforced by
`scripts/validate_run_evidence.py`. For every Run whose
`status == "done"`, the validator fails when any of the following
conditions does not hold:

- `prompt_snapshot_hash`, `tool_schemas_snapshot_hash`,
  `sandbox_image_ref`, and `gate_results_summary` are all present and
  non-empty on the Run record.
- The ledger carries at least one `gate.run.evidence_recorded` event
  for the Run.
- `Run.prompt_snapshot_hash` equals the matching `pipeline.start`
  payload field.
- `Run.tool_schemas_snapshot_hash` equals the matching `pipeline.start`
  payload field.
- `gate.run.evidence_recorded.payload.fields_populated` equals the
  sorted set of replay-equivalence fields populated on the
  Run.
- `Run.gate_results_summary` matches what scanning the ledger's
  `gate.check.passed` / `gate.check.failed` events produces (sorted
  `gates_passed`, sorted `gates_failed`, `all_passed == not gates_failed`).

The emitters (`scripts/finalize_run.py`,
`scripts/backfill_run_records.py`) write `pipeline.complete` with the
typed `status` field (constant `done` because both CLIs only fire on a
successful publish) plus a cloned `gate_results_summary`. The backfill
emits one `gate.check.passed` event per canonical brief gate so the
ledger is the verifiable source of the gate rollup.

## alternatives

- Validate only against the per-record schemas. Rejected because the
  schemas enforce shape but not bridge — a Run could claim hashes the
  ledger does not corroborate and both records would still pass.
- Push cross-check enforcement down to trace-to-eval-harness. Rejected
  because every emitter in the portfolio would then re-implement the
  same checks in its own packet generator, and malformed Runs land on
  `main` before the consumer ever sees them.
- Drop per-gate events from backfills. Rejected because cross-check 4
  requires the ledger to be the source-of-truth for
  `gate_results_summary`; emitting one `gate.check.passed` per
  canonical brief gate threads the needle.

## rationale

athena-site's DEC-CDCP-013 amended `event.schema.json` with typed
per-event-type payloads in Round 2 of the v2 run-evidence engineering
upgrade. The amendment closes the syntactic gap (a `pipeline.complete`
event without a `status` field now fails schema validation). Codex
flagged the semantic gap during the Round 2 review: typed payloads
catch shape drift, but a Run record could still claim a prompt hash
the ledger disagrees with, and both records would pass envelope
validation independently.

This DEC amends DEC-PUB-005 by adding the cross-check enforcement that
closes the semantic gap. Each of the four cross-checks turns a "the
agent claimed X" Run field into a verifiable assertion against the
ledger that the same Run produced. Each negative test covers one
mutation per check so a future refactor cannot silently weaken any of
them.

## evidence

- `decisions/DEC-PUB-005-brief-emits-conformant-run-evidence.md` is
  the DEC this one amends.
- `athena-site/decisions/DEC-CDCP-013-event-schema-typed-payloads.md`
  is the schema source the cross-checks lean on.
- `scripts/validate_run_evidence.py` carries the
  `cross_check_done_runs` function.
- `scripts/finalize_run.py` and `scripts/backfill_run_records.py` write
  the typed `pipeline.complete` payload and the per-gate events the
  cross-checks read.
- `tests/scripts/test_validate_run_evidence_cross_checks.py` covers
  one positive case and one negative case per check.
- `specs/0007-publishing/requirements.md` carries `R-PUB-010..R-PUB-013`.

## rollback

Revert the validator extension by dropping `cross_check_done_runs`
from `scripts/validate_run_evidence.py` and the call site in `main`,
revert the per-gate event emission in
`scripts/backfill_run_records.py`, revert the `gate_results_summary`
clone on `pipeline.complete` in both emitter CLIs, delete
`tests/scripts/test_validate_run_evidence_cross_checks.py`, drop the
new requirements from `specs/0007-publishing/`, and delete this DEC.
The sample records would then need to be regenerated, or kept as-is
because the envelope validation still passes.

## coverage

This DEC resolves the following requirements added to
`specs/0007-publishing/requirements.md`:

- `R-PUB-010` validator enforces required-for-done fields on every Run
  with `status == "done"`.
- `R-PUB-011` validator enforces hash agreement between the Run and
  `pipeline.start` for both `prompt_snapshot_hash` and
  `tool_schemas_snapshot_hash`.
- `R-PUB-012` validator enforces that the closing event's
  `fields_populated` equals the populated replay-equivalence fields on
  the Run.
- `R-PUB-013` validator enforces that `Run.gate_results_summary`
  matches what scanning `gate.check.*` events in the ledger produces.
