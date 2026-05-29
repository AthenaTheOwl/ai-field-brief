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

## Brief OS refinement layer (DEC-MTRX-006)

The Brief OS refinement layer sits on top of the matrix plane
without rewiring the cell + verifier + synthesis loop. The three
matrix passes get explicit names (Pass 1 = source note, Pass 2 =
faithfulness audit, Pass 3 = action extraction); the lens-to-pass
map is recorded in `AGENTS.md` and mirrors the lens entries under
`config/prompt_lenses.yaml`. Three new configuration files land
under `config/`:

| File | Purpose | Read by |
|---|---|---|
| `scoring_model.yaml` | Three-axis rubric + four penalties + thresholds. | Pass 3 synthesis; brief author |
| `profiles.yaml` | Named profiles + interests + negative preferences + optional scoring overrides. | Lens designer; Pass 3 synthesis; MatrixRun emitter |
| `action_surface_taxonomy.yaml` | Canonical 14-surface taxonomy bounding action-candidate surfaces. | Pass 3 synthesis; brief author; voice review |

The scoring model produces a `final_score` per item; the
thresholds gate promotion (`>= 12` Top signals, `[9, 12)`
Watchlist, `< 9` Archive). The profile is pinned per MatrixRun
and recorded on the Run record so the replay CLI re-resolves the
same configuration. The 14-surface taxonomy bounds the action
vocabulary; extending the taxonomy requires a new DEC and a bump
to the YAML.

The evidence-spine rules in `AGENTS.md` enforce the chain
end-to-end: no digest claim without verified cells; no cell
verified without source refs; no action promoted without the six
required fields plus a surface from the taxonomy plus a scoring
entry against the rubric. The brief template
(`templates/weekly-brief.md`) carries the matching section shape
(Field thesis, Top signals, Reusable patterns, Action queue,
Watchlist, Archive notes, Sources reviewed, Closing thought) so
the brief-author surface and the role contracts read the same
contract.
