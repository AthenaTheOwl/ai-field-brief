import { describe, expect, it } from "vitest";

import { parseWebEnv } from "@/lib/env";

/**
 * R-FND-007 smoke test for the web app.
 *
 * Importing src/lib/env with a valid override must not throw; missing
 * required keys must throw with a useful message.
 */
describe("parseWebEnv", () => {
  it("accepts a known-good env", () => {
    const parsed = parseWebEnv({
      DATABASE_URL: "postgresql://user:pw@host/db?sslmode=require",
      NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: "pk_test_dummy",
      CLERK_SECRET_KEY: "sk_test_dummy",
    });
    expect(parsed.DATABASE_URL).toContain("postgresql://");
    expect(parsed.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY).toContain("pk_");
    expect(parsed.CLERK_SECRET_KEY).toContain("sk_");
  });

  it("throws when DATABASE_URL is missing", () => {
    expect(() =>
      parseWebEnv({
        NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: "pk_test_dummy",
        CLERK_SECRET_KEY: "sk_test_dummy",
      }),
    ).toThrow(/DATABASE_URL/);
  });

  it("throws when CLERK_SECRET_KEY is missing", () => {
    expect(() =>
      parseWebEnv({
        DATABASE_URL: "postgresql://user:pw@host/db?sslmode=require",
        NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: "pk_test_dummy",
      }),
    ).toThrow(/CLERK_SECRET_KEY/);
  });
});
