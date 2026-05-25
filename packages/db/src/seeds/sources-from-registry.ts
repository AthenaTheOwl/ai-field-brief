import { fileURLToPath } from "node:url";

import type { SourceType } from "@aifieldbrief/sources";
import {
  loadSourceRegistry,
  REGISTRY_TYPE_TO_SOURCE_TYPE as SOURCE_REGISTRY_TYPE_TO_SOURCE_TYPE,
} from "@aifieldbrief/sources/ops";

import type { NewSource } from "../schema/sources";

export const REGISTRY_TYPE_TO_SOURCE_TYPE = SOURCE_REGISTRY_TYPE_TO_SOURCE_TYPE;

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
  const registry = loadSourceRegistry(registryPath).sources;
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
      cadence: source.cadence ?? "irregular",
      intake: source.intake,
      status: source.status,
      signal: qualityScore(source.quality?.signal),
      actionability: qualityScore(source.quality?.actionability),
      credibility: qualityScore(source.quality?.credibility),
      priority: source.quality?.signal ?? null,
      lastReviewed: source.lastReviewed ?? null,
      reliabilityScore: null,
      customKeywords: [],
      integrationConfig: {
        registry_id: source.id,
        registry_type: source.type,
        review_frequency: source.reviewFrequency ?? null,
      },
      notes: source.notes ?? null,
    };
  });
}

export function distinctRegistryTypes(registryPath = REGISTRY_PATH): string[] {
  return Array.from(
    new Set(loadSourceRegistry(registryPath).sources.map((source) => source.type)),
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
