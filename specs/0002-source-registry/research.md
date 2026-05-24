# research: source registry + ingestion

Research checked 2026-05-22:

## RSS / Atom / JSON Feed shapes

- RSS 2.0 root element is `<rss version="2.0"><channel>…<item>…`. Item
  fields: `title`, `link`, `description`, `pubDate` (RFC 822), `guid`.
- Atom 1.0 root element is `<feed xmlns="http://www.w3.org/2005/Atom">`
  with `<entry>` children. Entry fields: `title`, `link[@href]`, `id`,
  `updated` (ISO 8601), `summary` or `content`.
- JSON Feed 1.1 root is `{ "version": "https://jsonfeed.org/version/1.1",
  "items": [...] }`. Items: `id`, `url`, `title`, `content_html` or
  `content_text`, `date_published`.
- The connector sniffs the first non-whitespace character: `<` is XML
  (then root tag picks RSS vs Atom); `{` is JSON Feed.

## Podcast RSS

- Apple's itunes namespace lives at
  `http://www.itunes.com/dtds/podcast-1.0.dtd`. The connector reads
  `itunes:duration` (`HH:MM:SS` or seconds), `itunes:episode`, and
  `itunes:explicit`.
- Audio lives in `<enclosure url="…" type="audio/mpeg" length="…"/>`.
  The connector treats the enclosure url as `audio_url`.

## Article extraction

- Mozilla Readability is the gold-standard extractor but it depends on
  jsdom; jsdom carries ~3MB of deps including canvas peer. The Phase 2
  connector ships a smaller heuristic: parse with a tiny HTML parser
  (a regex-based reducer over `<p>`, `<article>`, headings, list items)
  to keep the package light. Phase 3 can swap in Readability if the
  smaller parser misses content.
- The heuristic strips `<script>`, `<style>`, `<nav>`, `<header>`,
  `<footer>`, `<aside>` blocks entirely, then collapses whitespace.

## GitHub Releases

- Octokit's `repos.listReleases` returns
  `{ id, tag_name, name, body, html_url, published_at, author, ... }`.
- The connector accepts the array directly so tests do not need
  network or auth.
- Title uses `name` if present, else `tag_name`. `canonical_url` is the
  `html_url`. `raw_text` is the release body.

## URL canonicalization

- Drop `utm_*` and `gclid` query keys (matches the v3 plan note).
- Lowercase the host (RFC 3986 §6.2.2.1).
- Trim a single trailing slash from the path when the path is not the
  root `/`.
- Sort remaining query keys lexicographically (deterministic dedupe key
  across feed order).
- Drop the URL fragment (Facebook-style `#?lang=en` noise).

## Content hash

- SHA-256 over `title + "\n" + canonical_url + "\n" + (body ?? "")` as
  UTF-8. Output as lowercase hex. Length 64 — matches the schema's
  `minLength: 32` floor with headroom.

## Connector versioning

- Per the existing fixtures, the convention is `<connector>@<semver>`:
  `rss@1.0.0`, `podcast-rss@1.0.0`, `article-url@1.0.0`,
  `octokit-releases@1.0.0`. Phase 2 ships the same string.

## SourceType union sync

- The TS union and the JSON Schema enum lived as two surfaces in Phase
  0. Phase 2 derives the TS union from a const tuple, then runs a test
  asserting the JSON Schema enum equals the tuple as a set. Adding a
  source type means: extend the const tuple, extend the JSON Schema
  enum, register a connector (full or stub). The test catches drift.

## Registry yaml -> SourceType mapping

The seed registry uses verbose human-friendly type strings
(`vendor-news`, `vendor-engineering`, `blog`, `podcast+newsletter`,
`collection+book`). The JSON Schema enum is narrower
(`rss`, `podcast-rss`, `article-url`, `github-releases`, etc.). The
seed loader carries an explicit `REGISTRY_TYPE_TO_SOURCE_TYPE` map:

- `vendor-news`, `vendor-engineering`, `vendor-research`, `blog`,
  `newsletter`, `blog+newsletter`, `collection+book` -> `rss`
  (these resolve to an Atom or RSS feed at runtime; the connector
  picks based on sniffing).
- `podcast`, `podcast+newsletter` -> `podcast-rss`.
- `github-releases` -> `github-releases`.

Anything not in the map fails the seed loader. The mapping test
asserts every distinct registry type value is covered.

## Open questions parked for later

- The Readability swap (`@mozilla/readability` + `jsdom`) once we
  measure heuristic-extractor recall against a 50-article corpus
  (spec 0003 follow-up).
- ETag + Last-Modified caching shape — the runner owns the cache;
  the connector only sees fresh bytes.
- Per-source-type backoff curves — booked for the spec 0003 runner.
