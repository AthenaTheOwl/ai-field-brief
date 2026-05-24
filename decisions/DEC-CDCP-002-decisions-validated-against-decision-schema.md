---
id: DEC-CDCP-002-decisions-validated-against-decision-schema
spec: specs/0010-cognitive-delivery-control-plane/
requirement: R-CDCP-002
date: 2026-05-24
status: approved
reversible: true
decision: |
  Every decisions/DEC-*.md file parses against the cross-repo
  decision.schema.json sourced from athena-site. The
  scripts/validate_decisions.py gate fetches the schema by URL on
  every run, with a local cache fallback at
  ops/schemas-cache/decision.schema.json so the script runs offline.
alternatives:
  - label: hand-rolled DEC structure check
    rejected_because: |
      A hand-rolled check drifts from the cross-repo contract over
      time. The schema lives in athena-site; pointing at it keeps
      the contract in one place. A hand-rolled check also lacks the
      type and pattern validation a JSON Schema validator gives.
  - label: copy the schema into this repo
    rejected_because: |
      Two copies of the schema drift independently. The repo holds a
      cache copy for offline runs, but the source of truth lives in
      athena-site per R-CDCP-010.
  - label: skip validation; trust the author
    rejected_because: |
      Phase 1 shipped fourteen requirements with no audit trail
      enforcement; the trust model failed there too. A schema check
      catches a missing rationale field or a malformed evidence
      entry before merge.
rationale: |
  The DEC is the per-requirement audit record. If the shape drifts,
  the audit trail loses load-bearing fields (alternatives missing
  rejection reasons, evidence entries without a kind tag, rollback
  paragraphs absent). The schema check fails the build on any drift.

  The remote-fetch-then-cache pattern keeps the contract centralized
  while letting CI runs work without a network call. The env-var
  override on the schema URL (promoted from eval-002 in the
  2026-W21 dream pass) makes the offline path testable end-to-end.
evidence:
  - kind: spec
    ref: specs/0010-cognitive-delivery-control-plane/requirements.md
  - kind: doc
    ref: scripts/validate_decisions.py
  - kind: doc
    ref: ops/schemas-cache/decision.schema.json
  - kind: doc
    ref: ../athena-site/ops/schemas/decision.schema.json
  - kind: run
    ref: tests/scripts/test_validate_decisions_offline.py
rollback: |
  Delete scripts/validate_decisions.py. Drop the validate_decisions
  step from .github/workflows/ci.yml. Keep the cache file under
  ops/schemas-cache/ as documentation. Existing DEC files survive
  untouched; the only loss is the per-PR schema check.
owner: science
---

## decision

Every DEC file parses against the cross-repo `decision.schema.json`.
`scripts/validate_decisions.py` fetches the schema by URL on every
run, with a local cache at `ops/schemas-cache/decision.schema.json`
for offline runs. The script exits 1 on any violation.

## alternatives

- Hand-rolled DEC structure check — drifts from the cross-repo
  contract; lacks type and pattern validation.
- Copy the schema into this repo — two copies drift independently.
- Skip validation — phase 1 already proved the trust model fails.

## rationale

The DEC is the per-requirement audit record. If the shape drifts,
the audit trail loses load-bearing fields. The schema check fails
the build on any drift. The remote-fetch-then-cache pattern
centralizes the contract while letting CI runs work offline. The
env-var override on the schema URL (promoted from eval-002 in the
2026-W21 dream pass) makes the offline path testable.

## evidence

- `specs/0010-cognitive-delivery-control-plane/requirements.md` —
  R-CDCP-002 acceptance.
- `scripts/validate_decisions.py` — the gate implementation.
- `ops/schemas-cache/decision.schema.json` — the offline cache.
- `../athena-site/ops/schemas/decision.schema.json` — the source of
  truth.
- `tests/scripts/test_validate_decisions_offline.py` — the offline
  path regression test (promoted from eval-002).

## rollback

Delete `scripts/validate_decisions.py`. Drop the step from
`.github/workflows/ci.yml`. Keep the cache file as documentation.
Existing DEC files survive untouched.
