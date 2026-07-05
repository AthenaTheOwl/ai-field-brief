import { existsSync, readFileSync } from "node:fs";
import { join, resolve } from "node:path";

import type { Connector } from "./contract";
import { getConnector } from "./registry";
import { SOURCE_TYPES, type SourceType } from "./types";

import "./connectors/rss";
import "./connectors/podcast-rss";
import "./connectors/article-url";
import "./connectors/github-releases";
import "./connectors/stubs";

export const REGISTRY_TYPE_TO_SOURCE_TYPE: Record<string, SourceType> = {
  "article-url": "article-url",
  "arxiv-feed": "arxiv-feed",
  "vendor-news": "rss",
  "vendor-engineering": "rss",
  "vendor-research": "rss",
  "research-lab-blog": "blog-rss",
  blog: "rss",
  "blog-rss": "blog-rss",
  newsletter: "rss",
  "newsletter-rss": "newsletter-rss",
  "blog+newsletter": "rss",
  "collection+book": "rss",
  podcast: "podcast-rss",
  "podcast-rss": "podcast-rss",
  "podcast+newsletter": "podcast-rss",
  "hf-papers": "hf-papers",
  "hn-feed": "hn-feed",
  "reddit-subreddit": "reddit-subreddit",
  rss: "rss",
  "github-releases": "github-releases",
  "youtube-channel": "youtube-channel",
  "youtube-playlist": "youtube-playlist",
  // Documentation/standards sites are plain URL fetches (no feed), so they
  // ingest through the article-url connector like other one-URL sources.
  "framework-docs": "article-url",
  "standards-docs": "article-url",
};

export interface SourceRegistryDocument {
  readonly version: string | number | null;
  readonly lastCurated: string | null;
  readonly defaultReviewFrequency: string | null;
  readonly sources: readonly SourceRegistrySource[];
}

export interface SourceRegistrySource {
  readonly id: string;
  readonly name: string;
  readonly type: string;
  readonly lane: string;
  readonly url: string;
  readonly cadence: string | null;
  readonly reviewFrequency: string | null;
  readonly intake: string;
  readonly status: string;
  readonly lastReviewed: string | null;
  readonly notes: string | null;
  readonly quality?: {
    readonly signal?: string | number;
    readonly actionability?: string | number;
    readonly credibility?: string | number;
  };
}

export type SourceFreshnessStatus = "fresh" | "due" | "overdue" | "unknown";

export type SourceReadinessStatus =
  | "ready"
  | "review-due"
  | "connector-stub"
  | "connector-missing"
  | "mapping-missing"
  | "source-inactive";

export interface SourceOpsRow {
  readonly id: string;
  readonly name: string;
  readonly lane: string;
  readonly registryType: string;
  readonly sourceType: SourceType | null;
  readonly cadence: string | null;
  readonly reviewFrequency: string | null;
  readonly lastReviewed: string | null;
  readonly freshnessStatus: SourceFreshnessStatus;
  readonly freshnessLabel: string;
  readonly nextReviewDate: string | null;
  readonly connectorType: SourceType | null;
  readonly connectorVersion: string | null;
  readonly connectorImplemented: boolean;
  readonly readinessStatus: SourceReadinessStatus;
  readonly readinessReason: string;
}

export interface SourceOpsQueue {
  readonly generatedAt: string;
  readonly rows: readonly SourceOpsRow[];
  readonly summary: {
    readonly total: number;
    readonly ready: number;
    readonly reviewDue: number;
    readonly connectorBlocked: number;
    readonly inactive: number;
  };
}

export interface BuildSourceOpsQueueOptions {
  readonly registryPath?: string;
  readonly registryText?: string;
  readonly asOf?: Date;
}

const REVIEW_FREQUENCY_DAYS: Record<string, number> = {
  daily: 1,
  weekly: 7,
  biweekly: 14,
  monthly: 30,
  quarterly: 90,
};

const SOURCE_TYPE_SET = new Set<string>(SOURCE_TYPES);

export function loadSourceRegistry(
  registryPath = findDefaultRegistryPath(),
): SourceRegistryDocument {
  return parseSourceRegistryYaml(readFileSync(registryPath, "utf8"));
}

