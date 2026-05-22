import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import yaml from "js-yaml";

/**
 * Reads briefs from the build-time snapshot at apps/web/.briefs-snapshot/.
 * The snapshot is populated by scripts/snapshot-briefs.mjs as part of
 * predev / prebuild.
 */

const SNAPSHOT_ROOT = path.resolve(process.cwd(), ".briefs-snapshot");

export interface BriefMeta {
  iso_week: string;
  through_date: string;
  generated_at: string;
  generated_by: string;
  title: string;
  volume: number;
  registry_version?: number;
  sweep?: { attempted: number; succeeded: number; failed: number };
  sources_reviewed?: Array<{
    id: string;
    status: string;
    items_captured?: number;
    items_included?: number;
    last_item_date?: string;
    error?: string;
  }>;
  notes?: string[];
}

export interface BriefRecord {
  week: string;
  title: string;
  volume: number;
  date: string;
  markdown: string;
  meta: BriefMeta | null;
}

function ensureSnapshot(): void {
  if (!fs.existsSync(SNAPSHOT_ROOT)) {
    throw new Error(
      `briefs snapshot missing at ${SNAPSHOT_ROOT}. Run \`node scripts/snapshot-briefs.mjs\` (this normally runs via predev/prebuild).`,
    );
  }
}

function isBriefWeekDir(name: string): boolean {
  return /^\d{4}-W\d{2}$/.test(name);
}

function readBriefDir(week: string): BriefRecord {
  const dir = path.join(SNAPSHOT_ROOT, week);
  const mdPath = path.join(dir, "brief.md");
  if (!fs.existsSync(mdPath)) {
    throw new Error(`brief.md missing under ${dir}`);
  }

  const raw = fs.readFileSync(mdPath, "utf8");
  const parsed = matter(raw);
  const markdown = parsed.content;

  let meta: BriefMeta | null = null;
  const metaPath = path.join(dir, "meta.yaml");
  if (fs.existsSync(metaPath)) {
    const metaRaw = fs.readFileSync(metaPath, "utf8");
    // JSON_SCHEMA keeps dates as strings — otherwise React refuses to
    // render the Date objects js-yaml deserializes by default.
    meta = yaml.load(metaRaw, { schema: yaml.JSON_SCHEMA }) as BriefMeta;
  }

  const titleMatch = /^#\s+(.+?)\s*$/m.exec(markdown);
  const title = meta?.title ?? titleMatch?.[1] ?? week;
  const volume = meta?.volume ?? 0;
  const date = meta?.through_date ?? "";

  return { week, title, volume, date, markdown, meta };
}

export function listBriefs(): BriefRecord[] {
  ensureSnapshot();
  return fs
    .readdirSync(SNAPSHOT_ROOT)
    .filter(isBriefWeekDir)
    .sort()
    .reverse()
    .map(readBriefDir);
}

export function getBrief(week: string): BriefRecord | null {
  ensureSnapshot();
  if (!isBriefWeekDir(week)) {
    return null;
  }
  const dir = path.join(SNAPSHOT_ROOT, week);
  if (!fs.existsSync(dir)) {
    return null;
  }
  return readBriefDir(week);
}

export function listWeeks(): string[] {
  ensureSnapshot();
  return fs.readdirSync(SNAPSHOT_ROOT).filter(isBriefWeekDir).sort().reverse();
}
