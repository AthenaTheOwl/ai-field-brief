# acceptance: cdcp-operating-model

## Gates

- `python scripts/spec_check.py` exits 0 with four active specs
  (`0000-bootstrap`, `0001-foundation`,
  `0010-cognitive-delivery-control-plane`,
  `0011-cdcp-operating-model`).
- `python scripts/voice_lint.py` exits 0 across the repo.
- `python scripts/validate_schemas.py` exits 0.
- `python scripts/validate_registry.py` exits 0 with the 15 seed
  sources still parsing.
- `python scripts/validate_decisions.py` exits 0.
- `python scripts/validate_roles.py` exits 0 with six role files
  validated.
- `python scripts/validate_tools.py` exits 0 with 16 tool entries
  validated.
- `python scripts/validate_policies.py` exits 0 with five policies
  plus the default-deny baseline confirmed.
- `pnpm install` resolves the workspace.
- `pnpm turbo run typecheck` exits 0.
- `pnpm turbo run test` exits 0.
- `pnpm --filter @aifieldbrief/web build` produces a `.next` output.

## Done means

Spec 0011 is done when:

1. The operating-model layer (six roles, tool registry, five policies,
   three state machines, three workflows, the deferred-role catalog,
   the event log) lands under `.agents/` and `ops/event-log/`.
2. The three new validators (`validate_roles`, `validate_tools`,
   `validate_policies`) ship under `scripts/` and run clean.
3. The CI workflow adds the three new gates as steps in the `gates`
   job.
4. `spec_check.py` reads `owner_role:` per R-* and a new
   `roles_deferred:` list in the allowlist covers the pre-existing
   R-* IDs.
5. R-CDCP-011..016 each name an owner role in
   `specs/0011-cdcp-operating-model/traceability.md` and resolve to
   `DEC-CDCP-002-install-operating-model.md` collectively.
6. The agent contract and the root README point readers at the new
   surface.

## Explicit non-acceptance

- No additional roles ship past the six worked examples; the other
  44 stay tracked in `.agents/CATALOG.md`.
- No execution engine for the policies or the state machines lands
  here; the YAML is documentation and gate input, not running code.
- No first dream output ships; the orchestrator role exists but the
  Friday cron lands in a later pass.
- No new top-level npm or pnpm dependencies.
- No deletion of `control-plane/workflows/single-change.yaml`; the
  legacy file carries a pointer.
