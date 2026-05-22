import { sql } from "drizzle-orm";
import { jsonb, pgTable, text, timestamp, uuid } from "drizzle-orm/pg-core";

import { users } from "./identity";
import { orgs } from "./identity";
import { workspaces } from "./workspaces";

/**
 * Audit events (R-FND-011).
 *
 * Every admin action records actor, target, before, after, IP, UA. Both
 * workspace_id and org_id are nullable so org-scoped events (member add,
 * billing change) can live alongside workspace-scoped events.
 */
export const auditEvents = pgTable("audit_events", {
  id: uuid("id").primaryKey().defaultRandom(),
  workspaceId: uuid("workspace_id").references(() => workspaces.id, {
    onDelete: "set null",
  }),
  orgId: uuid("org_id").references(() => orgs.id, { onDelete: "set null" }),
  actorUserId: uuid("actor_user_id")
    .notNull()
    .references(() => users.id, { onDelete: "restrict" }),
  action: text("action").notNull(),
  targetType: text("target_type").notNull(),
  targetId: text("target_id"),
  before: jsonb("before"),
  after: jsonb("after"),
  ip: text("ip"),
  ua: text("ua"),
  createdAt: timestamp("created_at", { withTimezone: true })
    .notNull()
    .default(sql`now()`),
});

export type AuditEvent = typeof auditEvents.$inferSelect;
export type NewAuditEvent = typeof auditEvents.$inferInsert;
