import type { BriefRecord } from "./briefs";

export const SITE_URL = "https://ai-field-brief.vercel.app";

const FEED_TITLE = "ai-field-brief";
const FEED_DESCRIPTION =
  "Weekly AI digest for builder-TPMs, with concrete moves and worked examples.";

interface FeedItem {
  id: string;
  url: string;
  title: string;
  summary: string;
  publishedIso: string;
  publishedRfc822: string;
}

function absoluteUrl(pathname: string): string {
  return `${SITE_URL}${pathname}`;
}

function xmlEscape(value: string): string {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

function normalizeText(value: string): string {
  return value.replace(/\s+/g, " ").trim();
}

function stripMarkdown(value: string): string {
  return normalizeText(
    value
      .replace(/```[\s\S]*?```/g, "")
      .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
      .replace(/[*_`]/g, ""),
  );
}

export function getBriefSummary(brief: BriefRecord): string {
  const metadataSummary = brief.meta?.summary?.trim();
  if (metadataSummary) {
    return metadataSummary;
  }

  const body = brief.markdown
    .replace(/^#\s+.+?\n+/, "")
    .replace(/^\*\*.+?\*\*\s*/s, "")
    .trim();

  const openingParagraph = body
    .split(/\n\s*\n/)
    .map((paragraph) => paragraph.trim())
    .find(
      (paragraph) =>
        paragraph.length > 0 &&
        paragraph !== "---" &&
        !paragraph.startsWith("##"),
    );

  return stripMarkdown(openingParagraph ?? brief.title);
}

function publishedDate(brief: BriefRecord): Date {
  const value = brief.date || brief.meta?.generated_at;
  const date = value
    ? new Date(value.includes("T") ? value : `${value}T00:00:00.000Z`)
    : new Date(0);

  if (Number.isNaN(date.getTime())) {
    return new Date(0);
  }
  return date;
}

function toFeedItem(brief: BriefRecord): FeedItem {
  const url = absoluteUrl(`/briefs/${brief.week}`);
  const date = publishedDate(brief);
  return {
    id: url,
    url,
    title: brief.title,
    summary: getBriefSummary(brief),
    publishedIso: date.toISOString(),
    publishedRfc822: date.toUTCString(),
  };
}

function latestUpdatedIso(items: FeedItem[]): string {
  return items[0]?.publishedIso ?? new Date(0).toISOString();
}

function latestUpdatedRfc822(items: FeedItem[]): string {
  return items[0]?.publishedRfc822 ?? new Date(0).toUTCString();
}

export function buildRssFeed(briefs: BriefRecord[]): string {
  const items = briefs.map(toFeedItem);
  const feedUrl = absoluteUrl("/feed.xml");

  return `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>${xmlEscape(FEED_TITLE)}</title>
    <link>${xmlEscape(SITE_URL)}</link>
    <description>${xmlEscape(FEED_DESCRIPTION)}</description>
    <language>en-US</language>
    <lastBuildDate>${xmlEscape(latestUpdatedRfc822(items))}</lastBuildDate>
    <atom:link href="${xmlEscape(feedUrl)}" rel="self" type="application/rss+xml" />
${items
  .map(
    (item) => `    <item>
      <title>${xmlEscape(item.title)}</title>
      <link>${xmlEscape(item.url)}</link>
      <guid isPermaLink="true">${xmlEscape(item.id)}</guid>
      <pubDate>${xmlEscape(item.publishedRfc822)}</pubDate>
      <description>${xmlEscape(item.summary)}</description>
    </item>`,
  )
  .join("\n")}
  </channel>
</rss>
`;
}

export function buildAtomFeed(briefs: BriefRecord[]): string {
  const items = briefs.map(toFeedItem);
  const feedUrl = absoluteUrl("/atom.xml");

  return `<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>${xmlEscape(FEED_TITLE)}</title>
  <subtitle>${xmlEscape(FEED_DESCRIPTION)}</subtitle>
  <id>${xmlEscape(SITE_URL)}</id>
  <updated>${xmlEscape(latestUpdatedIso(items))}</updated>
  <link href="${xmlEscape(SITE_URL)}" rel="alternate" />
  <link href="${xmlEscape(feedUrl)}" rel="self" type="application/atom+xml" />
${items
  .map(
    (item) => `  <entry>
    <title>${xmlEscape(item.title)}</title>
    <id>${xmlEscape(item.id)}</id>
    <link href="${xmlEscape(item.url)}" />
    <published>${xmlEscape(item.publishedIso)}</published>
    <updated>${xmlEscape(item.publishedIso)}</updated>
    <summary>${xmlEscape(item.summary)}</summary>
  </entry>`,
  )
  .join("\n")}
</feed>
`;
}

export function buildJsonFeed(briefs: BriefRecord[]): string {
  const items = briefs.map(toFeedItem);

  return `${JSON.stringify(
    {
      version: "https://jsonfeed.org/version/1.1",
      title: FEED_TITLE,
      home_page_url: SITE_URL,
      feed_url: absoluteUrl("/feed.json"),
      description: FEED_DESCRIPTION,
      language: "en-US",
      items: items.map((item) => ({
        id: item.id,
        url: item.url,
        title: item.title,
        summary: item.summary,
        content_text: item.summary,
        date_published: item.publishedIso,
      })),
    },
    null,
    2,
  )}\n`;
}
