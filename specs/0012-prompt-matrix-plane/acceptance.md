# acceptance: prompt matrix plane

## R-MTRX-001: matrix cells carry source refs

- The cell write helper rejects a cell with an empty `source_refs`
  array and returns a typed error naming the cell id.
- `schemas/matrix_cell.schema.json` validates every emitted cell;
  the `validate_schemas.py` gate catches a malformed cell on every
  push.

## R-MTRX-002: cell faithfulness is verified before synthesis

- A row summary that cites a `not_checked`, `needs_patch`, or
  `failed` cell fails the synthesis editor's output schema check
  (the cell-id reference must resolve to a `passed` cell).
- The cell verifier's faithfulness report records one verdict per
  cell. A run that produced N cells emits a report with N verdicts.

## R-MTRX-003: digest claims trace to verified cells

- Every published brief under `briefs/YYYY-WNN/` carries inline
  `<!-- cell-id: <id> -->` comments next to each pick that traces to
  a cell. The comments render as nothing in HTML but stay in the
  markdown source for replay.
- The synthesis editor refuses to ship a row summary without a
  cell-id reference on every sentence.

## R-MTRX-004: lens catalog drives the matrix run

- `config/prompt_lenses.yaml` parses against
  `schemas/prompt_lens.schema.json`. Adding a lens without filling
  the required fields fails the schema check.
- The lens designer's run output lists every selected lens id and
  the guard outcome per optional lens.

## R-MTRX-005: action candidates carry the six required fields

- The synthesis output schema rejects an action candidate missing
  any of: source_support, surface, test, expected_benefit, risk,
  disposition.
- A disposition outside the enum is rejected by the same schema.

## R-MTRX-006: matrix-plane DB migration is parked, not wired

- `packages/db/migrations/staged/001_prompt_matrix.sql` lives under
  the `staged/` subdir, which the drizzle config does not include in
  its migrator search.
- No TypeScript file under `packages/db/src/` imports or references
  any of the three table names (`prompt_lenses`, `matrix_runs`,
  `matrix_cells`).
- The follow-up DEC lands before any code reads or writes the
  tables.
