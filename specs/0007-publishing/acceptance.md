# acceptance: publishing

Run:

```sh
pnpm --filter @aifieldbrief/web test
pnpm turbo run typecheck
pnpm --filter @aifieldbrief/web build
python scripts/spec_check.py
python scripts/voice_lint.py
python scripts/validate_run_evidence.py
python -m pytest tests/scripts/test_run_evidence.py tests/scripts/test_run_evidence_cli.py tests/scripts/test_validate_run_evidence_cross_checks.py
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
- `validate_run_evidence.py` exits 1 on any cross-check violation
  (missing required-for-done field, missing terminal evidence event,
  hash mismatch between Run and pipeline.start, fields_populated
  mismatch, or `gate_results_summary` mismatch with the ledger). Each
  cross-check is covered by a focused negative test in
  `tests/scripts/test_validate_run_evidence_cross_checks.py`.
- `python scripts/replay_run.py --run-id run-874c5e341e13`,
  `--run-id run-d223cf166b70`, and `--run-id run-7131f5246462` each
  exit 0 with `replay_equivalent: true` at the recorded HEAD. The
  emitted replay artifacts land under
  `ops/event-ledger/replay-<run-id>-<ISO>.jsonl` and
  `ops/replay-records/<run-id>/<replay-event-id>.json`.
- The replay CLI exits 1 with a `git checkout <sha>` instruction on
  any HEAD mismatch, flips `replay_equivalent` to false on a missing
  output artifact or a snapshot-hash mismatch, and exits 1 on a
  missing Run record. Each surface is covered by a focused test in
  `tests/scripts/test_replay_run.py`.
- The emitted sample Run records carry `sandbox_image_ref` in the
  portable form (`repo://ai-field-brief@<sha>/`) per DEC-CDCP-014.
  Every `inputs[].ref` and `outputs[].artifact_id` wraps as either
  `repo://ai-field-brief@<sha>/<rel-path>` or
  `artifact://ai-field-brief/<id>`. Covered by
  `tests/scripts/test_run_evidence.py` (URI helpers) and by
  inspection of `ops/run-records/run-*.json`.
- `python scripts/finalize_sandbox_ref.py --all` rewrites every
  `@PENDING/` placeholder to the actual SHA in one pass, is
  idempotent on records with no PENDING markers, and refuses to
  write a non-40-char SHA via `--sha`. Covered by
  `tests/scripts/test_finalize_sandbox_ref.py`.
- The replay ledger filename carries microsecond resolution
  (`ops/event-ledger/replay-<run-id>-YYYY-MM-DDTHHMMSS.<micros>Z.jsonl`)
  so two replays of the same Run inside one wall-clock second land on
  distinct files. Closes the latent per-second collision bug flagged
  by the Workflow B-Recovery cross-portfolio audit; the same fix
  landed in supplier-risk-rag-agent (DEC-EVL-011) and
  procurement-negotiation-lab (DEC-FACTORY-013). Covered by
  inspection of `scripts/replay_run.py::_now_filename_iso`.
