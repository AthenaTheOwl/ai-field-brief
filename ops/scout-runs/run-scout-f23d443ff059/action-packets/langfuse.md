# Action packet: Wire Langfuse Code Evaluators + Experiments CI into ai-field-brief run-evidence loop

- Source: `langfuse` (https://langfuse.com/changelog)
- Snapshot: `ops/scout-snapshots/run-scout-f23d443ff059/langfuse-changelog.html`
- Cell ids: MTRX-scout-run-scout-f23d443ff059-langfuse-action_packet, MTRX-scout-run-scout-f23d443ff059-langfuse-repo_project_scan
- Disposition: prototype
- Effort: small (1-2 days; SDK + one Actions workflow file + 2 evaluator scripts)

## Hypothesis

Replacing ad-hoc score-asserting scripts with Langfuse Code Evaluators (deterministic Python checks) plus the new GitHub Actions Experiments step gives ai-field-brief a typed, observable, version-controlled eval surface — without writing a new framework.

## Test

On one scout-snapshot pipeline run, instrument trace ingestion to Langfuse, define 2 code evaluators (e.g., `faithfulness_status == passed`, `len(source_ref_quote) >= 10`), and run `langfuse experiments` in a GitHub Actions job against a 10-item dataset of past matrix cells. Compare detected regressions vs. current homegrown checks.

## Success metric

Within 1 week: (a) 100% of current invariant checks reproducible as code evaluators; (b) CI job fails on an injected regression; (c) MCP server returns scores back to a Claude agent in under 2s.

## Risk

New trust boundary: hosted MCP writes scores/comments on behalf of agents. Mitigate by scoping the API key to one project and a read-only initial run.

## Kill criterion

Kill if Code Evaluators remain GUI-only after 30 days with no programmatic registration API — they must be configurable from CI to be worth integrating. Also kill if the MCP write surface cannot be scoped to a single project key.
