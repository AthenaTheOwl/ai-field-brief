---
id: DEC-MTRX-009-matrix-cell-vocabulary-normalization
spec: specs/0012-prompt-matrix-plane/
requirement: R-MTRX-019
date: 2026-09-04
status: approved
reversible: true
decision: |
  Normalize the enum vocabulary in every `briefs/*/matrix/*.yaml` to match
  `schemas/matrix_cell.schema.json`, and add
  `scripts/validate_matrix_cells.py` to hold it. The mapping is fixed:
  `mode` values `pattern` and `insight` become `interpretive`, `risk`
  becomes `critique`, `thesis` and `horizon_scan` become `synthetic`;
  `ref_type` values `paraphrase` and `link` become `url`; and `status`
  value `candidate` becomes `created`. 172 substitutions across eight
  issues, 2026-W24 through 2026-W34.
alternatives:
  - label: widen the schema enums to admit the drifted vocabulary
    rejected_because: |
      The drifted values are a mix of extraction modes and content
      categories. `pattern`, `insight`, and `thesis` describe what a cell
      says; `extractive`, `interpretive`, and `synthetic` describe how it
      was produced. Admitting both collapses two axes into one field and
      makes the enum useless for filtering. The right home for a content
      category is `lens_id`, which already carries one.
  - label: leave the archive alone and validate only new briefs
    rejected_because: |
      A schema that eight of seventeen files violate is not a contract.
      Leaving the archive unvalidated also leaves the property tests under
      `tests/property/` running over files whose vocabulary they cannot
      assume, which is how the drift stayed invisible.
  - label: "map the candidate status value to verified"
    rejected_because: |
      Those cells carry `faithfulness_status: passed`, which is the field
      that records the Pass 2 verdict. Writing `verified` into `status` as
      well would assert a lifecycle claim this normalization has not
      checked. `created` is the weakest accurate value and loses nothing,
      because the verification signal already lives in its own field.
rationale: |
  `scripts/validate_schemas.py` checks that schema files parse and declare
  a recognized dialect. Nothing checked the documents those schemas
  describe. The cell vocabulary drifted from 2026-W24 onward and reached
  172 violations across eight published issues, found while authoring
  2026-W35. Every substitution in the mapping is a vocabulary translation
  with no change to cell content, source refs, confidence, or faithfulness
  status, so the audit trail keeps its meaning. The gate is the part that
  matters: without it the vocabulary drifts again the first time an author
  reaches for a word the enum does not carry.
evidence:
  - kind: doc
    ref: scripts/validate_matrix_cells.py
  - kind: doc
    ref: schemas/matrix_cell.schema.json
  - kind: run
    ref: .github/workflows/ci.yml
rollback: |
  `git revert` the normalization commit to restore the drifted vocabulary,
  then delete `scripts/validate_matrix_cells.py` and remove its step from
  `.github/workflows/ci.yml` and the AGENTS.md pre-commit list. Cell
  content is untouched by this change, so a revert loses nothing but the
  vocabulary alignment.
owner: science.cell-verifier
systems_map: |
  A schema constrains documents only where something reads both. With the
  schema checked and the documents unchecked, the schema became
  documentation of an intent, and the archive drifted away from it one
  convenient word at a time.
transferable_principle: |
  Validating the schema is not validating the data. The same gap appears
  wherever a type definition ships without a conformance test over the
  records it describes: API contracts, event payloads, config files.
falsification_test: |
  If an author needs a mode, ref_type, or status value the enum does not
  carry within the next four issues, the vocabulary is too narrow for the
  work, and the schema needs an amendment instead of the briefs needing a
  translation.
adoption_ladder:
  minimum_viable: |
    172 substitutions applied, `validate_matrix_cells` green over 6,184
    cells in 17 files.
  mid_adoption: |
    The gate runs in CI and in the pre-commit list, so a drifted value
    fails before merge.
  full_adoption: |
    Cell vocabulary is queryable across the whole archive, and mode and
    lens distributions per issue become a readable signal about how the
    corpus is produced.
  monitoring_signals:
    - "vocabulary violations caught per pull request"
    - "requests to extend an enum, which indicate the schema is too narrow"
    - "cells per mode per issue, as a check on extraction-versus-synthesis balance"
---

## decision

Normalize the enum vocabulary across `briefs/*/matrix/*.yaml` to match
`schemas/matrix_cell.schema.json` and add `scripts/validate_matrix_cells.py`
to hold it. Mapping: `mode` `pattern` and `insight` to `interpretive`,
`risk` to `critique`, `thesis` and `horizon_scan` to `synthetic`;
`ref_type` `paraphrase` and `link` to `url`; `status` `candidate` to
`created`. 172 substitutions across 2026-W24 through 2026-W34.

## alternatives

- Widen the schema to admit the drifted values: rejected because they mix
  an extraction-mode axis with a content-category axis, and the content
  category already has a home in `lens_id`.
- Validate only new briefs: rejected because a schema violated by eight of
  seventeen files is not a contract.
- Map `candidate` to `verified`: rejected because `faithfulness_status`
  already records the Pass 2 verdict, and `created` is the weakest accurate
  value.

## rationale

`validate_schemas.py` checks schema files, never the documents they
describe, so the cell vocabulary drifted unnoticed from 2026-W24. Every
substitution is a vocabulary translation; cell content, source refs,
confidence, and faithfulness status are untouched.

## evidence

- `scripts/validate_matrix_cells.py` (6,184 cells in 17 files, green)
- `schemas/matrix_cell.schema.json` (the enums being enforced)
- `.github/workflows/ci.yml` (the CI step)
- `specs/0012-prompt-matrix-plane/requirements.md#R-MTRX-019`

## rollback

Revert the normalization commit, delete the gate, and remove its CI step
and pre-commit entry. Cell content is untouched, so a revert loses only the
vocabulary alignment.
