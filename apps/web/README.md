# @aifieldbrief/web

Next.js 15 App Router scaffold for AI Field Brief. Phase 1 deliverable:
proof that the platform shape boots.

## What's wired in Phase 1

- Clerk middleware (`src/middleware.ts`) with public routes for `/`,
  `/api/healthz`, `/api/readyz`. Live Clerk keys are not committed; the
  middleware reads from env at runtime.
- Env validation at boot (`src/lib/env.ts`) via zod. Missing
  `DATABASE_URL`, `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`, or
  `CLERK_SECRET_KEY` fails startup.
- Tenant-scoped db helpers from `@aifieldbrief/db` re-exported through
  `src/lib/db.ts`.
- `/api/healthz` returns `{ ok: true }`.
- `/api/readyz` returns `{ ok, db }` after pinging the db.
- Landing page is a 5-line server component.

## What is not wired here

- Real Clerk sign-in screen — Clerk keys are not yet provisioned.
- Marketing copy, dashboards, settings UI — later specs.
- Stripe billing UI — spec 0011.
- Inngest endpoint — spec 0003.

## Local commands

```
pnpm --filter @aifieldbrief/web typecheck
pnpm --filter @aifieldbrief/web build
pnpm --filter @aifieldbrief/web test
```

`pnpm --filter @aifieldbrief/web dev` boots Next.js on `http://localhost:3000`
once `.env.local` is populated from `../../.env.example`.
