import { neon, type NeonQueryFunction } from "@neondatabase/serverless";
import { drizzle, type NeonHttpDatabase } from "drizzle-orm/neon-http";

import { getDbEnv } from "./env";
import * as schema from "./schema/index";

export type Database = NeonHttpDatabase<typeof schema>;

let client: Database | undefined;

/**
 * Lazily build the Drizzle client. R-FND-007 ensures env is validated
 * before this runs; missing DATABASE_URL throws at import of env.ts.
 *
 * Tests that want a different connection can pass a URL override.
 */
export function getDb(urlOverride?: string): Database {
  if (client && !urlOverride) {
    return client;
  }
  const env = getDbEnv();
  const url = urlOverride ?? env.DATABASE_URL;
  const sql: NeonQueryFunction<false, false> = neon(url);
  const db = drizzle(sql, { schema });
  if (!urlOverride) {
    client = db;
  }
  return db;
}

export { schema };
