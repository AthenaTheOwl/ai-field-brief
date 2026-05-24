/**
 * Canonical types for ingestion (R-SRC-013).
 *
 * `SOURCE_TYPES` stays in sync with the `source_type.enum` in
 * `schemas/source-item.schema.json`. A vitest case asserts the two
 * surfaces match as a set, so adding a new type means: extend this
 * tuple, extend the JSON schema enum, register a connector.
 */

export const SOURCE_TYPES = [
  "rss",
  "podcast-rss",
  "blog-rss",
  "newsletter-rss",
  "youtube-channel",
  "youtube-playlist",
  "article-url",
  "vendor-changelog",
  "arxiv-feed",
  "hf-papers",
  "inbox-forward",
  "slack-channel",
  "discord-channel",
  "twitter-list",
  "reddit-subreddit",
  "hn-feed",
  "github-releases",
  "webhook-push",
] as const;

export type SourceType = (typeof SOURCE_TYPES)[number];

export const SOURCE_ITEM_STATUS = [
  "ingested",
  "normalized",
  "transcribing",
  "transcribed",
  "extracted",
  "scored",
  "included",
  "dropped",
  "failed",
] as const;

export type SourceItemStatus = (typeof SOURCE_ITEM_STATUS)[number];

export interface Provenance {
  readonly fetcher: string;
  readonly fetched_at: string;
  readonly source_id: string;
  readonly source_version?: string | null;
  readonly request?: Record<string, unknown>;
  readonly response_status?: number | null;
  readonly rate_limit?: Record<string, unknown> | null;
}

export interface SourceItem {
  readonly id: string;
  readonly workspace_id: string;
  readonly source_id: string;
  readonly source_type: SourceType;
  readonly title: string;
  readonly url: string;
  readonly canonical_url: string;
  readonly published_at: string | null;
  readonly ingested_at: string;
  readonly raw_text: string | null;
  readonly raw_html: string | null;
  readonly raw_html_blob_url?: string | null;
  readonly audio_url: string | null;
  readonly audio_blob_url?: string | null;
  readonly content_hash: string;
  readonly status: SourceItemStatus;
  readonly metadata?: Record<string, unknown>;
  readonly provenance: Provenance;
  readonly error?: string | null;
}

export interface TranscriptSegment {
  readonly start: number;
  readonly end: number;
  readonly speaker: string;
  readonly text: string;
  readonly confidence?: number | null;
}

export interface Transcript {
  readonly id: string;
  readonly source_item_id: string;
  readonly workspace_id: string;
  readonly model: string;
  readonly language: string;
  readonly duration_seconds: number;
  readonly cost_usd?: number | null;
  readonly created_at: string;
  readonly audio_blob_url?: string | null;
  readonly audio_retention_until?: string | null;
  readonly segments: readonly TranscriptSegment[];
}

export type CitationTarget =
  | { readonly kind: "source_item"; readonly source_item_id: string }
  | {
      readonly kind: "transcript";
      readonly transcript_id: string;
      readonly segment_index?: number | null;
    };

export interface Citation {
  readonly id: string;
  readonly workspace_id: string;
  readonly claim_id: string;
  readonly target: CitationTarget;
  readonly span: {
    readonly text: string;
    readonly start_offset: number;
    readonly end_offset: number;
  };
  readonly verified?: boolean | null;
  readonly verifier_model?: string | null;
  readonly verified_at?: string | null;
}
