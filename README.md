# ai-field-brief

Weekly AI digest with concrete moves. Less news, more insight. Every
pick ships with a move you can run before next Friday and a worked
example — a contract test, an incident playbook, a procurement
checklist, a unit-economics table, a judge prompt.

**Live:** [ai-field-brief.vercel.app](https://ai-field-brief.vercel.app/)

**Latest:** [Contract speed, not model speed (2026-W21)](https://ai-field-brief.vercel.app/briefs/2026-W21)

## Read it for

- A 10-minute weekly sweep of AI primary sources — Anthropic, OpenAI,
  Latent Space, Simon Willison, Dwarkesh, Eugene Yan, Hamel Husain,
  Applied LLMs, plus a small set of strategy reads.
- Concrete moves, not summaries. Every pick names one thing to do
  this week and shows the artifact: a contract test, a runbook page,
  a procurement question, a judge prompt, a unit-economics table.
- Voice that doesn't sound like AI wrote it. `scripts/voice_lint.py`
  is a hard PR gate; the banlist covers the usual AI cadence and the
  antithetical-reversal pattern.

## How it works

Spec-driven multi-tenant SaaS. Phase 1 ships the public archive plus
the first weekly briefs. The roadmap covers automated source
ingestion (R-SRC, spec 0002), transcription, retrieval-augmented
generation, billing, integrations, and the publishing surface.

The brief itself is a markdown file per ISO week under `briefs/`. The
deployed site is a Next.js static prerender of those files; the
publishing pipeline lands with spec 0007.

See [Governance](#governance) below for the operating model.

## Project structure

- `apps/web` — Next.js public archive (currently the only shipped
  surface; renders briefs from a build-time snapshot).
- `apps/mobile`, `apps/extension`, `apps/mcp-server` — planned
  reader surfaces; specs to land in later phases.
- `packages/db` — Postgres schema and Drizzle client; multi-tenant
  baseline.
- `packages/sources` — source registry connectors (spec 0002 WIP).
- `packages/pipeline`, `packages/retrieval`, `packages/evals`,
  `packages/integrations`, `packages/observability` — planned;
  scoped under later phases.
- `inngest/` — workflow functions; lands with spec 0003.
- `briefs/` — published digests, one folder per ISO week with
  `brief.md` and `meta.yaml`. `briefs/INDEX.md` is the rolling table.
- `sources/registry.yaml` — curated source list with lane,
  cadence, and quality tags.
- `specs/` — what we're building, one folder per phase.
- `decisions/` — `DEC-*.md` files with alternatives, evidence,
  and rollback per requirement.
- `dreams/` — weekly offline-cognition output and human-gated
  promotion candidates.
- `playbook/` — runbooks the agent reads when running the weekly
  sweep, the dream pass, and the release flow.
- `scripts/` — eight executable gate scripts (see below).

## Governance

This repo runs on the
[Cognitive Delivery Control Plane](https://github.com/AthenaTheOwl/athena-site/blob/main/ops/control-plane.md)
operating model.

- `specs/` — what we're building (R-* requirements with traceability).
- `decisions/` — why we chose what we chose (DEC-* with alternatives
  and rollback).
- `dreams/` — what each week's retrospective surfaced.
- `.agents/AGENTS.md` — the single contract a coding agent reads
  first.
- `.agents/skills/<id>/SKILL.md` — graduated reuse packages.
- `.agents/roles/<id>/` — six worked-example role contracts.
- `.agents/tools.yaml` — the tool registry every role calls against.
- `.agents/policies/` — declarative permission rules with a
  default-deny baseline.
- `.agents/state-machines/` — artifact lifecycles for spec, run,
  release.
- `.agents/workflows/` — step graphs for single-change, weekly-dream,
  incident-response.
- `.agents/CATALOG.md` — the 44 deferred roles tracked by guild.
- `ops/event-log/YYYY-MM-DD.jsonl` — append-only workflow events.
- `ops/RELEASE_LEDGER.md` — every release with date, SHA, scope, proof.
- `ops/RESET_LEDGER.md` — every force-push, history rewrite, rollback.

Eight Python gates run on every push: `spec_check`, `voice_lint`,
`validate_schemas`, `validate_registry`, `validate_decisions`,
`validate_roles`, `validate_tools`, `validate_policies`. A failed
gate blocks the merge.

## Develop locally

```sh
pnpm install
pnpm --filter @aifieldbrief/web dev   # local archive at :3000
pnpm turbo run typecheck
pnpm turbo run test
pnpm --filter @aifieldbrief/web build
```

The `apps/web` predev and prebuild hooks run
`scripts/snapshot-briefs.mjs`, which copies `briefs/` into a
build-time snapshot the Next app reads from. Edit a brief, rerun the
dev server, and the change shows up.

## Phase 0 rule

Every feature from the v3 plan is either in a numbered phase,
explicitly out of scope, or blocked on account/provider setup. No
connector, prompt, model, workflow, or publish channel ships without
a fixture, an eval, a retry/rollback path, and a traceable
requirement.

## License

Code: Apache-2.0. Content under `briefs/`: CC BY 4.0.
