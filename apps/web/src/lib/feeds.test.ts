import { describe, expect, it } from "vitest";

import { listBriefs } from "./briefs";
import {
  buildAtomFeed,
  buildJsonFeed,
  buildRssFeed,
  SITE_URL,
} from "./feeds";

function tagValues(source: string, tagName: string): string[] {
  const tag = tagName.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return Array.from(
    source.matchAll(new RegExp(`<${tag}\\b[^>]*>([\\s\\S]*?)</${tag}>`, "g")),
    (match) => match[1] ?? "",
  );
}

function attributeValues(
  source: string,
  tagName: string,
  attributeName: string,
): string[] {
  const tag = tagName.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const attribute = attributeName.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return Array.from(source.matchAll(new RegExp(`<${tag}\\b[^>]*>`, "g")))
    .map((tagMatch) => tagMatch[0])
    .map((tagText) =>
      new RegExp(`${attribute}="([^"]+)"`).exec(tagText)?.[1] ?? "",
    );
}

interface JsonFeed {
  feed_url: string;
  items: Array<{
    id: string;
    url: string;
    title: string;
    summary: string;
    date_published: string;
  }>;
}

describe("public brief feeds", () => {
  const briefs = listBriefs();

  it("renders RSS with both published brief weeks", () => {
    const rss = buildRssFeed(briefs);

    expect(rss).toContain('<rss version="2.0"');
    expect(rss).toContain(`href="${SITE_URL}/feed.xml"`);
    expect(tagValues(rss, "title")).toEqual(
      expect.arrayContaining([
        "Contract speed, not model speed",
        "The audience sorts into shapes",
      ]),
    );
    expect(tagValues(rss, "link")).toEqual(
      expect.arrayContaining([
        `${SITE_URL}/briefs/2026-W21`,
        `${SITE_URL}/briefs/2026-W20`,
      ]),
    );
  });

  it("renders Atom with canonical entry URLs", () => {
    const atom = buildAtomFeed(briefs);

    expect(atom).toContain('<feed xmlns="http://www.w3.org/2005/Atom">');
    expect(attributeValues(atom, "link", "href")).toEqual(
      expect.arrayContaining([
        `${SITE_URL}/atom.xml`,
        `${SITE_URL}/briefs/2026-W21`,
        `${SITE_URL}/briefs/2026-W20`,
      ]),
    );
  });

  it("renders JSON Feed with metadata-backed dates and derived summaries", () => {
    const feed = JSON.parse(buildJsonFeed(briefs)) as JsonFeed;
    const w21 = feed.items.find((item) => item.id.endsWith("/2026-W21"));
    const w20 = feed.items.find((item) => item.id.endsWith("/2026-W20"));

    expect(feed.feed_url).toBe(`${SITE_URL}/feed.json`);
    expect(w21?.url).toBe(`${SITE_URL}/briefs/2026-W21`);
    expect(w21?.title).toBe("Contract speed, not model speed");
    expect(w21?.date_published).toBe("2026-05-22T00:00:00.000Z");
    expect(w21?.summary).toContain("AI is finishing its handshake");
    expect(w20?.url).toBe(`${SITE_URL}/briefs/2026-W20`);
  });
});
