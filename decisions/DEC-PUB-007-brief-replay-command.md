---
id: DEC-PUB-007-brief-replay-command
spec: specs/0007-publishing/
requirement: R-PUB-014
date: 2026-05-28
status: approved
reversible: true
amends: DEC-PUB-006-brief-emits-conformant-run-evidence-cross-checks
decision: |
  ai-field-brief ships `scripts/replay_run.py` performing equivalence
  replay against any backfilled or live brief Run record. The CLI is
  HEAD-strict: it reads `sandbox_image_ref` off the Run record, compares
  the recorded SHA to `git rev-parse HEAD`, and exits 1 with a
  `git checkout <sha>` instruction on any mismatch. At a matching HEAD
  the CLI re-computes `prompt_snapshot_hash` against the current
  playbook + extraction prompts + synthesis prompts using the same
  canonicalization the emitter uses, re-computes
  `tool_schemas_snapshot_hash` against the current source registry +
  extraction schema + active LLM identifier, and verifies that every
  output named in `Run.outputs[]` exists at its recorded path (hashing
  the current file and comparing only when the output carries a
  recorded hash). The verdict is `replay_equivalent: true` when every
  check matches; any divergence flips it false and is named in the
  replay report. The CLI appends one `run.evidence.replayed` event
  (`replay_method: equivalence`) to a new per-replay ledger at
  `ops/event-ledger/replay-<run-id>-<ISO>.jsonl` and writes the full
  replay report to `ops/replay-records/<run-id>/<replay-event-id>.json`.
  No live LLM re-execution is attempted.

  The amendment to DEC-PUB-006 is the `sandbox_image_ref` semantic for
  backfilled briefs: the field records the SHA at which the recorded
  prompt and tool-schema snapshot hashes are reproducible (the
  records-regeneration commit), not the brief-publishing commit. The
  publishing commit stays recoverable via
  `git log --diff-filter=A -- briefs/YYYY-WNN/brief.md`; the SHA the
  replay verifies against is the one the Run record names.
alternatives:
  - label: re-call the LLM and byte-compare the brief output
    rejected_because: |
      Brief generation is an LLM-agent playbook pass: a human or
      coding agent reads `playbook/run-weekly-brief.md`, sweeps the
      sources, and writes the brief through an LLM with no pinned
      sampler knobs. Wall-clock time and model state are not pinned;
      byte-identical replay is not reachable. Calling it "replay" when
      a fresh LLM call would not produce the same brief would
      overclaim. The honest framing is equivalence: the recorded
      preconditions still hold and the artifact still exists with the
      same content. `replay_method: equivalence` records the boundary
      so a future reader does not conflate it with deterministic
      replay.
  - label: leave `sandbox_image_ref` pointing at the publishing commit
      and accept that strict HEAD verification fails
    rejected_because: |
      DEC-PUB-005 named the publishing commit as the backfill SHA on
      the theory that the brief artifact and the gate context were
      what `sandbox_image_ref` should anchor. Round 5 surfaced the
      cost: `prompt_snapshot_hash` and `tool_schemas_snapshot_hash`
      are computed by the backfill against the current playbook +
      registry, which is the records-regeneration tree, not the
      publishing-commit tree. The two pieces of the same Run record
      then point at different SHAs and the strict HEAD check is
      unsatisfiable. Updating the semantic so `sandbox_image_ref`
      records the SHA at which the hashes are reproducible makes
      replay coherent; the publishing commit is still recoverable
      through git log and is the right answer to "when did this
      brief land", which is a separate question.
  - label: defer replay to the consumer (trace-to-eval-harness)
    rejected_because: |
      The consumer reads Run records and ledgers to produce review
      packets. A consumer-side replay would need to re-read the
      ai-field-brief repo state, re-derive the canonical hashes
      against the same playbook + registry the emitter saw, and reach
      a verdict against a SHA the consumer does not own. Keeping the
      replay command in ai-field-brief means the emitter and the
      replay share one canonicalization helper
      (`scripts/run_evidence.py`) and one definition of "equivalent".
      The portfolio pattern in Round 5 is one replay command per
      repo, owned by the repo that produced the artifact.
