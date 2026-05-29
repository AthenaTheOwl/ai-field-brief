# design: prompt matrix plane

## Shape

The matrix plane is a four-role loop sitting between source sweep
and digest synthesis. The loop's atomic artifact is the matrix cell:
one source-item × one lens × one verifiable answer.

```
sweep -> triage -> lens-designer -> matrix-runner -> cell-verifier ->
synthesis-editor -> brief author
```

The role contracts live under `.agents/roles/science.*/`. The
workflow lives at `.agents/workflows/matrix-analysis-loop.yaml`.

## Surfaces

| Surface | File | Purpose |
|---|---|---|
| Lens catalog | `config/prompt_lenses.yaml` | The reusable column definitions. |
| Lens prompts | `prompts/lenses/*.md` | One markdown prompt per lens, source-grounded. |
| Cell faithfulness prompt | `prompts/cell_faithfulness.md` | Seven-question check the verifier runs. |
| Synthesis prompt | `prompts/matrix_synthesis.md` | The synthesis editor's contract. |
| Cell schema | `schemas/matrix_cell.schema.json` | The typed shape every cell conforms to. |
| Run schema | `schemas/matrix_run.schema.json` | One run record per batch. |
| Lens schema | `schemas/prompt_lens.schema.json` | The catalog row shape. |
| Lens output schema | `schemas/lens_output.schema.json` | The structured envelope every lens returns. |

## Data flow

1. `science.lens-designer` reads the catalog, validates each entry,
   and emits a `lens_selection` artifact for the profile.
2. `science.matrix-runner` walks each source-item-lens pair and
   writes one cell conforming to `matrix_cell.schema.json`. Cells
   land with `faithfulness_status: not_checked`.
3. `science.cell-verifier` reads each cell against the source body,
   runs the seven-question check from `cell_faithfulness.md`, and
   writes back the cell `faithfulness_status` and `status` fields.
4. `science.matrix-synthesis-editor` reads the verified subset,
   clusters by row and theme, and drafts action candidates. Every
   line in the output traces to one or more cell ids.

## Storage today

Cells and runs live as file artifacts under the brief run folder
during the matrix pass. The relational store at
`packages/db/migrations/staged/001_prompt_matrix.sql` lands as a
reference for the future wiring pass; the staged path keeps the file
out of the active drizzle migrator until a follow-up DEC turns it on.

## Failure modes

- A lens prompt drifts away from source grounding. The lens
  designer catches the drift before the run starts; the cell
  verifier catches it on the cell.
- A cell quotes the source but reframes the claim. The verifier
  routes a `PATCH_CELL` verdict; the matrix runner rewrites the
  cell.
- A theme cluster pulls fewer than two verified cells. The synthesis
  editor escalates back to the verifier rather than ship the
  cluster.
- An action candidate cannot point at a verified cell. The candidate
  drops; the brief author does not see it.

## Out of scope this pass

- DB wiring. The migration sits under `staged/` per R-MTRX-006.
- UI. The matrix UI spec lives at `docs/UI_SPEC_PROMPT_MATRIX.md`;
  a UI implementation lands in a later spec.
- Profile guards beyond the `creative_os_only` example. Future
  profiles add guards alongside the lens entries.
