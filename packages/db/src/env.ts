import { z } from "zod";

/**
 * Boot-time env validation for @aifieldbrief/db.
 *
 * Importing this module reads from process.env and throws on missing keys.
 * That satisfies R-FND-007: missing env fails startup, not runtime.
 *
 * Tests inject env via `parseDbEnv(input)` and avoid touching process.env,
 * so the schema stays unit-testable without monkey-patching.
 */
export const dbEnvSchema = z.object({
  DATABASE_URL: z
    .string({ required_error: "DATABASE_URL is required" })
    .min(1, "DATABASE_URL must not be empty")
    .url("DATABASE_URL must be a valid URL"),
  DIRECT_DATABASE_URL: z
    .string({ required_error: "DIRECT_DATABASE_URL is required" })
    .min(1, "DIRECT_DATABASE_URL must not be empty")
    .url("DIRECT_DATABASE_URL must be a valid URL"),
});

export type DbEnv = z.infer<typeof dbEnvSchema>;

export function parseDbEnv(input: Record<string, string | undefined>): DbEnv {
  const parsed = dbEnvSchema.safeParse(input);
  if (!parsed.success) {
    const summary = parsed.error.issues
      .map((i) => `${i.path.join(".")}: ${i.message}`)
      .join("; ");
    throw new Error(`db env validation failed: ${summary}`);
  }
  return parsed.data;
}

let cached: DbEnv | undefined;

/**
 * Return the validated env. Cached after first call so repeated imports
 * skip re-validation. Tests can pass `override` to bypass process.env.
 */
export function getDbEnv(
  override?: Record<string, string | undefined>,
): DbEnv {
  if (override) {
    return parseDbEnv(override);
  }
  if (!cached) {
    cached = parseDbEnv(process.env);
  }
  return cached;
}
