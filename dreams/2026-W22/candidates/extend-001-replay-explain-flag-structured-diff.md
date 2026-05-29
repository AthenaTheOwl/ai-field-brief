---
id: extend-001-replay-explain-flag-structured-diff
target_kind: backlog_item
title: Add --explain to replay_run.py that emits a structured diff when replay_equivalent is false
human_review_required: true
status: candidate
evidence:
  - kind: code
    ref: scripts/replay_run.py - the CLI that today returns the verdict as a boolean plus a brief reason string
  - kind: artifact
    ref: "ops/replay-records/run-36e307499472/verdict.json - the verdict shape that today carries replay_equivalent true plus a reason field"
  - kind: artifact
    ref: ops/replay-records/run-d74d787e6756/verdict.json - same verdict shape
  - kind: artifact
    ref: ops/replay-records/run-1f1fc1f3d36d/verdict.json - same verdict shape
  - kind: decision
    ref: decisions/DEC-PUB-007-brief-replay-command.md - defines the verdict shape
  - kind: doc
    ref: ".github/workflows/run-evidence-gates.yml replay-smoke step - the CI consumer that today reads only `replay_equivalent`"
---

## proposal

Add a `--explain` flag to `scripts/replay_run.py` that, when `replay_equivalent: false`, writes a structured diff to `ops/replay-records/<run-id>/diff.json` alongside the existing `verdict.json`. The diff carries the per-field comparison:

```json
{
  "run_id": "run-<id>",
  "explain_version": "v1",
  "comparison_axes": [
    {
      "axis": "snapshot_hashes",
      "expected": {"<output_path>": "sha256-<a>"},
      "actual": {"<output_path>": "sha256-<b>"},
      "delta": [
        {"output_path": "<path>", "expected_hash": "sha256-<a>", "actual_hash": "sha256-<b>"}
      ]
    },
    {"axis": "output_paths_present", "missing": [...], "extra": [...]},
    {"axis": "event_ledger_length", "expected": N, "actual": M},
    {"axis": "event_ledger_id_set", "expected": [...], "actual": [...], "missing_ids": [...], "extra_ids": [...]}
  ],
  "first_failure_axis": "<axis>",
  "human_summary": "<one sentence>"
}
```

The CI replay-smoke step in `run-evidence-gates.yml` learns to upload `diff.json` as a workflow artifact when the gate fails, so the failed-PR reviewer reads the diff in the GitHub UI without re-running replay locally.

Make `--explain` default-off for the CLI to keep the existing UX unchanged; the CI gate passes `--explain` explicitly.

## why it earns its keep

The W22 report names "`replay_equivalent: false` is a boolean" as the third documented-but-unenforced edge. Today when the gate fails the next agent has to:

1. Read the verdict file and learn that replay failed.
2. Locally check out the sandbox SHA.
3. Locally restore the records from main.
4. Re-run `replay_run.py` with verbose output.
5. Diff the recomputed canonical hashes against the recorded ones by hand.

`--explain` collapses steps 2-5 into "open the diff.json artifact." The cost is one extra file per failed replay; the saving is roughly 15-30 minutes per debugging session. The gate's signal-to-noise improves from "something broke" to "the W21 sample's brief.md hash changed; everything else still matches."

The structured shape also gives the future portfolio replay panel in athena-site a per-axis surface to render. The current verdict shape gives the panel only a green or red light.

## cost

Small to medium. The diff computation runs over data the canonicalization helper already has; no new dependencies. The touched surface:

- `scripts/replay_run.py` - add `--explain` parsing; when verdict is false and the flag is set, walk the four comparison axes and emit `diff.json`. Roughly 100-150 lines.
- `.github/workflows/run-evidence-gates.yml` - add `--explain` to the replay-smoke command; add an artifact-upload step that picks up `diff.json` on gate failure.
- One small DEC (DEC-PUB-011 or similar) naming the `diff.json` shape as a v1 contract.
- Test: extend `audit-001`'s chaos suite (if landed) to assert each mutation class produces a non-empty `delta` array in the appropriate axis.

About one day of focused work, half a day if the chaos suite already exists.

## risk

- The diff shape becomes a contract. A future axis (e.g., a fifth comparison axis for cid resolution if `reduce-001` lands) needs to extend the schema without breaking the v1 consumers. Mitigation: the `explain_version` field plus the array-of-axes shape keep additions backwards-compatible.
- The diff exposes recorded snapshot hashes in the failed-PR artifact UI. The current Run records cover public briefs, so hash exposure carries no privacy cost today. Confirm no future Run record carries a hash for a non-public output before promoting this beyond v1.
- The CI artifact-upload step adds a small wall-clock cost per failed run, but only on failure. Zero cost on the happy path. Mitigation: scope the upload to the replay-smoke step's failure path only.

## timeline

Next sprint. This is small enough to ship in the same sprint as `audit-001` if the chaos suite lands first; the chaos suite gives the diff shape its first non-trivial consumer.

## promotion path

If approved, the change touches:

- `scripts/replay_run.py` - add `--explain` and the diff emitter.
- `.github/workflows/run-evidence-gates.yml` - pass `--explain` + upload diff.json artifact on failure.
- `decisions/DEC-PUB-011-replay-explain-structured-diff.md` - new DEC naming the diff shape.
- `specs/0007-publishing/requirements.md` - add `R-PUB-026` (replay CLI emits a structured diff when verdict is false and `--explain` is set).

Reviewer checks:

1. `python scripts/replay_run.py --run-id <sample> --explain` on a clean working tree produces no diff.json (verdict is true; nothing to explain).
2. A locally-introduced mutation (one of `audit-001`'s chaos cases) produces a diff.json with a non-empty `delta` array in the matching axis.
3. The CI workflow uploads diff.json as a named artifact only on replay-smoke failure.
4. The diff shape passes a small JSON Schema check (the schema lives at `ops/schemas-cache/replay-diff.schema.json`).

Owner role on promotion: `engineering.implementation`.

## risks if promoted blindly

- The diff shape lands without a schema. A future axis added by a different agent breaks the v1 consumers silently. Mitigation: ship the JSON Schema in the same PR as the diff emitter.
- The `--explain` flag becomes the default in a future change. The CLI's current UX is "verdict in stdout, structured record in verdict.json"; a default-on `--explain` doubles the on-disk output of every replay. Promote intentionally; keep `--explain` opt-in.
