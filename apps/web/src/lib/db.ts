/**
 * Re-export of the tenant-scoped query surface from @aifieldbrief/db.
 *
 * App code should import from `@/lib/db` and not reach into the package
 * directly; this keeps the public surface auditable.
 */
export {
  getDb,
  schema,
  queries,
  auditLog,
  assertWorkspaceId,
  getWorkspaceById,
  listMembers,
  createInvite,
  acceptInvite,
  TenantScopeError,
  AuditScopeError,
  sql,
  type Database,
} from "@aifieldbrief/db";