export function parseSourceRegistryYaml(text: string): SourceRegistryDocument {
  const topLevel: Record<string, string | number | null> = {};
  const sources: SourceRegistrySource[] = [];
  let inSources = false;
  let current: Record<string, unknown> | null = null;
  let nestedKey: "quality" | null = null;
  let pendingBlockKey: string | null = null;
  let pendingBlockIndent = -1;
  const pendingBlock: string[] = [];

  function flushBlock(): void {
    if (current && pendingBlockKey) {
      current[pendingBlockKey] = pendingBlock.join("\n").trim();
    }
    pendingBlockKey = null;
    pendingBlockIndent = -1;
    pendingBlock.length = 0;
  }

  for (const rawLine of text.split(/\r?\n/)) {
    const line = rawLine.replace(/\r$/, "");
    if (!line.trim() || line.trimStart().startsWith("#")) {
      continue;
    }
    const indent = line.length - line.trimStart().length;
    const trimmed = line.trim();

    if (pendingBlockKey && indent > pendingBlockIndent) {
      pendingBlock.push(trimmed);
      continue;
    }
    flushBlock();

    if (indent === 0) {
      if (trimmed === "sources:") {
        inSources = true;
        continue;
      }
      inSources = false;
      if (trimmed.includes(":")) {
        const [key, value] = splitKeyValue(trimmed);
        topLevel[key] = parseScalar(value);
      }
      continue;
    }

    if (!inSources) {
      continue;
    }
    if (indent === 2 && trimmed.startsWith("- ")) {
      nestedKey = null;
      current = {};
      sources.push(current as unknown as SourceRegistrySource);
      const rest = trimmed.slice(2);
      if (rest.includes(":")) {
        const [key, value] = splitKeyValue(rest);
        current[toCamelKey(key)] = parseScalar(value);
      }
      continue;
    }
    if (!current || indent < 4) {
      continue;
    }
    if (indent === 4 && trimmed === "quality:") {
      nestedKey = "quality";
      current.quality = {};
      continue;
    }
    if (indent === 4) {
      nestedKey = null;
      const [key, value] = splitKeyValue(trimmed);
      const camelKey = toCamelKey(key);
      if (value === ">-" || value === "|") {
        pendingBlockKey = camelKey;
        pendingBlockIndent = indent;
      } else {
        current[camelKey] = parseScalar(value);
      }
      continue;
    }
    if (indent === 6 && nestedKey === "quality") {
      const [key, value] = splitKeyValue(trimmed);
      const quality = current.quality as Record<string, unknown>;
      quality[key] = parseScalar(value);
    }
  }
  flushBlock();

  return {
    version: topLevel.version ?? null,
    lastCurated: stringOrNull(topLevel.last_curated),
    defaultReviewFrequency: stringOrNull(topLevel.default_review_frequency),
    sources,
  };
}

export function mapRegistryTypeToSourceType(type: string): SourceType | null {
  const mapped = REGISTRY_TYPE_TO_SOURCE_TYPE[type];
  if (mapped) {
    return mapped;
  }
  return SOURCE_TYPE_SET.has(type) ? (type as SourceType) : null;
}

export function buildSourceOpsQueue(
  options: BuildSourceOpsQueueOptions = {},
): SourceOpsQueue {
  const asOf = options.asOf ?? new Date();
  const registry = options.registryText
    ? parseSourceRegistryYaml(options.registryText)
    : loadSourceRegistry(options.registryPath);
  const rows = registry.sources.map((source) => buildSourceOpsRow(source, asOf));

  return {
    generatedAt: asOf.toISOString(),
    rows,
    summary: {
      total: rows.length,
      ready: rows.filter((row) => row.readinessStatus === "ready").length,
      reviewDue: rows.filter((row) => row.readinessStatus === "review-due").length,
      connectorBlocked: rows.filter((row) =>
        ["connector-stub", "connector-missing", "mapping-missing"].includes(
          row.readinessStatus,
        ),
      ).length,
      inactive: rows.filter((row) => row.readinessStatus === "source-inactive").length,
    },
  };
}

function buildSourceOpsRow(source: SourceRegistrySource, asOf: Date): SourceOpsRow {
  const sourceType = mapRegistryTypeToSourceType(source.type);
  const connector = sourceType ? safeConnector(sourceType) : null;
  const freshness = freshnessFor(source, asOf);
  const connectorImplemented = Boolean(
    connector && connector.version !== "0.0.0-stub",
  );
  const readiness = readinessFor({
    source,
    sourceType,
    connector,
    connectorImplemented,
    freshnessStatus: freshness.status,
  });

  return {
    id: source.id,
    name: source.name,
    lane: source.lane,
    registryType: source.type,
    sourceType,
    cadence: source.cadence,
    reviewFrequency: source.reviewFrequency,
    lastReviewed: source.lastReviewed,
    freshnessStatus: freshness.status,
    freshnessLabel: freshness.label,
    nextReviewDate: freshness.nextReviewDate,
    connectorType: sourceType,
    connectorVersion: connector?.version ?? null,
    connectorImplemented,
    readinessStatus: readiness.status,
    readinessReason: readiness.reason,
  };
}

