#!/usr/bin/env python3
"""Cadence gate for ai-field-brief.

Three checks:

1. **INDEX sync** — ``briefs/INDEX.md``'s top-of-table row references the
   newest ISO-week folder under ``briefs/``.
2. **README sync** — ``README.md``'s ``**Latest:**`` line names the newest
   brief's title.
3. **Cadence freshness** — the newest brief's ``meta.yaml`` ``through_date``
   is no older than ``--cadence-window`` days (default 8), allowing one
   slip-week before the gate trips.

An optional ``briefs/SKIPS.yaml`` file documents intentional misses; any
ISO week listed there is treated as a "covered" week for the cadence
calculation. SKIPS is the explicit acknowledgement: "we skipped W24 on
purpose, here is why."

Exits 1 with a categorized list of failures. Designed to run in CI on
every PR + on a Sunday cron so the cadence promise is mechanical rather
than memory-dependent.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import yaml


ROOT = Path(__file__).resolve().parents[1]
BRIEFS = ROOT / "briefs"
INDEX = BRIEFS / "INDEX.md"
README = ROOT / "README.md"
SKIPS = BRIEFS / "SKIPS.yaml"

WEEK_RE = re.compile(r"^(\d{4})-W(\d{2})(?:-[\w-]+)?$")
INDEX_ROW_RE = re.compile(r"\|\s*\[(\d{4}-W\d{2})\]\(\./(\d{4}-W\d{2})/brief\.md\)")
README_LATEST_RE = re.compile(r"\*\*Latest:\*\*\s*\[(?P<title>[^\]]+)\]")
LATEST_WEEK_IN_TITLE_RE = re.compile(r"(\d{4}-W\d{2})")


@dataclass(frozen=True)
class CadenceFailure:
    kind: str  # "index", "readme", "stale", "missing-meta", "no-briefs"
    detail: str


def latest_week_folder(briefs: Path) -> str | None:
    """Return the newest ISO-week folder name (excluding -rerun siblings)."""
    weeks: list[tuple[int, int, str]] = []
    if not briefs.is_dir():
        return None
    for entry in briefs.iterdir():
        if not entry.is_dir():
            continue
        match = WEEK_RE.match(entry.name)
        if not match:
            continue
        if entry.name.endswith("-rerun"):
            continue
        weeks.append((int(match.group(1)), int(match.group(2)), entry.name))
    if not weeks:
        return None
    weeks.sort()
    return weeks[-1][2]


def parse_index_top_row(index: Path) -> str | None:
    """Return the ISO-week named on the first data row of INDEX.md."""
    if not index.is_file():
        return None
    for line in index.read_text(encoding="utf-8").splitlines():
        m = INDEX_ROW_RE.search(line)
        if m:
            return m.group(1)
    return None


def parse_readme_latest_week(readme: Path) -> str | None:
    """Return the ISO-week parsed from the README's **Latest:** title."""
    if not readme.is_file():
        return None
    text = readme.read_text(encoding="utf-8")
    m = README_LATEST_RE.search(text)
    if not m:
        return None
    week_match = LATEST_WEEK_IN_TITLE_RE.search(m.group("title"))
    return week_match.group(1) if week_match else None


def parse_brief_through_date(brief_folder: Path) -> dt.date | None:
    """Read meta.yaml's through_date; return None if absent or malformed."""
    meta = brief_folder / "meta.yaml"
    if not meta.is_file():
        return None
    try:
        data = yaml.safe_load(meta.read_text(encoding="utf-8"))
    except yaml.YAMLError:
        return None
    raw = data.get("through_date") if isinstance(data, dict) else None
    if isinstance(raw, dt.date):
        return raw
    if isinstance(raw, str):
        try:
            return dt.date.fromisoformat(raw[:10])
        except ValueError:
            return None
    return None


def load_skips(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError:
        return set()
    if not isinstance(data, dict):
        return set()
    skips = data.get("skipped_weeks") or []
    return {str(w) for w in skips if isinstance(w, (str, int))}


def check(
    briefs_root: Path = BRIEFS,
    index_path: Path = INDEX,
    readme_path: Path = README,
    skips_path: Path = SKIPS,
    cadence_window_days: int = 8,
    today: dt.date | None = None,
) -> list[CadenceFailure]:
    """Run all three checks; return a list of failure records (empty = pass)."""
    if today is None:
        raise ValueError(
            "today must be provided — cadence_check does not consult the system "
            "clock implicitly. Pass dt.date.today() from the caller."
        )

    failures: list[CadenceFailure] = []

    latest_folder = latest_week_folder(briefs_root)
    if latest_folder is None:
        failures.append(CadenceFailure("no-briefs", "no ISO-week brief folders found"))
        return failures

    index_week = parse_index_top_row(index_path)
    if index_week != latest_folder:
        failures.append(
            CadenceFailure(
                "index",
                f"INDEX top row references {index_week!r}; newest folder is {latest_folder!r}",
            )
        )

    readme_week = parse_readme_latest_week(readme_path)
    if readme_week != latest_folder:
        failures.append(
            CadenceFailure(
                "readme",
                f"README **Latest:** names {readme_week!r}; newest folder is {latest_folder!r}",
            )
        )

    through_date = parse_brief_through_date(briefs_root / latest_folder)
    if through_date is None:
        failures.append(
            CadenceFailure(
                "missing-meta",
                f"briefs/{latest_folder}/meta.yaml has no parseable through_date",
            )
        )
    else:
        skips = load_skips(skips_path)
        age_days = (today - through_date).days
        if latest_folder not in skips and age_days > cadence_window_days:
            failures.append(
                CadenceFailure(
                    "stale",
                    f"newest brief {latest_folder} is {age_days} day(s) old "
                    f"(cadence window: {cadence_window_days})",
                )
            )

    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cadence-window",
        type=int,
        default=8,
        help="max days between today and the newest brief's through_date (default 8 = one slip-week)",
    )
    parser.add_argument(
        "--today",
        type=str,
        default=None,
        help="ISO date to use as 'today' (default: system date). Useful for tests.",
    )
    args = parser.parse_args()

    today = (
        dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    )

    failures = check(
        briefs_root=BRIEFS,
        index_path=INDEX,
        readme_path=README,
        skips_path=SKIPS,
        cadence_window_days=args.cadence_window,
        today=today,
    )

    if failures:
        print(
            f"cadence_check: {len(failures)} failure(s)",
            file=sys.stderr,
        )
        for f in failures:
            print(f"  - {f.kind}: {f.detail}", file=sys.stderr)
        return 1

    print("cadence_check OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
