---
id: DEC-PUB-011-ai-field-brief-chaos-test-suite
spec: specs/0007-publishing/
requirement: R-PUB-027
date: 2026-05-29
status: approved
reversible: true
amends: DEC-PUB-010-brief-timestamp-microsecond-fix
decision: |
  ai-field-brief installs a chaos test suite at
  `tests/scripts/test_chaos_run_evidence.py` that walks seven mutation
  classes against the canonical Run + ledger sample on disk and
  asserts that `scripts/validate_run_evidence.py` exits non-zero on
  every class. The suite is wired into
  `.github/workflows/run-evidence-gates.yml` as a new
  `chaos-validation` job that runs on every pull request and every
  push to main.

  The seven mutation classes cover Round 3's four cross-checks,
  Round 2's typed event payload validation, and the required-for-done
  gate:

  - M1: flip `Run.prompt_snapshot_hash` to a different valid-shaped
    hash. Cross-check 1 should fire.
  - M2: flip `Run.tool_schemas_snapshot_hash` to a different hash.
    Cross-check 2 should fire.
  - M3: add a phantom gate name to
    `Run.gate_results_summary.gates_passed`. Cross-check 4 should
    fire.
  - M4: drop the terminal `gate.run.evidence_recorded` event from the
    ledger. The required-terminal-event check should fire.
  - M5: drop `prompt_snapshot_hash` from the pipeline.start payload.
    The typed-event-payload validation (the `oneOf` discriminator on
    `event.schema.json`) should fire.
  - M6: claim a replay-equivalence field on the
    `gate.run.evidence_recorded.payload.fields_populated` list that
    the Run record does not populate. Cross-check 3 should
    fire.
  - M7: keep `Run.status = "done"` but drop `sandbox_image_ref`. The
    required-for-done gate should fire.

  Every chaos test copies the canonical sample into `tmp_path` before
  mutating. The on-disk canonical sample is never modified. A guard
  test reads the disk-resident sample at the end of the run and
  asserts the load-bearing fields are still present, so a future
  mistake that mutates the source surfaces immediately.
alternatives:
  - label: rely on the existing
      `tests/scripts/test_validate_run_evidence_cross_checks.py`
      suite as the only mutation coverage
    rejected_because: |
      The cross-checks test builds a minimum-viable Run + ledger pair
      in-memory and mutates that. It proves the validator's checks
      fire on a synthetic fixture but it does not prove the checks
      fire on the actual canonical sample that ships with the repo.
      A chaos suite that starts from the on-disk canonical sample
      catches a different failure mode: a validator regression that
      only manifests against the real shape of a backfilled Run (the
      `repo://` URI form, the twelve-gate rollup, the
      `prompt_snapshot_hash` matched against the synthesized
      pipeline.start). The two suites are complementary; chaos is
      the closing pass.
  - label: only test mutations against Round 3's cross-checks and
      skip the typed-payload (M5) and required-for-done (M7) classes
    rejected_because: |
      The task brief names seven mutation classes for a reason. M5
      proves Round 2's typed event payload schema rejects
      events that lose required fields; without M5, a future schema
      edit that loosens the `pipeline.start` `oneOf` branch could
      silently broaden what the validator accepts. M7 proves the
      required-for-done gate (not a cross-check but the first wall
      every done Run hits) still fires; without M7, a regression
      that bypassed the required-for-done loop would slip past the
      cross-check coverage. Seven classes is the right cardinality
      for closing the validator-coverage gap.
  - label: implement the chaos suite as a standalone script under
      `scripts/` instead of as a pytest module
    rejected_because: |
      Every other validator-coverage suite in the repo ships under
      `tests/scripts/` and runs via `pytest`
      (`test_validate_run_evidence_cross_checks.py`,
      `test_run_evidence_cli.py`,
      `test_finalize_sandbox_ref.py`). The chaos suite follows the
      same shape so a contributor reading the test layout sees one
      pattern, and so the CI step is a single `pytest` invocation
      instead of a bespoke script driver. A standalone script would
      diverge from the local pattern for no gain.
