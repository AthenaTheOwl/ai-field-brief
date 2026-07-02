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
const LOCK_DIR = path.join(APP_ROOT, ".briefs-snapshot.lock");
const REMOVE_RETRIES = 6;
const REMOVE_RETRY_DELAY_MS = 250;
const LOCK_RETRIES = 80;
const LOCK_RETRY_DELAY_MS = 100;

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

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

async function removeWithRetry(target) {
  for (let attempt = 0; attempt <= REMOVE_RETRIES; attempt += 1) {
    try {
      await rm(target, { recursive: true, force: true });
      return;
    } catch (err) {
      const transient =
        err &&
        typeof err === "object" &&
        ["EBUSY", "EPERM", "ENOTEMPTY"].includes(err.code);
      if (!transient || attempt === REMOVE_RETRIES) {
        throw err;
      }
      await sleep(REMOVE_RETRY_DELAY_MS * (attempt + 1));
    }
  }
}

async function withSnapshotLock(fn) {
  for (let attempt = 0; attempt <= LOCK_RETRIES; attempt += 1) {
    try {
      await mkdir(LOCK_DIR);
      break;
    } catch (err) {
      const locked = err && typeof err === "object" && err.code === "EEXIST";
      if (!locked || attempt === LOCK_RETRIES) {
        throw err;
      }
      await sleep(LOCK_RETRY_DELAY_MS);
    }
  }
  try {
    return await fn();
  } finally {
    await removeWithRetry(LOCK_DIR);
  }
}

async function main() {
  if (!(await exists(SRC))) {
    console.error(`snapshot-briefs: source not found at ${SRC}`);
    process.exit(1);
  }
  const sourceWeeks = await assertCompleteBriefTree(SRC, "source briefs");

  const snapshotWeeks = await withSnapshotLock(async () => {
    if (await exists(DEST)) {
      await removeWithRetry(DEST);
    }
    await mkdir(DEST, { recursive: true });
    await cp(SRC, DEST, { recursive: true });
    return assertCompleteBriefTree(DEST, "briefs snapshot");
  });

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
