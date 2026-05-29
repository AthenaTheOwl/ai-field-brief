---
id: DEC-PUB-009-ai-field-brief-ci-enforces-run-evidence-chain
spec: specs/0007-publishing/
requirement: R-PUB-022
date: 2026-05-29
status: approved
reversible: true
amends: DEC-PUB-008-brief-portable-repo-uri-migration
decision: |
  ai-field-brief's CI workflows enforce the run-evidence gate chain
  locked by DEC-CDCP-015 (athena-site) on every pull request and every
  push to main. The existing `.github/workflows/ci.yml` keeps the
  universal gates (schema-cache freshness, voice lint, no-BOM,
  spec-check, decisions validation, validate_run_evidence, pnpm
  lint/typecheck/test/build); a new
  `.github/workflows/run-evidence-gates.yml` adds the
  product-repo-specific gates from the contract:
  packet-generation-from-canonical-sample, packet-validation, and
  replay-smoke. Every gate runs as a matrix over the three canonical
  samples (`run-36e307499472`, `run-d74d787e6756`,
  `run-1f1fc1f3d36d`) so the chain is exercised end-to-end per Run.
  No `continue-on-error: true` and no `if: ${{ failure() }}` on any
  contract gate. No `--no-verify` bypass anywhere.

  The replay-smoke step closes the two-pass tail from DEC-PUB-008
  without modifying the canonical sample: after `git checkout
  <sandbox-sha>` the gate restores `ops/run-records/` and
  `ops/event-ledger/` from main so the on-disk
  `sandbox_image_ref` carries the finalized SHA (matching the just-
  checked-out HEAD) instead of the historical `@PENDING/` placeholder.
  This proves three things in one step: the recorded SHA is reachable
  in git history, the canonicalization at that SHA reproduces the
  recorded snapshot hashes, and every output named in the Run still
  exists at its recorded path.

  The trace-to-eval-harness sibling repo is checked out at
  `${{ github.workspace }}/trace-to-eval-harness` and pip-installed
  into the runner so `python -m trace_to_eval evidence
  from-cdcp-events` and `python -m trace_to_eval evidence validate`
  are callable. `--portfolio-root ${{ github.workspace }}` lets
  trace-to-eval-harness resolve `repo://ai-field-brief@<sha>/<path>`
  URIs into the checked-out tree.
alternatives:
  - label: extend the existing ci.yml with the new jobs instead of
      adding a second workflow file
    rejected_because: |
      The two contract surfaces have different needs: ci.yml stays
      single-checkout (pnpm + Python gates against the PR HEAD), while
      run-evidence-gates.yml needs a sibling checkout of
      trace-to-eval-harness AND a matrix over the three canonical
      samples AND a per-step `git checkout <sandbox-sha>` that would
      destabilize ci.yml's other jobs if they ran on the same checkout.
      Splitting the workflow keeps each file focused: ci.yml gates the
      working tree's correctness, run-evidence-gates.yml gates the
      run-evidence chain. Both block merges to main per
      DEC-CDCP-008's enforcement contract.
  - label: skip the replay-smoke gate entirely and rely on the
      committed `ops/replay-records/` verdicts as the proof
    rejected_because: |
      The committed replay records are a snapshot, not a contract.
      They prove the chain worked once at the moment of commit; they
      do not prove the chain still works on every PR. DEC-CDCP-015's
      replay-smoke gate is the running-CI proof: every PR re-derives
      the snapshot hashes at the recorded SHA against the current
      run_evidence.py canonicalization, so a regression that breaks
      replay equivalence is caught immediately on the PR that
      introduces it, not on the next regeneration pass. The committed
      verdicts stay as evidence; the CI gate stays as enforcement.
  - label: run packet generation + validation + replay smoke against
      only the W22 sample to halve CI time
    rejected_because: |
      The three samples are not interchangeable. W20 and W21 were
      backfilled from the publishing commits; W22 was regenerated
      under the two-pass protocol. Each sample exercises a slightly
      different code path through `run_evidence.py` and
      `replay_run.py`, and a regression in the backfill path that the
      W22 path does not exercise would slip past a single-sample gate.
      Running all three keeps the gate honest. CI matrix parallelism
      means the wall-clock cost is one job's worth of time, not three.
  - label: drop the `git checkout <sandbox-sha>` step and run replay
      from the PR HEAD with the recorded SHA as a soft check
    rejected_because: |
      Replay HEAD-strict is the load-bearing semantic from DEC-PUB-007.
      Running replay from a non-matching HEAD short-circuits before
      the hash recomputation step, so the gate would pass on a
      mutation that breaks the canonicalization helper. The strict
      semantic is the whole point of equivalence replay; the gate has
      to honor it. The records-restore-from-main step is the surgical
      fix for the two-pass tail without losing HEAD-strict semantics.