function safeConnector(sourceType: SourceType): Connector<unknown> | null {
  try {
    return getConnector(sourceType);
  } catch {
    return null;
  }
}

function readinessFor(input: {
  readonly source: SourceRegistrySource;
  readonly sourceType: SourceType | null;
  readonly connector: Connector<unknown> | null;
  readonly connectorImplemented: boolean;
  readonly freshnessStatus: SourceFreshnessStatus;
}): { status: SourceReadinessStatus; reason: string } {
  if (input.source.status !== "active") {
    return {
      status: "source-inactive",
      reason: `source status is ${input.source.status}`,
    };
  }
  if (!input.sourceType) {
    return {
      status: "mapping-missing",
      reason: `registry type ${input.source.type} has no SourceType mapping`,
    };
  }
  if (!input.connector) {
    return {
      status: "connector-missing",
      reason: `no connector registered for ${input.sourceType}`,
    };
  }
  if (!input.connectorImplemented) {
    return {
      status: "connector-stub",
      reason: `${input.sourceType} is registered as a stub connector`,
    };
  }
  if (input.freshnessStatus === "due" || input.freshnessStatus === "overdue") {
    return {
      status: "review-due",
      reason: "source registry review is due",
    };
  }
  return {
    status: "ready",
    reason: "full connector registered and registry review is current",
  };
}

function freshnessFor(
  source: SourceRegistrySource,
  asOf: Date,
): {
  readonly status: SourceFreshnessStatus;
  readonly label: string;
  readonly nextReviewDate: string | null;
} {
  if (!source.lastReviewed || !source.reviewFrequency) {
    return {
      status: "unknown",
      label: "no review date",
      nextReviewDate: null,
    };
  }
  const intervalDays = REVIEW_FREQUENCY_DAYS[source.reviewFrequency];
  const lastReviewed = parseDateOnly(source.lastReviewed);
  if (!intervalDays || !lastReviewed) {
    return {
      status: "unknown",
      label: "unknown review cadence",
      nextReviewDate: null,
    };
  }
  const nextReview = addDays(lastReviewed, intervalDays);
  const daysUntil = daysBetween(dateOnly(asOf), nextReview);
  const nextReviewDate = formatDateOnly(nextReview);
  if (daysUntil > 0) {
    return {
      status: "fresh",
      label: `fresh until ${nextReviewDate}`,
      nextReviewDate,
    };
  }
  if (daysUntil === 0) {
    return {
      status: "due",
      label: "review due today",
      nextReviewDate,
    };
  }
  return {
    status: "overdue",
    label: `overdue since ${nextReviewDate}`,
    nextReviewDate,
  };
}

function splitKeyValue(line: string): [string, string] {
  const index = line.indexOf(":");
  if (index < 0) {
    return [line.trim(), ""];
  }
  return [line.slice(0, index).trim(), line.slice(index + 1).trim()];
}

function parseScalar(value: string): string | number | null {
  const unquoted = value.replace(/^["']|["']$/g, "");
  if (/^-?\d+$/.test(unquoted)) {
    return Number(unquoted);
  }
  return unquoted || null;
}

function toCamelKey(key: string): string {
  return key.replace(/_([a-z])/g, (_match, letter: string) => letter.toUpperCase());
}

function stringOrNull(value: string | number | null | undefined): string | null {
  if (typeof value === "string") {
    return value;
  }
  if (typeof value === "number") {
    return String(value);
  }
  return null;
}

function parseDateOnly(value: string): Date | null {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value);
  if (!match) {
    return null;
  }
  const [, year, month, day] = match;
  return new Date(Date.UTC(Number(year), Number(month) - 1, Number(day)));
}

function dateOnly(value: Date): Date {
  return new Date(Date.UTC(value.getUTCFullYear(), value.getUTCMonth(), value.getUTCDate()));
}

function addDays(value: Date, days: number): Date {
  const next = new Date(value);
  next.setUTCDate(next.getUTCDate() + days);
  return next;
}

function daysBetween(start: Date, end: Date): number {
  return Math.round((end.getTime() - start.getTime()) / 86_400_000);
}

function formatDateOnly(value: Date): string {
  return value.toISOString().slice(0, 10);
}

function findDefaultRegistryPath(): string {
  const cwd = process.cwd();
  const candidates = [
    join(cwd, "sources", "registry.yaml"),
    join(cwd, "..", "sources", "registry.yaml"),
    join(cwd, "..", "..", "sources", "registry.yaml"),
  ].map((candidate) => resolve(candidate));

  return candidates.find((candidate) => existsSync(candidate)) ?? candidates[0]!;
}
