import { randomUUID } from "node:crypto";

import { canonicalizeUrl } from "../canonicalize";
import type { FetchCtx } from "../contract";
import { contentHash } from "../hash";
import type { SourceItem, SourceType } from "../types";

export interface BuildSourceItemInput {
  readonly sourceType: SourceType;
  readonly fetcher: string;
  readonly title: string;
  readonly url: string;
  readonly publishedAt: string | null;
  readonly rawText: string | null;
  readonly rawHtml?: string | null;
  readonly audioUrl?: string | null;
  readonly metadata?: Record<string, unknown>;
  readonly status?: SourceItem["status"];
}

export function buildSourceItem<TConfig>(
  ctx: FetchCtx<TConfig>,
  input: BuildSourceItemInput,
): SourceItem {
  const canonicalUrl = canonicalizeUrl(input.url);
  const hashInput = {
    title: input.title,
    canonicalUrl,
    body: input.rawText ?? input.rawHtml ?? "",
  };
  return {
    id: ctx.idFactory?.() ?? randomUUID(),
    workspace_id: ctx.workspaceId,
    source_id: ctx.sourceId,
    source_type: input.sourceType,
    title: input.title,
    url: input.url,
    canonical_url: canonicalUrl,
    published_at: input.publishedAt,
    ingested_at: (ctx.now ?? new Date()).toISOString(),
    raw_text: input.rawText,
    raw_html: input.rawHtml ?? null,
    audio_url: input.audioUrl ?? null,
    audio_blob_url: null,
    content_hash: ctx.hashFactory?.(hashInput) ?? contentHash(hashInput),
    status: input.status ?? "ingested",
    metadata: input.metadata ?? {},
    provenance: {
      fetcher: input.fetcher,
      fetched_at: (ctx.now ?? new Date()).toISOString(),
      source_id: ctx.sourceId,
      source_version: ctx.sourceVersion ?? null,
      request: ctx.request,
      response_status: ctx.responseStatus ?? null,
      rate_limit: ctx.rateLimit ?? null,
    },
    error: null,
  };
}

export function decodeEntities(input: string): string {
  return input
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/<!\[CDATA\[(.*?)\]\]>/gs, "$1");
}

export function stripHtml(input: string): string {
  return decodeEntities(input)
    .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, " ")
    .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

export function tagText(block: string, tagName: string): string | null {
  const escaped = tagName.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const match = new RegExp(`<${escaped}\\b[^>]*>([\\s\\S]*?)<\\/${escaped}>`, "i").exec(block);
  return match?.[1] ? stripHtml(match[1]) : null;
}

export function attrValue(block: string, tagName: string, attrName: string): string | null {
  const tagMatch = new RegExp(`<${tagName}\\b([^>]*)>`, "i").exec(block);
  const attrs = tagMatch?.[1];
  if (!attrs) {
    return null;
  }
  const attrMatch = new RegExp(`${attrName}=["']([^"']+)["']`, "i").exec(attrs);
  return attrMatch?.[1] ?? null;
}

export function isoDate(input: string | null): string | null {
  if (!input) {
    return null;
  }
  const time = Date.parse(input);
  return Number.isNaN(time) ? null : new Date(time).toISOString().replace(".000Z", "Z");
}

export function durationSeconds(input: string | null): number | null {
  if (!input) {
    return null;
  }
  if (/^\d+$/.test(input)) {
    return Number(input);
  }
  const parts = input.split(":").map((part) => Number(part));
  if (parts.some((part) => Number.isNaN(part))) {
    return null;
  }
  if (parts.length === 3) {
    const [hours, minutes, seconds] = parts as [number, number, number];
    return hours * 3600 + minutes * 60 + seconds;
  }
  if (parts.length === 2) {
    const [minutes, seconds] = parts as [number, number];
    return minutes * 60 + seconds;
  }
  return null;
}