rationale: |
  This is the closing pass of the engineering-grade upgrade for
  ai-field-brief's run-evidence chain. Round 1 emitted the records.
  Round 2 added the typed payload schema. Round 3 added the four
  Run + ledger cross-checks. Round 4 wired everything into CI. The
  gap that remained: nothing proved that the checks added in
  Rounds 2 and 3 would fire on a mutated canonical sample.
  A validator that quietly regressed to a no-op would let every
  bad Run through and the silence would only be broken when a
  replay drift surfaced months later.

  The chaos suite closes that gap with one mutation per class. Each
  mutation is the smallest possible change that violates one check;
  each assertion names the run_id plus the expected substring in
  the validator output so a regression that ate the wrong error
  message still surfaces a failure. The canonical sample on disk
  is the test fixture, copied into `tmp_path` per mutation so the
  ledger and Run record on disk are never touched.

  Wiring the suite into `run-evidence-gates.yml` as a parallel job
  (not folded into `packet-and-replay`) keeps the matrix legs
  independent: a chaos failure does not block the per-sample
  packet-and-replay run, and a packet-and-replay failure does not
  block the chaos sweep. Both are blocking gates per DEC-CDCP-015;
  neither carries `continue-on-error`.
evidence:
  - kind: decision
    ref: decisions/DEC-PUB-005-brief-emits-conformant-run-evidence.md
  - kind: decision
    ref: decisions/DEC-PUB-006-brief-emits-conformant-run-evidence-cross-checks.md
  - kind: decision
    ref: decisions/DEC-PUB-009-ai-field-brief-ci-enforces-run-evidence-chain.md
  - kind: decision
    ref: decisions/DEC-PUB-010-brief-timestamp-microsecond-fix.md
  - kind: code
    ref: scripts/validate_run_evidence.py
  - kind: code
    ref: tests/scripts/test_chaos_run_evidence.py
  - kind: code
    ref: tests/scripts/test_validate_run_evidence_cross_checks.py
  - kind: spec
    ref: specs/0007-publishing/requirements.md
  - kind: spec
    ref: specs/0007-publishing/acceptance.md
rollback: |
  Delete `tests/scripts/test_chaos_run_evidence.py`; revert the
  `chaos-validation` job added to
  `.github/workflows/run-evidence-gates.yml`; drop the `R-PUB-027`,
  `R-PUB-028`, and `R-PUB-029` rows from
  `specs/0007-publishing/requirements.md`; drop the matching
  acceptance bullets from `specs/0007-publishing/acceptance.md`;
  drop the matching rows from
  `specs/0007-publishing/traceability.md`; delete this DEC. The
  run-evidence chain reverts to the Round-3 + Round-4 coverage
  (cross-check unit tests plus the per-sample packet-and-replay
  matrix); the validator-coverage gap that this DEC closes
  re-opens. No artifact migration is needed because the chaos
  suite copies the canonical sample into `tmp_path` and never
  mutates anything on disk.
owner: science.proof-gate-runner
---

## decision

ai-field-brief installs a chaos test suite at
`tests/scripts/test_chaos_run_evidence.py` that walks seven mutation
classes against the canonical Run + ledger sample on disk and
asserts that `scripts/validate_run_evidence.py` exits non-zero on
every class. The suite is wired into
`.github/workflows/run-evidence-gates.yml` as a new
`chaos-validation` job that runs on every pull request and every
push to main.

The seven mutation classes cover Round 3's four cross-checks,
Round 2's typed event payload validation, and the required-for-done
gate. M1 flips `Run.prompt_snapshot_hash` to a different valid-shaped
hash, exercising cross-check 1. M2 flips
`Run.tool_schemas_snapshot_hash`, exercising cross-check 2. M3 adds a
phantom gate name to `Run.gate_results_summary.gates_passed`,
exercising cross-check 4. M4 drops the terminal
`gate.run.evidence_recorded` event from the ledger, exercising the
required-terminal-event check. M5 drops `prompt_snapshot_hash` from
the `pipeline.start` payload, exercising the typed-event-payload
validation. M6 claims a replay-equivalence field on the
`gate.run.evidence_recorded.payload.fields_populated` list that the
Run record does not populate, exercising cross-check 3. M7
keeps `Run.status = "done"` but drops `sandbox_image_ref`, exercising
the required-for-done gate.

