# acceptance: publishing

Run:

```sh
pnpm --filter @aifieldbrief/web test
pnpm turbo run typecheck
pnpm --filter @aifieldbrief/web build
python scripts/spec_check.py
python scripts/voice_lint.py
python scripts/validate_run_evidence.py
python -m pytest tests/scripts/test_run_evidence.py tests/scripts/test_run_evidence_cli.py tests/scripts/test_validate_run_evidence_cross_checks.py tests/scripts/test_chaos_run_evidence.py
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
- `python -m pytest tests/scripts/test_chaos_run_evidence.py` walks
  seven mutation classes against the canonical Run + ledger sample
  and asserts `scripts/validate_run_evidence.py` exits non-zero on
  every class. The classes cover Round 3's four cross-checks (M1
  prompt-hash, M2 tool-hash, M3 phantom gate, M6 fields_populated
  drift), Round 2's typed event payload schema (M5 pipeline.start
  payload missing prompt_snapshot_hash), the required-terminal-event
  check (M4 dropped gate.run.evidence_recorded), and the
  required-for-done gate (M7 done Run missing sandbox_image_ref).
  A zero exit code on any mutation fails the test with a message
  flagging the silent pass as a real validator gap.
- `.github/workflows/run-evidence-gates.yml` runs the chaos suite as
  a blocking `chaos-validation` job on every pull request and every
  push to main; the job carries no `continue-on-error: true` and is
  independent of the `packet-and-replay` matrix.
- Every chaos test copies the canonical sample into `tmp_path`
  before mutating, and the
  `test_canonical_sample_on_disk_is_not_modified` guard asserts the
  load-bearing fields on the disk-resident sample are still present
  after the run.
