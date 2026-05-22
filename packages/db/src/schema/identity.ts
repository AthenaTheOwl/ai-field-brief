import { sql } from "drizzle-orm";
import {
  boolean,
  pgEnum,
  pgTable,
  primaryKey,
  text,
  timestamp,
  uuid,
} from "drizzle-orm/pg-core";

/**
 * Identity + org tables (R-FND-002).
 *
 * Workspaces live under orgs (see ./workspaces.ts). Users may join many
 * orgs; org_members carries a composite PK on (org_id, user_id).
 */

export const orgRole = pgEnum("org_role", ["owner", "admin", "member"]);
export const orgPlan = pgEnum("org_plan", [
  "free",
  "pro",
  "team",
  "enterprise",
]);

export const users = pgTable("users", {
  id: uuid("id").primaryKey().defaultRandom(),
  clerkId: text("clerk_id").notNull().unique(),
  email: text("email").notNull(),
  name: text("name"),
  imageUrl: text("image_url"),
  // R-FND-004: 2FA gated on at Clerk; flag mirrored here for query joins.
  twoFactorEnabled: boolean("two_factor_enabled").notNull().default(false),
  lastSeenAt: timestamp("last_seen_at", { withTimezone: true }),
  // R-FND-014: every *_at column is timestamp-with-tz; storage is UTC.
  createdAt: timestamp("created_at", { withTimezone: true })
    .notNull()
    .default(sql`now()`),
});

export const orgs = pgTable("orgs", {
  id: uuid("id").primaryKey().defaultRandom(),
  clerkOrgId: text("clerk_org_id").notNull().unique(),
  slug: text("slug").notNull().unique(),
  name: text("name").notNull(),
  plan: orgPlan("plan").notNull().default("free"),
  billingCustomerId: text("billing_customer_id"),
  createdAt: timestamp("created_at", { withTimezone: true })
    .notNull()
    .default(sql`now()`),
});

export const orgMembers = pgTable(
  "org_members",
  {
    orgId: uuid("org_id")
      .notNull()
      .references(() => orgs.id, { onDelete: "cascade" }),
    userId: uuid("user_id")
      .notNull()
      .references(() => users.id, { onDelete: "cascade" }),
    role: orgRole("role").notNull().default("member"),
    joinedAt: timestamp("joined_at", { withTimezone: true })
      .notNull()
      .default(sql`now()`),
  },
  (table) => ({
    pk: primaryKey({ columns: [table.orgId, table.userId] }),
  }),
);

export type User = typeof users.$inferSelect;
export type NewUser = typeof users.$inferInsert;
export type Org = typeof orgs.$inferSelect;
export type NewOrg = typeof orgs.$inferInsert;
export type OrgMember = typeof orgMembers.$inferSelect;
export type NewOrgMember = typeof orgMembers.$inferInsert;
