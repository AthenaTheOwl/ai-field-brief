import { describe, expect, it } from "vitest";

import { log, AuditScopeError } from "../queries/audit";
import {
  acceptInvite,
  assertWorkspaceId,
  createInvite,
  getWorkspaceById,
  listMembers,
  TenantScopeError,
} from "../queries/workspaces";

/**
 * R-FND-001 belt-and-suspenders test.
 *
 * TypeScript already prevents calling these helpers without a workspaceId.
 * The cast-to-string lines below model the runtime case where an upstream
 * caller passes `undefined` from a query param or a partial DTO. Each
 * helper must throw before touching the database.
 */

const undef = undefined as unknown as string;
const blank = "";
const whitespace = "   ";

describe("assertWorkspaceId", () => {
  it("throws on undefined", () => {
    expect(() => assertWorkspaceId(undef)).toThrow(TenantScopeError);
  });

  it("throws on empty string", () => {
    expect(() => assertWorkspaceId(blank)).toThrow(TenantScopeError);
  });

  it("throws on whitespace-only string", () => {
    expect(() => assertWorkspaceId(whitespace)).toThrow(TenantScopeError);
  });

  it("accepts a non-empty string", () => {
    expect(() => assertWorkspaceId("00000000-0000-0000-0000-000000000001")).not.toThrow();
  });
});

describe("workspace helpers refuse missing workspaceId", () => {
  it("getWorkspaceById throws on undefined", async () => {
    await expect(getWorkspaceById(undef)).rejects.toThrow(TenantScopeError);
  });

  it("getWorkspaceById throws on empty", async () => {
    await expect(getWorkspaceById(blank)).rejects.toThrow(TenantScopeError);
  });

  it("listMembers throws on undefined", async () => {
    await expect(listMembers(undef)).rejects.toThrow(TenantScopeError);
  });

  it("createInvite throws on undefined", async () => {
    await expect(
      createInvite(undef, {
        email: "x@example.com",
        role: "viewer",
        token: "t",
        invitedBy: "u",
        expiresAt: new Date(Date.now() + 86_400_000),
      }),
    ).rejects.toThrow(TenantScopeError);
  });

  it("acceptInvite throws on empty workspaceId", async () => {
    await expect(
      acceptInvite(blank, { token: "t", userId: "u" }),
    ).rejects.toThrow(TenantScopeError);
  });
});

describe("audit.log refuses bad inputs", () => {
  it("throws when actorUserId is missing", async () => {
    await expect(
      log({
        actorUserId: "",
        action: "test",
        targetType: "workspace",
        workspaceId: "00000000-0000-0000-0000-000000000001",
      }),
    ).rejects.toThrow(AuditScopeError);
  });

  it("throws when both workspaceId and orgId are missing", async () => {
    await expect(
      log({
        actorUserId: "00000000-0000-0000-0000-000000000002",
        action: "test",
        targetType: "workspace",
      }),
    ).rejects.toThrow(AuditScopeError);
  });

  it("throws when action is missing", async () => {
    await expect(
      log({
        actorUserId: "00000000-0000-0000-0000-000000000002",
        action: "",
        targetType: "workspace",
        workspaceId: "00000000-0000-0000-0000-000000000001",
      }),
    ).rejects.toThrow(AuditScopeError);
  });

  it("throws when targetType is missing", async () => {
    await expect(
      log({
        actorUserId: "00000000-0000-0000-0000-000000000002",
        action: "test",
        targetType: "",
        workspaceId: "00000000-0000-0000-0000-000000000001",
      }),
    ).rejects.toThrow(AuditScopeError);
  });
});