rationale: |
  Round 1 of the v2 run-evidence engineering upgrade introduced typed
  event payloads and emitter cross-checks. Round 5 closes the loop
  with a replay command per repo: the engineering claim is that a
  Run record + its event ledger can be verified at any later point,
  not just at write time. For a deterministic pipeline that claim is
  byte-replay; for an LLM-agent pipeline like ai-field-brief it is
  equivalence — the recorded preconditions still hold and the
  artifacts still exist with the same content.

  The CLI surface mirrors the per-repo replay pattern: a single
  `--run-id` argument, strict HEAD verification, a typed
  `run.evidence.replayed` event written to a new per-replay ledger
  file (so the source-of-truth ledger stays immutable), and a full
  replay report at `ops/replay-records/<run-id>/<replay-event-id>.json`
  carrying the per-check verdicts. The CLI exits 0 on equivalent and
  1 on any divergence so a CI step can wire it into a future
  replay-gate without further plumbing.

  The amendment to `sandbox_image_ref` semantics is small but
  load-bearing: it makes the strict HEAD verification reachable on
  every backfilled Run, which is the precondition for the rest of
  the equivalence checks to execute. Without the amendment the
  publishing-commit SHA and the regeneration-tree hashes name
  different repo states and the CLI exits 1 before reaching the
  hash comparison. The brief-publishing commit stays recoverable
  via `git log --diff-filter=A` so the "when did this brief land"
  question still has a precise answer.

  What this replay does NOT do is documented in the script's module
  docstring and re-stated in the DEC body: it does not re-call the
  LLM. A future contributor reading the artifact should not conflate
  equivalence replay with deterministic replay. The
  `replay_method: equivalence` field on every emitted event is the
  schema-level anchor for that distinction.
evidence:
  - kind: decision
    ref: decisions/DEC-PUB-006-brief-emits-conformant-run-evidence-cross-checks.md
  - kind: decision
    ref: decisions/DEC-PUB-005-brief-emits-conformant-run-evidence.md
  - kind: code
    ref: scripts/replay_run.py
  - kind: code
    ref: scripts/run_evidence.py
  - kind: code
    ref: tests/scripts/test_replay_run.py
  - kind: artifact
    ref: ops/replay-records/run-874c5e341e13/
  - kind: artifact
    ref: ops/replay-records/run-d223cf166b70/
  - kind: artifact
    ref: ops/replay-records/run-7131f5246462/
  - kind: spec
    ref: specs/0007-publishing/requirements.md
rollback: |
  Delete `scripts/replay_run.py`, delete
  `tests/scripts/test_replay_run.py`, delete the
  `ops/replay-records/` directory and the
  `ops/event-ledger/replay-*.jsonl` files, restore the prior
  `sandbox_image_ref` semantic by either re-running
  `scripts/backfill_run_records.py --all` (which writes the
  publishing commit SHA) or hand-editing the three sample Run
  records back to their publishing-commit anchors, drop the
  `R-PUB-014..R-PUB-017` rows from `specs/0007-publishing/`, and
  delete this DEC. No data migration is needed because run records
  and ledgers are append-only audit trails with no fan-out.
owner: science.proof-gate-runner
---

## decision

ai-field-brief ships `scripts/replay_run.py` performing equivalence
replay against any backfilled or live brief Run record. The CLI is
HEAD-strict: it reads `sandbox_image_ref` off the Run record, compares
the recorded SHA to `git rev-parse HEAD`, and exits 1 with a
`git checkout <sha>` instruction on any mismatch. At a matching HEAD
the CLI re-computes `prompt_snapshot_hash` against the current
playbook + extraction prompts + synthesis prompts using the same
canonicalization the emitter uses, re-computes
`tool_schemas_snapshot_hash` against the current source registry +
extraction schema + active LLM identifier, and verifies that every
output named in `Run.outputs[]` exists at its recorded path (hashing
the current file and comparing only when the output carries a
recorded hash). The verdict is `replay_equivalent: true` when every
check matches; any divergence flips it false and is named in the
replay report. The CLI appends one `run.evidence.replayed` event
(`replay_method: equivalence`) to a new per-replay ledger at
`ops/event-ledger/replay-<run-id>-<ISO>.jsonl` and writes the full
replay report to `ops/replay-records/<run-id>/<replay-event-id>.json`.
No live LLM re-execution is attempted.

The amendment to DEC-PUB-006 is the `sandbox_image_ref` semantic for
backfilled briefs: the field records the SHA at which the recorded
prompt and tool-schema snapshot hashes are reproducible (the
records-regeneration commit), not the brief-publishing commit. The
publishing commit stays recoverable via
`git log --diff-filter=A -- briefs/YYYY-WNN/brief.md`; the SHA the
replay verifies against is the one the Run record names.

## alternatives

