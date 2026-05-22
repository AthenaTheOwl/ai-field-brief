# @aifieldbrief/sources

Connector contracts and fixtures. Connector implementations land in later
phases; this package's job in Phase 0 is to make sure those implementations
are gated on schemas that already exist.

## Contracts

- `schemas/source-item.schema.json` — canonical shape for any item ingested
  from any source type (RSS, podcast, YouTube, article, vendor changelog,
  arXiv, HF Papers, inbox-forward, Slack/Discord, Twitter/X, Reddit, HN,
  GitHub releases, generic webhook).
- `schemas/transcript.schema.json` — diarized transcript for audio/video.
- `schemas/citation.schema.json` — citation pointing into a source-item's
  raw text or a transcript span; required on every claim in a published
  brief (R-BOOT-004).
- `schemas/provenance.schema.json` — fetcher, fetched_at, source_id,
  source_version — survives into brief citations (R-BOOT-002).

Each schema has a sibling `*.fixtures.json` covering the seven seed source
types from `specs/0000-bootstrap/tasks.md`:

- RSS feed item
- Podcast RSS episode
- YouTube video
- Article URL
- GitHub release
- Generic webhook push
- Forwarded email (inbox)

`scripts/validate_schemas.py` reads every fixture in those arrays and
validates them against the matching schema. When `jsonschema` is installed
the validation is strict; without it the script still parses both files
and warns.

## Rule

> No connector without fixtures.

Adding a new source type means: add a fixture entry to
`source-item.fixtures.json` (and to the relevant transcript fixtures if the
source has audio), get the gate green, then build the connector. The
connector's first test reads the fixture, calls the connector, and
asserts the output equals the fixture.
