# Matrix Plane Design

## Pattern

The prompt matrix is a reusable analysis structure:

```text
Document/source rows × prompt-lens columns = grounded cells
```

A cell is a typed artifact, not a chat answer. Every cell carries:

- source item id
- lens id
- extraction mode
- answer
- source references
- confidence
- faithfulness status
- warnings

## Why it matters

Single-pass summaries flatten sources. Matrix cells preserve dimensionality.

A source can be weak as news but strong as a failure-mode example. Another can be low novelty but high implementation value. A matrix lets each lens surface different value without forcing everything into one summary.

## AI Brief usage

Rows:
- podcast episodes
- articles
- papers
- repos
- changelogs
- videos
- books/chapters

Columns:
- source gist
- claims and bets
- mechanisms
- reusable patterns
- adoption actions
- risks/caveats
- governance surfaces
- Creative OS impact
- contrarian take
- watchlist trigger

## Creative OS usage

Rows:
- scenes
- chapters
- episodes
- levels
- quests
- cinematics
- asset briefs

Columns:
- intent coverage
- canon/design state
- continuity
- reveal/seed discipline
- voice/style
- relationship movement
- gameplay loop
- audience/player state
- hidden risk
- patch recommendation

## Software control-plane usage

Rows:
- specs
- PRs
- commits
- incidents
- eval runs
- source signals

Columns:
- architecture impact
- implementation risk
- test/eval coverage
- security/blast radius
- ops/release impact
- rollback plan
- action candidate

## Rule

The digest, brief, patch queue, or promotion queue should be downstream of verified cells, not raw model prose.

## How this lands in the playbook

The matrix plane shows up as four new steps in
`playbook/run-weekly-brief.md`, sitting between the existing triage
step and the synthesize step:

- Step 4 (matrix cell production) pins to `science.matrix-runner`. The
  runner reads each `required: true` lens from
  `config/prompt_lenses.yaml`, applies it to each triaged source item,
  and writes one cell per source-item-lens pair conforming to
  `schemas/matrix_cell.schema.json`.
- Step 5 (cell faithfulness verification) pins to
  `science.cell-verifier`. The verifier runs the seven-question check
  in `prompts/cell_faithfulness.md` against each cell, marks the cell
  `passed`, `needs_patch`, or `failed`, and writes back
  `faithfulness_status` and `status`.
- Step 6 (theme and row synthesis) pins to
  `science.matrix-synthesis-editor`. The editor clusters verified
  cells into row summaries and theme clusters, drafts action
  candidates (each with the six required fields), and emits the input
  the brief author pulls from.
- Step 7 (synthesize) reads from the row summaries, not the raw
  sources. Every pick names the cell ids it leans on as inline
  comments so the published markdown stays clean while the trace
  stays intact.

Step 8 (the per-cell faithfulness audit) replaces the prior
per-pick audit. The cell verifier already ran the structural check;
this step is the brief author's final read for tone and framing
drift across the assembled picks.

The lens designer step (selecting which lenses run on which profile)
sits one layer above the playbook in
`.agents/workflows/matrix-analysis-loop.yaml`. For the manual weekly
pass, the default selection is the six `required: true` lenses; a
profile that wants `governance_surface`, `contrarian_take`, or
`watchlist_trigger` opts in via the workflow step.
