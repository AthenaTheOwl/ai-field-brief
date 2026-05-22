# traceability: foundation

| Requirement | Design surface | Planned proof |
|---|---|---|
| R-FND-001 | `packages/db/src/queries/workspaces.ts`, `assertWorkspaceId` | `packages/db/src/test/tenant-scoping.test.ts` |
| R-FND-002 | `packages/db/src/schema/identity.ts` (`orgs`, `org_members`) + `workspaces.orgId` FK | drizzle generate; schema typecheck |
| R-FND-003 | `packages/db/src/schema/workspaces.ts` (`workspace_members`, `workspace_invites`) | schema typecheck; invite flow lands in spec 0002 |
| R-FND-004 | `apps/web/src/middleware.ts` (Clerk middleware) + `users.twoFactorEnabled` | middleware boots; live verification deferred to user-provided Clerk |
| R-FND-005 | `packages/db/drizzle.config.ts` + `packages/db/drizzle/migrations/` | drizzle-kit generates against schema |
| R-FND-006 | `tsconfig.base.json` + per-package `tsconfig.json` | `pnpm --filter @aifieldbrief/db typecheck`, `pnpm --filter @aifieldbrief/web typecheck` |
| R-FND-007 | `packages/db/src/env.ts`, `apps/web/src/lib/env.ts` | env smoke test + boot-time throw |
| R-FND-008 | root `LICENSE` + `NOTICE` + CHANGELOG entry | already in repo from Phase 0 |
| R-FND-009 | root `README.md` (hook + planned shape + Phase 0 rule) | already in repo from Phase 0 |
| R-FND-010 | `.github/workflows/ci.yml` + `package.json` `verify` script | CI run on PR |
| R-FND-011 | `packages/db/src/schema/audit.ts` + `packages/db/src/queries/audit.ts` | vitest covers `log()` missing-args case |
| R-FND-012 | `packages/db/src/schema/workspaces.ts` (`workspaces.settings` jsonb) | drizzle typecheck; settings shape lands in spec 0010 / 0011 |
| R-FND-013 | `apps/web/src/app/layout.tsx`, `apps/web/src/app/page.tsx` (no `"use client"`) | `pnpm --filter @aifieldbrief/web build` |
| R-FND-014 | every `*_at` column uses `timestamp({ withTimezone: true })`; `workspaces.timezone` text | drizzle typecheck on schema files |
