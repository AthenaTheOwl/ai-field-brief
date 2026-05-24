# traceability: foundation

| Requirement | Design surface | Planned proof | Decision |
|---|---|---|---|
| R-FND-001 | `packages/db/src/queries/workspaces.ts`, `assertWorkspaceId` | `packages/db/src/test/tenant-scoping.test.ts` | [DEC-FND-001](../../decisions/DEC-FND-001-tenant-scoping-via-helper.md) |
| R-FND-002 | `packages/db/src/schema/identity.ts` (`orgs`, `org_members`) + `workspaces.orgId` FK | drizzle generate; schema typecheck | [DEC-FND-002](../../decisions/DEC-FND-002-org-above-workspace-via-clerk-orgs.md) |
| R-FND-003 | `packages/db/src/schema/workspaces.ts` (`workspace_members`, `workspace_invites`) | schema typecheck; invite flow lands in spec 0002 | [DEC-FND-003](../../decisions/DEC-FND-003-four-role-workspace-membership.md) |
| R-FND-004 | `apps/web/src/middleware.ts` (Clerk middleware) + `users.twoFactorEnabled` | middleware boots; live verification deferred to user-provided Clerk | [DEC-FND-004](../../decisions/DEC-FND-004-clerk-2fa-on-saml-enterprise-deferred.md) |
| R-FND-005 | `packages/db/drizzle.config.ts` + `packages/db/drizzle/migrations/` | drizzle-kit generates against schema | [DEC-FND-005](../../decisions/DEC-FND-005-drizzle-migrations-gated-by-ci-drift-check.md) |
| R-FND-006 | `tsconfig.base.json` + per-package `tsconfig.json` | `pnpm --filter @aifieldbrief/db typecheck`, `pnpm --filter @aifieldbrief/web typecheck` | [DEC-FND-006](../../decisions/DEC-FND-006-tsconfig-strict-plus-noUncheckedIndexedAccess.md) |
| R-FND-007 | `packages/db/src/env.ts`, `apps/web/src/lib/env.ts` | env smoke test + boot-time throw | [DEC-FND-007](../../decisions/DEC-FND-007-zod-env-validation-at-boot.md) |
| R-FND-008 | root `LICENSE` + `NOTICE` + CHANGELOG entry | already in repo from Phase 0 | [DEC-FND-008](../../decisions/DEC-FND-008-apache-2-code-cc-by-content-split.md) |
| R-FND-009 | root `README.md` (hook + planned shape + Phase 0 rule) | already in repo from Phase 0 | [DEC-FND-009](../../decisions/DEC-FND-009-readme-hook-plus-setup-pattern.md) |
| R-FND-010 | `.github/workflows/ci.yml` + `package.json` `verify` script | CI run on PR | [DEC-FND-010](../../decisions/DEC-FND-010-four-gate-scripts-block-pr.md) |
| R-FND-011 | `packages/db/src/schema/audit.ts` + `packages/db/src/queries/audit.ts` | vitest covers `log()` missing-args case | [DEC-FND-011](../../decisions/DEC-FND-011-audit-events-table-required-on-admin-actions.md) |
| R-FND-012 | `packages/db/src/schema/workspaces.ts` (`workspaces.settings` jsonb) | drizzle typecheck; settings shape lands in spec 0010 / 0011 | [DEC-FND-012](../../decisions/DEC-FND-012-workspace-settings-jsonb-not-typed-columns.md) |
| R-FND-013 | `apps/web/src/app/layout.tsx`, `apps/web/src/app/page.tsx` (no `"use client"`) | `pnpm --filter @aifieldbrief/web build` | [DEC-FND-013](../../decisions/DEC-FND-013-ssr-by-default-client-only-on-interaction.md) |
| R-FND-014 | every `*_at` column uses `timestamp({ withTimezone: true })`; `workspaces.timezone` text | drizzle typecheck on schema files | [DEC-FND-014](../../decisions/DEC-FND-014-utc-storage-workspace-timezone-render.md) |
