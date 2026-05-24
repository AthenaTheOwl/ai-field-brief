---
id: DEC-FND-013-ssr-by-default-client-only-on-interaction
spec: specs/0001-foundation/
requirement: R-FND-013
date: 2026-05-24
status: approved
reversible: true
decision: |
  Every page in the Next.js App Router renders as a server component
  by default. A `"use client"` directive lands only on the components
  that need it (form interaction, real-time state, browser-only APIs).
  The landing page (`apps/web/src/app/page.tsx`) and the root layout
  (`apps/web/src/app/layout.tsx`) ship as server components; the
  ClerkProvider wrapper in the layout is the only third-party
  boundary, and it stays server-friendly via Clerk's RSC support.
alternatives:
  - label: client-side rendering for the whole app
    rejected_because: |
      Client-side rendering means a blank screen until React mounts,
      which costs first-paint metrics and breaks SEO for the public
      `/briefs` reader. Server-rendered content arrives complete on
      first byte.
  - label: SSR opt-in (default to client)
    rejected_because: |
      The opt-in shape forces every new page to remember to mark
      itself server. The opt-out shape (default server, `"use client"`
      only when needed) matches how App Router's mental model already
      works.
  - label: full static generation with no SSR
    rejected_because: |
      Personalized routes (workspace-scoped briefs, the admin surface
      in spec 0011) need request-time data. Static-only forecloses
      those routes at the architecture level.
rationale: |
  SSR-by-default gives every public route a complete first paint and
  keeps the dynamic surface available for the routes that need it.
  The `"use client"` carve-out is per component, not per page, which
  means a server page can hold one interactive island without going
  full client. The pattern matches the App Router's mental model and
  the Vercel deploy shape.

  The decision is reversible: a per-page `"use client"` directive
  flips one page to client-only without touching the rest. The
  rollback cost is the SEO and first-paint penalty.
evidence:
  - kind: spec
    ref: specs/0001-foundation/requirements.md
  - kind: doc
    ref: apps/web/src/app/page.tsx
  - kind: doc
    ref: apps/web/src/app/layout.tsx
rollback: |
  Add `"use client"` to the layout file. Every descendant page
  inherits client rendering. The rollback is one directive line.
owner: platform
---

## decision

Every page in the App Router renders server-side by default.
`"use client"` lands only on components that need browser APIs or
interaction. The landing page and root layout ship as server
components; ClerkProvider in the layout is the only third-party
boundary.

## alternatives

- Client-side rendering for the whole app — blank first paint;
  breaks SEO for the public reader.
- SSR opt-in — every new page would have to remember to mark itself
  server.
- Full static generation — personalized routes need request-time
  data.

## rationale

SSR-by-default gives every public route a complete first paint and
keeps the dynamic surface available for the routes that need it.
The `"use client"` carve-out is per component, not per page.

## evidence

- `specs/0001-foundation/requirements.md` — R-FND-013 acceptance.
- `apps/web/src/app/page.tsx` — no `"use client"` directive; calls
  `listBriefs()` at render.
- `apps/web/src/app/layout.tsx` — no `"use client"`; wraps
  `ClerkProvider` server-side.

## rollback

Add `"use client"` to the layout. Every descendant page inherits
client rendering.
