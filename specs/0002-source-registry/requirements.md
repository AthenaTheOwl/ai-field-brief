# requirements: source registry + ingestion

## Scope

Phase 2 lands the source-registry data model and the connector contract that
every ingestion path runs through. Four connectors ship full implementations
(rss, podcast-rss, article-url, github-releases); the remaining 14 source
types from the SourceItem enum ship as stubs that register themselves and
throw `NotImplementedError` so missing impls fail loudly. Per-workspace cron
and Inngest workflows arrive in spec 0003; OAuth-gated connectors (Slack,
Discord, Twitter/X, Notion) arrive in spec 0010.

## Requirements

### R-SRC-001: source registry table per workspace

WHEN a workspace owner adds a source, THE SYSTEM SHALL store one row in
`sources` keyed by `workspace_id`, with `type`, `lane`, `url`, `cadence`,
`intake`, `status`, and quality signals.

Acceptance:
- `sources` table carries `id`, `workspace_id` (FK to `workspaces.id` on
  cascade), `name`, `type`, `lane`, `url`, `cadence`, `intake`, `status`,
  `signal`, `actionability`, `credibility`, `priority`, `last_reviewed`,
  `reliability_score`, `custom_keywords` jsonb, `integration_config` jsonb,
  `notes`, `created_at`, `deleted_at`.
- `type` is constrained at the application layer to the `SourceType` union
  exported by `@aifieldbrief/sources`.
- Composite index on `(workspace_id, status, lane)`.

### R-SRC-002: tenant-scoped CRUD helpers for sources

WHEN application code reads or writes a row in `sources`, THE SYSTEM SHALL
route through a query helper that takes `workspaceId` as its first
positional argument.

Acceptance:
- `packages/db/src/queries/sources.ts` exports `listSources`, `getSource`,
  `createSource`, `updateSource`, `retireSource`.
- Each helper calls `assertWorkspaceId` before any SQL.
- A vitest case asserts each helper throws on missing or blank
  `workspaceId`.

### R-SRC-003: connector contract

WHEN any source type gains a connector, THE SYSTEM SHALL implement the
`Connector<TConfig>` interface so the runner code in spec 0003 calls one
shape regardless of source type.

Acceptance:
- `packages/sources/src/contract.ts` exports a `Connector<TConfig>`
  interface with `sourceType: SourceType` and
  `fetch(ctx: FetchCtx<TConfig>): Promise<SourceItem[]>`.
- Every full connector exports a `VERSION` string and stamps
  `provenance.fetcher = "<connector>@<VERSION>"` on each produced item.

### R-SRC-004: connector registry

WHEN the runner needs a connector for a given source type, THE SYSTEM SHALL
resolve it through an in-memory registry keyed by `SourceType`.

Acceptance:
- `packages/sources/src/registry.ts` exports `getConnector(type)` and
  `registerConnector(connector)`.
- A vitest case asserts every value in the `SourceType` union has a
  registered connector — full implementation or stub.
- Unknown source-type lookups throw `UnknownSourceTypeError`.

### R-SRC-005: stub connectors fail loudly

WHEN a source type has no full impl yet, THE SYSTEM SHALL register a stub
connector that throws `NotImplementedError` on `fetch`.

Acceptance:
- `packages/sources/src/connectors/stubs.ts` registers stubs for the 14
  source types this pass does not cover.
- A vitest case calls each stub's `fetch` and asserts it throws
  `NotImplementedError` with the source-type name in the message.

### R-SRC-006: rss connector

WHEN a `rss` source produces a feed, THE SYSTEM SHALL parse RSS 2.0,
Atom 1.0, and JSON Feed shapes into `SourceItem[]`.

Acceptance:
- `packages/sources/src/connectors/rss.ts` parses the three shapes from
  raw text input.
- A vitest fixtures test feeds a known RSS XML string into the connector
  and asserts the output matches the canonical fixture in
  `packages/sources/schemas/source-item.fixtures.json`.

### R-SRC-007: podcast-rss connector

