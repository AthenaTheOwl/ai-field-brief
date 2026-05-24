import type { Connector, FetchCtx } from "../contract";
import { ConnectorInputError } from "../contract";
import { registerConnector } from "../registry";
import type { SourceItem } from "../types";
import {
  attrValue,
  buildSourceItem,
  decodeEntities,
  isoDate,
  stripHtml,
  tagText,
} from "./helpers";

export const VERSION = "1.0.0";

export interface RssConfig {
  readonly feedUrl?: string;
}

interface ParsedFeedItem {
  readonly title: string;
  readonly url: string;
  readonly publishedAt: string | null;
  readonly rawText: string | null;
  readonly metadata: Record<string, unknown>;
}

export const rssConnector: Connector<RssConfig> = {
  sourceType: "rss",
  version: VERSION,
  async fetch(ctx: FetchCtx<RssConfig>): Promise<SourceItem[]> {
    if (ctx.raw.kind !== "bytes") {
      throw new ConnectorInputError("rss connector expects bytes input");
    }
    return parseRssLike(ctx.raw.text).map((item) =>
      buildSourceItem(ctx, {
        sourceType: "rss",
        fetcher: `rss@${VERSION}`,
        title: item.title,
        url: item.url,
        publishedAt: item.publishedAt,
        rawText: item.rawText,
        metadata: {
          ...item.metadata,
          feed_url: ctx.config.feedUrl ?? null,
        },
      }),
    );
  },
};

export function parseRssLike(text: string): ParsedFeedItem[] {
  const trimmed = text.trim();
  if (trimmed.startsWith("{")) {
    return parseJsonFeed(trimmed);
  }
  if (/<feed\b/i.test(trimmed)) {
    return parseAtom(trimmed);
  }
  return parseRss(trimmed);
}

function parseJsonFeed(text: string): ParsedFeedItem[] {
  const parsed = JSON.parse(text) as {
    readonly items?: readonly {
      readonly id?: string;
      readonly url?: string;
      readonly title?: string;
      readonly content_html?: string;
      readonly content_text?: string;
      readonly date_published?: string;
      readonly tags?: readonly string[];
    }[];
  };
  return (parsed.items ?? []).flatMap((item) => {
    if (!item.title || !item.url) {
      return [];
    }
    const body = item.content_text ?? stripHtml(item.content_html ?? "");
    return [{
      title: item.title,
      url: item.url,
      publishedAt: isoDate(item.date_published ?? null),
      rawText: body || null,
      metadata: {
        guid: item.id ?? item.url,
        categories: item.tags ?? [],
      },
    }];
  });
}

function parseRss(text: string): ParsedFeedItem[] {
  const blocks = matchBlocks(text, "item");
  return blocks.flatMap((block) => {
    const title = tagText(block, "title");
    const url = tagText(block, "link") ?? tagText(block, "guid");
    if (!title || !url) {
      return [];
    }
    return [{
      title,
      url,
      publishedAt: isoDate(tagText(block, "pubDate")),
      rawText: tagText(block, "description"),
      metadata: {
        guid: tagText(block, "guid") ?? url,
        categories: matchBlocks(block, "category").map((entry) => decodeEntities(stripHtml(entry))),
      },
    }];
  });
}

function parseAtom(text: string): ParsedFeedItem[] {
  const blocks = matchBlocks(text, "entry");
  return blocks.flatMap((block) => {
    const title = tagText(block, "title");
    const url = attrValue(block, "link", "href") ?? tagText(block, "id");
    if (!title || !url) {
      return [];
    }
    return [{
      title,
      url,
      publishedAt: isoDate(tagText(block, "updated") ?? tagText(block, "published")),
      rawText: tagText(block, "summary") ?? tagText(block, "content"),
      metadata: {
        guid: tagText(block, "id") ?? url,
        categories: [],
      },
    }];
  });
}

function matchBlocks(text: string, tagName: string): string[] {
  return Array.from(
    text.matchAll(new RegExp(`<${tagName}\\b[^>]*>([\\s\\S]*?)<\\/${tagName}>`, "gi")),
    (match) => match[1] ?? "",
  );
}

registerConnector(rssConnector);
