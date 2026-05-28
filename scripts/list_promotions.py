"""Report promotion candidates filed under `promotions/<week>/`.

Walks every `promotions/<YYYY-WNN>/PROM-*.md`, parses the YAML
front-matter, and prints a table grouped by status (proposed, accepted,
landed, rejected, archived). Counts per `target_repo` and
`target_artifact_type` follow.

The script does not enforce shape — it reports. The promotions surface
is intentionally lightweight while the rollout settles. Exit code is
always 0 unless a YAML file fails to parse.
"""

from __future__ import annotations

import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROMOTIONS_DIR = ROOT / "promotions"

WEEK_DIR_PATTERN = re.compile(r"^[0-9]{4}-W[0-9]{2}$")

# Statuses in display order. Anything outside the set still shows, but
# at the bottom under "other".
KNOWN_STATUSES = ("proposed", "accepted", "landed", "rejected", "archived")

for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    except (AttributeError, ValueError):
        pass


def parse_front_matter(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        return None, "missing opening `---` front-matter delimiter on line 1"

    lines = text.splitlines()
    end_index = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_index = i
            break

    if end_index is None:
        return None, "missing closing `---` front-matter delimiter"

    front_matter_text = "\n".join(lines[1:end_index])

    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError as exc:
        raise SystemExit(
            "list_promotions: PyYAML is required. "
            "Install with `pip install pyyaml`."
        ) from exc

    try:
        data = yaml.safe_load(front_matter_text)
    except yaml.YAMLError as exc:
        return None, f"YAML parse error in front-matter: {exc}"

    if not isinstance(data, dict):
        return None, "front-matter must parse to a mapping"

    return data, None


def discover_promotions() -> list[Path]:
    if not PROMOTIONS_DIR.is_dir():
        return []
    candidates: list[Path] = []
    for week_dir in sorted(PROMOTIONS_DIR.iterdir()):
        if not week_dir.is_dir() or not WEEK_DIR_PATTERN.match(week_dir.name):
            continue
        candidates.extend(
            sorted(p for p in week_dir.glob("PROM-*.md") if p.is_file())
        )
    return candidates


def status_label(value: Any) -> str:
    if isinstance(value, str) and value in KNOWN_STATUSES:
        return value
    if isinstance(value, str):
        return f"other:{value}"
    return "other:unknown"


def main() -> int:
    promotions = discover_promotions()
    if not promotions:
        print("list_promotions: 0 candidates found (promotions/ is empty)")
        return 0

    by_status: Counter[str] = Counter()
    by_repo: Counter[str] = Counter()
    by_artifact: Counter[str] = Counter()
    by_week: defaultdict[str, list[str]] = defaultdict(list)
    parse_errors: list[str] = []

    for path in promotions:
        rel = path.relative_to(ROOT).as_posix()
        data, err = parse_front_matter(path)
        if err is not None:
            parse_errors.append(f"{rel}: {err}")
            continue
        assert data is not None

        status = status_label(data.get("status"))
        by_status[status] += 1

        repo = data.get("target_repo")
        if isinstance(repo, str) and repo:
            by_repo[repo] += 1

        artifact = data.get("target_artifact_type")
        if isinstance(artifact, str) and artifact:
            by_artifact[artifact] += 1

        week = data.get("brief")
        if isinstance(week, str) and week:
            by_week[week].append(data.get("id", path.stem))

    total = sum(by_status.values())
    week_count = len(by_week)
    print(
        f"promotions: {total} candidates across {week_count} brief(s)"
    )

    status_line_parts: list[str] = []
    for s in KNOWN_STATUSES:
        status_line_parts.append(f"{s}: {by_status.get(s, 0)}")
    other_keys = sorted(k for k in by_status if k not in KNOWN_STATUSES)
    for k in other_keys:
        status_line_parts.append(f"{k}: {by_status[k]}")
    print("  " + "   ".join(status_line_parts))
    print()

    if by_repo:
        print("by target_repo:")
        width = max(len(k) for k in by_repo) + 2
        for repo, count in by_repo.most_common():
            print(f"  {repo:<{width}}{count}")
        print()

    if by_artifact:
        print("by target_artifact_type:")
        width = max(len(k) for k in by_artifact) + 2
        for artifact, count in by_artifact.most_common():
            print(f"  {artifact:<{width}}{count}")
        print()

    if parse_errors:
        print("list_promotions: parse errors", file=sys.stderr)
        for v in parse_errors:
            print(f"  - {v}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