rationale: |
  DEC-CDCP-015 (athena-site) names the difference between "we have
  artifacts" and "main cannot accept unverifiable work." This DEC is
  ai-field-brief's local landing of that contract. The universal gates
  were already wired by DEC-CDCP-008 and DEC-PUB-006; the new piece is
  the product-repo-specific chain (packet generation → packet
  validation → replay smoke) running per canonical sample on every PR.

  The matrix shape is deliberate. Each sample exercises a distinct
  code path through `run_evidence.py` and `replay_run.py`, and the
  trace-to-eval-harness packet generator dereferences `repo://`
  URIs differently for backfilled versus regenerated records. A
  single-sample gate would let a regression in the unexercised path
  ride into main; the three-sample matrix closes that gap at the cost
  of one job's wall-clock time (matrix jobs run in parallel).

  The replay-smoke step's records-restore-from-main pattern is the
  honest engineering answer to the two-pass tail from DEC-PUB-008.
  At the recorded sandbox SHA the Run record itself carries
  `@PENDING/` because the SHA was not knowable at emit time; the
  records-on-main carry the finalized SHA. The gate checks out the
  recorded SHA (proving reachability + giving replay the right tree
  to hash against), then restores the records and ledger from main
  (so the on-disk sandbox_image_ref matches HEAD), then runs replay.
  Replay equivalent at this configuration proves the recorded SHA is
  reachable, the canonicalization at that SHA reproduces the recorded
  snapshot hashes, and every output exists at its recorded path. The
  alternative — re-finalizing the canonical samples to embed the
  records-containing SHA at the records-containing SHA — is a
  recursive-tail problem that the two-pass protocol explicitly
  documents as unreachable in one pass; the gate honors that
  documentation by working with the protocol, not against it.

  The pnpm audit step in `ci.yml` keeps its `|| true` suffix because
  it is a security advisory surface, not a DEC-CDCP-015 contract
  gate; the universal gates list in the contract does not include
  dependency advisories. That stays scoped under
  `.github/workflows/ci.yml::security` and is governed by a future
  security DEC, not this one.
evidence:
  - kind: decision
    ref: decisions/DEC-PUB-008-brief-portable-repo-uri-migration.md
  - kind: decision
    ref: decisions/DEC-PUB-007-brief-replay-command.md
  - kind: decision
    ref: decisions/DEC-PUB-006-brief-emits-conformant-run-evidence-cross-checks.md
  - kind: decision
    ref: decisions/DEC-CDCP-008-ci-failure-blocks-merge-to-main.md
  - kind: doc
    ref: .github/workflows/run-evidence-gates.yml
  - kind: doc
    ref: .github/workflows/ci.yml
  - kind: code
    ref: scripts/replay_run.py
  - kind: code
    ref: scripts/validate_run_evidence.py
  - kind: artifact
    ref: ops/run-records/run-36e307499472.json
  - kind: artifact
    ref: ops/run-records/run-d74d787e6756.json
  - kind: artifact
    ref: ops/run-records/run-1f1fc1f3d36d.json
  - kind: spec
    ref: specs/0007-publishing/requirements.md
rollback: |
  Delete `.github/workflows/run-evidence-gates.yml`, drop the
  `R-PUB-022..R-PUB-025` rows from `specs/0007-publishing/`, drop
  the new DEC-PUB-009 entries from
  `decisions/.spec-check-allowlist.yaml`, and delete this DEC. The
  existing `ci.yml` continues to enforce the universal gates; the
  only loss is the product-repo-specific chain (packet generation,
  packet validation, replay smoke) running on every PR. The
  trace-to-eval-harness sibling checkout pattern lives only in the
  new workflow file, so rolling back removes that dependency too.
  No data migration is needed because workflow files are stateless.
owner: science.proof-gate-runner
---

## decision

ai-field-brief's CI workflows enforce the run-evidence gate chain
locked by DEC-CDCP-015 (athena-site) on every pull request and every
push to main. The existing `.github/workflows/ci.yml` keeps the
universal gates (schema-cache freshness, voice lint, no-BOM,
spec-check, decisions validation, validate_run_evidence, pnpm
lint/typecheck/test/build); a new
`.github/workflows/run-evidence-gates.yml` adds the product-repo-
specific gates from the contract:
packet-generation-from-canonical-sample, packet-validation, and
replay-smoke. Every gate runs as a matrix over the three canonical
samples (`run-36e307499472`, `run-d74d787e6756`,
`run-1f1fc1f3d36d`) so the chain is exercised end-to-end per Run.
No `continue-on-error: true` and no `if: ${{ failure() }}` on any
contract gate. No `--no-verify` bypass anywhere.

The replay-smoke step closes the two-pass tail from DEC-PUB-008
without modifying the canonical sample: after `git checkout
<sandbox-sha>` the gate restores `ops/run-records/` and
`ops/event-ledger/` from main so the on-disk `sandbox_image_ref`
carries the finalized SHA (matching the just-checked-out HEAD)
instead of the historical `@PENDING/` placeholder. This proves three
things in one step: the recorded SHA is reachable in git history, the
canonicalization at that SHA reproduces the recorded snapshot hashes,
and every output named in the Run still exists at its recorded path.

