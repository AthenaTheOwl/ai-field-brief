---
id: reduce-001-content-addressable-sandbox-ref
target_kind: backlog_item
title: Retire the two-pass sandbox-SHA finalize protocol via content-addressable indirection
human_review_required: true
status: candidate
evidence:
  - kind: decision
    ref: decisions/DEC-PUB-008-brief-portable-repo-uri-migration.md - documents the two-pass tail as unavoidable under the current shape
  - kind: decision
    ref: decisions/DEC-PUB-009-ai-field-brief-ci-enforces-run-evidence-chain.md - documents the records-restore-from-main workaround
  - kind: code
    ref: scripts/finalize_sandbox_ref.py - the CLI that runs the second pass + the `--force` flag added in commit 2836c5f
  - kind: code
    ref: scripts/run_evidence.py - emits `@PENDING/` placeholders that the second pass replaces
  - kind: commit
    ref: e4fa4d5 chore(run-evidence)- finalize sandbox SHA + commit replay artifacts (the records-of-the-records dance)
  - kind: artifact
    ref: ".github/workflows/run-evidence-gates.yml lines 60-110 - the records-restore-from-main step that closes the two-pass tail in CI"
---

## proposal

Replace the `sandbox_image_ref: repo://ai-field-brief@<sha>/` field in Run records with a `sandbox_image_ref: cid:<content-hash>` indirection plus a separate `sandbox_image_refs.jsonl` ledger that maps each `cid:` to its eventual `<sha>` once the records-containing commit lands. The Run record itself never carries the SHA; the ledger does, and the ledger gets appended (not rewritten) after the records-containing commit ships.

Concrete shape:

- `run_evidence.py emit_pipeline_complete()` writes `sandbox_image_ref: cid:sha256-<canonicalized-content-hash>` into each new Run record. No `@PENDING/` placeholder; no second pass against the Run record file.
- A new `ops/sandbox-image-refs.jsonl` carries one line per content hash: `{"cid": "sha256-<hash>", "git_sha": "<sha>", "first_seen_at": "<iso>", "first_run_id": "<id>"}`. The ledger is append-only.
- `replay_run.py` resolves `cid:<hash>` to a `git_sha` via the ledger and proceeds with the existing HEAD-strict semantic.
- `finalize_sandbox_ref.py` becomes `register_sandbox_image_ref.py`: appends one line to the ledger after the records-containing commit ships. The Run record is never modified after emission.

## why it earns its keep

The two-pass tail is the most fragile surface in the v2 rollout. DEC-PUB-008 and DEC-PUB-009 spend roughly 80 lines together documenting why the two-pass protocol is the honest engineering answer to the "records-containing SHA inside the records" recursion, and why the records-restore-from-main step in `run-evidence-gates.yml` is the workaround. Every downstream consumer (the replay gate, the trace-to-eval-harness packet generator, the in-progress portfolio replay panel) has to know about the workaround or get the wrong answer.

Content-addressable indirection collapses the recursion. The Run record carries a `cid:` that depends only on the canonicalized record content; the SHA mapping lives in a separate, append-only ledger that gets written after the commit. No record file ever needs `--force` re-anchoring. The CI gate's records-restore-from-main step disappears. New repos that adopt the run-evidence contract get a one-pass protocol from day one.

This also closes the third "documented but unenforced" surface from the W22 report: the `@PENDING/` semantic. With content-addressable refs there is no PENDING state to test for.

## cost

Medium. The touched surface:

- `scripts/run_evidence.py` - change `sandbox_image_ref` shape; recompute the cid; emit ledger lines.
- `scripts/replay_run.py` - add cid->sha resolution before the existing git checkout step.
- `scripts/finalize_sandbox_ref.py` - rewrite as `register_sandbox_image_ref.py`.
- `scripts/validate_run_evidence.py` - cross-check that every cid in the Run record resolves to a ledger entry (or is the run-of-emission, in which case the ledger entry lands in the same PR).
- `.github/workflows/run-evidence-gates.yml` - delete the records-restore-from-main step; the matrix gate becomes one-pass.
- Migration: every existing Run record (`run-36e307499472`, `run-d74d787e6756`, `run-1f1fc1f3d36d`) gets a one-time rewrite to the new shape, plus three corresponding ledger entries.
- DECs: one new DEC (DEC-PUB-011 or similar) plus an `amends` field on DEC-PUB-008 and DEC-PUB-009 to record the retirement.

Roughly 400-600 lines of changes across the touched scripts, plus a migration commit. Two days of focused work.

## risk

- The cid:sha mapping ledger is now a new load-bearing artifact. If the ledger gets out of sync with the Run records (a Run record points at a cid the ledger does not know about), replay fails with a "unknown cid" error and the agent has to debug a new failure mode. Mitigation: validate_run_evidence cross-checks every Run record's cid resolves to a ledger entry; the gate fails the PR if not.
- The content hash that drives the cid depends on `canonicalize_payload_for_hash`. A canonicalizer change that produces different cids for the same logical content would invalidate the ledger. Mitigation: the canonicalizer is versioned; the cid carries the version (`cid:v1-sha256-<hash>`) so a v2 canonicalizer produces v2 cids without colliding with v1.
- The migration commit touches three load-bearing canonical samples. A migration bug would break the W22 replay chain in a way that needs careful recovery. Mitigation: ship the migration in a dedicated PR that runs the chaos suite from `audit-001` (if landed first) against the new shape before merging.
- One-pass content-addressable refs are a more elegant protocol, and elegance is not enforcement. trace-to-eval-harness still has to learn the new resolver shape. The cross-repo coordination cost is real.

## timeline

Next month, after `audit-001` lands. The chaos suite gives the migration a safety net; without it the migration is a flying-blind change to the most load-bearing canonicalization surface. Ordering: chaos suite first (week 1), migration design + DEC + sibling-repo coordination (week 2), migration implementation + canonical sample rewrite (week 3), CI workflow simplification (week 4).

If trace-to-eval-harness cannot adopt the new resolver shape in the same window, the migration ships as additive: Run records carry both `sandbox_image_ref` (legacy) and `sandbox_image_cid` (new) for one cycle, then the legacy field gets retired in a follow-up DEC.

## promotion path

This is a backlog_item, not a memory_update or test_generation, because the proposal spans multiple files, a migration, a new DEC, and cross-repo coordination. The promotion path is to open a tracked work item under `specs/0007-publishing/` with the proposal text as the spec body and the named DEC as the closing artifact.

Owner role on promotion: `engineering.implementation` (the migration is implementation work) with `science.proof-gate-runner` reviewing the gate-shape changes.

Reviewer checks at promotion time:

1. The chaos suite from `audit-001` is green against the new shape.
2. trace-to-eval-harness has a sibling PR ready to land the new resolver shape (or the additive-migration plan is documented).
3. The DEC names the v1 cid format (`cid:v1-sha256-<hash>`) as the contract.
4. The migration PR includes the three canonical-sample rewrites in one commit so the working tree never has a mixed-shape state.

## risks if promoted blindly

- Premature promotion without `audit-001` is the wrong order. A change to the canonicalization-adjacent code without a chaos surface is a hash-collision waiting to ship.
- Coordinating cross-repo simultaneous landings is hard. The additive-migration plan is the safety valve; the promotion path needs to confirm it exists in writing before the migration ships.
- The two-pass protocol, ugly as it is, ships today. The proposed protocol reads more elegant on paper. Paper does not run CI. Ship the chaos suite first to confirm the elegant protocol holds up under mutation in production-shaped conditions.
