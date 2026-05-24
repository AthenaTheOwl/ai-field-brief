import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

import type { SourceType } from "@aifieldbrief/sources";

import type { NewSource } from "../schema/sources";

export const REGISTRY_TYPE_TO_SOURCE_TYPE: Record<string, SourceType> = {
  "vendor-news": "rss",
  "vendor-engineering": "rss",
  "vendor-research": "rss",
  blog: "rss",
  newsletter: "rss",
  "blog+newsletter": "rss",
  "collection+book": "rss",
  podcast: "podcast-rss",
  "podcast+newsletter": "podcast-rss",
  "github-releases": "github-releases",
};

interface RegistrySource {
  readonly id: string;
  readonly name: string;
  readonly type: string;
  readonly lane: string;
  readonly url: string;
  readonly cadence: string;
  readonly review_frequency?: string;
  readonly intake: string;
  readonly status: string;
  readonly last_reviewed?: string;
  readonly notes?: string;
  readonly quality?: {
    readonly signal?: string;
    readonly actionability?: string;
    readonly credibility?: string;
  };
}

export type SourceSeedPayload = NewSource & {
  readonly type: SourceType;
};

const REGISTRY_PATH = fileURLToPath(
  new URL("../../../../sources/registry.yaml", import.meta.url),
);

export function loadSeedSources(
  workspaceId: string,
  registryPath = REGISTRY_PATH,
): SourceSeedPayload[] {
  const registry = parseRegistryYaml(readFileSync(registryPath, "utf8"));
  return registry.map((source) => {
    const sourceType = REGISTRY_TYPE_TO_SOURCE_TYPE[source.type];
    if (!sourceType) {
      throw new Error(`registry type has no SourceType mapping: ${source.type}`);
    }
    return {
      workspaceId,
      name: source.name,
      type: sourceType,
      lane: source.lane,
      url: source.url,
      cadence: source.cadence,
      intake: source.intake,
      status: source.status,
      signal: qualityScore(source.quality?.signal),
      actionability: qualityScore(source.quality?.actionability),
      credibility: qualityScore(source.quality?.credibility),
      priority: source.quality?.signal ?? null,
      lastReviewed: source.last_reviewed ?? null,
      reliabilityScore: null,
      customKeywords: [],
      integrationConfig: {
        registry_id: source.id,
        registry_type: source.type,
        review_frequency: source.review_frequency ?? null,
      },
      notes: source.notes ?? null,
    };
  });
}

export function distinctRegistryTypes(registryPath = REGISTRY_PATH): string[] {
  return Array.from(
    new Set(parseRegistryYaml(readFileSync(registryPath, "utf8")).map((source) => source.type)),
  ).sort();
}

function qualityScore(value: string | undefined): number | null {
  if (value === "high") {
    return 5;
  }
  if (value === "medium") {
    return 3;
  }
  if (value === "low") {
    return 1;
  }
  return null;
}

function parseRegistryYaml(text: string): RegistrySource[] {
  const sources: RegistrySource[] = [];
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

    if (indent === 0 && trimmed === "sources:") {
      inSources = true;
      continue;
    }
    if (!inSources) {
      continue;
    }
    if (indent === 2 && trimmed.startsWith("- ")) {
      nestedKey = null;
      current = {};
      sources.push(current as unknown as RegistrySource);
      const rest = trimmed.slice(2);
      if (rest.includes(":")) {
        const [key, value] = splitKeyValue(rest);
        current[key] = parseScalar(value);
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
      if (value === ">-" || value === "|") {
        pendingBlockKey = key;
        pendingBlockIndent = indent;
      } else {
        current[key] = parseScalar(value);
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
  return sources;
}

function splitKeyValue(line: string): [string, string] {
  const index = line.indexOf(":");
  if (index < 0) {
    return [line.trim(), ""];
  }
  return [line.slice(0, index).trim(), line.slice(index + 1).trim()];
}

function parseScalar(value: string): string {
  return value.replace(/^["']|["']$/g, "");
}
