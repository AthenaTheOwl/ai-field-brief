---
id: DEC-CDCP-001-install-cdcp-governance
spec: specs/0010-cognitive-delivery-control-plane/
requirement: R-CDCP-001
date: 2026-05-22
status: approved
reversible: true
decision: |
  Install the Cognitive Delivery Control Plane governance scaffold in
  this repo: .agents/, decisions/, dreams/, ops/RELEASE_LEDGER,
  ops/RESET_LEDGER, plus executable enforcement via
  scripts/validate_decisions.py and an extended scripts/spec_check.py
  that flags any R-* requirement without a DEC reference.
alternatives:
  - label: spec-only discipline
    rejected_because: |
      Specs alone name the what; they record no audit trail for why a
      path was chosen over alternatives. Phase 1 shipped fourteen
      requirements without one DEC; that gap is the load-bearing
      argument for adding the decisions ledger.
  - label: adopt a full framework stack (LangGraph, CrewAI, Strands)
    rejected_because: |
      Frameworks turn over every six months. The records (specs,
      decisions, traces, ledgers, tests, evals, deployment evidence)
      survive the framework. Adopting a framework now buys lock-in and
      changes no behavior the gates check.
  - label: build a 12-screen control-plane SaaS
    rejected_because: |
      Premature. Markdown ledgers plus executable gates cover the
      audit-trail and human-review needs at current artifact volume.
      A UI layer over the ledgers lands when volume warrants it; not
      now.
rationale: |
  The CDCP framing came out of a synthesis pass across athena-site and
  ai-field-brief. Specs were already gated. Decisions were not. The
  weekly brief work showed an offline-cognition shape worth naming
  (the dream job). The cross-repo schemas under athena-site/ops/schemas/
  just landed, so this repo points at them and avoids duplication.

  Installing the scaffold now (instead of waiting until artifact
  volume forces it) keeps the records consistent from the start.
  Backfilling later means the early commits get no DEC and the trail
  has a gap. Installing now also turns the discipline into executable
  gates: validate_decisions and the extended spec_check fail builds
  when records drift out of shape.
evidence:
  - kind: spec
    ref: specs/0010-cognitive-delivery-control-plane/
  - kind: doc
    ref: ../athena-site/ops/control-plane.md
  - kind: doc
    ref: ../athena-site/ops/schemas/decision.schema.json
  - kind: doc
    ref: ../athena-site/ops/schemas/dream-output.schema.json
  - kind: doc
    ref: ../athena-site/ops/schemas/skill.schema.json
rollback: |
  Delete this commit. The added directories (.agents/, decisions/,
  dreams/, ops/, control-plane/, specs/0010-*/) and the new script
  scripts/validate_decisions.py can be removed wholesale. The existing
  spec_check.py still works against the prior shape after the CDCP
  prefix line and the requirement-coverage rule are removed. No data
  loss: the cross-repo schemas remain in athena-site, and the backfill
  DECs (DEC-FND-001, DEC-FND-007) record information that was
  previously only implicit in the Phase 1 spec.
owner: editorial
---

## decision

Install the Cognitive Delivery Control Plane governance scaffold in
ai-field-brief and make it executable. The scaffold adds
`.agents/AGENTS.md`, a `decisions/` directory with backfilled DECs,
a `dreams/` directory with the README and contract reservation, an
`ops/` directory with the two ledgers, a `control-plane/workflows/`
declarative workflow, and the gate script
`scripts/validate_decisions.py`. The existing `scripts/spec_check.py`
gains a new rule that flags any R-* requirement without a DEC
reference.

## alternatives

- Spec-only discipline — already in place; records no audit trail
  for decisions.
- Framework stack (LangGraph, CrewAI, Strands) — framework soup; does
  not change behavior the gates check.
- 12-screen control-plane SaaS — premature; markdown ledgers cover
  the audit-trail need at current artifact volume.

## rationale

The synthesis from the prior turn lands here. Specs were already
gated. Decisions were not. The weekly brief work showed an
offline-cognition shape (the dream job) worth naming. The cross-repo
schemas just landed in athena-site, so this repo points at them and
skips duplication. Installing the scaffold now keeps the records consistent
from the start and turns the discipline into executable gates.

## evidence

- `specs/0010-cognitive-delivery-control-plane/` — the spec ledger
  this DEC resolves.
- `../athena-site/ops/control-plane.md` — the cross-repo charter that
  names the six artifact types.
- `../athena-site/ops/schemas/decision.schema.json` — the contract
  this DEC parses against.

## rollback

Delete this commit. Remove the added directories wholesale. Remove
the CDCP prefix and the requirement-coverage rule from
`scripts/spec_check.py`. The existing four python gates still work
against the prior shape. No data loss: the cross-repo schemas remain
in athena-site, and the two backfill DECs (DEC-FND-001, DEC-FND-007)
record information that was previously implicit in the Phase 1 spec.
