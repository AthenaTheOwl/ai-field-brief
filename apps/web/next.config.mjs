// Phase 1: real Clerk keys are user-provided and never committed. Provide a
// build-time placeholder so `next build` can SSR-prerender the layout
// (which mounts <ClerkProvider>) without throwing on a missing key. The
// placeholder is a Clerk-shaped sentinel that never authenticates; runtime
// reads the real key from process.env via src/lib/env.ts.
const CLERK_BUILD_PLACEHOLDER = "pk_test_Y2xlcmstcGxhY2Vob2xkZXItYWlmYi5jbGVyay5hY2NvdW50cy5kZXYk";
if (!process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY) {
  process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY = CLERK_BUILD_PLACEHOLDER;
}

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Phase 1 keeps the db package source-only; Next.js needs to know which
  // workspace packages to transpile.
  transpilePackages: ["@aifieldbrief/db"],
};

export default nextConfig;
