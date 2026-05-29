# requirements: prompt matrix plane

The matrix plane sits between source sweep and digest synthesis.
Briefs draw from verified matrix cells, not from raw source notes.
Every requirement here ties to one or more cells, lenses, or roles
the install pass shipped.

### R-MTRX-001: matrix cells carry source refs

Every matrix cell written by `science.matrix-runner` carries at least
one entry in its `source_refs` array.

Acceptance:

- The cell payload conforms to `schemas/matrix_cell.schema.json`.
- A cell with an empty `source_refs` array is rejected at write time.
- Each source ref names a URI, a `quote_or_span`, and a `ref_type`
  from the schema enum.

### R-MTRX-002: cell faithfulness is verified before synthesis

Every matrix cell passes through `science.cell-verifier` and lands
with `faithfulness_status` set to one of `passed`, `needs_patch`, or
`failed` before any synthesis step reads it.

Acceptance:

- A cell with `faithfulness_status: not_checked` cannot be cited by
  `science.matrix-synthesis-editor`.
- A `needs_patch` cell either patches forward to `passed` or drops.
- A `failed` cell drops from the run and the row summary does not
  reference it.

### R-MTRX-003: digest claims trace to verified cells

Every claim in a row summary, theme cluster, or action candidate
emitted by `science.matrix-synthesis-editor` carries an inline cell-id
reference to a cell with `faithfulness_status: passed`.

Acceptance:

- The synthesis output conforms to
  `.agents/roles/science.matrix-synthesis-editor/output.schema.json`.
- A row summary that cites a cell with any other faithfulness status
  is rejected at synthesis time.
- The published brief carries inline `cell-id:` comments next to each
  pick that traces to a cell.

### R-MTRX-004: lens catalog drives the matrix run

The matrix run reads `config/prompt_lenses.yaml` for the lens set.
Every `required: true` lens runs on every profile; optional lenses
run only when the profile opts in.

Acceptance:

- The catalog conforms to `schemas/prompt_lens.schema.json`.
- `science.lens-designer` validates the catalog before each run and
  refuses to ship a selection that pulls an absent lens.
- A lens with `profile_guard: <name>` runs only when the profile
  enables that guard.

### R-MTRX-005: action candidates carry the six required fields

Every action candidate emitted by
`science.matrix-synthesis-editor` carries: source support (verified
cell ids), action surface, test plan, expected benefit, risk, and
disposition.

Acceptance:

- An action candidate missing any of the six fields is rejected by
  the synthesis output schema.
- The disposition is one of `adopt_now`, `prototype`, `monitor`,
  `archive`, `reject`, `promote_to_os_candidate`.
- The source-support list names cell ids; the brief author can
  follow each id to a cell in the run.

### R-MTRX-006: matrix-plane DB migration is parked, not wired

The DB migration at
`packages/db/migrations/staged/001_prompt_matrix.sql` lands as a
reference artifact for a future Drizzle wiring pass. The brief
workflow today writes matrix cells to file artifacts under the run
folder; the relational store wiring lands behind a follow-up DEC.

Acceptance:

- The SQL file lives under `packages/db/migrations/staged/` and is
  not picked up by the drizzle migrator.
- No live db code path reads from or writes to the `prompt_lenses`,
  `matrix_runs`, or `matrix_cells` tables.
- The follow-up DEC names the schema sync test, the workspace
  scoping rule, and the audit-event plumbing the wiring pass must
  land.
