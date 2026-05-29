# simon-sqlite-agents

- **Source:** Simon Willison's Weblog (SQLite AGENTS.md primary)
- **URL:** https://simonwillison.net/2026/May/27/sqlite-agents/
- **Captured:** 2026-05-27
- **Priority:** high
- **Cells:** MTRX-W22-sqlite-source_gist, MTRX-W22-sqlite-reusable_pattern, MTRX-W22-sqlite-governance_surface

## What

SQLite shipped an AGENTS.md that rejects agentic code patches and
AI-generated PRs while accepting well-researched bug reports from
agents with reproducible test cases. The project removed "(currently)"
from its rejection statement and stood up a separate Bug Forum to
absorb low-quality AI-generated bug reports.

## Why it matters

This is a project-level policy artifact other open-source projects
will copy or fork. The shape is replicable: accept evidence, reject
narrative; accept reports, reject patches; isolate the AI-driven
channel from the human-curated one. The separate-Bug-Forum decision
is the architectural cousin of curl's slow-mode request.

## Action surface

agent-role, tool-policy, workflow

## Concrete move

If you maintain a public-facing project (open-source or commercial
support portal), publish an AGENTS.md or equivalent contract this
week. State the evidence the project requires; state the categories
of submission the project auto-closes. Cite SQLite as precedent.

## Caveats

SQLite's stance is conservative by project temperament. A more
liberal accept-pattern (accept agentic PRs with mandatory test
coverage) is a defensible alternative. What matters is that a
policy exists at all; every project need not mirror SQLite's
specific choice.
