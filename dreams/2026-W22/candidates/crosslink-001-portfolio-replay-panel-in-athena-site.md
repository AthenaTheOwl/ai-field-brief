---
id: crosslink-001-portfolio-replay-panel-in-athena-site
target_kind: backlog_item
title: Surface the three canonical Run samples in athena-site's portfolio replay panel
human_review_required: true
status: candidate
evidence:
  - kind: artifact
    ref: "ops/run-records/run-36e307499472.json - W20 canonical Run (carries the portable repo URIs the panel dereferences)"
  - kind: artifact
    ref: ops/run-records/run-d74d787e6756.json - W21 canonical Run
  - kind: artifact
    ref: ops/run-records/run-1f1fc1f3d36d.json - W22 canonical Run
  - kind: decision
    ref: decisions/DEC-PUB-008-brief-portable-repo-uri-migration.md - portable URIs are what makes the cross-repo panel possible at all
  - kind: decision
    ref: decisions/DEC-PUB-009-ai-field-brief-ci-enforces-run-evidence-chain.md - the gate the panel mirrors
  - kind: doc
    ref: trace-to-eval-harness (sibling repo) - the resolver athena-site's panel would call into
  - kind: doc
    ref: portfolio_repo_map (per user memory) - athena-site is the portfolio control plane, so portfolio-wide replay state belongs there not in any one product repo
---

## proposal

Stand up a `ops/portfolio-replay/` directory in athena-site that holds a JSONL of replay verdicts pulled from each product repo's canonical samples on a Friday cron. ai-field-brief contributes three rows per Friday (one per canonical sample, with `{repo, run_id, verdict, head_sha, recorded_at}`). athena-site renders the directory as a panel on the site under `/ops/portfolio-replay/` with a small green/red badge per row plus a deep link to the failing repo's run-records when the verdict is false.

ai-field-brief's contribution is the side that produces the rows:

1. A new `scripts/emit_portfolio_replay_row.py` that runs all three canonical replays, formats one JSONL row per sample, and prints to stdout.
2. A new `.github/workflows/portfolio-replay-cron.yml` (Friday 12:00 UTC) that runs the emitter and opens a small PR against athena-site under `ops/portfolio-replay/` with the new rows appended.
3. The PR title carries the run-IDs and a clear "ai-field-brief Friday replay rows" prefix so the athena-site reviewer can merge without reading the diff in detail.

athena-site's contribution (out of scope for this dream but named in the cross-link):

1. A schema for the `portfolio-replay/<YYYY-WNN>.jsonl` file.
2. The site route that renders the panel.
3. The auto-merge policy for the cron PR (or a human-merge step if auto-merge is too aggressive for v1).

## why it earns its keep

The v2 rollout shipped a portable URI scheme (`repo://ai-field-brief@<sha>/...`) precisely so cross-repo consumers can resolve outputs without bespoke path code. Today the consumer is trace-to-eval-harness running inside CI. The next step is a human-facing surface: a portfolio operator sees one panel with one row per (repo, canonical sample) pair and reads the portfolio's replay health at a glance.

This crosslink also forces a real interop test of the `repo://` scheme. Today the scheme is exercised by trace-to-eval-harness during the CI matrix gate; tomorrow it gets exercised by athena-site's site build. Two consumers is the threshold at which the scheme stops being one repo's choice and starts being a portfolio contract.

The cross-link also closes a gap in the W22 report: the `--portfolio-root` resolver shape is documented but not exercised outside CI. A weekly cron that pushes rows into athena-site exercises it from a different entry point.

## cost

Medium. The ai-field-brief side:

- `scripts/emit_portfolio_replay_row.py` - new CLI, ~150 lines. Reuses `replay_run.py` as a library call.
- `.github/workflows/portfolio-replay-cron.yml` - new workflow file, ~80 lines. Uses `gh pr create` against the sibling repo with a deploy key or a fine-scoped PAT.
- One DEC (DEC-PUB-012 or similar) naming the row shape as a contract.
- Coordination with athena-site to align the row schema and the panel route. This is the biggest cost - cross-repo schema alignment.

The athena-site side is roughly equal in size (schema + panel + auto-merge policy) but lives outside this dream's scope; the dream proposes ai-field-brief's contribution + the coordination ask.

Roughly three days for ai-field-brief's side plus the coordination round-trip.

## risk

- Cross-repo schema drift. The row shape needs to be the same contract on both sides; a one-side change breaks the panel silently. Mitigation: the row schema lives in athena-site's `ops/schemas/` and gets cached in ai-field-brief's `ops/schemas-cache/`, validated by the existing schema-cache-freshness gate.
- The cron pushes a PR every Friday whether or not the verdict changed. Noise risk for athena-site reviewers. Mitigation: the workflow short-circuits with no-PR if the verdict matches last Friday's row (diff against the last row in `ops/portfolio-replay/<prior-week>.jsonl`).
- Deploy-key or PAT management for the cross-repo PR. A leaked key opens a portfolio-wide blast radius. Mitigation: fine-scoped PAT with `contents:write` scoped to athena-site only, rotated every 90 days, and named in the security threat model.
- This is the first cross-repo cron in the portfolio. Operational complexity goes up. Mitigation: ship with a manual-trigger fallback (`workflow_dispatch`) so a portfolio operator can run the emit pass on demand if the cron breaks.

## timeline

Next month. The cross-repo coordination is the gating cost; the implementation is straightforward once the row schema is locked. Ordering: schema alignment with athena-site (week 1), emit script + workflow file (week 2), athena-site's panel route (week 3, owned by athena-site), end-to-end test of one Friday cron (week 4).

If athena-site cannot ship the panel side in the same window, this candidate sits as a "spec written, implementation paused" backlog item until the panel is ready.

## promotion path

If approved, the change touches (ai-field-brief side):

- `scripts/emit_portfolio_replay_row.py` - new file.
- `.github/workflows/portfolio-replay-cron.yml` - new file.
- `decisions/DEC-PUB-012-portfolio-replay-row-emission.md` - new DEC.
- `specs/0007-publishing/requirements.md` - R-PUB-027 (ai-field-brief emits a portfolio-replay row per canonical sample on a Friday cron).
- `ops/schemas-cache/portfolio-replay-row.schema.json` - cached copy of athena-site's row schema.

Athena-site side (named, not promoted by this dream):

- `ops/schemas/portfolio-replay-row.schema.json` - the row schema as a contract.
- `ops/portfolio-replay/<YYYY-WNN>.jsonl` - the weekly directory.
- A site route + render component for the panel.
- An auto-merge or human-merge policy for the cron PR.

Owner role on promotion: `control.coordinator` (cross-repo work is portfolio coordination, not feature shipping). The coordinator opens the athena-site companion thread and routes the row-schema design.

## risks if promoted blindly

- Cross-repo work without a coordinator-opened companion thread becomes one repo's lonely PR. The panel never lands. Promote only with the athena-site companion thread already open.
- The Friday cron's PR cadence is a recurring noise floor for athena-site reviewers. Confirm the no-change short-circuit lands in v1; otherwise the panel becomes the boy who cried wolf.
- A leaked PAT is a portfolio-wide problem. Confirm the PAT scope is `contents:write` on athena-site only and that rotation is in the security threat model before the cron lands.
