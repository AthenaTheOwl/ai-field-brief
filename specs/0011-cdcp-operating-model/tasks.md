# tasks: cdcp-operating-model

## Spec ledger

- [x] `specs/0011-cdcp-operating-model/requirements.md` with
  R-CDCP-011..016.
- [x] `specs/0011-cdcp-operating-model/design.md`.
- [x] `specs/0011-cdcp-operating-model/tasks.md` (this file).
- [x] `specs/0011-cdcp-operating-model/acceptance.md`.
- [x] `specs/0011-cdcp-operating-model/research.md`.
- [x] `specs/0011-cdcp-operating-model/traceability.md` with the
  `owner_role:` field per requirement.
- [x] `specs/README.md` lists the new spec folder.

## Roles

- [x] `.agents/roles/control.coordinator/{role.yaml,instructions.md,tools.yaml,output.schema.json,gates.yaml}`.
- [x] `.agents/roles/product.spec-writer/{role.yaml,instructions.md,tools.yaml,output.schema.json,gates.yaml}`.
- [x] `.agents/roles/engineering.implementation/{role.yaml,instructions.md,tools.yaml,output.schema.json,gates.yaml}`.
- [x] `.agents/roles/engineering.code-reviewer/{role.yaml,instructions.md,tools.yaml,output.schema.json,gates.yaml}`.
- [x] `.agents/roles/science.proof-gate-runner/{role.yaml,instructions.md,tools.yaml,output.schema.json,gates.yaml}`.
- [x] `.agents/roles/learning.dream-orchestrator/{role.yaml,instructions.md,tools.yaml,output.schema.json,gates.yaml}`.

## Tool registry

- [x] `.agents/tools.yaml` with 16 seed entries matching the
  cross-repo schema.

## Policies

- [x] `.agents/policies/default-deny.yaml` (priority 0).
- [x] `.agents/policies/coordinator-routing-only.yaml`.
- [x] `.agents/policies/implementation-can-edit-code.yaml`.
- [x] `.agents/policies/reviewer-cannot-edit-code.yaml`.
- [x] `.agents/policies/dream-candidates-require-human-approval.yaml`.

## State machines

- [x] `.agents/state-machines/spec-lifecycle.yaml`.
- [x] `.agents/state-machines/run-lifecycle.yaml`.
- [x] `.agents/state-machines/release-lifecycle.yaml`.

## Workflows

- [x] `.agents/workflows/single-change.yaml` (moved from
  `control-plane/workflows/`).
- [x] `.agents/workflows/weekly-dream.yaml`.
- [x] `.agents/workflows/incident-response.yaml`.
- [x] `control-plane/workflows/single-change.yaml` carries a
  `moved_to:` pointer.

## Catalog

- [x] `.agents/CATALOG.md` with the 44 deferred roles organized by
  guild.

## Event log

- [x] `ops/event-log/2026-05-24.jsonl` with the install event and the
  spec creation event.

## Scripts

- [x] `scripts/validate_roles.py`.
- [x] `scripts/validate_tools.py`.
- [x] `scripts/validate_policies.py`.
- [x] `scripts/spec_check.py` extended to read `owner_role:` per R-*.
- [x] `decisions/.spec-check-allowlist.yaml` carries a
  `roles_deferred:` section for every R-* that pre-dates R-CDCP-011.

## Schemas cache

- [x] `ops/schemas-cache/role.schema.json`.
- [x] `ops/schemas-cache/tool.schema.json`.
- [x] `ops/schemas-cache/policy.schema.json`.
- [x] `ops/schemas-cache/workflow.schema.json`.
- [x] `ops/schemas-cache/state-machine.schema.json`.
- [x] `ops/schemas-cache/event.schema.json`.

## CI workflow

- [x] `.github/workflows/ci.yml` `gates` job adds three new steps:
  `validate_roles`, `validate_tools`, `validate_policies`.

## AGENTS contract

- [x] `.agents/AGENTS.md` adds a "Role catalog" section pointing at
  the new directories and a "How to add a new role" subsection.

## Repo root

- [x] `README.md` Governance section lists the new `.agents/`
  subdirectories and `ops/event-log/`.

## Decision record

- [x] `decisions/DEC-CDCP-002-install-operating-model.md` resolves
  R-CDCP-011.

## Verification

- [x] `python scripts/spec_check.py` exits 0 with four active specs.
- [x] `python scripts/voice_lint.py` exits 0 across the repo.
- [x] `python scripts/validate_schemas.py` exits 0.
- [x] `python scripts/validate_registry.py` exits 0.
- [x] `python scripts/validate_decisions.py` exits 0.
- [x] `python scripts/validate_roles.py` exits 0 with six roles.
- [x] `python scripts/validate_tools.py` exits 0 with 16 tools.
- [x] `python scripts/validate_policies.py` exits 0 with five
  policies plus the default-deny baseline.
- [x] `pnpm install` resolves the workspace.
- [x] `pnpm turbo run typecheck` exits 0.
- [x] `pnpm turbo run test` exits 0.
- [x] `pnpm --filter @aifieldbrief/web build` produces a `.next`
  output.
