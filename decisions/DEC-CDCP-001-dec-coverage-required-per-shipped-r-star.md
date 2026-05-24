---
id: DEC-CDCP-001-dec-coverage-required-per-shipped-r-star
spec: specs/0010-cognitive-delivery-control-plane/
requirement: R-CDCP-001
date: 2026-05-24
status: approved
reversible: true
decision: |
  Every shipped R-* requirement must carry at least one
  decisions/DEC-*.md whose front-matter `requirement:` field names
  that ID. The spec_check.py gate walks every R-* defined in any
  specs/NNNN-*/requirements.md and confirms either a matching DEC
  exists or the ID is listed in decisions/.spec-check-allowlist.yaml
  under the `deferred` key.
alternatives:
  - label: trust-the-author DEC discipline
    rejected_because: |
      The phase 1 ledger landed 14 R-FND requirements without a
      single DEC; the trust-the-author model already failed once
      and an executable gate is the only durable enforcement layer.
  - label: DEC per spec instead of per requirement
    rejected_because: |
      A spec covers many R-* IDs with separate trade-offs per
      requirement. One DEC per spec rolls all the alternatives into
      one record and loses the per-requirement audit trail. The
      cross-repo schema models a DEC as the per-requirement record
      for that reason.
  - label: defer DEC coverage until spec 0001 ships
    rejected_because: |
      The longer the gap, the harder the backfill. Installing the
      coverage rule at spec 0010 caught the gap at 14 requirements;
      one more spec would have made the backfill harder.
rationale: |
  Specs name the what. DECs name the why. Without DECs, the audit
  trail for why a path won against alternatives lives only in commit
  messages and PR descriptions, both of which decay. The
  coverage-per-R-* rule keeps the audit trail load-bearing without
  forcing a DEC per spec.

  The allowlist file under decisions/.spec-check-allowlist.yaml
  gives the rule a graceful migration path: legacy R-* IDs land in
  the allowlist with a note; the gate skips them and prints the
  deferred count. New R-* IDs cannot ship without a matching DEC.
evidence:
  - kind: spec
    ref: specs/0010-cognitive-delivery-control-plane/requirements.md
  - kind: doc
    ref: scripts/spec_check.py
  - kind: doc
    ref: decisions/.spec-check-allowlist.yaml
  - kind: doc
    ref: ../athena-site/ops/schemas/decision.schema.json
rollback: |
  Remove the coverage-per-R-* rule from scripts/spec_check.py. Keep
  the allowlist file as documentation of the deferred IDs but stop
  reading it. Existing DECs survive untouched; the gate goes back to
  the four phase-0 rules.
owner: editorial
---

## decision

Every shipped R-* requirement carries at least one DEC. The
`scripts/spec_check.py` gate walks every R-* defined in any
`specs/NNNN-*/requirements.md` and confirms a matching DEC exists or
the ID is listed in `decisions/.spec-check-allowlist.yaml`. The gate
exits 1 if any R-* lacks both.

## alternatives

- Trust-the-author DEC discipline — phase 1 shipped 14 R-FND IDs
  without a single DEC; the trust model already failed once.
- DEC per spec instead of per requirement — rolls per-requirement
  trade-offs into one record and loses the audit trail.
- Defer DEC coverage until spec 0001 ships — the longer the gap,
  the harder the backfill.

## rationale

Specs name the what. DECs name the why. The audit trail for the why
lives in commit messages and PR descriptions otherwise, both of
which decay. The coverage rule keeps the audit trail load-bearing.
The allowlist file gives the rule a graceful migration path: legacy
IDs land with a note; the gate skips them and prints the deferred
count.

## evidence

- `specs/0010-cognitive-delivery-control-plane/requirements.md` —
  R-CDCP-001 acceptance.
- `scripts/spec_check.py` — the gate implementation; rule 7.
- `decisions/.spec-check-allowlist.yaml` — the deferred-ID list.
- `../athena-site/ops/schemas/decision.schema.json` — the
  cross-repo contract every DEC parses against.

## rollback

Remove rule 7 from `scripts/spec_check.py`. Keep the allowlist file
as documentation. Existing DECs survive untouched.
