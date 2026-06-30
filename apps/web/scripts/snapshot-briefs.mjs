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

import { cp, mkdir, readdir, rm, stat } from "node:fs/promises";
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

async function completeBriefWeeks(root) {
  const entries = await readdir(root, { withFileTypes: true });
  const weeks = entries
    .filter((entry) => entry.isDirectory() && /^\d{4}-W\d{2}$/.test(entry.name))
    .map((entry) => entry.name)
    .sort();

  const missingBriefs = [];
  for (const week of weeks) {
    const briefPath = path.join(root, week, "brief.md");
    if (!(await exists(briefPath))) {
      missingBriefs.push(path.relative(root, briefPath));
    }
  }

  return { weeks, missingBriefs };
}

async function assertCompleteBriefTree(root, label) {
  const { weeks, missingBriefs } = await completeBriefWeeks(root);
  if (weeks.length === 0) {
    throw new Error(`${label} has no ISO-week brief folders at ${root}`);
  }
  if (missingBriefs.length > 0) {
    throw new Error(
      `${label} is incomplete at ${root}; missing ${missingBriefs.join(", ")}`,
    );
  }
  return weeks;
}

async function main() {
  if (!(await exists(SRC))) {
    console.error(`snapshot-briefs: source not found at ${SRC}`);
    process.exit(1);
  }
  const sourceWeeks = await assertCompleteBriefTree(SRC, "source briefs");

  if (await exists(DEST)) {
    await rm(DEST, { recursive: true, force: true });
  }
  await mkdir(DEST, { recursive: true });
  await cp(SRC, DEST, { recursive: true });
  const snapshotWeeks = await assertCompleteBriefTree(DEST, "briefs snapshot");

  console.log(
    `snapshot-briefs: copied ${snapshotWeeks.length} week(s) ${SRC} -> ${DEST}`,
  );
  if (snapshotWeeks.length !== sourceWeeks.length) {
    throw new Error(
      `snapshot-briefs: copied ${snapshotWeeks.length} week(s), expected ${sourceWeeks.length}`,
    );
  }
}

main().catch((err) => {
  console.error("snapshot-briefs: failed", err);
  process.exit(1);
});
