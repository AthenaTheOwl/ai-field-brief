# Changelog

All notable changes to ai-field-brief get an entry here. New entries
go at the top.

## [Unreleased]

### Phase 0 — bootstrap

- Specs scaffold under `specs/0000-bootstrap/` (7 R-BOOT-* requirements).
- Monorepo skeleton: pnpm workspaces, Turborepo, TypeScript strict baseline.
- Gate scripts: `scripts/spec_check.py`, `scripts/voice_lint.py`,
  `scripts/validate_schemas.py`, `scripts/validate_registry.py`.
- CI workflow (`.github/workflows/ci.yml`) wired to run every gate on PR.
- Apache-2.0 LICENSE; CC BY 4.0 reserved for published content via sibling
  content-mirror repo.
- `.env.example` documents every env var the v3 plan calls for.
