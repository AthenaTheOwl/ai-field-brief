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
    coverage_report,
    latest_week_folder,
    parse_brief_iso_week,
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


def test_old_published_week_cannot_waive_freshness(tmp_path: Path) -> None:
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
    assert any(f.kind == "stale" for f in failures)


def test_due_week_can_be_explicitly_skipped(tmp_path: Path) -> None:
    briefs, index, readme = _scaffold(tmp_path, "2026-W23", "2026-06-03")
    skips = briefs / "SKIPS.yaml"
    skips.write_text("skipped_weeks:\n  - 2026-W24\n", encoding="utf-8")
    failures = check(briefs, index, readme, skips, today=dt.date(2026, 6, 12))
    assert not any(f.kind in ("stale", "missing-week") for f in failures)


def test_fresh_issue_does_not_hide_historical_gap(tmp_path: Path) -> None:
    briefs, index, readme = _scaffold(tmp_path, "2026-W25", "2026-06-19")
    older = briefs / "2026-W23"
    older.mkdir()
    (older / "brief.md").write_text("# older\n", encoding="utf-8")
    (older / "meta.yaml").write_text("iso_week: 2026-W23\nthrough_date: 2026-06-05\n", encoding="utf-8")
    failures = check(briefs, index, readme, briefs / "SKIPS.yaml", today=dt.date(2026, 6, 19))
    assert [(f.kind, f.detail) for f in failures] == [
        ("missing-week", "2026-W24 has no complete issue or explicit skip")
    ]


def test_current_week_due_on_friday_missing_after_slip_week(tmp_path: Path) -> None:
    briefs, _, _ = _scaffold(tmp_path, "2026-W41", "2026-10-09")
    skips = briefs / "SKIPS.yaml"
    thursday = coverage_report(briefs, dt.date(2026, 10, 15), skips)
    assert (thursday["missing_weeks"], thursday["pending_weeks"]) == ([], [])
    friday = coverage_report(briefs, dt.date(2026, 10, 16), skips)
    assert (friday["missing_weeks"], friday["pending_weeks"]) == ([], ["2026-W42"])
    tuesday = coverage_report(briefs, dt.date(2026, 10, 20), skips)
    assert (tuesday["missing_weeks"], tuesday["pending_weeks"]) == (["2026-W42"], [])


@pytest.mark.parametrize("day", [23, 24, 25, 26])
def test_slip_week_passes_friday_through_monday(tmp_path: Path, day: int) -> None:
    """W43 is due Fri 2026-10-23; with W42 through Sun 2026-10-18 the gate stays green to Monday."""
    briefs, index, readme = _scaffold(tmp_path, "2026-W42", "2026-10-18")
    failures = check(briefs, index, readme, briefs / "SKIPS.yaml", today=dt.date(2026, 10, day))
    assert failures == []


def test_friday_through_issue_goes_stale_while_next_week_is_pending(tmp_path: Path) -> None:
    """W41 through Fri 2026-10-09: freshness fails Sunday, coverage still lists W42 as pending."""
    briefs, index, readme = _scaffold(tmp_path, "2026-W41", "2026-10-09")
    skips = briefs / "SKIPS.yaml"
    expected = {16: set(), 17: set(), 18: {"stale"}, 19: {"stale"}, 20: {"missing-week", "stale"}}
    for day, kinds in expected.items():
        today = dt.date(2026, 10, day)
        assert {f.kind for f in check(briefs, index, readme, skips, today=today)} == kinds
        pending = coverage_report(briefs, today, skips)["pending_weeks"]
        assert pending == ([] if day == 20 else ["2026-W42"])


def test_slip_week_fails_on_tuesday(tmp_path: Path) -> None:
    briefs, index, readme = _scaffold(tmp_path, "2026-W42", "2026-10-18")
    failures = check(briefs, index, readme, briefs / "SKIPS.yaml", today=dt.date(2026, 10, 27))
    assert ("missing-week", "2026-W43 has no complete issue or explicit skip") in [
        (f.kind, f.detail) for f in failures
    ]
    assert {f.kind for f in failures} == {"missing-week", "stale"}


