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

## R-MTRX-007: scoring model gates digest promotion

- `python -c "import yaml; yaml.safe_load(open('config/scoring_model.yaml', encoding='utf-8'))"`
  parses without error and the parsed document carries `axes`
  with `source_quality`, `profile_relevance`, and `actionability`
  keys plus a `penalties` block with `hype_penalty`,
  `duplicate_penalty`, `source_staleness_penalty`, and
  `weak_evidence_penalty` keys.
- The `thresholds` block names `include_in_digest.min: 12`,
  `watchlist.min: 9` with `max: 11.999`, and `archive.max: 8.999`.
- An action candidate emitted by the synthesis editor without a
  `final_score` entry fails the brief-author review pass.

## R-MTRX-008: profiles config pins every MatrixRun to a profile id

- `config/profiles.yaml` parses as YAML and the `profiles` map
  carries the `personal` and `broad_builder` keys with non-empty
  `interests` and `negative_preferences` lists.
- A MatrixRun with no `profile_id` is rejected by
  `schemas/matrix_run.schema.json` before any Pass 3 synthesis
  reads it.
- The MatrixRun's `profile_id` value resolves against the
  `profiles` map; an unknown id fails the run schema check.

## R-MTRX-009: action-surface taxonomy is canonical and bounded

- `config/action_surface_taxonomy.yaml` parses as YAML and the
  `surfaces` list carries exactly 14 entries with the canonical
  ids (`prompt`, `config`, `eval`, `workflow`, `agent-role`,
  `tool-policy`, `runtime-adapter`, `source-registry`,
  `architecture`, `experiment`, `watchlist`, `creative-os`,
  `software-control-plane`, `personal-knowledge-base`).
- An action candidate whose `surface` does not match an id in the
  list is rejected by the brief-author review pass.
- `AGENTS.md` carries the extension rule (new surface requires a
  new DEC plus a bump to the YAML).

## R-MTRX-010: three-pass note system names the lens-to-role map

- `AGENTS.md` carries a `## Three-pass note system` section that
  names Pass 1, Pass 2, and Pass 3 explicitly with the lens ids
  and the owning role for each.
- The pass-to-lens map matches the entries under
  `config/prompt_lenses.yaml` (every cited lens id exists in the
  catalog).
- `playbook/run-weekly-brief.md` steps 4, 5, and 6 carry the same
  pass labels and reference the same lens ids and roles.

## R-MTRX-011: evidence-spine rules enforce the chain end-to-end

- `AGENTS.md` carries a `## AI Brief OS — evidence-spine rules`
  section at the top of the file.
- The rules name the three configuration files
  (`config/scoring_model.yaml`, `config/profiles.yaml`,
  `config/action_surface_taxonomy.yaml`) as the configuration
  surfaces the chain reads.
- The rules list the six required fields for any promoted action
  candidate (source support, action surface, test plan, expected
  benefit, risk, disposition).

## R-MTRX-012: brief template carries the Brief OS section shape

- `templates/weekly-brief.md` carries the seven Brief OS sections
  (Field thesis, Top signals, Reusable patterns, Action queue,
  Watchlist, Archive notes, Sources reviewed) plus a Closing
  thought block.
- Every Top signal placeholder carries the
  Source/Payload/Mechanism/Why it matters/Reusable
  pattern/Action surface/Try/Confidence/Evidence shape.
- The template's voice-notes block lists the 14 canonical action
  surfaces inline so an author cannot drift from
  `config/action_surface_taxonomy.yaml`.

## R-MTRX-013: playbook references the Brief OS configurations

- `playbook/run-weekly-brief.md` Inputs section names
  `config/scoring_model.yaml`, `config/profiles.yaml`, and
  `config/action_surface_taxonomy.yaml` alongside the matrix
  schemas and prompts.
- Step 6 (Pass 3) cites the score thresholds inline
  (`>= 12` Top signals, `[9, 12)` Watchlist, `< 9` Archive).
- Step 6 names the action-surface lookup against
  `config/action_surface_taxonomy.yaml` and the six required
  action-candidate fields.

## R-MTRX-014: MatrixRun records its profile_id

- `schemas/matrix_run.schema.json` declares `profile_id` as a
  required field and rejects a run without one.
- The brief author can read the `profile_id` from the MatrixRun
  artifact under the run folder and from the matching Run record
  under `ops/run-records/`.
- The replay CLI reads the recorded `profile_id` and resolves it
  against `config/profiles.yaml` at the recorded SHA so the
  profile configuration that drove promotion is reproducible.

## R-MTRX-015: Pass 4 lens catalog carries the three systems lenses

- `python -c "import yaml; d=yaml.safe_load(open('config/prompt_lenses.yaml', encoding='utf-8')); ids={l['id'] for l in d['lenses']}; assert {'systems_thinking','transferable_principle','falsification_test'} <= ids"`
  parses without error.
- The three prompt files (`prompts/lenses/systems_thinking.md`,
  `prompts/lenses/transferable_principle.md`,
  `prompts/lenses/falsification_test.md`) exist on disk.
- Each entry's `mode` matches the prompt header
  (`interpretive`, `synthetic`, `critique`).

## R-MTRX-016: synthesis prompt carries the Pass 4 contract

- `prompts/matrix_synthesis.md` carries a `## Pass 4: systems
  synthesis` section.
- The section names all four fields (`systems_map`,
  `transferable_principle`, `falsification_test`,
  `adoption_ladder`) and records the non-negotiable rule.
- The section names the four `adoption_ladder` sub-fields
  (`minimum_viable`, `mid_adoption`, `full_adoption`,
  `monitoring_signals`).

## R-MTRX-017: brief template carries the four Top Signal fields

- Each of the three Top Signal placeholders in
  `templates/weekly-brief.md` carries the four new fields
  (`Systems map`, `Transferable principle`, `Falsification test`,
  `Adoption ladder`) between `Try:` and `Confidence:`.
- The `Adoption ladder` placeholder carries four sub-bullets
  (`Minimum viable`, `Mid`, `Full`, `Monitoring`).
- The voice-notes block records the four-field rule and cites
  DEC-MTRX-007 and DEC-CDCP-020.

## R-MTRX-018: AGENTS.md records the four-field non-negotiable

- `AGENTS.md` carries a paragraph under the evidence-spine section
  naming the four fields and the demotion-to-Archive rule.
- The three-pass note section carries a Pass 4 bullet with the
  three lens ids and `science.matrix-synthesis-editor` as the
  owning role.
- The DEC references (`DEC-MTRX-007`, `DEC-CDCP-020`) appear
  inline in the evidence-spine section.
