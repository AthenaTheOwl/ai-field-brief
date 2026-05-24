---
id: DEC-CDCP-003-dreams-validated-against-dream-output-schema
spec: specs/0010-cognitive-delivery-control-plane/
requirement: R-CDCP-003
date: 2026-05-24
status: approved
reversible: true
decision: |
  Dream-job outputs at dreams/<week>/output.json parse against the
  cross-repo dream-output.schema.json from athena-site. A future
  scripts/validate_dreams.py gate lands alongside the first machine-
  readable dream output; today the contract is reserved by
  dreams/README.md and the run-weekly-dream playbook.
alternatives:
  - label: free-form dream report only (no JSON output)
    rejected_because: |
      A free-form report cannot be audited at scale. The candidates
      surfaced by the dream job (memory updates, generated tests,
      SKILL patches) need a machine-readable shape so the human
      reviewer can route them per-kind. The cross-repo schema names
      that shape.
  - label: define a local dream output schema
    rejected_because: |
      The dream job runs in every repo on the operating model;
      keeping one schema in athena-site avoids drift. This repo
      caches a copy under ops/schemas-cache/ for offline runs.
  - label: hold the contract until the first output lands
    rejected_because: |
      The contract shapes the dream pass; the orchestrator already
      writes candidates with the schema-defined fields
      (human_review_required, kind, mode, summary). Reserving the
      contract now keeps the candidate writer honest.
rationale: |
  The dream job produces multi-kind output: memory updates, backlog
  items, generated tests, skill patches, prompt patches, config
  patches. Each kind routes to a different role for promotion. A
  shared schema across the kinds gives the router a uniform read.

  Every candidate carries `human_review_required: true` per the
  schema default. The flag is structural; the dream orchestrator
  cannot file a candidate without it. The
  candidates-human-gated rule (R-CDCP-009) reads the flag.
evidence:
  - kind: spec
    ref: specs/0010-cognitive-delivery-control-plane/requirements.md
  - kind: doc
    ref: dreams/README.md
  - kind: doc
    ref: ../athena-site/ops/schemas/dream-output.schema.json
  - kind: doc
    ref: ops/schemas-cache/dream-output.schema.json
  - kind: run
    ref: dreams/2026-W21/report.md
rollback: |
  Drop the schema reference from dreams/README.md. The free-form
  weekly dream report still lands under dreams/YYYY-WNN/report.md;
  the only loss is the per-candidate machine-readable shape. No data
  loss; existing candidates survive untouched.
owner: editorial
---

## decision

Dream-job outputs at `dreams/<week>/output.json` parse against the
cross-repo `dream-output.schema.json`. A future
`scripts/validate_dreams.py` gate lands with the first machine-
readable dream output; today the contract is reserved by
`dreams/README.md` and the weekly-dream playbook.

## alternatives

- Free-form report only — cannot be audited at scale.
- Define a local schema — drifts from the cross-repo source.
- Hold the contract until the first output lands — the contract
  shapes the pass; reserving it now keeps the writer honest.

## rationale

The dream job produces multi-kind output (memory updates, backlog
items, generated tests, skill patches, prompt patches, config
patches). Each kind routes to a different role. A shared schema
gives the router a uniform read. Every candidate carries
`human_review_required: true` per the schema default; the
candidates-human-gated rule (R-CDCP-009) reads the flag.

## evidence

- `specs/0010-cognitive-delivery-control-plane/requirements.md` —
  R-CDCP-003 acceptance.
- `dreams/README.md` — documents the eight dream modes and the
  human-gate rule.
- `../athena-site/ops/schemas/dream-output.schema.json` — the
  source of truth.
- `ops/schemas-cache/dream-output.schema.json` — the offline cache.
- `dreams/2026-W21/report.md` — first weekly dream run; six
  candidates filed with the schema-defined fields.

## rollback

Drop the schema reference from `dreams/README.md`. Free-form weekly
reports still land. No data loss.
