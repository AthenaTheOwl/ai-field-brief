import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";
import yaml from "js-yaml";

/**
 * Reads briefs from the build-time snapshot when present, with a repo-root
 * fallback for deploy configurations that run `next build` directly. Brief
 * weeks are discovered from folders; no week names are baked into the app.
 */

const APP_ROOT = path.basename(process.cwd()) === "web"
  ? process.cwd()
  : path.resolve(process.cwd(), "apps", "web");
const SNAPSHOT_ROOT = path.resolve(APP_ROOT, ".briefs-snapshot");
const REPO_BRIEFS_ROOT = path.resolve(APP_ROOT, "..", "..", "briefs");

export interface BriefMeta {
  iso_week: string;
  through_date: string;
  generated_at: string;
  generated_by: string;
  title: string;
  summary?: string;
  volume: number;
  registry_version?: number;
  sweep?: { attempted: number; succeeded: number; failed: number };
  top_signal_count?: number;
  action_packet_count?: number;
  scout_count?: number;
  sources_reviewed?: Array<{
    id?: string;
    label?: string;
    url?: string;
    status?: string;
    disposition?: string;
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

export function formatBriefActivity(meta: BriefMeta | null): string {
  if (!meta) {
    return "Read the latest brief.";
  }

  if (meta.sweep) {
    const succeeded = meta.sweep.succeeded ?? 0;
    const attempted = meta.sweep.attempted ?? 0;
    const topSignals = typeof meta.top_signal_count === "number" ? meta.top_signal_count : null;
    const actionPackets = typeof meta.action_packet_count === "number" ? meta.action_packet_count : null;

    const parts = [`${succeeded} of ${attempted} sources swept`];
    if (topSignals !== null) {
      parts.push(`${topSignals} Top signals`);
    }
    if (actionPackets !== null) {
      parts.push(`${actionPackets} action packets`);
    }
    return `${parts.join(", ")}.`;
  }

  if (meta.sources_reviewed?.length) {
    const okCount = meta.sources_reviewed.filter((source) => source.status === "ok").length;
    const includedCount = meta.sources_reviewed.reduce(
      (sum, source) => sum + (source.items_included ?? 0),
      0,
    );
    return `${okCount} sources swept, ${includedCount} items included.`;
  }

  return "Read the latest brief.";
}


function isBriefWeekDir(name: string): boolean {
  return /^\d{4}-W\d{2}$/.test(name);
}

function briefRootStatus(root: string): {
  exists: boolean;
  weeks: string[];
  missingBriefs: string[];
} {
  if (!fs.existsSync(root)) {
    return { exists: false, weeks: [], missingBriefs: [] };
  }

  const weeks = fs.readdirSync(root).filter(isBriefWeekDir).sort();
  const missingBriefs = weeks
    .map((week) => path.join(root, week, "brief.md"))
    .filter((briefPath) => !fs.existsSync(briefPath))
    .map((briefPath) => path.relative(root, briefPath));

  return { exists: true, weeks, missingBriefs };
}

export function resolveBriefsRoot(): string {
  const snapshot = briefRootStatus(SNAPSHOT_ROOT);
  if (snapshot.weeks.length > 0 && snapshot.missingBriefs.length === 0) {
    return SNAPSHOT_ROOT;
  }

  const repoRoot = briefRootStatus(REPO_BRIEFS_ROOT);
  if (repoRoot.weeks.length > 0 && repoRoot.missingBriefs.length === 0) {
    return REPO_BRIEFS_ROOT;
  }

  const problems = [
    `snapshot=${SNAPSHOT_ROOT} exists=${snapshot.exists} weeks=${snapshot.weeks.length} missing=${snapshot.missingBriefs.join(", ") || "none"}`,
    `repo=${REPO_BRIEFS_ROOT} exists=${repoRoot.exists} weeks=${repoRoot.weeks.length} missing=${repoRoot.missingBriefs.join(", ") || "none"}`,
  ];
  throw new Error(
    `briefs source unavailable or incomplete. Run \`node apps/web/scripts/snapshot-briefs.mjs\` from the repo root or \`node scripts/snapshot-briefs.mjs\` from apps/web. ${problems.join("; ")}`,
  );
}

function readBriefDir(root: string, week: string): BriefRecord {
  const dir = path.join(root, week);
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
    // JSON_SCHEMA keeps dates as strings; otherwise React refuses to
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
  const root = resolveBriefsRoot();
  return fs
    .readdirSync(root)
    .filter(isBriefWeekDir)
    .sort()
    .reverse()
    .map((week) => readBriefDir(root, week));
}

export function getBrief(week: string): BriefRecord | null {
  const root = resolveBriefsRoot();
  if (!isBriefWeekDir(week)) {
    return null;
  }
  const dir = path.join(root, week);
  if (!fs.existsSync(dir)) {
    return null;
  }
  return readBriefDir(root, week);
}

export function listWeeks(): string[] {
  const root = resolveBriefsRoot();
  return fs.readdirSync(root).filter(isBriefWeekDir).sort().reverse();
}
