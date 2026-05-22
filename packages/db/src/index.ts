/**
 * Public surface for @aifieldbrief/db.
 *
 * Consumers go through the query helpers (which enforce R-FND-001) and
 * do not touch the raw drizzle client. The client.ts module is exposed
 * for tests and migrations; production app code imports from ./queries.
 */
export * as schema from "./schema/index";
export * as queries from "./queries/index";
export { getDb, type Database } from "./client";
export { getDbEnv, parseDbEnv, dbEnvSchema, type DbEnv } from "./env";

// Re-export drizzle's `sql` so consumers can build raw fragments (e.g. the
// readyz route's `select 1` ping) without depending on drizzle-orm directly.
export { sql } from "drizzle-orm";

// Re-export at the top level for ergonomic import sites in apps.
export {
  acceptInvite,
  assertWorkspaceId,
  createInvite,
  getWorkspaceById,
  listMembers,
  TenantScopeError,
  log as auditLog,
  AuditScopeError,
  type AcceptInviteInput,
  type AuditLogInput,
  type CreateInviteInput,
} from "./queries/index";
