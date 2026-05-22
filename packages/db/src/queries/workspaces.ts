import { and, eq, isNull } from "drizzle-orm";

import { getDb, type Database } from "../client";
import {
  workspaceInvites,
  workspaceMembers,
  workspaces,
  type Workspace,
  type WorkspaceInvite,
  type WorkspaceMember,
  type WorkspaceRole,
} from "../schema/workspaces";

/**
 * Tenant-scope guard (R-FND-001).
 *
 * Every workspace-scoped helper in this module calls this before any SQL.
 * The TS signature already requires a string; this is the runtime belt.
 */
export class TenantScopeError extends Error {
  public constructor(message: string) {
    super(message);
    this.name = "TenantScopeError";
  }
}

export function assertWorkspaceId(workspaceId: string): void {
  if (typeof workspaceId !== "string" || workspaceId.trim().length === 0) {
    throw new TenantScopeError(
      "workspaceId is required for tenant-scoped queries (R-FND-001)",
    );
  }
}

interface QueryOptions {
  readonly db?: Database;
}

function resolveDb(options?: QueryOptions): Database {
  return options?.db ?? getDb();
}

export async function getWorkspaceById(
  workspaceId: string,
  options?: QueryOptions,
): Promise<Workspace | undefined> {
  assertWorkspaceId(workspaceId);
  const db = resolveDb(options);
  const rows = await db
    .select()
    .from(workspaces)
    .where(
      and(eq(workspaces.id, workspaceId), isNull(workspaces.deletedAt)),
    )
    .limit(1);
  return rows[0];
}

export async function listMembers(
  workspaceId: string,
  options?: QueryOptions,
): Promise<WorkspaceMember[]> {
  assertWorkspaceId(workspaceId);
  const db = resolveDb(options);
  return db
    .select()
    .from(workspaceMembers)
    .where(eq(workspaceMembers.workspaceId, workspaceId));
}

export interface CreateInviteInput {
  readonly email: string;
  readonly role: WorkspaceRole;
  readonly token: string;
  readonly invitedBy: string;
  readonly expiresAt: Date;
}

export async function createInvite(
  workspaceId: string,
  input: CreateInviteInput,
  options?: QueryOptions,
): Promise<WorkspaceInvite> {
  assertWorkspaceId(workspaceId);
  const db = resolveDb(options);
  const rows = await db
    .insert(workspaceInvites)
    .values({
      workspaceId,
      email: input.email,
      role: input.role,
      token: input.token,
      invitedBy: input.invitedBy,
      expiresAt: input.expiresAt,
    })
    .returning();
  const created = rows[0];
  if (!created) {
    throw new Error("createInvite: insert returned no row");
  }
  return created;
}

export interface AcceptInviteInput {
  readonly token: string;
  readonly userId: string;
}

export async function acceptInvite(
  workspaceId: string,
  input: AcceptInviteInput,
  options?: QueryOptions,
): Promise<WorkspaceMember> {
  assertWorkspaceId(workspaceId);
  const db = resolveDb(options);
  const inviteRows = await db
    .select()
    .from(workspaceInvites)
    .where(
      and(
        eq(workspaceInvites.workspaceId, workspaceId),
        eq(workspaceInvites.token, input.token),
      ),
    )
    .limit(1);
  const invite = inviteRows[0];
  if (!invite) {
    throw new Error("acceptInvite: invite not found for workspace");
  }
  if (invite.acceptedAt) {
    throw new Error("acceptInvite: invite already accepted");
  }
  if (invite.expiresAt.getTime() < Date.now()) {
    throw new Error("acceptInvite: invite expired");
  }
  await db
    .update(workspaceInvites)
    .set({ acceptedAt: new Date() })
    .where(eq(workspaceInvites.id, invite.id));
  const memberRows = await db
    .insert(workspaceMembers)
    .values({
      workspaceId,
      userId: input.userId,
      role: invite.role,
      invitedBy: invite.invitedBy,
    })
    .returning();
  const member = memberRows[0];
  if (!member) {
    throw new Error("acceptInvite: member insert returned no row");
  }
  return member;
}