Every chaos test copies the canonical sample into `tmp_path` before
mutating. The on-disk canonical sample is never modified. A guard
test reads the disk-resident sample at the end of the run and
asserts the load-bearing fields are still present, so a future
mistake that mutates the source surfaces immediately.

## alternatives

- Rely on the existing
  `tests/scripts/test_validate_run_evidence_cross_checks.py` suite
  as the only mutation coverage. Rejected because that suite builds
  a synthetic in-memory pair; it proves the checks fire on a
  fixture but not on the actual canonical sample. The chaos suite
  starts from the on-disk shape (the `repo://` URI form, the
  twelve-gate rollup, the synthesized pipeline.start) and is
  complementary to the cross-checks unit suite.
- Only test mutations against Round 3's cross-checks and skip the
  typed-payload (M5) and required-for-done (M7) classes. Rejected
  because M5 proves Round 2's typed event payload schema rejects
  events that lose required fields, and M7 proves the
  required-for-done gate still fires. Seven classes is the right
  cardinality for closing the coverage gap.
- Implement the chaos suite as a standalone script under `scripts/`
  instead of as a pytest module. Rejected because every other
  validator-coverage suite in the repo ships under `tests/scripts/`
  and runs via pytest. Matching the local pattern keeps the test
  layout legible and the CI step a single pytest invocation.

## rationale

This is the closing pass of the engineering-grade upgrade for
ai-field-brief's run-evidence chain. Round 1 emitted the records.
Round 2 added the typed payload schema. Round 3 added the four
Run + ledger cross-checks. Round 4 wired everything into CI. The
gap that remained: nothing proved that the checks added in
Rounds 2 and 3 would fire on a mutated canonical sample.
A validator that quietly regressed to a no-op would let every bad
Run through and the silence would only be broken when a replay
drift surfaced months later.

The chaos suite closes that gap with one mutation per class. Each
mutation is the smallest possible change that violates one check;
each assertion names the run_id plus the expected substring in
the validator output so a regression that ate the wrong error
message still surfaces a failure. The canonical sample on disk is
the test fixture, copied into `tmp_path` per mutation so the
ledger and Run record on disk are never touched.

Wiring the suite into `run-evidence-gates.yml` as a parallel job
keeps the matrix legs independent: a chaos failure does not block
the per-sample packet-and-replay run, and a packet-and-replay
failure does not block the chaos sweep. Both are blocking gates
per DEC-CDCP-015; neither carries `continue-on-error`.

## rollback

Delete `tests/scripts/test_chaos_run_evidence.py`; revert the
`chaos-validation` job added to
`.github/workflows/run-evidence-gates.yml`; drop the `R-PUB-027`,
`R-PUB-028`, and `R-PUB-029` rows from
`specs/0007-publishing/requirements.md`; drop the matching
acceptance bullets from `specs/0007-publishing/acceptance.md`;
drop the matching rows from
`specs/0007-publishing/traceability.md`; delete this DEC. The
run-evidence chain reverts to the Round-3 + Round-4 coverage
(cross-check unit tests plus the per-sample packet-and-replay
matrix); the validator-coverage gap that this DEC closes
re-opens. No artifact migration is needed because the chaos
suite copies the canonical sample into `tmp_path` and never
mutates anything on disk.

## coverage

This DEC resolves the following requirements added to
`specs/0007-publishing/requirements.md`:

- `R-PUB-027`: chaos test suite covers seven mutation classes
  against the canonical Run + ledger sample.
- `R-PUB-028`: the chaos suite is wired into
  `.github/workflows/run-evidence-gates.yml` as a blocking
  `chaos-validation` job.
- `R-PUB-029`: every chaos test copies the canonical sample into
  `tmp_path` and a guard asserts the on-disk sample is unchanged.
