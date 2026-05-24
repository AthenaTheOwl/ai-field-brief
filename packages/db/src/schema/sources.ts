import { sql } from "drizzle-orm";
import {
  date,
  index,
  integer,
  jsonb,
  numeric,
  pgTable,
  text,
  timestamp,
  uuid,
} from "drizzle-orm/pg-core";

import { workspaces } from "./workspaces";

export const sources = pgTable(
  "sources",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    workspaceId: uuid("workspace_id")
      .notNull()
      .references(() => workspaces.id, { onDelete: "cascade" }),
    name: text("name").notNull(),
    type: text("type").notNull(),
    lane: text("lane").notNull(),
    url: text("url").notNull(),
    cadence: text("cadence").notNull(),
    intake: text("intake").notNull(),
    status: text("status").notNull(),
    signal: integer("signal"),
    actionability: integer("actionability"),
    credibility: integer("credibility"),
    priority: text("priority"),
    lastReviewed: date("last_reviewed"),
    reliabilityScore: numeric("reliability_score"),
    customKeywords: jsonb("custom_keywords").notNull().default(sql`'[]'::jsonb`),
    integrationConfig: jsonb("integration_config").notNull().default(sql`'{}'::jsonb`),
    notes: text("notes"),
    createdAt: timestamp("created_at", { withTimezone: true })
      .notNull()
      .default(sql`now()`),
    deletedAt: timestamp("deleted_at", { withTimezone: true }),
  },
  (table) => ({
    workspaceStatusLaneIdx: index("sources_workspace_status_lane_idx").on(
      table.workspaceId,
      table.status,
      table.lane,
    ),
  }),
);

export const sourceReliabilityHistory = pgTable("source_reliability_history", {
  id: uuid("id").primaryKey().defaultRandom(),
  sourceId: uuid("source_id")
    .notNull()
    .references(() => sources.id, { onDelete: "cascade" }),
  weekOf: date("week_of").notNull(),
  includedRate: numeric("included_rate"),
  avgPriority: numeric("avg_priority"),
  totalItems: integer("total_items"),
  snapshotAt: timestamp("snapshot_at", { withTimezone: true })
    .notNull()
    .default(sql`now()`),
});

export type Source = typeof sources.$inferSelect;
export type NewSource = typeof sources.$inferInsert;
export type SourceReliabilityHistory = typeof sourceReliabilityHistory.$inferSelect;
export type NewSourceReliabilityHistory = typeof sourceReliabilityHistory.$inferInsert;
