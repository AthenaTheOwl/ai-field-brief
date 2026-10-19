# Changelog

All notable changes to ai-field-brief get an entry here. New entries
go at the top.

## [Unreleased]

### Weekly coverage and W42 review copy (spec 0007)

- Add the October 18 W42 catch-up with four signals, 36 evidence cells,
  action scores and a same-author faithfulness report. The source check
  covers twenty public surfaces. Independent factual review passed;
  publication remains gated on CI.
- Detect older missing weeks even when the newest issue is fresh, reject
  future through-dates, and emit JSON coverage against the Friday deadline.
  DEC-PUB-014 records the change; CI runs the cadence regression cases.

### Phase 2 - source registry + ingestion (spec 0002)

- `specs/0002-source-registry/` ledger lands with R-SRC-001..016 traced.
- `packages/sources` ships the connector contract, registry, URL
  canonicalization, content hashing, four full connectors (`rss`,
  `podcast-rss`, `article-url`, `github-releases`), and registered
  stubs for the remaining source types.
- `packages/db` ships `sources` and `source_reliability_history` tables,
  tenant-scoped source query helpers, and a seed loader for
  `sources/registry.yaml`.
- R-SRC-001..016 now have DEC coverage and owner roles in traceability.
- HTTP fetch, Inngest runner logic, OAuth connectors, CRUD UI, and
  reliability writes stay deferred to their owning specs.

### Phase 1 - foundation (spec 0001)

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

### Phase 0 - bootstrap

- Specs scaffold under `specs/0000-bootstrap/` (7 R-BOOT-* requirements).
- Monorepo skeleton: pnpm workspaces, Turborepo, TypeScript strict baseline.
- Gate scripts: `scripts/spec_check.py`, `scripts/voice_lint.py`,
  `scripts/validate_schemas.py`, `scripts/validate_registry.py`.
- CI workflow (`.github/workflows/ci.yml`) wired to run every gate on PR.
- Apache-2.0 LICENSE; CC BY 4.0 reserved for published content via sibling
  content-mirror repo.
- `.env.example` documents every env var the v3 plan calls for.
