import type { Connector, FetchCtx } from "../contract";
import { ConnectorInputError } from "../contract";
import { registerConnector } from "../registry";
import type { SourceItem } from "../types";
import { buildSourceItem, stripHtml, tagText } from "./helpers";

export const VERSION = "1.0.0";

export interface ArticleUrlConfig {
  readonly byline?: string | null;
  readonly publishedAt?: string | null;
  readonly language?: string | null;
}

export const articleUrlConnector: Connector<ArticleUrlConfig> = {
  sourceType: "article-url",
  version: VERSION,
  async fetch(ctx: FetchCtx<ArticleUrlConfig>): Promise<SourceItem[]> {
    if (ctx.raw.kind !== "html") {
      throw new ConnectorInputError("article-url connector expects html input");
    }
    const title = tagText(ctx.raw.html, "h1") ?? tagText(ctx.raw.html, "title") ?? ctx.raw.url;
    const rawText = extractArticleText(ctx.raw.html);
    return [
      buildSourceItem(ctx, {
        sourceType: "article-url",
        fetcher: `article-url@${VERSION}`,
        title,
        url: ctx.raw.url,
        publishedAt: ctx.config.publishedAt ?? null,
        rawText,
        rawHtml: ctx.raw.html,
        status: "extracted",
        metadata: {
          byline: ctx.config.byline ?? null,
          reading_time_minutes: Math.max(1, Math.ceil(rawText.split(/\s+/).length / 220)),
          language: ctx.config.language ?? "en",
        },
      }),
    ];
  },
};

function extractArticleText(html: string): string {
  const body =
    /<article\b[^>]*>([\s\S]*?)<\/article>/i.exec(html)?.[1] ??
    /<main\b[^>]*>([\s\S]*?)<\/main>/i.exec(html)?.[1] ??
    html;
  return stripHtml(
    body
      .replace(/<h1\b[^>]*>[\s\S]*?<\/h1>/gi, " ")
      .replace(/<nav\b[^>]*>[\s\S]*?<\/nav>/gi, " ")
      .replace(/<header\b[^>]*>[\s\S]*?<\/header>/gi, " ")
      .replace(/<footer\b[^>]*>[\s\S]*?<\/footer>/gi, " ")
      .replace(/<aside\b[^>]*>[\s\S]*?<\/aside>/gi, " "),
  );
}

registerConnector(articleUrlConnector);
