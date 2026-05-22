# requirements: foundation

## Scope

Phase 1 lands the platform shape that every later spec depends on: a Next.js 15
web app skeleton, a tenant-scoped Drizzle schema against Neon Postgres, env
validation at boot, audit-event plumbing, and the multi-tenant access pattern
that downstream specs inherit.

Live wiring for Clerk and Stripe stays out of scope here. Spec 0001 documents
the env keys via `.env.example` and adds the schema tables; spec 0011 brings
Stripe up; Clerk goes live when the user provides keys.

## Requirements

### R-FND-001: tenant-scoped data access

WHEN any application code reads or writes a row that belongs to a workspace,
THE SYSTEM SHALL go through a Drizzle query helper that takes `workspaceId`
as a typed parameter.

Acceptance:
- Every helper in `packages/db/src/queries/workspaces.ts` accepts a
  `workspaceId: string` parameter.
- A vitest case asserts the helper throws on an empty or undefined
  `workspaceId` at runtime.
- Raw drizzle clients are not re-exported from `packages/db/src/index.ts`;
  consumers go through the helpers.

### R-FND-002: org-above-workspace identity model

WHEN a workspace gets created, THE SYSTEM SHALL attach it to a row in
`orgs`, with org membership tracked separately from workspace membership.

Acceptance:
- `orgs` table has `clerk_org_id`, `slug`, `name`, `plan`,
  `billing_customer_id`, `created_at`.
- `org_members` carries a composite primary key `(org_id, user_id)` with a
  role of `owner | admin | member`.
- `workspaces.org_id` is a non-null foreign key.
- A user may join multiple orgs; nothing in the schema blocks that.

### R-FND-003: workspace member roles + invite flow

WHEN a workspace member gets added, THE SYSTEM SHALL record a role of
`owner | admin | editor | viewer` and persist any pending invites in a
separate table with a unique token.

Acceptance:
- `workspace_members` composite PK `(workspace_id, user_id)` carries the
  4-role enum plus `joined_at` and `invited_by`.
- `workspace_invites` carries `email`, `role`, unique `token`, `expires_at`,
  nullable `accepted_at`.
- Invite acceptance is the only path that writes to `workspace_members`
  for non-owners.

### R-FND-004: 2FA + SSO architecture stays day-1

WHEN Clerk goes live, THE SYSTEM SHALL keep 2FA on by default and carry
SSO fields on `users` and `orgs` for the SAML/OIDC path.

Acceptance:
- `users.two_factor_enabled` is a boolean column with default `false`.
- `orgs.plan` has room for an `enterprise` value that gates SSO config in
  a later spec.
- `.env.example` lists `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`,
  `CLERK_SECRET_KEY`, `CLERK_WEBHOOK_SECRET`.
- The Next.js `middleware.ts` wires `clerkMiddleware` with public-route
  carve-outs for `/`, `/api/healthz`, `/api/readyz`.

### R-FND-005: Postgres + Drizzle migration discipline

WHEN the schema changes, THE SYSTEM SHALL track every change as a Drizzle
migration under `packages/db/drizzle/migrations/` so CI can detect drift.

Acceptance:
- `drizzle.config.ts` points at `src/schema/index.ts` and writes migrations
  to `drizzle/migrations/`.
- `pnpm --filter @aifieldbrief/db typecheck` passes with the schema files in
  place.
- The `drizzle/migrations/` folder exists in the repo; pgvector is deferred
  to spec 0005, so no vector columns land in this phase.

### R-FND-006: strict TypeScript across the workspace

WHEN any TypeScript code lands, THE SYSTEM SHALL inherit
`tsconfig.base.json` and pass `pnpm typecheck` with zero errors.

Acceptance:
- `apps/web/tsconfig.json` and `packages/db/tsconfig.json` extend
  `../../tsconfig.base.json`.
- `pnpm --filter @aifieldbrief/web typecheck` exits 0.
- `pnpm --filter @aifieldbrief/db typecheck` exits 0.

