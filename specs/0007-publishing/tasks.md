# tasks: publishing

- [x] Add static RSS, Atom, and JSON Feed routes.
- [x] Add shared feed summary builder.
- [x] Add subscription form to the public home page.
- [x] Add Resend contact capture route.
- [x] Add weekly digest builder and cron endpoint.
- [x] Add tests for feed and email digest construction.
- [x] Add Vercel cron entry for Friday weekly delivery.
- [x] Add `scripts/run_evidence.py` emitter library.
- [x] Add `scripts/finalize_run.py` live publish-time CLI.
- [x] Add `scripts/backfill_run_records.py` backfill CLI.
- [x] Add `scripts/validate_run_evidence.py` validator gate.
- [x] Wire the validator into `.github/workflows/ci.yml`.
- [x] Reference `finalize_run.py` from `playbook/run-weekly-brief.md`
  at the publish step.
- [x] Backfill Run records + event ledgers for W20, W21, W22 under
  `ops/run-records/` and `ops/event-ledger/`.
- [x] Emit the typed `pipeline.complete` payload (`status` plus
  optional `gate_results_summary`) from both `finalize_run.py` and
  `backfill_run_records.py`.
- [x] Emit one synthetic `gate.check.passed` event per canonical
  brief gate from `backfill_run_records.py`.
- [x] Extend `scripts/validate_run_evidence.py` with the
  required-for-done field set, the required-terminal-event check, and
  the four ledger/Run cross-checks (hashes, fields_populated,
  gate rollup).
- [x] Add cross-check coverage in
  `tests/scripts/test_validate_run_evidence_cross_checks.py` (one
  positive case plus one negative case per check).
- [x] Regenerate the W20/W21/W22 sample Run + ledger pairs through
  the fixed emitters.
- [x] Add `scripts/replay_run.py` equivalence replay CLI plus
  `tests/scripts/test_replay_run.py` (positive cases for W20/W21/W22
  plus HEAD-mismatch, missing-record, missing-artifact, and
  prompt-hash-mismatch negatives).
- [x] Re-anchor `sandbox_image_ref` on the three sample Run records
  to the SHA at which the recorded snapshot hashes are reproducible
  (the records-regeneration commit), and commit the replay artifacts
  produced by running the CLI against that SHA.
- [x] Migrate the emitter to the portable URI grammar from DEC-CDCP-014:
  `sandbox_image_ref` becomes `repo://ai-field-brief@<sha>/`,
  inputs/outputs wrap as `repo://...` or `artifact://...` per shape,
  `workspace_id` stays the bare repo identifier.
- [x] Add `resolve_uri(uri, portfolio_root)` to both
  `scripts/validate_run_evidence.py` and `scripts/run_evidence.py`;
  update `scripts/replay_run.py` to accept both URI and legacy
  `sandbox_image_ref` shapes via the shared
  `run_evidence.parse_sandbox_sha` helper.
- [x] Add `scripts/finalize_sandbox_ref.py` (second-pass CLI) that
  rewrites every `@PENDING/` placeholder to the actual SHA. The
  emitter writes the placeholder; the regenerate flow runs the
  rewriter after the first commit lands.
- [x] Regenerate the W20/W21/W22 Run + ledger pairs through the
  fixed emitter, run `finalize_sandbox_ref.py --all`, and commit the
  rewritten records in a second commit.
- [x] Add positive + negative coverage for the URI helpers + the
  finalize_sandbox_ref CLI under `tests/scripts/`.
