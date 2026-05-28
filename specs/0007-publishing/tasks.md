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