- Re-call the LLM and byte-compare the brief output. Rejected because
  brief generation runs through an LLM with no pinned sampler knobs;
  byte-identical replay is not reachable for an LLM-agent pipeline.
  The honest framing is equivalence, and `replay_method: equivalence`
  records the boundary on every emitted event.
- Leave `sandbox_image_ref` at the publishing commit and accept that
  strict HEAD verification fails. Rejected because the recorded
  hashes were computed against the records-regeneration tree, not the
  publishing-commit tree; the two pieces of the same Run record then
  name different repo states and the HEAD check is unsatisfiable. The
  amendment makes replay coherent without losing the publishing-commit
  information (it stays recoverable via git log).
- Defer replay to the consumer. Rejected because the per-repo replay
  pattern keeps one canonicalization helper and one definition of
  equivalence in the repo that emitted the artifact.

## rationale

Round 1 of the v2 run-evidence engineering upgrade introduced typed
event payloads and emitter cross-checks. Round 5 closes the loop with
a replay command per repo: the engineering claim is that a Run record
plus its event ledger can be verified at any later point, not just at
write time. For a deterministic pipeline that claim is byte-replay;
for an LLM-agent pipeline like ai-field-brief it is equivalence — the
recorded preconditions still hold and the artifacts still exist with
the same content.

The CLI surface mirrors the per-repo replay pattern: a single
`--run-id` argument, strict HEAD verification, a typed
`run.evidence.replayed` event written to a new per-replay ledger file
(so the source-of-truth ledger stays immutable), and a full replay
report carrying the per-check verdicts. The CLI exits 0 on equivalent
and 1 on any divergence so a CI step can wire it in later.

The amendment to `sandbox_image_ref` semantics is small but
load-bearing: it makes strict HEAD verification reachable on every
backfilled Run, which is the precondition for the rest of the
equivalence checks to execute. Without the amendment the
publishing-commit SHA and the regeneration-tree hashes name different
repo states and the CLI exits 1 before reaching the hash comparison.
The brief-publishing commit stays recoverable via
`git log --diff-filter=A` so the "when did this brief land" question
still has a precise answer.

What this replay does NOT do is documented in the script's module
docstring and re-stated here: it does not re-call the LLM. A future
contributor reading the artifact should not conflate equivalence
replay with deterministic replay. The `replay_method: equivalence`
field on every emitted event is the schema-level anchor for that
distinction.

## evidence

- `decisions/DEC-PUB-006-brief-emits-conformant-run-evidence-cross-checks.md`
  is the DEC this one amends.
- `decisions/DEC-PUB-005-brief-emits-conformant-run-evidence.md`
  established the emitter shape replay reads.
- `scripts/replay_run.py` carries the CLI.
- `scripts/run_evidence.py` carries the canonicalization helpers
  replay shares with the emitter.
- `tests/scripts/test_replay_run.py` carries the positive cases for
  W20/W21/W22 plus the four negative cases (HEAD mismatch, missing
  Run record, missing artifact, prompt-hash mismatch on a mutated
  playbook copy).
- `ops/replay-records/run-874c5e341e13/`,
  `ops/replay-records/run-d223cf166b70/`, and
  `ops/replay-records/run-7131f5246462/` carry the equivalent verdict
  for each of the three sample Runs.
- `specs/0007-publishing/requirements.md` carries
  `R-PUB-014..R-PUB-017`.

## rollback

Delete `scripts/replay_run.py`, delete
`tests/scripts/test_replay_run.py`, delete the
`ops/replay-records/` directory and the
`ops/event-ledger/replay-*.jsonl` files, restore the prior
`sandbox_image_ref` semantic by either re-running
`scripts/backfill_run_records.py --all` (which writes the publishing
commit SHA) or hand-editing the three sample Run records back to
their publishing-commit anchors, drop the `R-PUB-014..R-PUB-017` rows
from `specs/0007-publishing/`, and delete this DEC.

## coverage

This DEC resolves the following requirements added to
`specs/0007-publishing/requirements.md`:

- `R-PUB-014` ai-field-brief ships an equivalence replay command per
  Run record (HEAD-strict, no live LLM re-execution).
- `R-PUB-015` replay re-computes both snapshot hashes against the
  current tree and compares to the recorded values.
- `R-PUB-016` replay verifies every Run output exists at the recorded
  path and hashes it when an artifact hash is recorded on the output.
- `R-PUB-017` replay appends a typed `run.evidence.replayed` event
  with `replay_method: equivalence` to a new per-replay ledger file
  and writes the full verdict to `ops/replay-records/`.
