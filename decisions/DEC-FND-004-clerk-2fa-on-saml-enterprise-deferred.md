---
id: DEC-FND-004-clerk-2fa-on-saml-enterprise-deferred
spec: specs/0001-foundation/
requirement: R-FND-004
date: 2026-05-24
status: approved
reversible: true
decision: |
  Clerk owns 2FA and SSO at the identity layer. The schema carries
  `users.two_factor_enabled` as a mirrored boolean for query joins, and
  `orgs.plan` reserves an `enterprise` value that gates SSO configuration
  in a later spec. The Next.js `middleware.ts` wires `clerkMiddleware`
  with public-route carve-outs for `/`, `/api/healthz`, `/api/readyz`,
  and the `/briefs` static surface. Live SSO and 2FA enforcement land
  when the user provides Clerk keys; the schema fields are present today
  so the later turn-on is config-only.
alternatives:
  - label: build 2FA + SSO in the app layer
    rejected_because: |
      A TOTP library plus a SAML library plus session management plus
      recovery codes covers ground Clerk already covers in production.
      The app layer would re-implement battle-tested code that does not
      ship product value.
  - label: defer schema fields until SSO ships
    rejected_because: |
      Adding `two_factor_enabled` and the `enterprise` plan value later
      means a schema migration with backfill on every existing row. The
      cost of carrying two unused-today columns is zero; the cost of
      adding them later is one migration per tenant.
  - label: skip the public-route carve-outs and rely on Clerk's defaults
    rejected_because: |
      Health endpoints under auth would block every uptime probe and
      every Vercel deployment check. Explicit carve-outs for `/healthz`
      and `/readyz` are the right shape; the landing page and the
      public `/briefs` reader join them because those routes form the
      product's public face.
rationale: |
  Delegating 2FA + SSO to Clerk shrinks the auth surface to one vendor
  contract plus the local mirror. The schema fields land at Phase 1 so
  the SSO turn-on later is config (Clerk dashboard + env keys), not
  migration. The middleware shape carves out the four routes that must
  stay public for the product to function.

  The decision is reversible: replacing Clerk with a local auth stack
  is bounded (rewrite middleware + add TOTP + add SAML), and the schema
  fields stay correct under either model.
evidence:
  - kind: spec
    ref: specs/0001-foundation/requirements.md
  - kind: doc
    ref: apps/web/src/middleware.ts
  - kind: doc
    ref: packages/db/src/schema/identity.ts
  - kind: doc
    ref: .env.example
  - kind: doc
    ref: design only; live SSO enforcement deferred to a later integrations spec
rollback: |
  Replace `clerkMiddleware` with a local session middleware. Implement
  TOTP for 2FA and SAML for SSO in the app layer. Drop the `orgs.plan`
  `enterprise` value if SSO never ships. Schema-side rollback is
  bounded; the cost is the missing TOTP and SAML implementations.
owner: platform
---

## decision

Clerk owns 2FA and SSO at the identity layer. The schema carries
`users.two_factor_enabled` as a mirror plus `orgs.plan` with room for
an `enterprise` value. `apps/web/src/middleware.ts` wires
`clerkMiddleware` with public-route carve-outs for `/`, `/api/healthz`,
`/api/readyz`, and the `/briefs` static surface.

## alternatives

- Build 2FA + SSO in the app layer — re-implements Clerk's tested
  surface without shipping product value.
- Defer schema fields until SSO ships — adding `two_factor_enabled`
  and the `enterprise` plan later means a per-row migration.
- Skip middleware carve-outs — health checks and the public brief
  reader would land under auth.

## rationale

Delegating 2FA + SSO to Clerk shrinks the auth surface to one vendor
contract plus the local mirror. Schema fields land at Phase 1 so the
SSO turn-on later is config (Clerk dashboard + env keys), not
migration. The middleware carves out the four routes that must stay
public.

## evidence

- `specs/0001-foundation/requirements.md` — R-FND-004 acceptance.
- `apps/web/src/middleware.ts` — `clerkMiddleware` + `createRouteMatcher`
  public routes; falls back to `NextResponse.next()` until keys land.
- `packages/db/src/schema/identity.ts` — `users.twoFactorEnabled`
  default false; `orgPlan` enum includes `enterprise`.
- `.env.example` lists `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`,
  `CLERK_SECRET_KEY`, `CLERK_WEBHOOK_SECRET`.
- Live SSO enforcement is design only; implementation deferred to a
  later integrations spec that ships the Clerk SAML config.

## rollback

Replace `clerkMiddleware` with a local session middleware; implement
TOTP for 2FA and SAML for SSO in the app layer; drop the
`orgs.plan` `enterprise` value if SSO never ships.
