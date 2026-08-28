import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from source_audit import collect_items, compute_stats, tier_for  # noqa: E402


def test_current_metadata_tracks_reviews_inclusions_and_url_prefixes(tmp_path: Path) -> None:
    briefs = tmp_path / "briefs"
    week = briefs / "2026-W34"
    (week / "items").mkdir(parents=True)
    (week / "meta.yaml").write_text(
        """\
sources_reviewed:
  - label: Stateful workflow paper
    url: https://arxiv.org/abs/2608.19741
    disposition: top_signal
  - label: Dogwood announcement
    url: https://aws.amazon.com/blogs/opensource/introducing-dogwood-runtime-verification-for-ai-agents/
    disposition: scout
  - label: Useful project, no pick this week
    url: https://example.test/project/release/1
    disposition: reviewed_no_pick
  - label: Private synthesis input
    url: google-drive://Daily Systems Brief
    disposition: synthesis_input
""",
        encoding="utf-8",
    )
    (week / "items" / "legacy.md").write_text(
        "**Source:** Thinkingbox and WorkflowArena\n**Cells:** old-cell\n",
        encoding="utf-8",
    )
    registry = [
        {
            "id": "thinkingbox",
            "name": "Thinkingbox and WorkflowArena",
            "url": "https://arxiv.org/abs/2608.19741",
            "status": "active",
        },
        {
            "id": "aws-blog",
            "name": "AWS Open Source Blog",
            "url": "https://aws.amazon.com/blogs/opensource/",
            "status": "active",
        },
        {
            "id": "project",
            "name": "Useful project",
            "url": "https://example.test/project",
            "status": "active",
        },
        {
            "id": "never-reviewed",
            "name": "Never reviewed",
            "url": "https://never.example.test",
            "status": "active",
        },
    ]

    appearances = collect_items(briefs)
    stats, unmatched = compute_stats(registry, appearances)

    assert len(appearances) == 3
    assert unmatched == []
    assert stats["thinkingbox"].reviews == 1
    assert stats["thinkingbox"].appearances == 1
    assert stats["thinkingbox"].cell_promoted == 1
    assert stats["aws-blog"].appearances == 1
    assert stats["project"].reviews == 1
    assert stats["project"].appearances == 0
    assert tier_for(stats["project"], 1) == "retire-review"
    assert tier_for(stats["never-reviewed"], 1) == "unreviewed"


def test_legacy_items_are_used_when_metadata_is_absent(tmp_path: Path) -> None:
    briefs = tmp_path / "briefs"
    items = briefs / "2026-W20" / "items"
    items.mkdir(parents=True)
    (items / "signal.md").write_text(
        "**Source:** Legacy source\n**Cells:** MTRX-1, MTRX-2\n",
        encoding="utf-8",
    )
    registry = [
        {
            "id": "legacy",
            "name": "Legacy source",
            "url": "https://legacy.example.test",
            "status": "active",
        }
    ]

    stats, unmatched = compute_stats(registry, collect_items(briefs))

    assert unmatched == []
    assert stats["legacy"].reviews == 1
    assert stats["legacy"].appearances == 1
    assert stats["legacy"].cell_promoted == 1
