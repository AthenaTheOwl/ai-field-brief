import { and, eq, isNull, type SQL } from "drizzle-orm";
import { SOURCE_TYPES, type SourceType } from "@aifieldbrief/sources";

import { getDb, type Database } from "../client";
import { sources, type NewSource, type Source } from "../schema/sources";
import { assertWorkspaceId } from "./workspaces";

const SOURCE_TYPE_SET = new Set<string>(SOURCE_TYPES);

export class SourceTypeError extends Error {
  public constructor(sourceType: string) {
    super(`unknown source type: ${sourceType}`);
    this.name = "SourceTypeError";
  }
}

export interface SourceQueryOptions {
  readonly db?: Database;
}

export interface ListSourcesOptions extends SourceQueryOptions {
  readonly status?: string;
  readonly lane?: string;
  readonly limit?: number;
  readonly offset?: number;
}

export type CreateSourceInput = Omit<
  NewSource,
  "id" | "workspaceId" | "createdAt" | "deletedAt"
> & {
  readonly type: SourceType;
};

export type UpdateSourcePatch = Partial<CreateSourceInput>;

function resolveDb(options?: SourceQueryOptions): Database {
  return options?.db ?? getDb();
}

function assertSourceType(sourceType: string): asserts sourceType is SourceType {
  if (!SOURCE_TYPE_SET.has(sourceType)) {
    throw new SourceTypeError(sourceType);
  }
}

export async function listSources(
  workspaceId: string,
  options?: ListSourcesOptions,
): Promise<Source[]> {
  assertWorkspaceId(workspaceId);
  const filters: SQL[] = [
    eq(sources.workspaceId, workspaceId),
    isNull(sources.deletedAt),
  ];
  if (options?.status) {
    filters.push(eq(sources.status, options.status));
  }
  if (options?.lane) {
    filters.push(eq(sources.lane, options.lane));
  }
  return resolveDb(options)
    .select()
    .from(sources)
    .where(and(...filters))
    .limit(options?.limit ?? 50)
    .offset(options?.offset ?? 0);
}

export async function getSource(
  workspaceId: string,
  sourceId: string,
  options?: SourceQueryOptions,
): Promise<Source | undefined> {
  assertWorkspaceId(workspaceId);
  const rows = await resolveDb(options)
    .select()
    .from(sources)
    .where(
      and(
        eq(sources.workspaceId, workspaceId),
        eq(sources.id, sourceId),
        isNull(sources.deletedAt),
      ),
    )
    .limit(1);
  return rows[0];
}

export async function createSource(
  workspaceId: string,
  input: CreateSourceInput,
  options?: SourceQueryOptions,
): Promise<Source> {
  assertWorkspaceId(workspaceId);
  assertSourceType(input.type);
  const rows = await resolveDb(options)
    .insert(sources)
    .values({ ...input, workspaceId })
    .returning();
  const created = rows[0];
  if (!created) {
    throw new Error("createSource: insert returned no row");
  }
  return created;
}

export async function updateSource(
  workspaceId: string,
  sourceId: string,
  patch: UpdateSourcePatch,
  options?: SourceQueryOptions,
): Promise<Source | undefined> {
  assertWorkspaceId(workspaceId);
  if (patch.type) {
    assertSourceType(patch.type);
  }
  const rows = await resolveDb(options)
    .update(sources)
    .set(patch)
    .where(
      and(
        eq(sources.workspaceId, workspaceId),
        eq(sources.id, sourceId),
        isNull(sources.deletedAt),
      ),
    )
    .returning();
  return rows[0];
}

export async function retireSource(
  workspaceId: string,
  sourceId: string,
  options?: SourceQueryOptions,
): Promise<Source | undefined> {
  assertWorkspaceId(workspaceId);
  const rows = await resolveDb(options)
    .update(sources)
    .set({ status: "retired", deletedAt: new Date() })
    .where(
      and(
        eq(sources.workspaceId, workspaceId),
        eq(sources.id, sourceId),
        isNull(sources.deletedAt),
      ),
    )
    .returning();
  return rows[0];
}
