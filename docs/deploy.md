# deploy

Operational notes for shipping ai-field-brief to Vercel. The Phase 1
scaffold is intentionally narrow — a public briefs reader plus the
healthz/readyz endpoints — so the first deploy is a five-minute
exercise, not a release event. Subsequent phases (auth, RAG, billing)
land behind the same Vercel project.

## prerequisites

- A Vercel account on the free tier.
- A Neon Postgres project (free tier) with `pgvector` enabled.
- Clerk application (free tier) with publishable + secret keys.
- The repo pushed to `github.com/AthenaTheOwl/ai-field-brief`.

## one-time setup

1. **Vercel new project** → import the GitHub repo.
2. **Framework preset** → Next.js (auto-detected).
3. **Root Directory** → leave at repo root (`./`). The `vercel.json`
   at the root names `apps/web` as the build target via the Turbo
   filter.
4. **Build & Output settings** → leave defaults; `vercel.json` overrides:
   - Install: `pnpm install --frozen-lockfile=false`
   - Build: `pnpm turbo run build --filter=@aifieldbrief/web`
   - Output: `apps/web/.next`
5. **Environment variables** (see `.env.example` for the full list).
   The minimum to deploy the public archive:
   - `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`
   - `CLERK_SECRET_KEY`
   - `DATABASE_URL` (Neon pooler URL)
   - `DIRECT_DATABASE_URL` (Neon direct URL)
6. **Deploy**.

The first deploy renders `/`, `/briefs`, and every `/briefs/<week>`
route as static HTML at build time. Adding a new brief = commit
markdown + push = Vercel rebuilds = new static pages live in ~60s.

## what's deployed today

- `/` — landing, links to the latest brief and the archive.
- `/briefs` — index of every published brief.
- `/briefs/<YYYY-WNN>` — one brief per page, rendered as prose from
  the markdown source under `briefs/<YYYY-WNN>/brief.md`.
- `/api/healthz` — `{ ok: true }`.
- `/api/readyz` — `{ ok, db }` — pings the configured Postgres URL.

## what's not deployed yet

Tied to upcoming specs, in order:

- Source registry CRUD UI (`/app/sources`) — spec 0002.
- Run timeline UI (`/app/runs/[id]`) — spec 0003.
- Review queue (`/app/inbox`) — spec 0006.
- Action backlog (`/app/actions`) — spec 0008.
- Ask my briefs RAG (`/app/ask`) — spec 0009.
- Billing UI (`/app/billing`) — spec 0011.
- Custom domains per workspace — spec 0007 R-PUB-010.
- RSS / Atom / JSON Feed / podcast feed — spec 0007 R-PUB-003 and 009.
- Inngest workflows + per-workspace cron — spec 0003.

## build-time data flow

```
repo root /briefs/<week>/brief.md   (committed)
                |
                | pnpm prebuild runs scripts/snapshot-briefs.mjs
                v
apps/web/.briefs-snapshot/<week>/brief.md   (gitignored)
                |
                | apps/web/src/lib/briefs.ts reads at SSR
                v
next build statically renders /briefs/<week>
                |
                | Vercel serves the prerendered HTML
                v
public URL
```

The snapshot indirection exists because Vercel's monorepo deploys can
prune sibling files above the app root in some configurations. The
snapshot keeps the brief renderer hermetic to `apps/web/`.

## production smoke after deploy

```
curl -sS https://<your-domain>/api/healthz | jq .
curl -sS https://<your-domain>/api/readyz | jq .
curl -sS https://<your-domain>/briefs | grep -q "ai-field-brief"
curl -sS https://<your-domain>/briefs/2026-W21 | grep -q "Contract speed"
```

If `readyz` returns `{ ok: false, db: "down" }`, verify
`DATABASE_URL` is the Neon pooler URL and that the project hasn't been
auto-suspended after inactivity.

## rollback

Vercel keeps every prior deploy. To roll back: Project → Deployments →
pick the prior green deploy → Promote to Production. No code change
required.

For a content-only rollback (a brief was published in error), revert
the commit that added the brief and push; Vercel rebuilds without it.
