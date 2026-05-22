# Changelog

All notable changes to ai-field-brief get an entry here. New entries
go at the top.

## [Unreleased]

### Phase 1 — foundation (spec 0001)

- `specs/0001-foundation/` ledger lands with R-FND-001..014 traced.
- `packages/db` ships Drizzle schema (identity, workspaces, audit,
  api_keys), Neon HTTP client, zod env validation, and tenant-scoped
  query helpers with a vitest belt-and-suspenders test for missing
  `workspaceId`.
- `apps/web` ships a Next.js 15 App Router scaffold with Clerk
  middleware (no live keys), zod env validation, `/api/healthz` and
  `/api/readyz` route handlers, and a server-rendered landing page.
- `pnpm install` from repo root resolves all 5 workspace packages.
- pgvector is deferred to spec 0005; Stripe billing to spec 0011;
  Inngest workflow tables to spec 0003.

### Phase 0 — bootstrap

- Specs scaffold under `specs/0000-bootstrap/` (7 R-BOOT-* requirements).
- Monorepo skeleton: pnpm workspaces, Turborepo, TypeScript strict baseline.
- Gate scripts: `scripts/spec_check.py`, `scripts/voice_lint.py`,
  `scripts/validate_schemas.py`, `scripts/validate_registry.py`.
- CI workflow (`.github/workflows/ci.yml`) wired to run every gate on PR.
- Apache-2.0 LICENSE; CC BY 4.0 reserved for published content via sibling
  content-mirror repo.
- `.env.example` documents every env var the v3 plan calls for.
