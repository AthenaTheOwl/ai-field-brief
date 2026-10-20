#!/usr/bin/env python3
"""Cadence gate for ai-field-brief.

Five checks:

1. **INDEX sync** — ``briefs/INDEX.md``'s top-of-table row references the
   newest ISO-week folder under ``briefs/``.
2. **README sync** — ``README.md``'s ``**Latest:**`` line names the newest
   brief's title.
3. **Cadence freshness** — the newest brief's ``meta.yaml`` ``through_date``
   is no older than ``--cadence-window`` days (default 8), allowing one
   slip-week before the gate trips.
4. **ISO-week truth** — the folder, ``meta.yaml`` ``iso_week``, and the ISO
   week containing ``through_date`` agree.
5. **Coverage** — every week from the first issue through the most recent
   Friday has a brief and metadata, or an explicit entry in SKIPS.yaml.
   A fresh latest issue cannot hide an older missing week. A due week
   stays pending, not missing, until the cadence window has run out on
   it, so coverage allows the same slip-week as check 3.

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
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
BRIEFS = ROOT / "briefs"
INDEX = BRIEFS / "INDEX.md"
README = ROOT / "README.md"
SKIPS = BRIEFS / "SKIPS.yaml"

WEEK_RE = re.compile(r"^(\d{4})-W(\d{2})$")
INDEX_ROW_RE = re.compile(r"\|\s*\[(\d{4}-W\d{2})\]\(\./(\d{4}-W\d{2})/brief\.md\)")
README_LATEST_RE = re.compile(r"\*\*Latest:\*\*\s*\[(?P<title>[^\]]+)\]")
LATEST_WEEK_IN_TITLE_RE = re.compile(r"(\d{4}-W\d{2})")


@dataclass(frozen=True)
class CadenceFailure:
    kind: str  # categorized sync, metadata, date or coverage failure
    detail: str


def latest_week_folder(briefs: Path) -> str | None:
    """Return the newest canonical ISO-week folder (excluding all suffixes)."""
    weeks: list[tuple[int, int, str]] = []
    if not briefs.is_dir():
        return None
    for entry in briefs.iterdir():
        if not entry.is_dir():
            continue
        match = WEEK_RE.match(entry.name)
        if not match:
            continue
        try:
            dt.date.fromisocalendar(int(match.group(1)), int(match.group(2)), 1)
        except ValueError:
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


def parse_brief_iso_week(brief_folder: Path) -> str | None:
    """Read and validate the canonical ISO-week label from meta.yaml."""

    meta = brief_folder / "meta.yaml"
    if not meta.is_file():
        return None
    try:
        data = yaml.safe_load(meta.read_text(encoding="utf-8"))
    except yaml.YAMLError:
        return None
    raw = data.get("iso_week") if isinstance(data, dict) else None
    return raw if isinstance(raw, str) and re.fullmatch(r"\d{4}-W\d{2}", raw) else None


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


def coverage_report(
    briefs_root: Path,
    today: dt.date,
    skips_path: Path,
    cadence_window_days: int = 8,
) -> dict:
    """Report weekly gaps against the Friday deadline without inventing issues.

    A week is due once its Friday has passed. It counts as missing only
    when more than ``cadence_window_days`` days have passed since the
    Sunday that closes the week before it: the allowance check 3 gives an
    issue that covers through that Sunday. Until then it is pending,
    unless a later canonical issue already exists: then the gap is
    missing at once, so a fresh newer issue cannot hide it.
    """
    folders: dict[dt.date, Path] = {}
    if briefs_root.is_dir():
        for entry in briefs_root.iterdir():
            match = WEEK_RE.fullmatch(entry.name)
            if not entry.is_dir() or not match:
                continue
            try:
                monday = dt.date.fromisocalendar(int(match[1]), int(match[2]), 1)
            except ValueError:
                continue
            folders[monday] = entry
    due_friday = today - dt.timedelta(days=(today.weekday() - 4) % 7)
    due_monday = due_friday - dt.timedelta(days=4)
    overdue_monday = today - dt.timedelta(days=cadence_window_days)
    skipped = load_skips(skips_path)
    complete_mondays = [
        monday
        for monday, folder in folders.items()
        if all((folder / name).is_file() for name in ("brief.md", "meta.yaml"))
    ]
    newest_issue = max(complete_mondays) if complete_mondays else None
    missing = []
    pending = []
    if folders:
        cursor = min(folders)
        while cursor <= due_monday:
            week = f"{cursor.isocalendar().year}-W{cursor.isocalendar().week:02d}"
            folder = folders.get(cursor)
            complete = folder and all((folder / name).is_file() for name in ("brief.md", "meta.yaml"))
            if not complete and week not in skipped:
                overdue = cursor <= overdue_monday or (newest_issue is not None and cursor < newest_issue)
                (missing if overdue else pending).append(week)
            cursor += dt.timedelta(days=7)
    return {
        "as_of": today.isoformat(),
        "deadline": "Friday",
        "cadence_window_days": cadence_window_days,
        "due_through_week": f"{due_monday.isocalendar().year}-W{due_monday.isocalendar().week:02d}",
        "canonical_issue_count": len(folders),
        "missing_weeks": missing,
        "pending_weeks": pending,
        "skipped_weeks": sorted(skipped),
    }


def check(
    briefs_root: Path = BRIEFS,
    index_path: Path = INDEX,
    readme_path: Path = README,
    skips_path: Path = SKIPS,
    cadence_window_days: int = 8,
    today: dt.date | None = None,
) -> list[CadenceFailure]:
    """Run the checks; return a list of failure records (empty = pass)."""
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

    coverage = coverage_report(briefs_root, today, skips_path, cadence_window_days)
    for week in coverage["missing_weeks"]:
        failures.append(CadenceFailure("missing-week", f"{week} has no complete issue or explicit skip"))

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
        iso_year, iso_week, _ = through_date.isocalendar()
        expected_iso_week = f"{iso_year}-W{iso_week:02d}"
        meta_iso_week = parse_brief_iso_week(briefs_root / latest_folder)
        if latest_folder != expected_iso_week or meta_iso_week != expected_iso_week:
            failures.append(
                CadenceFailure(
                    "iso-week",
                    f"folder={latest_folder!r}, meta.iso_week={meta_iso_week!r}, "
                    f"through_date {through_date} belongs to {expected_iso_week}",
                )
            )
        age_days = (today - through_date).days
        if age_days < 0:
            failures.append(CadenceFailure("future-date", f"newest brief through_date {through_date} is after {today}"))
        # A skip belongs to the missing week. Listing an old published week
        # cannot waive freshness indefinitely.
        due_week = coverage["due_through_week"]
        if due_week not in load_skips(skips_path) and age_days > cadence_window_days:
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
        "--json",
        action="store_true",
        help="emit coverage and categorized failures as JSON",
    )
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

    if args.json:
        report = coverage_report(BRIEFS, today, SKIPS, args.cadence_window)
        report["failures"] = [{"kind": f.kind, "detail": f.detail} for f in failures]
        print(json.dumps(report, indent=2))
        return int(bool(failures))

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
