---
id: DEC-PUB-005-brief-emits-conformant-run-evidence
spec: specs/0007-publishing/
requirement: R-PUB-004
date: 2026-05-27
status: approved
reversible: true
decision: |
  Every weekly brief generation cycle MUST emit a conformant Event
  ledger plus a final Run record, with the replay-equivalence fields
  populated where derivable. The ledger lands at
  `ops/event-ledger/<run-id>.jsonl` and the Run record lands at
  `ops/run-records/<run-id>.json`; both conform to the cached
  cross-repo schemas mirrored from athena-site under
  `ops/schemas-cache/`. The emitter ships in three forms: a library
  (`scripts/run_evidence.py`), a publish-time CLI
  (`scripts/finalize_run.py`) that the playbook calls between
  voice-lint and commit, and a backfill CLI
  (`scripts/backfill_run_records.py`) that synthesizes records for
  already-published briefs. The validator gate at
  `scripts/validate_run_evidence.py` walks both directories on every
  push and exits non-zero on schema violations.
alternatives:
  - label: rely on briefs/YYYY-WNN/meta.yaml as the only run log
    rejected_because: |
      The meta.yaml is human-readable and useful for the next playbook
      run, but it does not carry the replay-equivalence fields
      (prompt_snapshot_hash, tool_schemas_snapshot_hash, sandbox_image_ref,
      gate_results_summary) that athena-site's DEC-CDCP-011 added to the
      Run schema. Without an emitter that populates those fields, the
      cross-repo amendment is a dead letter for ai-field-brief.
  - label: emit only the Run record, skip the per-step JSONL ledger
    rejected_because: |
      A Run record alone carries the rollup but not the timeline. The
      consumer-side packet generator in trace-to-eval-harness
      (`trace-to-eval evidence from-cdcp-events`, Codex's commit
      bfd1d48) reads CDCP event ledgers to produce review packets; the
      ledger is the source of the gate.check.*, tool.call.*, and
      pipeline.* events the consumer dispatches on. Skipping the
      ledger would break the bridge from ai-field-brief into the
      review packet flow.
  - label: emit run-evidence only on live runs, not on backfill
    rejected_because: |
      The first three published briefs (W20, W21, W22) shipped before
      this emitter existed. Without a backfill the run-records
      directory carries an arbitrary cutoff, and the cross-repo packet
      generator cannot draw a packet for the W22 demo that trace-to-eval
      phase D.1 will consume. Backfill closes that gap with the four
      fields derivable retroactively: prompt + tool hashes (current
      sources), sandbox_image_ref (publishing-commit SHA), and
      gate_results_summary (canonical brief-gate set, all passed
      because the brief landed on main).
  - label: populate all six replay-equivalence fields including
      determinism and checkpoint_ref
    rejected_because: |
      The brief author calls a model API without pinned sampler knobs,
      so determinism has no derivable values. There is no managed
      brief-run checkpoint store yet, so checkpoint_ref has nothing to
      reference. Populating those fields with placeholder values would
      lie about replay equivalence. The schema treats absence as "not
      derivable" — the honest record. This mirrors the choice the
      procurement-lab precedent made in DEC-FACTORY-007.
rationale: |
  This is the ai-field-brief emission slice of the Phase D run-evidence
  rollout. athena-site's DEC-CDCP-011 (commit f314fd7) amended the
  Run schema with six replay-equivalence fields. procurement-lab's
  DEC-FACTORY-007 shipped the first emitter in the portfolio with a
  fully automated pipeline at hand. ai-field-brief is the second
  portfolio repo to emit, and the orchestrator here is a human-driven
  playbook pass and not a Python pipeline — so the emitter ships
  in three forms (library, finalize CLI, backfill CLI) so the playbook
  can stay agent-readable while still producing engineering-grade
  artifacts.

  Run evidence is the bridge between agents and engineering-grade
  trust. Without it the brief author's pass is a black box: a draft
  appeared, gates passed, a commit landed. With it, the brief carries
  a Run record naming which playbook, which sources, which model, and
  which gates produced this brief — auditable in the same shape as
  every other Run record in the portfolio. The consumer-side packet
  generator (`trace-to-eval evidence from-cdcp-events`) reads these
  source fields to produce a review packet; Phase D.1 will wire the
  brief's emitted ledger through that CLI to generate a sample packet
  for W22.

  Listing the bridge in writing also makes it explicit which fields
  this repo populates today and which it does not, so a future
  contributor reading a Run record knows the absence of determinism
  and checkpoint_ref names "not derivable" and not "forgotten."
evidence:
  - kind: decision
    ref: athena-site/decisions/DEC-CDCP-011-run-schema-replay-equivalence-fields.md
  - kind: decision
    ref: procurement-negotiation-lab/decisions/DEC-FACTORY-007-factory-emits-conformant-run-evidence.md
  - kind: code
    ref: scripts/run_evidence.py
  - kind: code
    ref: scripts/finalize_run.py
  - kind: code
    ref: scripts/backfill_run_records.py
  - kind: code
    ref: scripts/validate_run_evidence.py
  - kind: spec
    ref: specs/0007-publishing/requirements.md
  - kind: doc
    ref: playbook/run-weekly-brief.md
