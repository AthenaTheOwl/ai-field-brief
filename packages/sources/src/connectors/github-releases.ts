import type { Connector, FetchCtx, GithubReleaseLike } from "../contract";
import { ConnectorInputError } from "../contract";
import { registerConnector } from "../registry";
import type { SourceItem } from "../types";
import { buildSourceItem } from "./helpers";

export const VERSION = "1.0.0";

export interface GithubReleasesConfig {
  readonly repo: string;
}

export const githubReleasesConnector: Connector<GithubReleasesConfig> = {
  sourceType: "github-releases",
  version: VERSION,
  async fetch(ctx: FetchCtx<GithubReleasesConfig>): Promise<SourceItem[]> {
    if (ctx.raw.kind !== "github-releases") {
      throw new ConnectorInputError("github-releases connector expects releases input");
    }
    const repoName = ctx.config.repo.split("/").at(-1) ?? ctx.config.repo;
    return ctx.raw.releases.map((release: GithubReleaseLike) =>
      buildSourceItem(ctx, {
        sourceType: "github-releases",
        fetcher: `octokit-releases@${VERSION}`,
        title: `${repoName} ${release.name ?? release.tag_name}`,
        url: release.html_url,
        publishedAt: release.published_at ?? null,
        rawText: release.body ?? null,
        metadata: {
          repo: ctx.config.repo,
          tag: release.tag_name,
          release_id: release.id,
          author: release.author?.login ?? null,
        },
      }),
    );
  },
};

registerConnector(githubReleasesConnector);
