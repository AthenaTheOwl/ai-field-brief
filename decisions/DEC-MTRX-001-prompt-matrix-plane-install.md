---
id: DEC-MTRX-001-prompt-matrix-plane-install
spec: specs/0012-prompt-matrix-plane/
requirement: R-MTRX-001
date: 2026-05-29
status: approved
reversible: true
decision: |
  ai-field-brief installs the prompt matrix plane: four schemas
  (matrix_cell, matrix_run, prompt_lens, lens_output), ten lens
  prompts, two synthesis prompts, four science roles
  (lens-designer, matrix-runner, cell-verifier,
  matrix-synthesis-editor), one workflow, two design docs, ten
  catalog entries, and one staged DB migration. Briefs ship from
  verified matrix cells, not from raw source notes. The
  evidence-spine rule lands in `.agents/AGENTS.md` as
  non-negotiable: no digest claim ships unless it traces to one or
  more verified cells; no cell counts as verified unless it carries
  source refs; no action candidate gets promoted unless it carries
  the six required fields.
alternatives:
  - label: ship the matrix as advisory only
    rejected_because: |
      The matrix plane only earns its weight if the digest cannot
      route around it. Advisory cells produce a second-class
      artifact the brief author can ignore; the rule is what makes
      the cell the join key between source and digest.
  - label: skip the matrix; double down on per-pick faithfulness audits
    rejected_because: |
      Per-pick audits caught overstatement (DEC-PUB-004) but ran
      against the assembled brief, not the source-to-claim mapping.
      The matrix gives a finer-grained unit of audit and lets
      multiple picks share one verified cell.
  - label: land the matrix plane as a multi-repo schema in athena-site
    rejected_because: |
      Premature. The matrix plane runs in one repo today
      (ai-field-brief); cross-repo schema graduation per
      DEC-CDCP-010 happens once a second repo emits the same shape.
      Schemas live under `schemas/` here; an athena-site move lands
      via a new DEC when another repo joins.
rationale: |
  Three published briefs in, the most reliable failure mode is a
  digest claim that drifts away from its source. The per-pick
  faithfulness audit (DEC-PUB-004) caught some of these but ran
  against the assembled brief, not the source-to-claim mapping.
  The matrix plane moves the audit one layer down: each
  source-lens pair produces one cell with source refs; each cell
  passes through a verifier before any synthesis reads it; the
  synthesis editor refuses to cite a non-verified cell. The
  digest becomes a function of verified cells, not raw model
  prose. The four roles map the work cleanly to the
  proof-gate-runner shape already in use: read the artifact, run
  the check, write a verdict with a root cause on every non-pass.
evidence:
  - kind: doc
    ref: docs/MATRIX_PLANE_DESIGN.md
  - kind: doc
    ref: docs/UI_SPEC_PROMPT_MATRIX.md
  - kind: spec
    ref: specs/0012-prompt-matrix-plane/
  - kind: decision
    ref: decisions/DEC-PUB-004-faithfulness-audit-before-publish.md
  - kind: decision
    ref: decisions/DEC-CDCP-010-cross-repo-schemas-live-in-athena-site.md
rollback: |
  Remove the four schemas under `schemas/`, the ten lens prompts
  under `prompts/lenses/`, the two synthesis prompts under
  `prompts/`, the four role directories under `.agents/roles/`, the
  workflow under `.agents/workflows/matrix-analysis-loop.yaml`, the
  two docs under `docs/`, the lens catalog at
  `config/prompt_lenses.yaml`, and the staged migration at
  `packages/db/migrations/staged/`. Remove the evidence-spine
  section from `.agents/AGENTS.md` and the four matrix steps
  (4-6 plus the per-cell audit framing in step 8) from the
  playbook. Drop spec 0012 and the MTRX prefix from
  `scripts/spec_check.py`. Future briefs revert to the per-pick
  audit shape published briefs already follow.
owner: science.proof-gate-runner
---

## decision

ai-field-brief installs the prompt matrix plane. Briefs ship from
verified matrix cells, not from raw source notes. The evidence-spine
rule lands in `.agents/AGENTS.md` as non-negotiable: no digest claim
ships unless it traces to one or more verified cells; no cell counts
as verified unless it carries source refs; no action candidate gets
promoted unless it carries the six required fields (source support,
action surface, test plan, expected benefit, risk, disposition).

## alternatives

- Ship the matrix as advisory only. Rejected because an advisory
  matrix produces a second-class artifact the brief author can
  ignore; the rule is what makes the cell the join key between
  source and digest.
- Skip the matrix and double down on per-pick faithfulness audits.
  Rejected because per-pick audits ran against the assembled brief,
  not the source-to-claim mapping; the matrix gives a finer-grained
  unit of audit and lets multiple picks share one verified cell.
- Land the matrix plane as a cross-repo schema under athena-site.
  Rejected as premature; the matrix plane runs in one repo today
  and cross-repo schema graduation per DEC-CDCP-010 waits until a
  second repo emits the same shape.

## rationale

Three published briefs in, the most reliable failure mode is a
digest claim that drifts away from its source. The matrix plane
moves the audit one layer down: each source-lens pair produces one
cell with source refs; each cell passes through a verifier before
any synthesis reads it; the synthesis editor refuses to cite a
non-verified cell. The digest becomes a function of verified cells,
not raw model prose.

## evidence

- `docs/MATRIX_PLANE_DESIGN.md` carries the shape and the
  per-domain row/column tables.
- `docs/UI_SPEC_PROMPT_MATRIX.md` carries the UI surface for a
  later product pass.
- `specs/0012-prompt-matrix-plane/` carries R-MTRX-001..006 with
  acceptance per requirement.
- `decisions/DEC-PUB-004-faithfulness-audit-before-publish.md` is
  the per-pick audit this DEC supersedes for cells (the per-pick
  read survives as the brief-author's final pass in playbook step
  8).
- `decisions/DEC-CDCP-010-cross-repo-schemas-live-in-athena-site.md`
  is the cross-repo schema rule that scoped this install to
  repo-local `schemas/`.

## rollback

Remove the schemas, prompts, roles, workflow, docs, catalog, and
staged migration shipped under this DEC. Remove the evidence-spine
section from `.agents/AGENTS.md` and the four matrix steps from the
playbook. Drop spec 0012 and the MTRX prefix from
`scripts/spec_check.py`. Future briefs revert to the per-pick audit
shape published briefs already follow.
