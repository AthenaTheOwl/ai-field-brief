# simon-curl-pressure

- **Source:** Simon Willison's Weblog (Daniel Stenberg primary)
- **URL:** https://simonwillison.net/2026/May/26/the-pressure/
- **Captured:** 2026-05-26
- **Priority:** high
- **Cells:** MTRX-W22-curl-source_gist, MTRX-W22-curl-mechanism_extraction, MTRX-W22-curl-reusable_pattern, MTRX-W22-curl-adoption_action, MTRX-W22-curl-governance_surface

## What

curl's Daniel Stenberg reports >1 AI-assisted security report per
day on average — 4-5x the 2024 rate and 2x the 2025 rate. Almost
none of the reports surface terrible vulnerabilities; all recent
findings have been LOW or MEDIUM severity.

## Why it matters

This is the W22 brief 1 thesis surfacing on a different lane.
Agent output rate exceeds human review capacity; the maintainer is
the bottleneck. SQLite's AGENTS.md is the same shape with a
different door — accept reports with reproducible evidence, reject
agentic PRs. The pattern generalizes to internal security teams,
not just open-source maintainers.

## Action surface

workflow, tool-policy, source-registry

## Concrete move

For project maintainers and corporate security teams: publish an
AI-assisted-report policy that names the required evidence
(reproducible command, expected vs actual, raw error text) and
auto-closes reports without it. Pair with a "slow-mode" lever on
bounty programs so the agent's output can be throttled when triage
queue depth exceeds a threshold.

## Caveats

Stenberg's data is anecdotal-by-volume (curl-specific), not a
multi-project survey. The "all LOW/MEDIUM" line is a comforting
counterfactual but the trajectory is not given.
