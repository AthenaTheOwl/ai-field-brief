import { readFileSync } from "node:fs";

import { describe, expect, it } from "vitest";

import { getConnector, type SourceItem } from "../src";

const fixtures = JSON.parse(
  readFileSync(new URL("../schemas/source-item.fixtures.json", import.meta.url), "utf8"),
) as SourceItem[];

function fixture(sourceType: SourceItem["source_type"]): SourceItem {
  const found = fixtures.find((entry) => entry.source_type === sourceType);
  if (!found) {
    throw new Error(`missing fixture for ${sourceType}`);
  }
  return found;
}

function testCtx(expected: SourceItem, raw: Parameters<ReturnType<typeof getConnector>["fetch"]>[0]["raw"], config: unknown) {
  return {
    workspaceId: expected.workspace_id,
    sourceId: expected.source_id,
    config,
    raw,
    now: new Date(expected.ingested_at),
    sourceVersion: expected.provenance.source_version ?? null,
    responseStatus: expected.provenance.response_status ?? null,
    rateLimit: expected.provenance.rate_limit ?? null,
    request: expected.provenance.request,
    idFactory: () => expected.id,
    hashFactory: () => expected.content_hash,
  };
}

function expectCanonical(actual: SourceItem, expected: SourceItem): void {
  expect(actual.id).toBe(expected.id);
  expect(actual.workspace_id).toBe(expected.workspace_id);
  expect(actual.source_id).toBe(expected.source_id);
  expect(actual.source_type).toBe(expected.source_type);
  expect(actual.title).toBe(expected.title);
  expect(actual.url).toBe(expected.url);
  expect(actual.canonical_url).toBe(expected.canonical_url);
  expect(actual.published_at).toBe(expected.published_at);
  expect(actual.raw_text).toBe(expected.raw_text);
  expect(actual.audio_url).toBe(expected.audio_url ?? null);
  expect(actual.content_hash).toBe(expected.content_hash);
  expect(actual.provenance.fetcher).toBe(expected.provenance.fetcher);
}

describe("full connector fixtures", () => {
  it("round-trips the rss fixture", async () => {
    const expected = fixture("rss");
    const xml = `
      <rss version="2.0"><channel><item>
        <title>${expected.title}</title>
        <link>${expected.url}</link>
        <description>${expected.raw_text}</description>
        <pubDate>Fri, 15 May 2026 14:00:00 GMT</pubDate>
        <guid>${expected.metadata?.guid as string}</guid>
        <category>agents</category><category>eval</category>
      </item></channel></rss>
    `;
    const rows = await getConnector("rss").fetch(
      testCtx(expected, { kind: "bytes", text: xml }, { feedUrl: expected.metadata?.feed_url }),
    );
    expectCanonical(rows[0] as SourceItem, expected);
  });

  it("round-trips the podcast-rss fixture", async () => {
    const expected = fixture("podcast-rss");
    const xml = `
      <rss version="2.0"><channel><item>
        <title>${expected.title}</title>
        <link>${expected.url}</link>
        <description>${expected.raw_text}</description>
        <pubDate>Thu, 14 May 2026 08:00:00 GMT</pubDate>
        <itunes:episode>142</itunes:episode>
        <itunes:duration>00:59:00</itunes:duration>
        <enclosure url="${expected.audio_url}" type="audio/mpeg" />
      </item></channel></rss>
    `;
    const rows = await getConnector("podcast-rss").fetch(
      testCtx(expected, { kind: "bytes", text: xml }, { feedUrl: expected.metadata?.feed_url }),
    );
    expectCanonical(rows[0] as SourceItem, expected);
    expect(rows[0]?.metadata?.duration_seconds).toBe(3540);
  });

  it("round-trips the article-url fixture", async () => {
    const expected = fixture("article-url");
    const html = `
      <html><head><title>${expected.title}</title></head>
      <body><article><h1>${expected.title}</h1><p>${expected.raw_text}</p></article></body></html>
    `;
    const rows = await getConnector("article-url").fetch(
      testCtx(
        expected,
        { kind: "html", html, url: expected.url },
        { byline: "J. Doe", publishedAt: expected.published_at, language: "en" },
      ),
    );
    expectCanonical(rows[0] as SourceItem, expected);
  });

  it("round-trips the github-releases fixture", async () => {
    const expected = fixture("github-releases");
    const rows = await getConnector("github-releases").fetch(
      testCtx(
        expected,
        {
          kind: "github-releases",
          releases: [{
            id: 12345678,
            tag_name: "v1.42.0",
            name: "v1.42.0",
            body: expected.raw_text,
            html_url: expected.url,
            published_at: expected.published_at,
          }],
        },
        { repo: "anthropics/anthropic-sdk-python" },
      ),
    );
    expectCanonical(rows[0] as SourceItem, expected);
  });
});
