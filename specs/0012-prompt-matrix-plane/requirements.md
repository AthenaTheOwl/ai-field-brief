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

### R-MTRX-007: scoring model gates digest promotion

`config/scoring_model.yaml` is the typed rubric the Brief OS uses
to gate every item the matrix plane produced. The rubric carries
three axes (`source_quality`, `profile_relevance`, `actionability`)
plus four penalties, and the combined `final_score` routes each
item into Top signals, Watchlist, or Archive.

Acceptance:

- `config/scoring_model.yaml` parses as YAML and carries an `axes`
  block with the three named axes and a `penalties` block with the
  four named penalties.
- The `thresholds` block names `include_in_digest`, `watchlist`,
  and `archive` with the boundaries documented in the file
  (`>= 12`, `[9, 12)`, `< 9`).
- The synthesis editor's Pass 3 output records the rubric values
  alongside every action candidate so the brief-author review pass
  can read the score and the penalties before approving the pick.

### R-MTRX-008: profiles config pins every MatrixRun to a profile id

`config/profiles.yaml` carries the named profiles a MatrixRun can
pin to. The initial registry carries `personal` and `broad_builder`;
every MatrixRun records its `profile_id` and the synthesis editor
reads the profile's interests and negative preferences before
scoring.

Acceptance:

- `config/profiles.yaml` parses as YAML and carries a `profiles`
  map with at least the `personal` and `broad_builder` keys.
- Each profile carries an `interests` list and a
  `negative_preferences` list.
- A MatrixRun without a `profile_id` is rejected by the run schema
  before any Pass 3 synthesis reads it.

### R-MTRX-009: action-surface taxonomy is canonical and bounded

`config/action_surface_taxonomy.yaml` is the canonical list of
action surfaces a digest claim or action candidate may cite. The
initial taxonomy carries 14 surfaces; the synthesis editor rejects
an action candidate whose `surface` does not resolve against this
file.

Acceptance:

- `config/action_surface_taxonomy.yaml` parses as YAML and carries
  a `surfaces` list of 14 entries, each with `id` and `notes`.
- Adding a surface requires a new DEC and a bump to this file; the
  rule is recorded in `AGENTS.md` under the evidence-spine
  section.
- The brief template references the surface labels inline so the
  brief author cannot drift from the canonical list.

### R-MTRX-010: three-pass note system names the lens-to-role map

`AGENTS.md` names the three-pass note system explicitly and maps
each pass to the lenses in `config/prompt_lenses.yaml` and the
science role that runs it. Pass 1 = structured source note
(`source_gist`, `claims_and_bets`, `mechanism_extraction`,
`science.matrix-runner`); Pass 2 = faithfulness audit
(`prompts/cell_faithfulness.md`, `science.cell-verifier`); Pass 3
= action extraction (`reusable_pattern`, `adoption_action`,
`risk_and_caveats`, `science.matrix-synthesis-editor`).

Acceptance:

- `AGENTS.md` carries a "Three-pass note system" section that
  names every pass, its lenses, and its owning role.
- The pass-to-lens map matches the entries under
  `config/prompt_lenses.yaml`.
- The playbook's matrix steps (4, 5, 6) cite the same three-pass
  labels so the agent reads one map across all three documents.

### R-MTRX-011: evidence-spine rules enforce the chain end-to-end

`AGENTS.md` carries the Brief OS evidence-spine rules as a
non-negotiable, non-optional section. The rules enforce the chain
end-to-end: no digest claim without verified cells; no cell
verified without source refs; no action candidate promoted without
the six required fields plus an action surface from the canonical
taxonomy plus a scoring entry against the rubric.

Acceptance:

- `AGENTS.md` carries the evidence-spine rules at the top of the
  file under a named section.
- The rules name `config/scoring_model.yaml`,
  `config/profiles.yaml`, and
  `config/action_surface_taxonomy.yaml` as the three configuration
  surfaces the rules read.
- Amending any rule requires a new DEC; the rule is recorded under
  this DEC and DEC-MTRX-001.

### R-MTRX-012: brief template carries the Brief OS section shape

`templates/weekly-brief.md` carries the Brief OS digest format:
the meta block (with `profile_id` and `matrix_run_id`); Field
thesis; Top signals (per-pick Source, Payload, Mechanism, Why it
matters, Reusable pattern, Action surface, Try, Confidence,
Evidence); Reusable patterns; Action queue (with surface, effort,
risk, test columns); Watchlist (with revisit trigger);
Archive notes; Sources reviewed; Closing thought.

Acceptance:

- The template carries all seven Brief OS sections in the listed
  order.
