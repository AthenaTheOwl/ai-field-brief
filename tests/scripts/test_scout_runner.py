"""Unit tests for scripts/scout_runner.py.

Covers the deterministic, offline surface only: argparse wiring, the
SHA-256 hash helper, source-ids parsing, registry filtering, and a
mocked-fetch end-to-end that produces a valid sandbox manifest +
checkpoint without touching the network.
"""

from __future__ import annotations

import json
import pathlib
import sys
from typing import Any

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import scout_runner  # type: ignore[import-not-found]  # noqa: E402


def test_parse_source_ids_splits_and_deduplicates() -> None:
    """parse_source_ids handles whitespace, dedup, and empty tokens."""
    assert scout_runner.parse_source_ids(None) == []
    assert scout_runner.parse_source_ids("") == []
    assert scout_runner.parse_source_ids("e2b,pydantic-ai") == ["e2b", "pydantic-ai"]
    assert scout_runner.parse_source_ids(
        " e2b , e2b , mastra "
    ) == ["e2b", "mastra"]


def test_build_arg_parser_accepts_source_ids_and_lane() -> None:
    """argparse parses --source-ids and --lane independently."""
    parser = scout_runner.build_arg_parser()
    ns = parser.parse_args(["--source-ids", "e2b-github,mastra-github"])
    assert ns.source_ids == "e2b-github,mastra-github"
    assert ns.lane is None

    ns2 = parser.parse_args(["--lane", "frontier-scout"])
    assert ns2.lane == "frontier-scout"
    assert ns2.source_ids is None


def test_build_arg_parser_rejects_both_flags() -> None:
    """--source-ids and --lane are mutually exclusive."""
    parser = scout_runner.build_arg_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(
            ["--lane", "frontier-scout", "--source-ids", "e2b-github"]
        )


def test_sha256_bytes_is_deterministic() -> None:
    """Same bytes -> same digest; different bytes -> different digest."""
    payload = b"frontier-scout-snapshot-bytes"
    a = scout_runner.sha256_bytes(payload)
    b = scout_runner.sha256_bytes(payload)
    assert a == b
    assert len(a) == 64
    assert all(ch in "0123456789abcdef" for ch in a)

    other = scout_runner.sha256_bytes(payload + b" ")
    assert other != a


def test_select_sources_filters_by_lane_then_by_ids() -> None:
    """select_sources prefers explicit source_ids over lane filter."""
    registry: dict[str, Any] = {
        "sources": [
            {"id": "a", "lane": "frontier-scout", "url": "https://a"},
            {"id": "b", "lane": "primary-source", "url": "https://b"},
            {"id": "c", "lane": "frontier-scout", "url": "https://c"},
        ]
    }
    by_lane = scout_runner.select_sources(
        registry, lane="frontier-scout", source_ids=[]
    )
    assert [s["id"] for s in by_lane] == ["a", "c"]

    by_ids = scout_runner.select_sources(
        registry, lane=None, source_ids=["b", "c"]
    )
    assert sorted(s["id"] for s in by_ids) == ["b", "c"]


def test_snapshot_source_writes_file_and_records_hash(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """snapshot_source mocked: writes bytes + hash without network IO."""
    body = b"<html>frontier scout fixture</html>"

    def fake_fetch(url: str, *, timeout: int = 0) -> tuple[bytes, int | None, str | None]:
        assert url == "https://example.test/scout"
        return body, 200, None

    monkeypatch.setattr(scout_runner, "fetch_source", fake_fetch)

    snapshot_dir = tmp_path / "snap"
    rec = scout_runner.snapshot_source(
        {"id": "fixture", "url": "https://example.test/scout"},
        snapshot_dir=snapshot_dir,
    )
    assert rec["source_id"] == "fixture"
    assert rec["sha256"] == scout_runner.sha256_bytes(body)
    assert rec["bytes"] == len(body)
    snapshot_path = pathlib.Path(rec["snapshot_path"])
    assert snapshot_path.is_file()
    assert snapshot_path.read_bytes() == body


def test_snapshot_source_records_failure_without_writing(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A 404 returns an error record and writes no file."""

    def fake_fetch(url: str, *, timeout: int = 0) -> tuple[bytes, int | None, str | None]:
        return b"", 404, "HTTPError 404: Not Found"

    monkeypatch.setattr(scout_runner, "fetch_source", fake_fetch)

    snapshot_dir = tmp_path / "snap-missing"
    rec = scout_runner.snapshot_source(
        {"id": "broken", "url": "https://example.test/missing"},
        snapshot_dir=snapshot_dir,
    )
    assert "sha256" not in rec
    assert rec["error"].startswith("HTTPError 404")
    assert rec["http_status"] == 404
    assert not (snapshot_dir / "broken.html").exists()


def test_build_sandbox_manifest_shape() -> None:
    """Manifest carries the required keys + scout runtime provider."""
    manifest = scout_runner.build_sandbox_manifest(
        run_id="run-scout-deadbeef0123",
        snapshot_dir=pathlib.Path("/tmp/snap"),
        source_ids=["e2b-github"],
    )
    assert manifest["manifest_version"] == scout_runner.MANIFEST_VERSION
    assert manifest["runtime_provider"] == scout_runner.RUNTIME_PROVIDER
    assert manifest["model"] is None
    assert manifest["env_refs"] == []
    assert manifest["tool_surface"] == [{"tool_name": "webfetch"}]
    assert manifest["mounts"][0]["kind"] == "snapshot-dir"
    # Round-trips through JSON without losing shape.
    assert json.loads(json.dumps(manifest))["source_ids"] == ["e2b-github"]


def test_build_checkpoint_marks_awaiting_lens_application() -> None:
    """Checkpoint status is the agreed handoff token to the lens step."""
    ck = scout_runner.build_checkpoint(
        run_id="run-scout-deadbeef0123",
        fetched_sources=["e2b-github", "mastra-github"],
        lens_ids=["source_arbitrage", "repo_project_scan"],
        failed_sources=["humanlayer-github"],
    )
    assert ck["status"] == "awaiting_lens_application"
    assert ck["fetched_sources"] == ["e2b-github", "mastra-github"]
    assert ck["failed_sources"] == ["humanlayer-github"]
    assert ck["lens_ids"] == ["source_arbitrage", "repo_project_scan"]
