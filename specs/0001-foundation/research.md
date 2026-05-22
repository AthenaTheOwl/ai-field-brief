# research: foundation

Research checked 2026-05-22:

- Next.js 15 ships React 19 and the App Router as the default. Server
  components are the SSR-by-default path for R-FND-013. Route handlers
  under `src/app/api/*/route.ts` cover the healthz/readyz endpoints.
- Clerk's `@clerk/nextjs` v6 ships `clerkMiddleware` with a
  `publicRoutes` array. The middleware wraps every route by default; the
  carve-out list keeps `/`, `/api/healthz`, `/api/readyz` open. Live keys
  are deferred; the middleware code lands so spec 0002 can land protected
  routes without revisiting the wiring.
- Drizzle ORM with `@neondatabase/serverless` runs the Neon HTTP driver in
  edge and serverless. The same `drizzle-orm/pg-core` schema runs against
  any Postgres for tests and migrations; we keep both drivers wired.
- `drizzle-kit` reads `drizzle.config.ts` for generate/push. Migrations
  land under `drizzle/migrations/`. Phase 1 ships the config and an empty
  migrations folder; the first generate runs once a real `DATABASE_URL`
  shows up.
- pgvector lives at `extension pgvector` in Neon and matches the v3 plan's
  spec 0005 retrieval path. It stays out of this phase to keep the schema
  surface small and the migration boundary clean.
- Vitest 2.x with the `happy-dom` environment runs fast on Windows + ESM.
  The db package's tests run in a `node` environment; the web app's smoke
  test runs in `happy-dom`. Both packages keep their own
  `vitest.config.ts`.
- zod's `parse` throws on missing or wrong-shape keys. Importing the env
  module at the top of the dependency tree gives R-FND-007 a single
  failure surface at startup.
- Turborepo's `^build` dependency keeps the db package built before the
  web app's typecheck. The existing `turbo.json` already covers the
  pipeline; no new task entries are needed for Phase 1.

## Open questions parked for later

- Neon branch strategy for preview deploys (spec 0011 / spec 0012).
- Migration drift CI job (`db:migrate:check`) — booked for spec 0001's
  follow-up once a hosted Neon DB is provisioned.
- Clerk webhook payload shape for `user.created` and
  `organization.created` (spec 0002's user-onboarding flow).