The trace-to-eval-harness sibling repo is checked out at
`${{ github.workspace }}/trace-to-eval-harness` and pip-installed
into the runner so `python -m trace_to_eval evidence
from-cdcp-events` and `python -m trace_to_eval evidence validate`
are callable. `--portfolio-root ${{ github.workspace }}` lets
trace-to-eval-harness resolve `repo://ai-field-brief@<sha>/<path>`
URIs into the checked-out tree.

## alternatives

- Extend `ci.yml` with the new jobs instead of adding a second
  workflow file. Rejected because the two surfaces have different
  needs: ci.yml stays single-checkout, run-evidence-gates.yml needs a
  sibling checkout AND a matrix AND a per-step
  `git checkout <sandbox-sha>` that would destabilize ci.yml's other
  jobs if they shared the same checkout. Splitting keeps each file
  focused; both block merges to main per DEC-CDCP-008.
- Skip the replay-smoke gate and rely on the committed
  `ops/replay-records/` verdicts. Rejected because the committed
  records prove the chain worked once; the CI gate proves the chain
  still works on every PR. A regression in the canonicalization
  helper would slip past a snapshot-only proof and surface only at
  the next regeneration.
- Run the chain only against the W22 sample to halve CI time.
  Rejected because the three samples exercise distinct code paths
  through the emitter and replay; a single-sample gate would let a
  regression in the unexercised path ride into main. Matrix
  parallelism means the wall-clock cost is one job's worth of time.
- Drop `git checkout <sandbox-sha>` and run replay from the PR HEAD
  as a soft check. Rejected because replay HEAD-strict is the
  load-bearing semantic from DEC-PUB-007. Running from a non-matching
  HEAD short-circuits before hash recomputation, so the gate would
  pass on a mutation that breaks the canonicalization helper. The
  records-restore-from-main step is the surgical fix for the
  two-pass tail without losing HEAD-strict semantics.

## rationale

DEC-CDCP-015 names the difference between "we have artifacts" and
"main cannot accept unverifiable work." This DEC is ai-field-brief's
local landing of that contract. The universal gates were already
wired by DEC-CDCP-008 and DEC-PUB-006; the new piece is the
product-repo-specific chain (packet generation, packet validation,
replay smoke) running per canonical sample on every PR.

The matrix shape is deliberate. Each sample exercises a distinct
code path through `run_evidence.py` and `replay_run.py`, and the
trace-to-eval-harness packet generator dereferences `repo://` URIs
differently for backfilled versus regenerated records. A
single-sample gate would let a regression in the unexercised path
ride into main; the three-sample matrix closes that gap.

The replay-smoke step's records-restore-from-main pattern is the
honest engineering answer to the two-pass tail from DEC-PUB-008. At
the recorded sandbox SHA the Run record itself carries `@PENDING/`
because the SHA was not knowable at emit time; the records-on-main
carry the finalized SHA. The gate checks out the recorded SHA
(proving reachability and giving replay the right tree to hash
against), restores the records and ledger from main (so the on-disk
sandbox_image_ref matches HEAD), then runs replay. Replay equivalent
at this configuration proves the recorded SHA is reachable, the
canonicalization at that SHA reproduces the recorded snapshot hashes,
and every output exists at its recorded path.

The pnpm audit step in `ci.yml` keeps its `|| true` suffix because it
is a security advisory surface, not a DEC-CDCP-015 contract gate; the
universal gates list in the contract does not include dependency
advisories. That stays scoped under
`.github/workflows/ci.yml::security` and is governed by a future
security DEC, not this one.

## rollback

Delete `.github/workflows/run-evidence-gates.yml`, drop the
`R-PUB-022..R-PUB-025` rows from `specs/0007-publishing/`, drop the
new DEC-PUB-009 entries from `decisions/.spec-check-allowlist.yaml`,
and delete this DEC. The existing `ci.yml` continues to enforce the
universal gates; the only loss is the product-repo-specific chain
running on every PR. No data migration is needed because workflow
files are stateless.

## coverage

This DEC resolves the following requirements added to
`specs/0007-publishing/requirements.md`:

- `R-PUB-022` ai-field-brief ships a CI workflow
  (`.github/workflows/run-evidence-gates.yml`) that triggers on every
  pull request and every push to main, runs on ubuntu-latest, and sets
  up Python 3.11 plus Node 20.
- `R-PUB-023` the workflow gates packet generation from each canonical
  sample's event ledger via `python -m trace_to_eval evidence
  from-cdcp-events`, and gates packet validation via
  `python -m trace_to_eval evidence validate`. Both run as a matrix
  over `run-36e307499472`, `run-d74d787e6756`, and `run-1f1fc1f3d36d`.
- `R-PUB-024` the replay-smoke gate extracts the recorded sandbox SHA
  from each Run record, verifies the SHA is reachable in git history,
  checks out the recorded SHA, restores the finalized Run records and
  event ledger from main (closing the two-pass tail from DEC-PUB-008
  without modifying the canonical sample), and runs
  `scripts/replay_run.py --run-id <sample>` expecting exit 0
  (replay_equivalent: true).
- `R-PUB-025` no contract gate carries `continue-on-error: true` or
  `if: ${{ failure() }}` framing; every step is blocking per the
  enforcement clause of DEC-CDCP-008 and DEC-CDCP-015.
