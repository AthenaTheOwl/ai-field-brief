# tasks: source registry + ingestion

## Phase 2 — packages/sources

- [x] Switch `package.json` from echo placeholders to real
  lint/typecheck/test scripts.
- [x] `src/types.ts` — `SOURCE_TYPES` const tuple, `SourceType` union,
  `SourceItem`, `Provenance`, `Transcript`, `Citation` types mirroring
  the JSON schemas.
- [x] `src/contract.ts` — `Connector<TConfig>` interface + `FetchCtx` +
  `ConnectorInput` discriminated union + error classes.
- [x] `src/canonicalize.ts` — `canonicalizeUrl` pure function.
- [x] `src/hash.ts` — `contentHash` pure function.
- [x] `src/registry.ts` — `registerConnector`, `getConnector`,
  `listSourceTypes`, `UnknownSourceTypeError`.
- [x] `src/connectors/rss.ts` — RSS 2.0 + Atom 1.0 + JSON Feed parser.
- [x] `src/connectors/podcast-rss.ts` — RSS + itunes namespace.
- [x] `src/connectors/article-url.ts` — Readability-style extractor.
- [x] `src/connectors/github-releases.ts` — Octokit-shaped release mapper.
- [x] `src/connectors/stubs.ts` — 14 stub connectors that register and
  throw `NotImplementedError`.
- [x] `src/index.ts` — re-exports types, contract, registry, and triggers
  connector registration.
- [x] `test/canonicalize.test.ts` — utm strip + case-fold host + slash
  trim + already-canonical + unicode path + query-key order.
- [x] `test/hash.test.ts` — determinism + divergence on body change.
- [x] `test/registry.test.ts` — every `SourceType` registers; stub throws
  `NotImplementedError`; unknown type throws `UnknownSourceTypeError`.
- [x] `test/fixtures.test.ts` — round-trip the 4 full connectors against
  the canonical fixtures.
- [x] `test/types.test.ts` — `SOURCE_TYPES` matches the JSON Schema enum.
- [x] `vitest.config.ts` + `tsconfig.json`.

## Phase 2 — packages/db

- [x] `src/schema/sources.ts` — `sources` + `source_reliability_history`
  tables with FK + index.
- [x] `src/schema/index.ts` — re-export.
- [x] `src/queries/sources.ts` — `listSources`, `getSource`,
  `createSource`, `updateSource`, `retireSource` with
  `assertWorkspaceId` guards.
- [x] `src/queries/index.ts` — re-export.
- [x] `src/index.ts` — top-level re-exports for ergonomic imports.
- [x] `src/seeds/sources-from-registry.ts` — read `sources/registry.yaml`,
  produce insert payloads via `REGISTRY_TYPE_TO_SOURCE_TYPE` mapping.
- [x] `src/test/sources.test.ts` — missing-workspaceId case for every
  helper.
- [x] `src/test/seeds.test.ts` — loader returns 15 rows; mapping is total
  over the registry file.

## Phase 2 — repo wiring

- [x] Spec 0002 ledger (this file's five siblings).
- [x] Update `specs/README.md` to list spec 0002.
- [x] Update `CHANGELOG.md` with Phase 2 entry.
- [x] `pnpm install` resolves the workspace; `pnpm turbo run typecheck`
  + `pnpm turbo run test` exit 0.

## Source ops queue MVP

- [x] `packages/sources/src/ops.ts` loads the static registry and computes
  freshness/readiness rows from registered connector metadata.
- [x] `apps/web/src/app/ops/sources/page.tsx` renders the operator queue
  without source URL fetches.
- [x] `packages/sources/test/ops.test.ts` covers current registry readiness
  plus review-due, stub connector, and missing mapping states.

## Frontier scout lane

- [x] Add `frontier-scout` as a declared registry lane.
- [x] Add active scout sources for sandboxes, browser automation,
  agent frameworks, approval loops, evals/tracing, MCP directories,
  structured extraction, and model routing.
- [x] Add `sources/scout-radar.md` as the review loop for early signal.
- [x] Add `source_arbitrage`, `repo_project_scan`, and `action_packet`
  prompt lenses.
- [x] Add a `frontier_scout` profile and scout-score overlay.
- [x] Extend the weekly brief template with Action packets and Scout
  radar sections.

## Out of scope for Phase 2 (booked for later)

- Inngest functions + per-workspace cron (spec 0003).
- HTTP fetch + ETag + retry logic (spec 0003).
- Source-registry CRUD UI under `apps/web/app/sources/` (spec 0002
  follow-up).
- OAuth flows for Slack / Discord / Twitter / Notion (spec 0010).
- Reliability score computation against real briefs (spec 0006).
