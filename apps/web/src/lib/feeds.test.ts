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
  const latest = briefs[0];
  const previous = briefs[1];

  if (!latest || !previous) {
    throw new Error("feed tests require at least two published briefs");
  }

  it("renders RSS with discovered published brief weeks", () => {
    const rss = buildRssFeed(briefs);

    expect(rss).toContain('<rss version="2.0"');
    expect(rss).toContain(`href="${SITE_URL}/feed.xml"`);
    expect(tagValues(rss, "title")).toEqual(
      expect.arrayContaining([latest.title, previous.title]),
    );
    expect(tagValues(rss, "link")).toEqual(
      expect.arrayContaining([
        `${SITE_URL}/briefs/${latest.week}`,
        `${SITE_URL}/briefs/${previous.week}`,
      ]),
    );
  });

  it("renders Atom with canonical entry URLs", () => {
    const atom = buildAtomFeed(briefs);

    expect(atom).toContain('<feed xmlns="http://www.w3.org/2005/Atom">');
    expect(attributeValues(atom, "link", "href")).toEqual(
      expect.arrayContaining([
        `${SITE_URL}/atom.xml`,
        `${SITE_URL}/briefs/${latest.week}`,
        `${SITE_URL}/briefs/${previous.week}`,
      ]),
    );
  });

  it("renders JSON Feed with metadata-backed dates and derived summaries", () => {
    const feed = JSON.parse(buildJsonFeed(briefs)) as JsonFeed;
    const latestItem = feed.items.find((item) =>
      item.id.endsWith(`/${latest.week}`),
    );
    const previousItem = feed.items.find((item) =>
      item.id.endsWith(`/${previous.week}`),
    );

    expect(feed.feed_url).toBe(`${SITE_URL}/feed.json`);
    expect(latestItem?.url).toBe(`${SITE_URL}/briefs/${latest.week}`);
    expect(latestItem?.title).toBe(latest.title);
    expect(latestItem?.date_published).toBe(
      `${latest.date}T00:00:00.000Z`,
    );
    expect(latestItem?.summary.length).toBeGreaterThan(40);
    expect(previousItem?.url).toBe(`${SITE_URL}/briefs/${previous.week}`);
  });
});
