import { getDb, type Database } from "../client";
import { auditEvents, type AuditEvent } from "../schema/audit";

/**
 * Audit log helper (R-FND-011).
 *
 * Both workspaceId and orgId may be null — org-scoped events (billing,
 * org-member add) and workspace-scoped events (settings change, key
 * rotation) share the same table. actorUserId is always required.
 */
export interface AuditLogInput {
  readonly workspaceId?: string | null;
  readonly orgId?: string | null;
  readonly actorUserId: string;
  readonly action: string;
  readonly targetType: string;
  readonly targetId?: string | null;
  readonly before?: unknown;
  readonly after?: unknown;
  readonly ip?: string | null;
  readonly ua?: string | null;
}

interface AuditOptions {
  readonly db?: Database;
}

export class AuditScopeError extends Error {
  public constructor(message: string) {
    super(message);
    this.name = "AuditScopeError";
  }
}

export async function log(
  input: AuditLogInput,
  options?: AuditOptions,
): Promise<AuditEvent> {
  if (!input.actorUserId || typeof input.actorUserId !== "string") {
    throw new AuditScopeError("audit.log: actorUserId is required");
  }
  if (!input.action || typeof input.action !== "string") {
    throw new AuditScopeError("audit.log: action is required");
  }
  if (!input.targetType || typeof input.targetType !== "string") {
    throw new AuditScopeError("audit.log: targetType is required");
  }
  if (
    (input.workspaceId == null || input.workspaceId === "") &&
    (input.orgId == null || input.orgId === "")
  ) {
    throw new AuditScopeError(
      "audit.log: at least one of workspaceId or orgId is required",
    );
  }
  const db = options?.db ?? getDb();
  const rows = await db
    .insert(auditEvents)
    .values({
      workspaceId: input.workspaceId ?? null,
      orgId: input.orgId ?? null,
      actorUserId: input.actorUserId,
      action: input.action,
      targetType: input.targetType,
      targetId: input.targetId ?? null,
      before: input.before ?? null,
      after: input.after ?? null,
      ip: input.ip ?? null,
      ua: input.ua ?? null,
    })
    .returning();
  const created = rows[0];
  if (!created) {
    throw new Error("audit.log: insert returned no row");
  }
  return created;
}
