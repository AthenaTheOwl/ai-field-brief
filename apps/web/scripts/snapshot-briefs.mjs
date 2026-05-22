#!/usr/bin/env node
/**
 * Copies the repo-root `briefs/` tree into `apps/web/.briefs-snapshot/`.
 *
 * Why: in a Turborepo monorepo deploy, the Vercel build's working
 * directory is `apps/web/`. Relative paths above the app root work in
 * local dev but get pruned in some deploy configurations. Snapshotting
 * the briefs into the app's own tree at build time keeps the static
 * brief renderer hermetic — no surprises in production.
 *
 * Runs as `prebuild` and `predev`. Snapshot directory is gitignored.
 */

import { cp, mkdir, rm, stat } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const APP_ROOT = path.resolve(__dirname, "..");
const REPO_ROOT = path.resolve(APP_ROOT, "..", "..");
const SRC = path.join(REPO_ROOT, "briefs");
const DEST = path.join(APP_ROOT, ".briefs-snapshot");

async function exists(p) {
  try {
    await stat(p);
    return true;
  } catch {
    return false;
  }
}

async function main() {
  if (!(await exists(SRC))) {
    console.error(`snapshot-briefs: source not found at ${SRC}`);
    process.exit(1);
  }

  if (await exists(DEST)) {
    await rm(DEST, { recursive: true, force: true });
  }
  await mkdir(DEST, { recursive: true });
  await cp(SRC, DEST, { recursive: true });

  console.log(`snapshot-briefs: copied ${SRC} -> ${DEST}`);
}

main().catch((err) => {
  console.error("snapshot-briefs: failed", err);
  process.exit(1);
});
