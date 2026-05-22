import { NextResponse } from "next/server";

import { getDb, sql } from "@/lib/db";

export const dynamic = "force-dynamic";
export const runtime = "nodejs";

/**
 * Readiness check (R-OBS-007, R-FND-007).
 *
 * Pings the db with a trivial query. Returns 200 with `db: 'ok'` on
 * success, 503 with `db: 'down'` on any error. The handler does not
 * throw — observability cares about the boolean.
 */
export async function GET(): Promise<NextResponse> {
  try {
    const db = getDb();
    await db.execute(sql`select 1`);
    return NextResponse.json({ ok: true, db: "ok" satisfies "ok" });
  } catch (err) {
    const message = err instanceof Error ? err.message : "unknown";
    return NextResponse.json(
      { ok: false, db: "down" satisfies "down", error: message },
      { status: 503 },
    );
  }
}
