"""Tests for scripts/cadence_check.py.

Covers all four failure modes (index drift, readme drift, stale brief,
missing meta) plus the SKIPS.yaml allowlist + the clean-pass case.
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path

import pytest


sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from cadence_check import (  # noqa: E402  — sys.path injection above
    CadenceFailure,
    check,
    latest_week_folder,
    parse_brief_through_date,
    parse_index_top_row,
    parse_readme_latest_week,
)


def _scaffold(tmp_path: Path, week: str, through: str) -> tuple[Path, Path, Path]:
    """Build a minimal briefs/ + INDEX.md + README.md matching `week`."""
    briefs = tmp_path / "briefs"
    briefs.mkdir()
    week_folder = briefs / week
    week_folder.mkdir()
    (week_folder / "brief.md").write_text("# brief\n", encoding="utf-8")
    (week_folder / "meta.yaml").write_text(
        f"iso_week: {week}\nthrough_date: {through}\n",
        encoding="utf-8",
    )

    index = briefs / "INDEX.md"
    index.write_text(
        "# brief index\n\n"
        "| ISO week | Date | Title | Sources reviewed | Notes |\n"
        "|---|---|---|---|---|\n"
        f"| [{week}](./{week}/brief.md) | {through} | sample | 8 of 15 | testing |\n",
        encoding="utf-8",
    )

    readme = tmp_path / "README.md"
    readme.write_text(
        f"# AI field brief\n\n"
        f"**Latest:** [a title ({week})](https://example.com/briefs/{week})\n",
        encoding="utf-8",
    )

    return briefs, index, readme


def test_clean_repo_passes(tmp_path: Path) -> None:
    briefs, index, readme = _scaffold(tmp_path, "2026-W23", "2026-06-03")
    failures = check(
        briefs_root=briefs,
        index_path=index,
        readme_path=readme,
        skips_path=briefs / "SKIPS.yaml",
        cadence_window_days=8,
        today=dt.date(2026, 6, 5),
    )
    assert failures == []


def test_no_briefs_returns_failure(tmp_path: Path) -> None:
    briefs = tmp_path / "briefs"
    briefs.mkdir()
    failures = check(
        briefs_root=briefs,
        index_path=briefs / "INDEX.md",
        readme_path=tmp_path / "README.md",
        skips_path=briefs / "SKIPS.yaml",
        cadence_window_days=8,
        today=dt.date(2026, 6, 5),
    )
    assert any(f.kind == "no-briefs" for f in failures)


def test_index_drift_fails(tmp_path: Path) -> None:
    briefs, index, readme = _scaffold(tmp_path, "2026-W23", "2026-06-03")
    # Newer folder lands without updating INDEX.
    (briefs / "2026-W24").mkdir()
    (briefs / "2026-W24" / "meta.yaml").write_text(
        "iso_week: 2026-W24\nthrough_date: 2026-06-10\n", encoding="utf-8"
    )
    # README also needs to drift in this scenario, otherwise it'd be a
    # readme-only failure too; for the test we update the README so only
    # INDEX is wrong.
    readme.write_text(
        "**Latest:** [example (2026-W24)](https://x/2026-W24)\n", encoding="utf-8"
    )
    failures = check(
        briefs_root=briefs,
        index_path=index,
        readme_path=readme,
        skips_path=briefs / "SKIPS.yaml",
        cadence_window_days=8,
        today=dt.date(2026, 6, 11),
    )
    assert any(f.kind == "index" for f in failures)


def test_readme_drift_fails(tmp_path: Path) -> None:
    briefs, index, readme = _scaffold(tmp_path, "2026-W23", "2026-06-03")
    readme.write_text(
        "**Latest:** [an older title (2026-W21)](https://x/2026-W21)\n", encoding="utf-8"
    )
    failures = check(
        briefs_root=briefs,
        index_path=index,
        readme_path=readme,
        skips_path=briefs / "SKIPS.yaml",
        cadence_window_days=8,
        today=dt.date(2026, 6, 5),
    )
    assert any(f.kind == "readme" for f in failures)


def test_stale_brief_fails(tmp_path: Path) -> None:
    briefs, index, readme = _scaffold(tmp_path, "2026-W23", "2026-06-03")
    failures = check(
        briefs_root=briefs,
        index_path=index,
        readme_path=readme,
        skips_path=briefs / "SKIPS.yaml",
        cadence_window_days=8,
        today=dt.date(2026, 7, 1),  # 28 days after through_date
    )
    assert any(f.kind == "stale" for f in failures)


def test_stale_brief_allowed_via_skips(tmp_path: Path) -> None:
    briefs, index, readme = _scaffold(tmp_path, "2026-W23", "2026-06-03")
    skips = briefs / "SKIPS.yaml"
    skips.write_text(
        "skipped_weeks:\n  - 2026-W23\n", encoding="utf-8"
    )
    failures = check(
        briefs_root=briefs,
        index_path=index,
        readme_path=readme,
        skips_path=skips,
        cadence_window_days=8,
        today=dt.date(2026, 7, 1),
    )
    assert not any(f.kind == "stale" for f in failures)


def test_missing_meta_fails(tmp_path: Path) -> None:
    briefs, index, readme = _scaffold(tmp_path, "2026-W23", "2026-06-03")
    (briefs / "2026-W23" / "meta.yaml").unlink()
    failures = check(
        briefs_root=briefs,
        index_path=index,
        readme_path=readme,
        skips_path=briefs / "SKIPS.yaml",
        cadence_window_days=8,
        today=dt.date(2026, 6, 5),
    )
    assert any(f.kind == "missing-meta" for f in failures)


def test_latest_week_folder_skips_rerun_suffixes(tmp_path: Path) -> None:
    briefs = tmp_path / "briefs"
    briefs.mkdir()
    (briefs / "2026-W22").mkdir()
    (briefs / "2026-W22-rerun").mkdir()
    (briefs / "2026-W23").mkdir()
    assert latest_week_folder(briefs) == "2026-W23"


def test_check_refuses_implicit_today(tmp_path: Path) -> None:
    """The cadence check refuses to silently consult the system clock."""
    briefs = tmp_path / "briefs"
    briefs.mkdir()
    with pytest.raises(ValueError):
        check(
            briefs_root=briefs,
            index_path=briefs / "INDEX.md",
            readme_path=tmp_path / "README.md",
            skips_path=briefs / "SKIPS.yaml",
            cadence_window_days=8,
            today=None,
        )


def test_live_repo_passes_cadence_window() -> None:
    """The current repo state must satisfy the cadence gate on its own briefs.

    Uses a generous future date as 'today' so the test stays stable past
    the natural cadence window — the goal is to prove the live INDEX +
    README sync, not the wall-clock freshness.
    """
    repo = Path(__file__).resolve().parents[2]
    briefs = repo / "briefs"
    index = briefs / "INDEX.md"
    readme = repo / "README.md"
    failures = check(
        briefs_root=briefs,
        index_path=index,
        readme_path=readme,
        skips_path=briefs / "SKIPS.yaml",
        cadence_window_days=9999,  # disable the stale check for this test
        today=dt.date(2026, 6, 5),
    )
    # Only INDEX + README sync should be asserted here.
    sync_failures = [f for f in failures if f.kind in ("index", "readme")]
    if sync_failures:
        for f in sync_failures:
            print(f"  {f.kind}: {f.detail}")
    assert sync_failures == [], "live INDEX/README should sync with newest folder"
