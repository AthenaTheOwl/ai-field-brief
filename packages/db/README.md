# @aifieldbrief/db

Drizzle schema + Neon client + tenant-scoped query helpers for AI Field
Brief.

## Rule

Every workspace-scoped query takes `workspaceId` as its first positional
argument. The helper body runs `assertWorkspaceId(workspaceId)` before any
SQL. A missing or blank value throws `TenantScopeError`.

```ts
import { getWorkspaceById } from "@aifieldbrief/db/queries";

const ws = await getWorkspaceById(workspaceId);
```

Forgetting the argument is a TypeScript error. Passing `undefined` cast to
string is the runtime guard.

## Layout

- `src/schema/identity.ts` — `users`, `orgs`, `org_members`.
- `src/schema/workspaces.ts` — `workspaces`, `workspace_members`,
  `workspace_invites`.
- `src/schema/audit.ts` — `audit_events`.
- `src/schema/api_keys.ts` — `workspace_api_keys`.
- `src/queries/workspaces.ts` — workspace helpers.
- `src/queries/audit.ts` — `log()` for `audit_events`.
- `src/env.ts` — zod schema for `DATABASE_URL` + `DIRECT_DATABASE_URL`.
- `src/client.ts` — Neon HTTP driver + Drizzle bindings.

## Migrations

`pnpm db:generate` writes a new migration under `drizzle/migrations/`.
`pnpm db:migrate` applies pending migrations. Neither runs in CI for Phase 1
because no hosted Postgres is wired; both commands work locally once
`DATABASE_URL` and `DIRECT_DATABASE_URL` point at a Neon branch.

## Out of scope here

- pgvector tables and embedding helpers — spec 0005.
- Inngest run tables — spec 0003.
- Stripe billing tables — spec 0011.