def test_newer_issue_does_not_hide_slip_week_gap(tmp_path: Path) -> None:
    """W44 published Mon 2026-10-26 with W43 absent: W43 is missing, not pending."""
    briefs, index, readme = _scaffold(tmp_path, "2026-W42", "2026-10-18")
    newer = briefs / "2026-W44"
    newer.mkdir()
    (newer / "brief.md").write_text("# newer\n", encoding="utf-8")
    (newer / "meta.yaml").write_text("iso_week: 2026-W44\nthrough_date: 2026-10-26\n", encoding="utf-8")
    index.write_text(index.read_text(encoding="utf-8").replace("2026-W42", "2026-W44"), encoding="utf-8")
    readme.write_text(readme.read_text(encoding="utf-8").replace("2026-W42", "2026-W44"), encoding="utf-8")
    failures = check(briefs, index, readme, briefs / "SKIPS.yaml", today=dt.date(2026, 10, 26))
    assert [(f.kind, f.detail) for f in failures] == [
        ("missing-week", "2026-W43 has no complete issue or explicit skip")
    ]


def test_coverage_follows_cadence_window(tmp_path: Path) -> None:
    briefs, index, readme = _scaffold(tmp_path, "2026-W42", "2026-10-18")
    skips = briefs / "SKIPS.yaml"
    assert check(briefs, index, readme, skips, cadence_window_days=10, today=dt.date(2026, 10, 28)) == []
    failures = check(briefs, index, readme, skips, cadence_window_days=10, today=dt.date(2026, 10, 29))
    assert {f.kind for f in failures} == {"missing-week", "stale"}


def test_coverage_crosses_iso_year_boundary(tmp_path: Path) -> None:
    briefs, _, _ = _scaffold(tmp_path, "2026-W53", "2026-12-31")
    report = coverage_report(briefs, dt.date(2027, 1, 12), briefs / "SKIPS.yaml")
    assert report["missing_weeks"] == ["2027-W01"]


def test_empty_folder_is_not_coverage(tmp_path: Path) -> None:
    briefs, _, _ = _scaffold(tmp_path, "2026-W41", "2026-10-09")
    (briefs / "2026-W42").mkdir()
    report = coverage_report(briefs, dt.date(2026, 10, 20), briefs / "SKIPS.yaml")
    assert report["missing_weeks"] == ["2026-W42"]


def test_rerun_and_invalid_week_do_not_count(tmp_path: Path) -> None:
    briefs, _, _ = _scaffold(tmp_path, "2026-W41", "2026-10-09")
    (briefs / "2026-W42-early-cut").mkdir()
    (briefs / "2026-W99").mkdir()
    assert latest_week_folder(briefs) == "2026-W41"
    assert coverage_report(briefs, dt.date(2026, 10, 20), briefs / "SKIPS.yaml")["missing_weeks"] == ["2026-W42"]


def test_future_through_date_fails(tmp_path: Path) -> None:
    briefs, index, readme = _scaffold(tmp_path, "2026-W42", "2026-10-16")
    failures = check(briefs, index, readme, briefs / "SKIPS.yaml", today=dt.date(2026, 10, 15))
    assert any(f.kind == "future-date" for f in failures)


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


def test_future_iso_week_label_fails(tmp_path: Path) -> None:
    briefs, index, readme = _scaffold(tmp_path, "2026-W29", "2026-07-11")
    failures = check(
        briefs_root=briefs,
        index_path=index,
        readme_path=readme,
        skips_path=briefs / "SKIPS.yaml",
        cadence_window_days=8,
        today=dt.date(2026, 7, 11),
    )
    assert parse_brief_iso_week(briefs / "2026-W29") == "2026-W29"
    mismatch = next(f for f in failures if f.kind == "iso-week")
    assert "belongs to 2026-W28" in mismatch.detail


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
