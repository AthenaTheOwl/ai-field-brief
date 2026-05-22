import { describe, expect, it } from "vitest";

import { parseDbEnv } from "../env";

/**
 * R-FND-007: env validation at boot.
 * The schema rejects missing or non-URL values; valid inputs parse clean.
 */
describe("parseDbEnv", () => {
  it("accepts a known-good env", () => {
    const parsed = parseDbEnv({
      DATABASE_URL: "postgresql://user:pw@host/db?sslmode=require",
      DIRECT_DATABASE_URL: "postgresql://user:pw@host/db?sslmode=require",
    });
    expect(parsed.DATABASE_URL).toContain("postgresql://");
    expect(parsed.DIRECT_DATABASE_URL).toContain("postgresql://");
  });

  it("throws when DATABASE_URL is missing", () => {
    expect(() =>
      parseDbEnv({
        DIRECT_DATABASE_URL: "postgresql://user:pw@host/db?sslmode=require",
      }),
    ).toThrow(/DATABASE_URL/);
  });

  it("throws when DIRECT_DATABASE_URL is missing", () => {
    expect(() =>
      parseDbEnv({
        DATABASE_URL: "postgresql://user:pw@host/db?sslmode=require",
      }),
    ).toThrow(/DIRECT_DATABASE_URL/);
  });

  it("throws when DATABASE_URL is blank", () => {
    expect(() =>
      parseDbEnv({
        DATABASE_URL: "",
        DIRECT_DATABASE_URL: "postgresql://user:pw@host/db?sslmode=require",
      }),
    ).toThrow(/DATABASE_URL/);
  });
});