WHEN a `podcast-rss` source produces a feed, THE SYSTEM SHALL parse the
itunes namespace fields and surface `audio_url` from the enclosure tag.

Acceptance:
- `packages/sources/src/connectors/podcast-rss.ts` reads `itunes:duration`
  into `metadata.duration_seconds` and the `<enclosure url=…>` into
  `audio_url`.
- A vitest fixtures test asserts the produced item matches the
  `podcast-rss` fixture.

### R-SRC-008: article-url connector

WHEN an `article-url` source receives a single URL, THE SYSTEM SHALL run a
Readability-style extraction over the raw HTML and produce one
`SourceItem`.

Acceptance:
- `packages/sources/src/connectors/article-url.ts` accepts raw HTML and a
  source URL and returns a `SourceItem` with `raw_text` populated.
- A vitest fixtures test runs a known HTML document through the connector
  and asserts the output matches the canonical fixture.

### R-SRC-009: github-releases connector

WHEN a `github-releases` source receives a list of releases, THE SYSTEM
SHALL map each release into one `SourceItem` with repo + tag in metadata.

Acceptance:
- `packages/sources/src/connectors/github-releases.ts` accepts a
  pre-fetched releases array (Octokit-shaped objects) and returns a
  `SourceItem[]`.
- A vitest fixtures test feeds a release object array into the connector
  and asserts the output matches the canonical fixture.

### R-SRC-010: URL canonicalization for dedupe

WHEN a connector emits a `SourceItem`, THE SYSTEM SHALL set
`canonical_url` to a normalized URL with utm params stripped, host
lowercased, and trailing slash trimmed.

Acceptance:
- `packages/sources/src/canonicalize.ts` exports `canonicalizeUrl(input)`
  as a pure function.
- A vitest case covers utm strip, host case-fold, trailing slash trim,
  no-op on already-canonical, unicode path, and query-key ordering.

### R-SRC-011: content hash for dedupe

WHEN a connector emits a `SourceItem`, THE SYSTEM SHALL compute
`content_hash` as a stable digest over `title + canonical_url + body`.

Acceptance:
- `packages/sources/src/hash.ts` exports `contentHash({ title,
  canonicalUrl, body })`.
- A vitest case asserts the same inputs produce the same hash and that
  changing the body changes the hash.

### R-SRC-012: provenance survives the connector

WHEN a connector emits a `SourceItem`, THE SYSTEM SHALL set
`provenance.fetcher` to `<connector>@<VERSION>`, `provenance.fetched_at`
to the call time, and `provenance.source_id` to the registry entry id.

Acceptance:
- Every full connector under `packages/sources/src/connectors/` writes the
  three fields.
- The fixtures test asserts the `provenance.fetcher` string matches the
  connector's exported `VERSION`.

### R-SRC-013: SourceType union matches the JSON Schema enum

WHEN a new source type lands, THE SYSTEM SHALL extend both the TS
`SourceType` union and the JSON Schema enum together.

Acceptance:
- `packages/sources/src/types.ts` exports `SOURCE_TYPES` as a const tuple
  and `SourceType` derived from it.
- A vitest case loads `packages/sources/schemas/source-item.schema.json`
  and asserts the `source_type.enum` array equals `SOURCE_TYPES` as a
  set.

### R-SRC-014: reliability score history

WHEN a brief run finishes, THE SYSTEM SHALL append one row to
`source_reliability_history` per active source with that week's included
rate and avg priority.

Acceptance:
- `source_reliability_history` table carries `id`, `source_id` (FK
  cascade), `week_of`, `included_rate`, `avg_priority`, `total_items`,
  `snapshot_at`.
- The write path lands in spec 0003 (run workflow); spec 0002 ships the
  table shape and FK only.

### R-SRC-015: seed loader reads sources/registry.yaml

WHEN the registry seed needs to populate `sources` for a workspace, THE
SYSTEM SHALL read `sources/registry.yaml` and produce `NewSource`
payloads without touching the database.

