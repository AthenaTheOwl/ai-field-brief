# ai-field-brief

A weekly AI brief that runs a voice gate on itself before it ships. The banlist
holds 90-plus phrases plus structural rules — empty adverbial openers, the
antithetical reversal, the "not X but Y" cadence — and a single hit blocks the
merge. The brief refuses to sound like a model wrote it, and it has to prove it
every week.

**Live:** [ai-field-brief.vercel.app](https://ai-field-brief.vercel.app/)

**Feeds:** [RSS](https://ai-field-brief.vercel.app/feed.xml),
[Atom](https://ai-field-brief.vercel.app/atom.xml),
[JSON Feed](https://ai-field-brief.vercel.app/feed.json)

**Email:** weekly digest delivery uses Resend contacts and broadcasts
when `RESEND_API_KEY`, `RESEND_SEGMENT_ID`, `DIGEST_FROM_EMAIL`, and
`CRON_SECRET` are set on the deployed app.

**Latest:** [Loop engineering reached the runtime layer: discovery, durability, and audit gates now carry the work (2026-W26)](https://ai-field-brief.vercel.app/briefs/2026-W26)

## What it does

Most AI digests hand you a pile of links and call it a week. This one hands you
a move. Every pick names one thing to do before next Friday and shows the
artifact behind it — a contract test, an incident runbook, a procurement
question, a judge prompt, a unit-economics table. A pick you can't act on isn't
a pick.

The reading underneath it is wide. A weekly sweep crosses 173 active sources
(registry v5): primary vendor and research surfaces, practitioner blogs,
podcasts, videos, papers, GitHub releases, startup changelogs, HN and Reddit
feeds, and a `frontier-scout` lane that watches the tools and protocols nobody
is following yet. The W26 issue reviewed 27 of 29 attempted and shipped seven
Top signals, each with a concrete action, a confidence label, evidence cells, a
systems map, a falsification test, and an adoption ladder.

The brief is a markdown file per ISO week under `briefs/`. The site is a Next.js
static prerender of those files; the RSS, Atom, JSON Feed, and weekly email
routes are generated from the same snapshot. One source of truth, five surfaces.

## Try it

The gate that keeps the prose honest is one command, no setup:

```sh
python scripts/voice_lint.py
```

```
voice-lint: clean. 261 file(s) scanned.
```

Every brief and every public markdown file passes this before merge. It runs in
CI alongside seven sibling gates, and a failed gate blocks the PR. The banlist is
the point — the cadence it catches is the cadence the briefs would otherwise
drift into.

## How it works

Spec-driven, multi-tenant by design. Phase 1 ships the public archive and the
weekly briefs. The roadmap covers automated source ingestion (R-SRC, spec 0002),
transcription, retrieval, billing, integrations, and the publishing surface —
each gated behind a fixture, an eval, a rollback path, and a traceable
requirement before it ships.

Eight Python gates run on every push: `spec_check`, `voice_lint`,
`validate_schemas`, `validate_registry`, `validate_decisions`, `validate_roles`,
`validate_tools`, `validate_policies`. The repo carries 67 DEC records under
`decisions/` — each with alternatives, evidence, and a rollback — thirteen
worked role contracts under `.agents/roles/`, a release ledger at
`ops/RELEASE_LEDGER.md`, and a reset ledger at `ops/RESET_LEDGER.md` that logs
every force-push and history rewrite. The discipline is the product as much as
the brief is.

## How it connects

This repo runs on the
[Cognitive Delivery Control Plane](https://github.com/AthenaTheOwl/athena-site/blob/main/ops/control-plane.md),
the operating model documented in
[athena-site](https://github.com/AthenaTheOwl/athena-site). `specs/`,
`decisions/`, and `dreams/` are first-class directories you can fork directly;
the schemas live under `ops/schemas-cache/` and point back to athena-site.
`promotions/` is the bridge out — PROM-* candidates name a target repo and an
artifact type for picks mature enough to land elsewhere in the portfolio. Three
product repos run the same control plane; the throughline is in the
[control-plane charter](https://github.com/AthenaTheOwl/athena-site/blob/main/ops/control-plane.md).

## Run it locally

```sh
pnpm install
pnpm --filter @aifieldbrief/web dev   # local archive at :3000
pnpm turbo run typecheck
pnpm turbo run test
pnpm --filter @aifieldbrief/web build
```

The `apps/web` predev and prebuild hooks run `scripts/snapshot-briefs.mjs`,
which copies `briefs/` into a build-time snapshot the Next app reads from. Edit a
brief, rerun the dev server, the change shows up.

<!-- live-url: https://ai-field-brief.vercel.app/ -->

## Layout

```
apps/web/          Next.js public archive (the only shipped surface)
apps/mobile/, apps/extension/, apps/mcp-server/   planned reader surfaces
packages/          db, sources, pipeline, retrieval, evals (most planned)
briefs/            one folder per ISO week: brief.md + meta.yaml; INDEX.md is the table
sources/registry.yaml   the curated 173-source list, with lane and cadence tags
specs/  decisions/  dreams/  promotions/   the control-plane artifacts
.agents/           AGENTS.md, roles, tools.yaml, policies, state machines
scripts/           the gate scripts that run on every push
```

## License

Code: Apache-2.0. Content under `briefs/`: CC BY 4.0.
