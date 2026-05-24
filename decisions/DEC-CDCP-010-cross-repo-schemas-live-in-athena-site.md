---
id: DEC-CDCP-010-cross-repo-schemas-live-in-athena-site
spec: specs/0010-cognitive-delivery-control-plane/
requirement: R-CDCP-010
date: 2026-05-24
status: approved
reversible: true
decision: |
  Every CDCP artifact contract (decision.schema.json,
  dream-output.schema.json, role.schema.json, tool.schema.json,
  policy.schema.json, skill.schema.json, event.schema.json,
  state-machine.schema.json, workflow.schema.json, artifact.schema.json)
  lives in athena-site/ops/schemas/ as the source of truth. This
  repo holds a cached copy under ops/schemas-cache/ for offline CI
  runs; the cache is documented as a cache, not as a source. New
  schema fields land in athena-site first; this repo follows.
alternatives:
  - label: copy schemas into every consuming repo
    rejected_because: |
      N copies drift in N directions. The DEC schema landed an
      offline-cache env-var override after the first ten DECs were
      written; with copies, the override would need ten updates. One
      source means one update.
  - label: pin schemas to a versioned release in athena-site
    rejected_because: |
      Premature. The schemas are still settling; pinning costs more
      than the version drift gains. When the schemas stabilize, a
      future DEC can add the pin.
  - label: define schemas in this repo and reference them from athena-site
    rejected_because: |
      This repo is one of multiple consumers. Putting the source in
      a consumer makes the cross-repo dependency point inward; it
      should point at the shared layer. Athena-site is the shared
      layer.
rationale: |
  The cross-repo schemas are the lingua franca: every repo on the
  operating model parses the same artifacts against the same shapes.
  A drift in one repo is a drift in the contract. Pointing every
  validator at the same URL keeps the contract centralized.

  The cache pattern lets CI runs work without a network call (a
  GitHub Actions runner can fetch the schema, but a contributor
  running gates on a plane cannot). The env-var override on the
  schema URL makes the cache path testable end-to-end (promoted
  from eval-002 in the 2026-W21 dream pass).
evidence:
  - kind: spec
    ref: specs/0010-cognitive-delivery-control-plane/requirements.md
  - kind: doc
    ref: ops/schemas-cache/
  - kind: doc
    ref: scripts/validate_decisions.py
  - kind: doc
    ref: scripts/validate_roles.py
  - kind: doc
    ref: ../athena-site/ops/schemas/
  - kind: run
    ref: tests/scripts/test_validate_decisions_offline.py
rollback: |
  Copy the schemas from athena-site into ops/schemas/ in this repo
  and rewrite the validators to read the local path. The cache
  directory under ops/schemas-cache/ becomes the source. Cross-repo
  drift returns; no data loss. Reverting back to the centralized
  source is a path edit in each validator.
owner: editorial
---

## decision

Every CDCP artifact contract lives in `athena-site/ops/schemas/` as
the source of truth. This repo holds a cached copy under
`ops/schemas-cache/` for offline CI runs. New schema fields land
in athena-site first; this repo follows.

## alternatives

- Copy schemas into every consuming repo — N copies drift in N
  directions.
- Pin to a versioned release — premature; schemas are still
  settling.
- Define schemas here and reference from athena-site — puts the
  source in a consumer.

## rationale

The cross-repo schemas are the lingua franca: every repo on the
operating model parses the same artifacts against the same shapes.
Pointing every validator at the same URL centralizes the contract.
The cache pattern lets CI runs work without a network call; the
env-var override on the URL makes the cache path testable end-to-end
(promoted from eval-002 in the 2026-W21 dream pass).

## evidence

- `specs/0010-cognitive-delivery-control-plane/requirements.md` —
  R-CDCP-010 acceptance.
- `ops/schemas-cache/` — the offline cache directory with six
  cached schemas.
- `scripts/validate_decisions.py`, `scripts/validate_roles.py` —
  validators that fetch from the URL with cache fallback.
- `../athena-site/ops/schemas/` — the source of truth.
- `tests/scripts/test_validate_decisions_offline.py` — the offline
  path regression test.

## rollback

Copy the schemas into `ops/schemas/` and rewrite the validators to
read the local path. The cache directory becomes the source.
Cross-repo drift returns; no data loss.
