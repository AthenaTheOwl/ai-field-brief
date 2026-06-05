#!/usr/bin/env python3
"""Per-source signal-density audit.

Walks sources/registry.yaml and briefs/*/items/*.md to compute, per source:
- inclusion count across N most recent briefs
- last brief week the source appeared in
- days since last_reviewed
- yield (items per brief)
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

import yaml


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "sources" / "registry.yaml"
DEFAULT_OUT_DIR = ROOT / "ops" / "source-audits"
SOURCE_RE = re.compile(r"\*\*Source:\*\*\s*([^\n\r]+)")
CELLS_RE = re.compile(r"\*\*Cells:\*\*\s*([^\n\r]+)")


@dataclass
class SourceStat:
    id: str
    name: str
    status: str
    last_reviewed: str | None
    appearances: int = 0
    cell_promoted: int = 0  # items whose Cells: line is non-empty
    last_week: str | None = None
    weeks_seen: set[str] = field(default_factory=set)


def load_registry(path: Path) -> list[dict]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data.get("sources", []) or []


def collect_items(briefs_root: Path) -> list[tuple[str, str, list[str]]]:
    """Return [(week, source_name, cells), ...] for every item file."""
    out: list[tuple[str, str, list[str]]] = []
    for item in briefs_root.rglob("items/*.md"):
        try:
            week = item.parent.parent.name  # briefs/2026-W22/items/x.md
        except IndexError:
            continue
        text = item.read_text(encoding="utf-8", errors="replace")
        m = SOURCE_RE.search(text)
        if not m:
            continue
        src_name = m.group(1).strip()
        cells_match = CELLS_RE.search(text)
        cells: list[str] = []
        if cells_match:
            raw = cells_match.group(1).strip()
            if raw and raw.lower() not in ("none", "n/a", "-"):
                cells = [c.strip() for c in raw.split(",") if c.strip()]
        out.append((week, src_name, cells))
    return out


def match_source(item_source: str, registry: list[dict]) -> str | None:
    """Substring-match item Source: text against registry names.

    Returns the registry source id, or None if no match.
    Deterministic by sort order on registry id when ambiguous.
    """
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
    items: list[tuple[str, str, list[str]]],
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
    for week, src_name, cells in items:
        sid = match_source(src_name, registry)
        if sid is None:
            unmatched.append((week, src_name))
            continue
        stat = stats[sid]
        stat.appearances += 1
        if cells:
            stat.cell_promoted += 1
        stat.weeks_seen.add(week)
        if week > (stat.last_week or ""):
            stat.last_week = week
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
    """Suggested tier from yield. Tunable thresholds."""
    if brief_count == 0:
        return "?"
    yield_ratio = stat.appearances / brief_count
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
    out.append(f"| core | {len(by_tier['core'])} | yield ≥ 0.5 items/brief |")
    out.append(f"| standard | {len(by_tier['standard'])} | 0.1 ≤ yield < 0.5 |")
    out.append(f"| candidate | {len(by_tier['candidate'])} | <0.1 yield but non-zero |")
    out.append(f"| retire-review | {len(by_tier['retire-review'])} | 0 appearances in window |")
    out.append("")

    out.append("## Sources flagged for retire-review (0 items in window)")
    out.append("")
    retire = sorted(
        by_tier["retire-review"],
        key=lambda s: (days_since(s.last_reviewed, today) or 0, s.id),
        reverse=True,
    )
    if not retire:
        out.append("None.")
    else:
        out.append("| Source | Status | Last reviewed | Days since |")
        out.append("|---|---|---|---|")
        for s in retire[:50]:
            d = days_since(s.last_reviewed, today)
            d_str = str(d) if d is not None else "—"
            out.append(f"| {s.name} | {s.status} | {s.last_reviewed or '—'} | {d_str} |")
        if len(retire) > 50:
            out.append(f"")
            out.append(f"_(showing 50 of {len(retire)})_")
    out.append("")

    out.append("## Core + standard sources (yield ≥ 0.1 items/brief)")
    out.append("")
    high = sorted(
        by_tier["core"] + by_tier["standard"],
        key=lambda s: -s.appearances,
    )
    if not high:
        out.append("None.")
    else:
        out.append("| Source | Tier | Items | Promoted to matrix | Last week |")
        out.append("|---|---|---|---|---|")
        for s in high:
            tier = tier_for(s, len(brief_weeks))
            out.append(
                f"| {s.name} | {tier} | {s.appearances} | "
                f"{s.cell_promoted} | {s.last_week or '—'} |"
            )
    out.append("")

    if unmatched:
        out.append("## Unmatched item sources (referenced in briefs, not in registry)")
        out.append("")
        out.append("Reviewer action: add to registry or fix the item Source: text.")
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
        "Source-name matching is fuzzy: an item's `**Source:**` field is matched "
        "against registry `name` by case-insensitive substring containment in "
        "either direction. Tier thresholds (yield ≥ 0.5 = core; ≥ 0.1 = standard; "
        ">0 = candidate; 0 = retire-review) are heuristic — tune in "
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
    items = [(w, n, c) for (w, n, c) in items_all if w in weeks]

    stats, unmatched = compute_stats(registry, items)
    today = dt.date.today()
    report = render(stats, unmatched, weeks, today, registry_version)

    out_path = args.out or (DEFAULT_OUT_DIR / f"{today.isoformat()}.md")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")
    print(f"wrote {out_path}")
    print(
        f"  {sum(1 for s in stats.values() if s.appearances == 0)} sources flagged for retire-review,"
        f" {sum(1 for s in stats.values() if s.appearances > 0)} active,"
        f" {len(unmatched)} unmatched item-source(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
