import type { ContentHashInput } from "./hash";
import type { SourceItem, SourceType } from "./types";

export interface BytesInput {
  readonly kind: "bytes";
  readonly text: string;
}

export interface HtmlInput {
  readonly kind: "html";
  readonly html: string;
  readonly url: string;
}

export interface GithubReleaseLike {
  readonly id: number;
  readonly tag_name: string;
  readonly name?: string | null;
  readonly body?: string | null;
  readonly html_url: string;
  readonly published_at?: string | null;
  readonly author?: { readonly login?: string | null } | null;
}

export interface GithubReleasesInput {
  readonly kind: "github-releases";
  readonly releases: readonly GithubReleaseLike[];
}

export type ConnectorInput = BytesInput | HtmlInput | GithubReleasesInput;

export interface FetchCtx<TConfig = unknown> {
  readonly workspaceId: string;
  readonly sourceId: string;
  readonly config: TConfig;
  readonly raw: ConnectorInput;
  readonly now?: Date;
  readonly lastCursor?: string | null;
  readonly sourceVersion?: string | null;
  readonly responseStatus?: number | null;
  readonly request?: Record<string, unknown>;
  readonly rateLimit?: Record<string, unknown> | null;
  readonly idFactory?: () => string;
  readonly hashFactory?: (input: ContentHashInput) => string;
}

export interface Connector<TConfig = unknown> {
  readonly sourceType: SourceType;
  readonly version: string;
  fetch(ctx: FetchCtx<TConfig>): Promise<SourceItem[]>;
}

export class ConnectorInputError extends Error {
  public constructor(message: string) {
    super(message);
    this.name = "ConnectorInputError";
  }
}

export class NotImplementedError extends Error {
  public constructor(sourceType: SourceType) {
    super(`source connector not implemented: ${sourceType}`);
    this.name = "NotImplementedError";
  }
}
