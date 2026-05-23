# tasks: cognitive-delivery-control-plane

## Spec ledger

- [x] `specs/0010-cognitive-delivery-control-plane/requirements.md` with
  R-CDCP-001..010.
- [x] `specs/0010-cognitive-delivery-control-plane/design.md`.
- [x] `specs/0010-cognitive-delivery-control-plane/tasks.md` (this file).
- [x] `specs/0010-cognitive-delivery-control-plane/acceptance.md`.
- [x] `specs/0010-cognitive-delivery-control-plane/research.md`.
- [x] `specs/0010-cognitive-delivery-control-plane/traceability.md`.
- [x] `specs/README.md` lists the new spec folder.

## Decisions directory

- [x] `decisions/README.md` documents the format and the add-a-decision
  flow.
- [x] `decisions/DEC-CDCP-001-install-cdcp-governance.md`.
- [x] `decisions/DEC-FND-001-tenant-scoping-via-helper.md` (backfill).
- [x] `decisions/DEC-FND-007-zod-env-validation-at-boot.md` (backfill).
- [x] `decisions/.spec-check-allowlist.yaml` lists the R-FND-* IDs whose
  backfill DECs land in a later pass.

## Agent contract

- [x] `.agents/AGENTS.md` with coding style, domain decisions, workflow
  conventions, and cross-repo links.
- [x] `.agents/skills/run-weekly-brief/SKILL.md` v0.1.0 graduating
  `playbook/run-weekly-brief.md`.

## Dreams

- [x] `dreams/README.md` documents the eight dream modes and the
  human-gate rule.

## Ops ledgers

- [x] `ops/RELEASE_LEDGER.md` with backfilled entries for the nine
  pre-CDCP commits.
- [x] `ops/RESET_LEDGER.md` with the documented format and "No resets
  recorded." entry.

## Control plane workflow

- [x] `control-plane/workflows/single-change.yaml` declaring the nine
  workflow steps.

## Scripts

- [x] `scripts/validate_decisions.py` with the network + cache schema
  load and per-DEC validation.
- [x] `scripts/spec_check.py` extension that walks R-* IDs against DEC
  references with the allowlist exception.
- [x] `ops/schemas-cache/decision.schema.json` cached copy of the
  cross-repo schema.

## CI workflow

- [x] `.github/workflows/ci.yml` `gates` job adds `validate_decisions`
  as a step after `validate_registry`.

## Repo root

- [x] `README.md` carries a "Governance" section near the top pointing
  at specs, decisions, dreams, agents, ledgers, and the athena-site
  charter.

## Verification

- [x] `python scripts/spec_check.py` exits 0 with three active specs.
- [x] `python scripts/voice_lint.py` exits 0 across the repo.
- [x] `python scripts/validate_schemas.py` exits 0.
- [x] `python scripts/validate_registry.py` exits 0.
- [x] `python scripts/validate_decisions.py` exits 0 with three DEC
  files validated.
- [x] `pnpm install` resolves the workspace.
- [x] `pnpm --filter @aifieldbrief/web build` produces a `.next` output.
