# acceptance: publishing

Run:

```sh
pnpm --filter @aifieldbrief/web test
pnpm turbo run typecheck
pnpm --filter @aifieldbrief/web build
python scripts/spec_check.py
python scripts/voice_lint.py
python scripts/validate_run_evidence.py
python -m pytest tests/scripts/test_run_evidence.py tests/scripts/test_run_evidence_cli.py
```

Manual checks:

- Visit `/feed.xml`, `/atom.xml`, and `/feed.json`.
- Submit a test email on a deployment with Resend env vars set.
- Call `/api/cron/weekly-digest?dry_run=1` and confirm the latest
  brief appears in the response.

Run-evidence verifiability conditions:

- `python scripts/backfill_run_records.py --week 2026-W22` writes a
  Run record under `ops/run-records/` plus a ledger under
  `ops/event-ledger/`. Both pass `validate_run_evidence.py`.
- `python scripts/finalize_run.py --brief briefs/<week>/ --gates ...`
  writes the same shape on a live publish.
- The committed sample Run records for W20, W21, W22 all carry
  `prompt_snapshot_hash`, `tool_schemas_snapshot_hash`,
  `sandbox_image_ref`, and `gate_results_summary`.
- `validate_run_evidence.py` exits 1 on any malformed record (covered
  by `tests/scripts/test_run_evidence_cli.py`).
