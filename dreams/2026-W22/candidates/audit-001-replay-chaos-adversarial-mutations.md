---
id: audit-001-replay-chaos-adversarial-mutations
target_kind: test_generation
spec_id: specs/0007-publishing
test_path: tests/scripts/test_replay_run_chaos.py
human_review_required: true
status: candidate
evidence:
  - kind: code
    ref: scripts/replay_run.py - the canonicalization + hash recomputation path that the chaos test mutates around
  - kind: code
    ref: scripts/run_evidence.py - the `canonicalize_payload_for_hash` helper whose determinism the chaos test probes
  - kind: artifact
    ref: ops/run-records/run-36e307499472.json - canonical W20 sample for adversarial input fuzzing
  - kind: artifact
    ref: ops/run-records/run-d74d787e6756.json - canonical W21 sample
  - kind: artifact
    ref: ops/run-records/run-1f1fc1f3d36d.json - canonical W22 sample (regenerated under the two-pass protocol)
  - kind: decision
    ref: decisions/DEC-PUB-009-ai-field-brief-ci-enforces-run-evidence-chain.md - the gate the chaos test hardens
  - kind: doc
    ref: ".github/workflows/run-evidence-gates.yml - the replay-smoke step the chaos test extends"
---

## proposal

Add a chaos-test suite at `tests/scripts/test_replay_run_chaos.py` that programmatically mutates each of the three canonical Run records and asserts `replay_run.py` reports `replay_equivalent: false` cleanly (no crash, no false positive) for each mutation class. Mutation classes to cover:

1. Reorder keys inside a nested object (canonicalizer must still detect equivalence; expect `true`).
2. Flip a single byte inside a recorded snapshot hash (expect `false`, no crash).
3. Replace a `repo://` URI host segment with an unknown repo name (expect `false` with a clear "unresolved URI" reason).
4. Truncate the `event-ledger` JSONL by one line (expect `false` with a "ledger length mismatch" reason).
5. Inject a duplicate `event_id` into the ledger (expect `false` with a duplicate-id reason).
6. Swap the recorded `sandbox_image_ref` SHA for an unreachable SHA (expect `false` with a reachability reason).
7. Add a trailing newline to a recorded output file path (expect `true` if canonicalization handles trailing whitespace; expect `false` with a clear reason if not - either answer is allowed, but the test pins the current behavior).

Each mutation runs against a temporary copy of the canonical sample; the canonical files on disk stay untouched. The test is added to `ci.yml` as a non-matrix step (the chaos surface is independent of the canonical sample identity).

## why it earns its keep

The replay equivalence gate (DEC-PUB-009) is the load-bearing proof that `main` cannot accept unverifiable work. The gate today exercises the happy path: three canonical samples, each producing `replay_equivalent: true` against an unmodified working tree. The gate has never been exercised against a mutated input. A regression in `canonicalize_payload_for_hash` that produces the same hash for different inputs (a collision-class bug) or that crashes on malformed input (a robustness-class bug) would slip past the current matrix.

The chaos test pins the gate's adversarial surface. It also closes the gap named in the W22 report under "fragile edges": `canonicalize_payload_for_hash` non-determinism risk. The current sample N is three; a chaos test with seven mutation classes against three samples yields 21 explicit cases, which is a credible adversarial coverage floor.

## cost

Small. The test file is ~150-200 lines (one helper to mutate a Run record, one parametrized test per mutation class). No new dependencies; the chaos test uses the existing `replay_run.py` CLI plus pytest's `tmp_path` fixture. The CI step adds ~10 seconds to the wall clock.

## risk

- A chaos test that pins current behavior locks the canonicalizer's tolerance to today's choices. If mutation class 7 (trailing newline) is currently treated as "still equivalent" and the test pins that, a future tightening of the canonicalizer breaks the test instead of producing a clean assertion failure. Mitigation: the test's `expected` value lives in a `CHAOS_EXPECTATIONS` table at the top of the file with a comment explaining the choice; future tightening updates the table in the same commit.
- Adversarial coverage is a moving target. Seven mutation classes is the v1 surface; v2 should add binary-file mutations (a recorded snapshot that is not a JSON file), encoding mutations (UTF-8 to UTF-16), and structural mutations (missing required fields). The test is intentionally scoped to the JSON-content surface for v1.
- The chaos test runs against canonical samples on disk; an accidental write back to the canonical file would corrupt the sample. Mitigation: the test reads the canonical file once at module load, copies into `tmp_path`, and never writes back. A pre-test check asserts the canonical file's mtime is unchanged after the test runs.

## timeline

Next sprint. The chaos surface is small enough that one engineer can land it in 1-2 days. The test ships behind a small DEC (call it DEC-PUB-010 or DEC-SCI-001) that names the chaos surface as a contract, so a future contributor knows to add a new mutation class when they extend the canonicalizer.

## promotion path

If approved, the change touches three files:

- `tests/scripts/test_replay_run_chaos.py` - new file with the parametrized chaos suite.
- `.github/workflows/ci.yml` - add a `chaos-tests` step after `validate_run_evidence` and before the pnpm gates.
- `decisions/DEC-PUB-010-replay-chaos-test-surface.md` - new DEC naming the chaos surface as a contract and listing the seven v1 mutation classes.

Reviewer checks:

1. Each mutation class produces the expected verdict on the current `main` (green baseline).
2. A locally-introduced regression in `canonicalize_payload_for_hash` (e.g., remove the key-sort step) flips one or more mutations from the expected verdict (red on regression).
3. The chaos suite finishes in under 30 seconds wall-clock on the CI runner.
4. No canonical sample file under `ops/run-records/`, `ops/event-ledger/`, or `ops/replay-records/` has its mtime changed by the test run.

Owner role: `science.proof-gate-runner` (the gate is the role's surface per DEC-PUB-009).