rollback: |
  Remove the validator from `.github/workflows/ci.yml`, delete
  `scripts/validate_run_evidence.py`, `scripts/finalize_run.py`,
  `scripts/backfill_run_records.py`, and `scripts/run_evidence.py`,
  delete the `R-PUB-004..R-PUB-009` requirements from
  `specs/0007-publishing/requirements.md` plus the matching rows in
  `traceability.md`, drop this DEC, and remove the allowlist entries
  for `R-PUB-005..R-PUB-009`. The cached schemas stay because other
  validators still rely on them. No data migration is needed because
  the ledger files are append-only audit trails with no fan-out.
owner: science.proof-gate-runner
---

## decision

Every weekly brief generation cycle MUST emit a conformant Event ledger
plus a final Run record, with the replay-equivalence fields populated
where derivable. The ledger lands at `ops/event-ledger/<run-id>.jsonl`
and the Run record lands at `ops/run-records/<run-id>.json`; both
conform to the cached cross-repo schemas mirrored from athena-site
under `ops/schemas-cache/`. The emitter ships in three forms: a
library (`scripts/run_evidence.py`), a publish-time CLI
(`scripts/finalize_run.py`) the playbook calls between voice-lint and
commit, and a backfill CLI (`scripts/backfill_run_records.py`) that
synthesizes records for already-published briefs. The validator gate
at `scripts/validate_run_evidence.py` walks both directories on every
push and exits non-zero on violations.

## alternatives

- Rely on `briefs/YYYY-WNN/meta.yaml` as the only run log. Rejected
  because meta.yaml does not carry the replay-equivalence fields the
  cross-repo schema amendment added.
- Emit only the Run record, skip the per-step JSONL ledger. Rejected
  because the consumer-side packet generator in trace-to-eval-harness
  dispatches on the ledger event types.
- Emit run-evidence only on live runs, not on backfill. Rejected
  because the first three published briefs (W20, W21, W22) shipped
  before the emitter existed; without a backfill the records
  directory carries an arbitrary cutoff and the W22 demo packet has
  nothing to read.
- Populate all six replay-equivalence fields. Rejected because the
  brief author calls a model API without pinned sampler knobs and
  there is no managed checkpoint store yet; populating those fields
  with placeholders would lie about replay equivalence.

## rationale

Run evidence is the bridge between agents and engineering-grade trust.
athena-site's DEC-CDCP-011 amended the Run schema with the six
replay-equivalence fields; procurement-lab's DEC-FACTORY-007 shipped
the first emitter; ai-field-brief is the second. The brief author's
pass is a human-driven playbook pass, so the emitter ships in three
forms so the playbook stays agent-readable while still producing the
same Run-shaped artifacts every other Run in the portfolio emits.

The consumer-side packet generator (`trace-to-eval evidence
from-cdcp-events`, Codex's commit bfd1d48) reads the ledger to produce
review packets. Phase D.1 will wire ai-field-brief's emitted ledger
through that CLI to generate a sample packet for W22.

## evidence

- `athena-site/decisions/DEC-CDCP-011-run-schema-replay-equivalence-fields.md`
  is the schema source-of-truth.
- `procurement-negotiation-lab/decisions/DEC-FACTORY-007-factory-emits-conformant-run-evidence.md`
  is the first-emitter precedent.
- `scripts/run_evidence.py` is the emitter library.
- `scripts/finalize_run.py` is the live publish-time CLI.
- `scripts/backfill_run_records.py` is the backfill CLI.
- `scripts/validate_run_evidence.py` is the validator gate.
- `specs/0007-publishing/requirements.md` lists `R-PUB-004..R-PUB-009`.
- `playbook/run-weekly-brief.md` references `finalize_run.py` at the
  publish step.

## rollback

Remove the validator from `.github/workflows/ci.yml`, delete the four
new `scripts/*.py` files, drop the `R-PUB-004..R-PUB-009` rows from
`specs/0007-publishing/`, delete this DEC, and remove the allowlist
entries for `R-PUB-005..R-PUB-009`. The cached schemas stay because
other validators still rely on them. No data migration needed because
the ledger files are append-only audit trails.

## coverage

This DEC resolves the following requirements added to
`specs/0007-publishing/requirements.md`:

- `R-PUB-004` brief generation emits a conformant Event ledger to
  `ops/event-ledger/<run-id>.jsonl` on every Run (live and backfill).
- `R-PUB-005` brief generation emits a conformant Run record to
  `ops/run-records/<run-id>.json` per Run.
- `R-PUB-006` `prompt_snapshot_hash` and `tool_schemas_snapshot_hash`
  are always populated.
- `R-PUB-007` `sandbox_image_ref` is populated as repo-path plus HEAD
  SHA (or publishing-commit SHA for backfills).
- `R-PUB-008` `gate_results_summary` is populated from `gate.check.*`
  events on live runs and from the canonical brief-gate set on
  backfills.
- `R-PUB-009` `validate_run_evidence.py` runs on every push to main
  and exits non-zero on schema violations.
