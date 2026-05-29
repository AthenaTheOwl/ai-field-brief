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