### R-FND-007: env validation at boot

WHEN the web app or db package starts, THE SYSTEM SHALL validate required
env vars through zod and fail startup on missing keys.

Acceptance:
- `packages/db/src/env.ts` defines a zod schema for `DATABASE_URL` and
  `DIRECT_DATABASE_URL`; importing the module with a missing key throws.
- `apps/web/src/lib/env.ts` defines a zod schema for `DATABASE_URL`,
  `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`, and `CLERK_SECRET_KEY`.
- A vitest case asserts the module parses a known-good set of values.

### R-FND-008: Apache-2.0 + content license boundary

WHEN code or content gets published, THE SYSTEM SHALL ship under Apache-2.0
for code with a NOTICE file, and reserve CC BY 4.0 for the content mirror
in a sibling repo.

Acceptance:
- The root `LICENSE` carries Apache-2.0 text (already in repo).
- `NOTICE` lists the project author and Apache notice (already in repo).
- The CHANGELOG entry for Phase 1 names spec 0001 by ID.

### R-FND-009: README opens with door hook + setup steps

WHEN a reader lands on the repo root, THE SYSTEM SHALL show the N° 18 hook,
the what/why/how, and the setup commands.

Acceptance:
- The root README's first three sections cover hook, planned shape, and
  Phase 0 rule (already in repo).
- The Phase 1 update to the README, if any, appends Phase 1 setup commands
  without rewriting the existing copy.

### R-FND-010: gate scripts + lint/typecheck/test/build block PRs

WHEN a PR opens against `main`, THE SYSTEM SHALL run `spec_check`,
`voice_lint`, `validate_schemas`, `validate_registry`, plus
`turbo run lint typecheck test build` and a security audit.

Acceptance:
- `.github/workflows/ci.yml` runs the four python gates plus the turbo
  pipeline (already in repo from Phase 0).
- `pnpm verify` chains every local gate.
- Adding the `@aifieldbrief/db` and `@aifieldbrief/web` packages does not
  break the existing pipeline.

### R-FND-011: audit log table for admin actions

WHEN an admin changes a setting, rotates a key, adds or removes a member,
or shifts a role, THE SYSTEM SHALL append a row to `audit_events` with
actor, target, before, after, IP, and user-agent.

Acceptance:
- `audit_events` carries `id`, nullable `workspace_id`, nullable `org_id`,
  `actor_user_id`, `action`, `target_type`, `target_id`, `before` jsonb,
  `after` jsonb, `ip`, `ua`, `created_at`.
- `packages/db/src/queries/audit.ts` exports a `log` helper that writes one
  row with all required fields.
- The vitest tenant-scoping case covers the audit helper's missing-args
  behavior alongside the workspace helpers.

### R-FND-012: workspace settings stored on `workspaces.settings`

WHEN a workspace stores per-tenant config (rubric ref, voice rules ref,
integration creds, billing ref), THE SYSTEM SHALL keep that config on a
JSONB column on the `workspaces` row.

Acceptance:
- `workspaces.settings` is a jsonb column with a `{}` default.
- Later specs (0005 rubric, 0010 integrations, 0011 billing) add typed
  accessors over `settings` and do not add top-level columns for each.

### R-FND-013: SSR by default for the web app

WHEN a page renders, THE SYSTEM SHALL run server-side by default; client
components only land where interaction requires them.

Acceptance:
- The `apps/web/src/app/page.tsx` landing page is a server component (no
  `"use client"` directive).
- The `apps/web/src/app/layout.tsx` shell is a server component that wraps
  Clerk providers.

### R-FND-014: UTC storage + per-workspace timezone

WHEN a timestamp gets stored, THE SYSTEM SHALL store it in UTC; the
workspace timezone column drives display.

Acceptance:
- Every `*_at` column in the schema files uses `timestamp with time zone`.
- `workspaces.timezone` is a text column with default `'UTC'`.
- A docstring on `workspaces.timezone` names the rule.
