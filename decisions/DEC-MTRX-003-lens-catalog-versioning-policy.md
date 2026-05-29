---
id: DEC-MTRX-003-lens-catalog-versioning-policy
spec: specs/0012-prompt-matrix-plane/
requirement: R-MTRX-004
date: 2026-05-29
status: approved
reversible: true
decision: |
  The lens catalog at `config/prompt_lenses.yaml` is the single
  source of truth for which lenses run on which profile. Every
  catalog entry conforms to `schemas/prompt_lens.schema.json`. A
  new lens lands via a file edit through the engineering
  implementation role: a candidate row in the catalog, a prompt
  file under `prompts/lenses/<id>.md`, and a schema entry
  reference. The `science.lens-designer` role validates the
  catalog at run time and refuses a selection that pulls an absent
  lens. Optional lenses (`required: false`) can carry an optional
  `profile_guard: <name>` field; the lens runs only when the
  profile opts into that guard.
alternatives:
  - label: let the lens designer write to the catalog directly
    rejected_because: |
      The lens designer is a read-only role per its role.yaml. A
      writable designer would conflate selection (which lenses
      this run uses) with curation (which lenses the catalog
      lists). The selection-vs-curation split mirrors the
      product.spec-writer vs engineering.implementation split.
  - label: version each lens with a semver tag in its id
    rejected_because: |
      Premature. The catalog ships ten lenses today; lens churn
      is low. The catalog's `version` field on each entry covers
      monotonic version-tracking; semver-per-lens lands when a
      breaking change to a lens output schema needs both shapes
      to coexist.
  - label: split the catalog by profile (one yaml per profile)
    rejected_because: |
      The current profile set (`weekly-brief` plus the future
      `creative_os`) is small enough that the single catalog plus
      a `profile_guard` field per entry is simpler than N catalog
      files. Splitting becomes worth it once a profile shares no
      lenses with the others.
rationale: |
  The catalog is the join key between the profile (what kind of
  brief is being written) and the cells the run produces (what
  lenses fan out across the source set). Keeping it in one file
  lets the lens designer validate the whole set on every run and
  catch a missing prompt or schema before any cell write. The
  `profile_guard` field gives a typed way for an optional lens
  (Creative OS impact, governance surface, watchlist trigger) to
  declare which profile pulls it; the workflow checks the guard
  per profile instead of hard-coding the lens set per profile.
evidence:
  - kind: doc
    ref: config/prompt_lenses.yaml
  - kind: doc
    ref: schemas/prompt_lens.schema.json
  - kind: doc
    ref: .agents/roles/science.lens-designer/instructions.md
  - kind: doc
    ref: prompts/lenses/creative_os_impact.md
rollback: |
  Collapse the catalog into per-profile YAML files (one per brief
  profile) and drop the `profile_guard` field. The lens prompts
  under `prompts/lenses/` stay; the schema stays. The lens
  designer role rewrites its run-time selection to read the
  per-profile file instead of the merged catalog.
owner: science.lens-designer
---

## decision

The lens catalog at `config/prompt_lenses.yaml` is the single
source of truth for which lenses run on which profile. New lenses
land via a file edit through the engineering implementation role;
the lens designer role validates the catalog at run time but does
not write to it. Optional lenses can carry a `profile_guard`
field; the lens runs only when the profile opts into that guard.

## alternatives

- Let the lens designer write to the catalog directly. Rejected
  because the designer is a read-only role and conflating
  selection with curation breaks the same split the spec-writer /
  implementation roles model.
- Version each lens with a semver tag in its id. Rejected as
  premature; the catalog's `version` field on each entry covers
  monotonic version-tracking and lens churn is low.
- Split the catalog by profile. Rejected because the current
  profile set is small and a single catalog plus `profile_guard`
  is simpler than N catalog files.

## rationale

The catalog is the join key between the profile and the cells
the run produces. Keeping it in one file lets the lens designer
validate the whole set on every run and catch a missing prompt
or schema before any cell write. The `profile_guard` field gives
a typed way for an optional lens to declare which profile pulls
it.

## evidence

- `config/prompt_lenses.yaml` carries the ten installed lenses
  plus the schema reference and the `profile_guard` example on
  `creative_os_impact`.
- `schemas/prompt_lens.schema.json` is the typed shape every
  catalog row conforms to.
- The lens designer role's instructions name the validation pass
  it runs at selection time.

## rollback

Collapse the catalog into per-profile YAML files. The lens
prompts and schema stay; the lens designer's run-time selection
rewrites to read the per-profile file instead of the merged
catalog.
