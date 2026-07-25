"""Regression coverage for weekly brief cache invalidation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_weekly_briefs_are_part_of_the_turbo_global_hash() -> None:
    """A new ISO-week directory must invalidate cached web builds and tests."""
    config = json.loads((ROOT / "turbo.json").read_text(encoding="utf-8"))

    global_dependencies = config.get("globalDependencies", [])

    assert "briefs/**" in global_dependencies