- Every Top signal placeholder carries an `Evidence:` field for
  cell ids and a `Confidence:` field for the high/medium/low
  label.
- The template's voice-notes block names the canonical action
  surface labels inline so an author cannot drift from
  `config/action_surface_taxonomy.yaml`.

### R-MTRX-013: playbook references the Brief OS configurations

`playbook/run-weekly-brief.md` cites the three Brief OS
configuration files in its Inputs section and references the
scoring thresholds + action-surface taxonomy lookup in steps 4-6
where the matrix passes run.

Acceptance:

- The playbook's Inputs section lists
  `config/scoring_model.yaml`, `config/profiles.yaml`, and
  `config/action_surface_taxonomy.yaml`.
- Step 6 (Pass 3) cites the score thresholds (`>= 12` Top signals,
  `[9, 12)` Watchlist, `< 9` Archive) inline.
- Step 6 also names the surface lookup against
  `config/action_surface_taxonomy.yaml` and the six required
  action-candidate fields.

### R-MTRX-014: MatrixRun records its profile_id

Every MatrixRun emitted under the Brief OS refinement records the
`profile_id` it ran under. The synthesis editor reads the profile's
interests and negative preferences and applies any per-profile
scoring overrides before promoting items to Top signals or the
Watchlist.

Acceptance:

- The MatrixRun schema requires `profile_id` and rejects a run
  with an empty or unknown id.
- A profile id used in a MatrixRun must resolve against the
  `profiles` map in `config/profiles.yaml`.
- The Run-record emitter records the `profile_id` alongside the
  run id so the replay CLI can re-resolve the profile under the
  same configuration.

### R-MTRX-015: Pass 4 lens catalog carries the three systems lenses

`config/prompt_lenses.yaml` carries three Pass 4 lens entries
(`systems_thinking`, `transferable_principle`, `falsification_test`)
under `category: synthesis`. Each entry names a markdown prompt
under `prompts/lenses/` and runs on the Top picks the Pass 3
scoring gate promoted, not on every source item swept.

Acceptance:

- `config/prompt_lenses.yaml` parses as YAML and carries the three
  entries with ids `systems_thinking`, `transferable_principle`,
  and `falsification_test`.
- Each entry references a prompt file under `prompts/lenses/` that
  exists on disk.
- The three entries name modes (`interpretive`, `synthetic`,
  `critique`) that match the prompt headers.

### R-MTRX-016: synthesis prompt carries the Pass 4 contract

`prompts/matrix_synthesis.md` carries a Pass 4 section that names
the three lens cells the editor reads (`systems_map`,
`transferable_principle`, `falsification_test`) and the
synthesis-time `adoption_ladder` (four sub-fields:
`minimum_viable`, `mid_adoption`, `full_adoption`,
`monitoring_signals`). The prompt records the non-negotiable rule
that a Top Signal missing any of the four fields demotes to
Archive notes.

Acceptance:

- `prompts/matrix_synthesis.md` carries a `## Pass 4: systems
  synthesis` section.
- The section names all four fields and records the non-negotiable
  rule.
- The section explains that `adoption_ladder` is a synthesis-time
  construct, not a per-source lens.

### R-MTRX-017: brief template carries the four Top Signal fields

`templates/weekly-brief.md` carries four new placeholders on every
Top Signal (Systems map, Transferable principle, Falsification
test, Adoption ladder) between the existing `Try:` and
`Confidence:` lines. The Adoption ladder placeholder carries four
sub-bullets (Minimum viable, Mid, Full, Monitoring).

Acceptance:

- The template's three Top Signal placeholders each carry the four
  new fields in the same order.
- The Adoption ladder placeholder carries four sub-bullets.
- The voice-notes block at the bottom records the new evidence-spine
  rule (every Top Signal carries all four fields, citing DEC-MTRX-007
  and DEC-CDCP-020).

### R-MTRX-018: AGENTS.md records the four-field non-negotiable

`AGENTS.md` carries an addition to the evidence-spine section
naming the four fields every Top Signal must carry per
DEC-MTRX-007 and DEC-CDCP-020. The three-pass note section
extends to name Pass 4 explicitly with the three lens ids and the
adoption-ladder construct.

Acceptance:

- `AGENTS.md` carries a paragraph under the evidence-spine section
  listing the four fields (`systems_map`,
  `transferable_principle`, `falsification_test`,
  `adoption_ladder`) and the demotion rule.
- The three-pass note section carries a fourth bullet for Pass 4
  with the three lens ids and the owning role.
- The DEC reference (DEC-MTRX-007 + DEC-CDCP-020) appears inline.