Acceptance:
- `packages/db/src/seeds/sources-from-registry.ts` exports
  `loadSeedSources(workspaceId)` that returns an array of insert
  payloads.
- A vitest case asserts the function returns 15 rows for the seed
  registry and that each carries the input `workspace_id`.

### R-SRC-016: registry yaml types map cleanly to SourceType

WHEN the registry yaml declares a source type that the JSON Schema enum
does not list (e.g. `vendor-news`, `blog`, `podcast+newsletter`), THE
SYSTEM SHALL map it to a canonical `SourceType` via a small mapping table
the seed loader uses.

Acceptance:
- `packages/db/src/seeds/sources-from-registry.ts` exports a
  `REGISTRY_TYPE_TO_SOURCE_TYPE` mapping that covers every distinct
  `type` value in `sources/registry.yaml`.
- A vitest case asserts the mapping is total over the registry contents.

### R-SRC-017: static source ops queue

WHEN an operator checks source operations, THE SYSTEM SHALL render a
server-side page backed by local registry and connector metadata that
shows source freshness and connector readiness without crawling source
URLs during page render.

Owner role: `product.subscriber-experience`.

Acceptance:
- `packages/sources/src/ops.ts` loads `sources/registry.yaml`, maps
  registry types to canonical `SourceType` values, reads registered
  connector versions, and computes source ops rows.
- `apps/web/src/app/ops/sources/page.tsx` lists source id, lane, registry
  type, cadence, freshness, connector type, connector version, and
  readiness status.
- A vitest case covers readiness computation against the current registry
  and fixture rows for review-due, stub-connector, and missing-mapping
  states.
- The request path performs no live network fetch.

### R-SRC-018: tier-1 ecosystem sweep registry

WHEN the W22 brief expands beyond the 52-entry tier-1 seed, THE SYSTEM
SHALL maintain a registry that spans vendor blogs, research-lab blogs,
practitioner blogs, podcasts, video channels, course pages, textbook
pages, forums, and aggregators, with verifiable URLs and per-entry
quality triples.

Owner role: `product.source-curator`.

Acceptance:
- `sources/registry.yaml` carries at least 130 active source entries
  organized into the four lanes (primary-source, fast-signal,
  builder-practice, strategy).
- Every entry carries a `quality` mapping with `signal`, `actionability`,
  and `credibility` keys; either band labels (high/medium/low) or
  integer ratings 1-5.
- Recoveries from prior W22 failures (`microsoft-ai-blog`, `cohere-blog`,
  `chip-huyen`, `latent-space`, `thursdai`, `last-week-in-ai`,
  `practical-ai`, `mlops-community`) carry the corrected URL and a
  `last_reviewed: 2026-05-29` stamp.
- The seed loader and ops queue (R-SRC-015, R-SRC-017) load the expanded
  registry without changes to the loader contract.
- `scripts/validate_registry.py` exits 0 against the expanded file.

### R-SRC-019: long-tail recovery sweep (forums + courses + textbooks + aggregators)

WHEN Workflow I's Phase 1 expansion drops a category mid-flight, THE
SYSTEM SHALL ship a follow-up sweep that lands the missing long-tail
sources (forums, community, courses, lectures, textbooks, long-form
references, aggregators, newsletters) so the W23 brief sweeps over the
full registry the W22 brief was meant to draw from.

Owner role: `product.source-curator`.

Acceptance:
- `sources/registry.yaml` carries 25 additional active entries split
  across forums + community (6), courses + lectures (7), textbooks +
  long-form (5), and aggregators + newsletters (7).
- Each new entry carries a verified canonical URL, a `quality` triple
  on the 1-5 scale, `status: active`, `last_reviewed: 2026-05-29`, and
  a `notes` line explaining quirks (e.g. WebFetch blocks Reddit).
- `version` in `sources/registry.yaml` bumps to 4.
- `scripts/validate_registry.py` exits 0 against the expanded file.
- Total active sources sit at 159 after the sweep.
