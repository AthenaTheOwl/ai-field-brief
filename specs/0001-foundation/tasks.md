# tasks: foundation

## Phase 1 — `packages/db`

- [x] Scaffold `packages/db` with `package.json`, `tsconfig.json`,
  `drizzle.config.ts`, and `vitest.config.ts`.
- [x] `src/env.ts` — zod schema for `DATABASE_URL` + `DIRECT_DATABASE_URL`.
- [x] `src/client.ts` — Neon HTTP driver + Drizzle bindings.
- [x] `src/schema/identity.ts` — `users`, `orgs`, `org_members`.
- [x] `src/schema/workspaces.ts` — `workspaces`, `workspace_members`,
  `workspace_invites`.
- [x] `src/schema/audit.ts` — `audit_events`.
- [x] `src/schema/api_keys.ts` — `workspace_api_keys`.
- [x] `src/queries/workspaces.ts` — workspace-scoped helpers with
  `assertWorkspaceId` guard.
- [x] `src/queries/audit.ts` — `log()` helper for `audit_events`.
- [x] `src/test/tenant-scoping.test.ts` — vitest cases for missing /
  blank workspace IDs.

## Phase 1 — `apps/web`

- [x] Scaffold `apps/web` with `package.json`, `next.config.mjs`,
  `tsconfig.json`, `tailwind.config.ts`, `postcss.config.cjs`.
- [x] `src/lib/env.ts` — zod schema for db + Clerk keys.
- [x] `src/lib/db.ts` — re-export from `@aifieldbrief/db`.
- [x] `src/app/layout.tsx` + `src/app/page.tsx`.
- [x] `src/app/api/healthz/route.ts` + `src/app/api/readyz/route.ts`.
- [x] `src/middleware.ts` — Clerk middleware with public routes.
- [x] `vitest.config.ts` + smoke test for env parsing.

## Phase 1 — repo wiring

- [x] Spec 0001 ledger (this file's six siblings).
- [x] Update `specs/README.md` to list spec 0001.
- [x] `pnpm install` at repo root.

## Out of scope for Phase 1 (booked for later)

- pgvector tables and helpers (spec 0005).
- Stripe + billing tables (spec 0011).
- Inngest workflow tables (spec 0003).
- Source registry runtime tables (spec 0002).
- Live Clerk keys (user-provided, no commit).
