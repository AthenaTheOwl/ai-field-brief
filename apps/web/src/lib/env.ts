import { z } from "zod";

/**
 * R-FND-007: env validation at boot.
 *
 * The schema names the keys the web app must have to boot. Clerk keys are
 * checked but not used until live wiring lands; checking them here keeps
 * the failure mode at startup and avoids mid-request surprises.
 *
 * Tests pass an explicit input through `parseWebEnv`; production code
 * goes through `getWebEnv()` which reads from process.env once.
 */
export const webEnvSchema = z.object({
  DATABASE_URL: z
    .string({ required_error: "DATABASE_URL is required" })
    .min(1, "DATABASE_URL must not be empty")
    .url("DATABASE_URL must be a valid URL"),
  NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: z
    .string({
      required_error: "NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY is required",
    })
    .min(1, "NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY must not be empty"),
  CLERK_SECRET_KEY: z
    .string({ required_error: "CLERK_SECRET_KEY is required" })
    .min(1, "CLERK_SECRET_KEY must not be empty"),
});

export type WebEnv = z.infer<typeof webEnvSchema>;

export function parseWebEnv(input: Record<string, string | undefined>): WebEnv {
  const parsed = webEnvSchema.safeParse(input);
  if (!parsed.success) {
    const summary = parsed.error.issues
      .map((i) => `${i.path.join(".")}: ${i.message}`)
      .join("; ");
    throw new Error(`web env validation failed: ${summary}`);
  }
  return parsed.data;
}

let cached: WebEnv | undefined;

export function getWebEnv(
  override?: Record<string, string | undefined>,
): WebEnv {
  if (override) {
    return parseWebEnv(override);
  }
  if (!cached) {
    cached = parseWebEnv(process.env);
  }
  return cached;
}
