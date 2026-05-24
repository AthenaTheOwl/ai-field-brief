---
id: DEC-SRC-007-podcast-rss-itunes-enclosure-parser
spec: specs/0002-source-registry/
requirement: R-SRC-007
date: 2026-05-24
status: approved
reversible: true
decision: |
  Extend feed parsing for podcast RSS by reading itunes episode fields,
  duration, and enclosure audio URL into the canonical `SourceItem`.
alternatives:
  - label: treat podcasts as plain rss
    rejected_because: |
      The transcription path needs `audio_url`; plain rss parsing would
      drop the handoff field.
  - label: defer podcast support to transcription spec
    rejected_because: |
      The source item must carry the audio URL before transcription can
      fan out.
rationale: |
  Podcast intake is one of the seed source shapes. Capturing the audio
  enclosure in Phase 2 gives spec 0004 a clear input field.
evidence:
  - kind: doc
    ref: packages/sources/src/connectors/podcast-rss.ts
  - kind: run
    ref: packages/sources/test/fixtures.test.ts
rollback: |
  Route podcast feeds through the rss connector and make the
  transcription runner locate enclosures itself.
owner: platform
---

## decision

Parse podcast RSS fields into canonical source items.

## alternatives

- Treat as plain rss: rejected because `audio_url` would be lost.
- Defer to transcription: rejected because transcription needs the
  source item first.

## rationale

The podcast connector prepares audio handoff without network behavior.

## evidence

- `packages/sources/src/connectors/podcast-rss.ts`
- `packages/sources/test/fixtures.test.ts`

## rollback

Route podcasts through rss and move enclosure extraction downstream.
