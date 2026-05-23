# acceptance: cognitive-delivery-control-plane

## Gates

- `python scripts/spec_check.py` exits 0 with three active specs
  (`0000-bootstrap`, `0001-foundation`, `0010-cognitive-delivery-control-plane`).
- `python scripts/voice_lint.py` exits 0 across the repo.
- `python scripts/validate_schemas.py` exits 0.
- `python scripts/validate_registry.py` exits 0 with the 15 seed
  sources still parsing.
- `python scripts/validate_decisions.py` exits 0 with three DEC files
  validated (`DEC-CDCP-001`, `DEC-FND-001`, `DEC-FND-007`).
- `pnpm install` resolves the workspace.
- `pnpm --filter @aifieldbrief/db typecheck` exits 0.
- `pnpm --filter @aifieldbrief/web typecheck` exits 0.
- `pnpm --filter @aifieldbrief/db test` runs green.
- `pnpm --filter @aifieldbrief/web build` produces a `.next` output.

## Done means

Spec 0010 is done when:

1. The CDCP scaffold (specs/0010, decisions/, dreams/, .agents/, ops/,
   control-plane/) lands as files under `e:\claude_code\random-apps\ai-field-brief`.
2. `scripts/validate_decisions.py` walks the three DEC files and exits 0.
3. `scripts/spec_check.py` walks every R-* and confirms every one is
   either covered by a DEC, allowlisted in
   `decisions/.spec-check-allowlist.yaml`, or covered by the bootstrap
   exemption for R-CDCP-*.
4. The CI workflow adds the new gate step.
5. The root README points readers at the governance artifacts.

## Explicit non-acceptance

- No backfill DECs for R-FND-002..006, R-FND-008..014 in this pass; the
  allowlist defers them and a later pass lands them.
- No first dream output; the README documents the format and the gate
  for that artifact lands when the first weekly dream lands.
- No mobile or extension wiring touched here.
- No new top-level npm or pnpm dependencies.
