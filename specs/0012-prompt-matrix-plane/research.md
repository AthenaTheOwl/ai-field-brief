# research: prompt matrix plane

## Pattern origin

The prompt-matrix shape names the missing middle layer between raw
source sweep and digest synthesis. The shape is a reusable
analytical table: rows are source items, columns are prompt lenses,
cells are grounded, verifiable outputs. The pattern surfaced in two
parallel reads: a friend's screenshot of a multi-lens analysis
workbook and ChatGPT's pulse identification of the matrix join key
during the Cognitive Delivery OS framing thread.

## Why the matrix beats a flat summary

A single-pass summary flattens dimensionality. A source can be weak
as news but strong as a failure-mode example; another can be low
novelty but high implementation value. A matrix lets each lens
surface different value without forcing everything into one
summary. The cell becomes the audit unit: a digest claim either
points at a verified cell or it does not ship.

## Prior art

- `DEC-PUB-004` (faithfulness audit) shipped the first pre-publish
  check. That check sits per-pick; the matrix plane moves the check
  per-cell, which is finer-grained and lets multiple picks share a
  cell.
- The athena-site control-plane charter at
  `../athena-site/ops/control-plane.md` names six artifact types and
  the cross-repo contracts. The matrix cell, run, and lens are new
  artifact types under that charter's umbrella; the matrix plane
  install does not amend the charter, only ships repo-local
  artifacts that conform to it.
- The proof-gate-runner role under
  `.agents/roles/science.proof-gate-runner/` models the pattern the
  cell verifier follows: read the artifact, run the check, write
  one verdict per item with a root-cause read on every non-pass.

## Why "science" guild and not "analysis"

The Phase 1 plan named the four roles under a new `analysis` guild.
The cross-repo `role.schema.json` guild enum (athena-site) does not
include `analysis`; per DEC-CDCP-010 cross-repo schemas live in
athena-site. Extending the enum is out of scope for this pass. The
matrix plane is evidence-grounded verification work, which sits
cleanly under the science guild today.

A future `analysis` guild can graduate via athena-site if and when
other analysis-flavored roles (research synthesizers, eval
curators, failure analysts) accumulate enough mass to justify the
schema amendment.

## Out of scope

- The relational store wiring for cells, lenses, and runs. The
  staged migration carries the schema; the wiring waits for a
  follow-up DEC that names the workspace scoping rule and the
  audit-event plumbing.
- The UI for the matrix view. The UI spec lives at
  `docs/UI_SPEC_PROMPT_MATRIX.md` for a later product pass.
- A `model.call` tool registry entry with budget caps. The matrix
  runner shares the brief workflow's harness today.
