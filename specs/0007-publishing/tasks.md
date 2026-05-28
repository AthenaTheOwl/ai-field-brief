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
