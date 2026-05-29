# tasks: prompt matrix plane

## Install pass (2026-05-29, this commit set)

- [x] Install the four matrix-plane schemas under `schemas/`.
- [x] Install the lens catalog at `config/prompt_lenses.yaml` with
      repo-relative paths.
- [x] Install the lens prompts under `prompts/lenses/`.
- [x] Install `prompts/cell_faithfulness.md` and
      `prompts/matrix_synthesis.md`.
- [x] Install the four science roles under `.agents/roles/`.
- [x] Install the matrix workflow at
      `.agents/workflows/matrix-analysis-loop.yaml`.
- [x] Install the matrix design and UI spec docs under `docs/`.
- [x] Install the example matrix YAMLs under `examples/`.
- [x] Park the DB migration at
      `packages/db/migrations/staged/001_prompt_matrix.sql`.
- [x] Add the evidence-spine rule to `.agents/AGENTS.md`.
- [x] Update the playbook with the matrix steps (4-6) and renumber
      the downstream steps.
- [x] Extend `scripts/spec_check.py` ALLOWED_PREFIXES with `MTRX`.
- [x] File the DEC set: DEC-MTRX-001..005.

## Brief OS refinement pass (2026-05-29, DEC-MTRX-006)

- [x] Land `config/scoring_model.yaml` (axes, penalties,
      thresholds) — R-MTRX-007.
- [x] Land `config/profiles.yaml` with `personal` and
      `broad_builder` profiles — R-MTRX-008.
- [x] Land `config/action_surface_taxonomy.yaml` with 14 canonical
      surfaces — R-MTRX-009.
- [x] Name the three-pass note system in `AGENTS.md` with the
      pass-to-lens-to-role map — R-MTRX-010.
- [x] Land the evidence-spine rules in `AGENTS.md` as a
      non-negotiable section — R-MTRX-011.
- [x] Update `templates/weekly-brief.md` with the Brief OS section
      shape (Field thesis, Top signals, Reusable patterns, Action
      queue, Watchlist, Archive notes, Sources reviewed) —
      R-MTRX-012.
- [x] Update `playbook/run-weekly-brief.md` Inputs and step 6 to
      cite the three configuration files and the score thresholds —
      R-MTRX-013.
- [x] Record `profile_id` on every MatrixRun and Run record so the
      replay CLI re-resolves the configuration at the recorded SHA —
      R-MTRX-014.
- [x] File the DEC: DEC-MTRX-006.

## Systems-thinking upgrade pass (2026-05-29, DEC-MTRX-007)

- [x] Land `prompts/lenses/systems_thinking.md`,
      `prompts/lenses/transferable_principle.md`, and
      `prompts/lenses/falsification_test.md` — R-MTRX-015.
- [x] Extend `config/prompt_lenses.yaml` with the three Pass 4
      lens entries — R-MTRX-015.
- [x] Add the `## Pass 4: systems synthesis` section to
      `prompts/matrix_synthesis.md` with the four-field contract —
      R-MTRX-016.
- [x] Add the four Top Signal fields (Systems map, Transferable
      principle, Falsification test, Adoption ladder) to
      `templates/weekly-brief.md` — R-MTRX-017.
- [x] Extend `AGENTS.md` evidence-spine with the four-field
      non-negotiable and the Pass 4 bullet in the three-pass
      section — R-MTRX-018.
- [x] File the DEC: DEC-MTRX-007.

## Follow-up pass

- [ ] Wire the staged DB migration once the cell store moves off
      file artifacts (R-MTRX-006). Adds the schema-sync test, the
      workspace scoping helper, and the audit-event row.
- [ ] Build the matrix UI surface per `docs/UI_SPEC_PROMPT_MATRIX.md`.
- [ ] Land the source-curator and digest-editor role contracts so
      the workflow stops routing through `control.coordinator` for
      the source-selection and digest-assembly steps.
- [ ] Land profile guards beyond `creative_os_only` so the catalog
      can ship lenses scoped to research, ops, or creative profiles.
- [ ] Build a `model.call` tool entry under `.agents/tools.yaml`
      with budget and rate-limit policies so the matrix runner stops
      sharing the brief workflow's harness.
- [ ] Add per-profile scoring overrides under
      `config/profiles.yaml` once a second profile needs a different
      axis weighting than the personal profile.
- [ ] Add an `actions/` backlog that promotes Pass 3 action
      candidates carrying `disposition: adopt_now` or `prototype`
      into a tracked queue with revisit triggers.
