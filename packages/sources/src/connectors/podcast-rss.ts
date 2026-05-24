import type { Connector, FetchCtx } from "../contract";
import { ConnectorInputError } from "../contract";
import { registerConnector } from "../registry";
import type { SourceItem } from "../types";
import {
  attrValue,
  buildSourceItem,
  durationSeconds,
  isoDate,
  stripHtml,
  tagText,
} from "./helpers";

export const VERSION = "1.0.0";

export interface PodcastRssConfig {
  readonly feedUrl?: string;
}

export const podcastRssConnector: Connector<PodcastRssConfig> = {
  sourceType: "podcast-rss",
  version: VERSION,
  async fetch(ctx: FetchCtx<PodcastRssConfig>): Promise<SourceItem[]> {
    if (ctx.raw.kind !== "bytes") {
      throw new ConnectorInputError("podcast-rss connector expects bytes input");
    }
    return parsePodcastRss(ctx.raw.text).map((item) =>
      buildSourceItem(ctx, {
        sourceType: "podcast-rss",
        fetcher: `podcast-rss@${VERSION}`,
        title: item.title,
        url: item.url,
        publishedAt: item.publishedAt,
        rawText: item.rawText,
        audioUrl: item.audioUrl,
        status: "transcribing",
        metadata: {
          feed_url: ctx.config.feedUrl ?? null,
          episode_number: item.episodeNumber,
          duration_seconds: item.durationSeconds,
        },
      }),
    );
  },
};

interface ParsedPodcastItem {
  readonly title: string;
  readonly url: string;
  readonly publishedAt: string | null;
  readonly rawText: string | null;
  readonly audioUrl: string | null;
  readonly episodeNumber: number | null;
  readonly durationSeconds: number | null;
}

function parsePodcastRss(text: string): ParsedPodcastItem[] {
  return Array.from(
    text.matchAll(/<item\b[^>]*>([\s\S]*?)<\/item>/gi),
    (match) => match[1] ?? "",
  ).flatMap((block) => {
    const title = tagText(block, "title");
    const url = tagText(block, "link") ?? tagText(block, "guid");
    if (!title || !url) {
      return [];
    }
    const enclosure = attrValue(block, "enclosure", "url");
    const episode = tagText(block, "itunes:episode");
    return [{
      title,
      url,
      publishedAt: isoDate(tagText(block, "pubDate")),
      rawText: tagText(block, "description") ?? stripHtml(tagText(block, "content:encoded") ?? ""),
      audioUrl: enclosure,
      episodeNumber: episode ? Number(episode) : null,
      durationSeconds: durationSeconds(tagText(block, "itunes:duration")),
    }];
  });
}

registerConnector(podcastRssConnector);
