---
id: DEC-MTRX-002-four-science-roles-for-matrix-plane
spec: specs/0012-prompt-matrix-plane/
requirement: R-MTRX-002
date: 2026-05-29
status: approved
reversible: true
decision: |
  The matrix plane ships four new roles under the science guild:
  `science.lens-designer`, `science.matrix-runner`,
  `science.cell-verifier`, and `science.matrix-synthesis-editor`.
  Each role directory carries the standard five-file set
  (role.yaml, instructions.md, tools.yaml, output.schema.json,
  gates.yaml) matching the science.proof-gate-runner shape. The
  Phase 1 plan named the four roles under a new `analysis` guild;
  this DEC records the adaptation to `science` because the
  cross-repo `role.schema.json` guild enum (control, product,
  research, design, engineering, science, security, operations,
  domain, learning, documentation, commercial) does not include
  `analysis` and per DEC-CDCP-010 cross-repo schemas live in
  athena-site.
alternatives:
  - label: ship the roles under a new `analysis` guild
    rejected_because: |
      The cross-repo `role.schema.json` enum does not include
      `analysis`. Extending the enum requires an athena-site PR
      plus a new cross-repo DEC and a schema-cache sync round.
      Out of scope for this install pass.
  - label: ship the four roles under the `domain` guild
    rejected_because: |
      The `domain` guild is reserved for subject-matter and
      editorial roles. Cell verification and matrix synthesis are
      evidence-grounded verification work, which is the science
      guild's charter.
  - label: collapse the four roles into one mega-role
    rejected_because: |
      One role for lens design, cell production, verification, and
      synthesis breaks the same separation-of-concerns rule the
      proof-gate-runner / implementation / reviewer split keeps.
      The matrix runner produces cells; the verifier checks them;
      the synthesis editor reads only verified output. Collapsing
      removes the audit boundary.
rationale: |
  The four-role split mirrors the existing
  proof-gate-runner / implementation / code-reviewer pattern:
  one role produces, one role checks, one role synthesizes.
  Keeping the four roles under `science` reuses the existing guild
  semantics (the guild that owns proof gates and evidence
  verification) and avoids a cross-repo schema change. The roles
  land with read-only permissions and a single tool
  (`repo.read`); the model call shares the brief workflow's
  harness today and graduates to a dedicated `model.call` tool
  entry in a follow-up DEC.
evidence:
  - kind: doc
    ref: .agents/roles/science.lens-designer/role.yaml
  - kind: doc
    ref: .agents/roles/science.matrix-runner/role.yaml
  - kind: doc
    ref: .agents/roles/science.cell-verifier/role.yaml
  - kind: doc
    ref: .agents/roles/science.matrix-synthesis-editor/role.yaml
  - kind: doc
    ref: .agents/roles/science.proof-gate-runner/role.yaml
  - kind: decision
    ref: decisions/DEC-CDCP-010-cross-repo-schemas-live-in-athena-site.md
rollback: |
  Remove the four role directories under
  `.agents/roles/science.lens-designer/`,
  `.agents/roles/science.matrix-runner/`,
  `.agents/roles/science.cell-verifier/`, and
  `.agents/roles/science.matrix-synthesis-editor/`. Drop the four
  role ids from the `repo.read` tool's `allowed_roles` list under
  `.agents/tools.yaml`. Drop the matrix-plane workflow at
  `.agents/workflows/matrix-analysis-loop.yaml`. Drop the
  CATALOG.md `Installed` block update.
owner: science.proof-gate-runner
---

## decision

The matrix plane ships four new roles under the science guild:
`science.lens-designer`, `science.matrix-runner`,
`science.cell-verifier`, and `science.matrix-synthesis-editor`.
Each role carries the standard five-file set matching the
proof-gate-runner shape. The plan's `analysis` guild label adapts
to `science` because the cross-repo role.schema.json guild enum
does not include `analysis`.

## alternatives

- Ship under a new `analysis` guild. Rejected because the
  cross-repo schema enum does not include `analysis`; extending
  the enum requires an athena-site PR plus a new cross-repo DEC.
- Ship under the `domain` guild. Rejected because `domain` is
  reserved for subject-matter and editorial roles; cell
  verification and matrix synthesis are evidence-grounded
  verification work, which the science guild owns.
- Collapse the four roles into one mega-role. Rejected because
  one role for production + verification + synthesis breaks the
  same audit boundary the proof-gate-runner / implementation /
  reviewer split keeps.

## rationale

The four-role split mirrors the existing produce-check-synthesize
shape the proof-gate-runner / implementation / code-reviewer
roles already model. Keeping the four roles under `science`
reuses the guild's evidence-verification semantics and avoids a
cross-repo schema change.

## evidence

- The four role.yaml files under `.agents/roles/science.*/`.
- The science.proof-gate-runner role under
  `.agents/roles/science.proof-gate-runner/` as the shape source.
- DEC-CDCP-010 as the cross-repo schema rule that scoped the
  guild choice.

## rollback

Remove the four role directories, drop the four role ids from
`repo.read`'s `allowed_roles`, drop the workflow file, and revert
the CATALOG.md `Installed` block.
