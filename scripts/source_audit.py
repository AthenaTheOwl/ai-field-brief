#!/usr/bin/env python3
"""Per-source signal-density audit.

Walks sources/registry.yaml and each brief's current meta.yaml (falling back to
legacy briefs/*/items/*.md) to compute, per source:
- review and inclusion counts across N most recent briefs
- last brief week the source appeared in
- days since last_reviewed
- yield (inclusions per review)
- recommended status: core / standard / candidate / retire-review

Source-name matching is fuzzy: an item's `**Source:**` field is matched
against registry names by case-insensitive substring containment in either
direction. Names like "Anthropic News + Simon Willison" match both
"Anthropic News" and "Simon Willison" in the registry; ambiguous matches
are recorded but credited only to the first match (deterministic by sort
order on registry id).

Writes a Markdown report to ops/source-audits/<date>.md (or --out).
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "sources" / "registry.yaml"
DEFAULT_OUT_DIR = ROOT / "ops" / "source-audits"
SOURCE_RE = re.compile(r"\*\*Source:\*\*\s*([^\n\r]+)")
CELLS_RE = re.compile(r"\*\*Cells:\*\*\s*([^\n\r]+)")
EXCLUDED_DISPOSITIONS = {
    "archive",
    "continuity_input",
    "failed_current_index",
    "reviewed_no_pick",
    "scout_input",
    "synthesis_input",
}
INTERNAL_URL_SCHEMES = {"google-drive", "internal"}


@dataclass(frozen=True)
class SourceAppearance:
    week: str
    name: str
    url: str | None
    disposition: str
    included: bool
    cells: tuple[str, ...] = ()


@dataclass
class SourceStat:
    id: str
    name: str
    status: str
    last_reviewed: str | None
    reviews: int = 0
    appearances: int = 0
    cell_promoted: int = 0  # items whose Cells: line is non-empty
    last_week: str | None = None
    weeks_seen: set[str] = field(default_factory=set)


def load_registry(path: Path) -> list[dict]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data.get("sources", []) or []


def _meta_appearances(week_dir: Path) -> list[SourceAppearance] | None:
    meta_path = week_dir / "meta.yaml"
    if not meta_path.exists():
        return None
    try:
        payload = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return None
    sources = payload.get("sources_reviewed")
    if not isinstance(sources, list):
        return None
    out: list[SourceAppearance] = []
    for source in sources:
        if not isinstance(source, dict):
            continue
        name = str(source.get("label") or "").strip()
        url = str(source.get("url") or "").strip() or None
        if not name:
            continue
        if url and urlsplit(url).scheme.lower() in INTERNAL_URL_SCHEMES:
            continue
        disposition = str(source.get("disposition") or "reviewed").strip().lower()
        included = disposition not in EXCLUDED_DISPOSITIONS
        cells = ("top-signal",) if disposition.startswith("top_signal") else ()
        out.append(
            SourceAppearance(
                week=week_dir.name,
                name=name,
                url=url,
                disposition=disposition,
                included=included,
                cells=cells,
            )
        )
    return out


def _legacy_appearances(week_dir: Path) -> list[SourceAppearance]:
    out: list[SourceAppearance] = []
    for item in sorted((week_dir / "items").glob("*.md")):
        text = item.read_text(encoding="utf-8", errors="replace")
        match = SOURCE_RE.search(text)
        if not match:
            continue
        cells_match = CELLS_RE.search(text)
        cells: tuple[str, ...] = ()
        if cells_match:
            raw = cells_match.group(1).strip()
            if raw and raw.lower() not in ("none", "n/a", "-"):
                cells = tuple(cell.strip() for cell in raw.split(",") if cell.strip())
        out.append(
            SourceAppearance(
                week=week_dir.name,
                name=match.group(1).strip(),
                url=None,
                disposition="legacy-item",
                included=True,
                cells=cells,
            )
        )
    return out


def collect_items(briefs_root: Path) -> list[SourceAppearance]:
    """Collect current metadata, with legacy item files as a per-week fallback."""

    out: list[SourceAppearance] = []
    for week_dir in sorted(path for path in briefs_root.iterdir() if path.is_dir()):
        metadata = _meta_appearances(week_dir)
        out.extend(metadata if metadata is not None else _legacy_appearances(week_dir))
    return out


def _canonical_url(value: str) -> str:
    parsed = urlsplit(value.strip())
    path = parsed.path.rstrip("/") or "/"
    return urlunsplit((parsed.scheme.lower(), parsed.netloc.lower(), path, "", ""))


def match_source(
    item_source: str,
    registry: list[dict],
    source_url: str | None = None,
) -> str | None:
    """Match by canonical URL first, then fall back to source-name containment.

    Returns the registry source id, or None if no match.
    Deterministic by sort order on registry id when ambiguous.
    """
    if source_url:
        observed = _canonical_url(source_url)
        observed_parts = urlsplit(observed)
        url_candidates: list[tuple[int, str]] = []
        for source in registry:
            registry_url = str(source.get("url") or "").strip()
            if not registry_url:
                continue
            candidate = _canonical_url(registry_url)
            candidate_parts = urlsplit(candidate)
            if candidate == observed:
                url_candidates.append((len(candidate), source["id"]))
                continue
            prefix = candidate.rstrip("/") + "/"
            if (
                candidate_parts.scheme == observed_parts.scheme
                and candidate_parts.netloc == observed_parts.netloc
                and observed.startswith(prefix)
            ):
                url_candidates.append((len(candidate), source["id"]))
        if url_candidates:
            return sorted(url_candidates, key=lambda row: (-row[0], row[1]))[0][1]

    src_lower = item_source.lower()
    candidates: list[str] = []
    for s in registry:
        name = s.get("name", "")
        if not name:
            continue
        name_lower = name.lower()
        if name_lower in src_lower or src_lower in name_lower:
            candidates.append(s["id"])
    if not candidates:
        return None
    return sorted(candidates)[0]


def compute_stats(
    registry: list[dict],
    items: list[SourceAppearance],
) -> tuple[dict[str, SourceStat], list[tuple[str, str]]]:
    """Roll items up per registry source. Returns (stats, unmatched)."""
    stats: dict[str, SourceStat] = {
        s["id"]: SourceStat(
            id=s["id"],
            name=s.get("name", s["id"]),
            status=s.get("status", "unknown"),
            last_reviewed=str(s["last_reviewed"]) if s.get("last_reviewed") else None,
        )
        for s in registry
    }
    unmatched: list[tuple[str, str]] = []  # (week, source_name)
    for item in items:
        sid = match_source(item.name, registry, item.url)
        if sid is None:
            unmatched.append((item.week, item.name))
            continue
        stat = stats[sid]
        stat.reviews += 1
        if not item.included:
            continue
        stat.appearances += 1
        if item.cells:
            stat.cell_promoted += 1
        stat.weeks_seen.add(item.week)
        if item.week > (stat.last_week or ""):
            stat.last_week = item.week
    return stats, unmatched


def days_since(date_str: str | None, today: dt.date) -> int | None:
    if not date_str:
        return None
    try:
        d = dt.date.fromisoformat(date_str[:10])
    except ValueError:
        return None
    return (today - d).days


def tier_for(stat: SourceStat, brief_count: int) -> str:
    """Suggest a tier from observed inclusion yield, preserving unreviewed sources."""
    if brief_count == 0 or stat.reviews == 0:
        return "unreviewed"
    yield_ratio = stat.appearances / stat.reviews
    if yield_ratio >= 0.5:
        return "core"
    if yield_ratio >= 0.1:
        return "standard"
    if stat.appearances > 0:
        return "candidate"
    return "retire-review"


def render(
    stats: dict[str, SourceStat],
    unmatched: list[tuple[str, str]],
    brief_weeks: list[str],
    today: dt.date,
    registry_version: int | None,
) -> str:
    out: list[str] = []
    out.append(f"# Source-density audit — {today.isoformat()}")
    out.append("")
    out.append(f"- Registry version: `{registry_version}`")
    out.append(f"- Briefs in window: {len(brief_weeks)} ({', '.join(brief_weeks) or '—'})")
    out.append(f"- Sources in registry: {len(stats)}")
    out.append("")

    by_tier: dict[str, list[SourceStat]] = defaultdict(list)
    for sid, s in stats.items():
        by_tier[tier_for(s, len(brief_weeks))].append(s)

    out.append("## Tier summary")
    out.append("")
    out.append("| Tier | Count | Definition |")
    out.append("|---|---|---|")
    out.append(f"| core | {len(by_tier['core'])} | yield ≥ 0.5 inclusions/review |")
    out.append(f"| standard | {len(by_tier['standard'])} | 0.1 ≤ yield < 0.5 |")
    out.append(f"| candidate | {len(by_tier['candidate'])} | <0.1 yield but non-zero |")
    out.append(f"| retire-review | {len(by_tier['retire-review'])} | reviewed but not included |")
    out.append(f"| unreviewed | {len(by_tier['unreviewed'])} | not reviewed in this window |")
    out.append("")

    out.append("## Sources flagged for retire-review")
    out.append("")
    retire = sorted(
        by_tier["retire-review"],
        key=lambda s: (days_since(s.last_reviewed, today) or 0, s.id),
        reverse=True,
    )
    if not retire:
        out.append("None.")
    else:
        out.append("| Source | Reviews | Included | Last reviewed | Days since |")
        out.append("|---|---:|---:|---|---:|")
        for s in retire[:50]:
            d = days_since(s.last_reviewed, today)
            d_str = str(d) if d is not None else "—"
            out.append(
                f"| {s.name} | {s.reviews} | {s.appearances} | "
                f"{s.last_reviewed or '—'} | {d_str} |"
            )
        if len(retire) > 50:
            out.append(f"")
            out.append(f"_(showing 50 of {len(retire)})_")
    out.append("")

    out.append("## Core + standard sources (yield ≥ 0.1 inclusions/review)")
    out.append("")
    high = sorted(
        by_tier["core"] + by_tier["standard"],
        key=lambda s: -s.appearances,
    )
    if not high:
        out.append("None.")
    else:
        out.append("| Source | Tier | Reviewed | Included | Top signals | Last week |")
        out.append("|---|---|---:|---:|---:|---|")
        for s in high:
            tier = tier_for(s, len(brief_weeks))
            out.append(
                f"| {s.name} | {tier} | {s.reviews} | {s.appearances} | "
                f"{s.cell_promoted} | {s.last_week or '—'} |"
            )
    out.append("")

    if unmatched:
        out.append("## Citation-only and unmatched sources")
        out.append("")
        out.append(
            "These references are not automatically defects. Add recurring feeds and "
            "framework surfaces to the registry; leave one-off papers and articles as "
            "citation-level inputs unless they become a repeated source."
        )
        out.append("")
        unmatched_counts: dict[str, int] = defaultdict(int)
        for week, name in unmatched:
            unmatched_counts[name] += 1
        out.append("| Source text in item | Occurrences |")
        out.append("|---|---|")
        for name, c in sorted(unmatched_counts.items(), key=lambda x: -x[1]):
            out.append(f"| {name} | {c} |")
        out.append("")

    out.append("## Methodology")
    out.append("")
    out.append(
        "Current brief metadata is matched to the registry by canonical URL and "
        "longest same-origin URL prefix before a fuzzy name fallback. Legacy item "
        "files are used only when a week has no `sources_reviewed` metadata. Yield "
        "is inclusions per review; an unreviewed source is never labeled for "
        "retirement. Tier thresholds (yield ≥ 0.5 = core; ≥ 0.1 = standard; "
        ">0 = candidate; reviewed with 0 inclusions = retire-review) are heuristic. "
        "Tune them in "
        "`scripts/source_audit.py::tier_for`."
    )
    out.append("")

    return "\n".join(out) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--briefs", type=Path, default=ROOT / "briefs")
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument(
        "--window",
        type=int,
        default=8,
        help="how many most-recent brief weeks to include (default 8).",
    )
    args = parser.parse_args()

    registry_data = yaml.safe_load(args.registry.read_text(encoding="utf-8"))
    registry_version = registry_data.get("version")
    registry = registry_data.get("sources", [])

    weeks_all = sorted(
        d.name for d in args.briefs.iterdir()
        if d.is_dir() and d.name.startswith("2026-W") and not d.name.endswith("-rerun")
    )
    weeks = weeks_all[-args.window :]
    items_all = collect_items(args.briefs)
    items = [item for item in items_all if item.week in weeks]

    stats, unmatched = compute_stats(registry, items)
    today = dt.date.today()
    report = render(stats, unmatched, weeks, today, registry_version)

    out_path = args.out or (DEFAULT_OUT_DIR / f"{today.isoformat()}.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")
    print(f"wrote {out_path}")
    print(
        f"  {sum(1 for s in stats.values() if tier_for(s, len(weeks)) == 'retire-review')}"
        " sources flagged for retire-review,"
        f" {sum(1 for s in stats.values() if s.appearances > 0)} included,"
        f" {sum(1 for s in stats.values() if s.reviews == 0)} unreviewed,"
        f" {len(unmatched)} unmatched item-source(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
