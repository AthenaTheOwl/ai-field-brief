"""Validate the source registry for ai-field-brief.

Looked-up locations (first one found wins):
  - sources/registry.yaml
  - packages/sources/registry.yaml

Phase 0 rules — when a registry file exists it must:
  1. Parse as a top-level mapping.
  2. Carry `version` (int) and `sources` (list).
  3. Have unique source `id` values, each kebab-case.
  4. Each source carries the required keys: id, name, type, lane, url,
     intake, status. Quality is optional now but must be a mapping if
     present.
  5. Use a `lane` value from a fixed enum (or, if `lanes` is declared at
     the file top level, from that declared list).
  6. Use an `intake` value from {full, show-notes-only, human-notes,
     webhook-push}.
  7. Use a `status` value from {active, paused, retired}.
  8. URLs must start with `http://` or `https://`.

When no registry exists (Phase 0 default), exit 0 with an explanatory note.

If `pyyaml` is not installed, fall back to a tiny built-in line parser that
covers the subset the registry file uses (top-level keys, indented list
entries with simple `key: value` pairs). This keeps the gate runnable on a
bare Python install.

Exit codes: 0 OK, 1 violations found.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

CANDIDATE_PATHS = (
    ROOT / "sources" / "registry.yaml",
    ROOT / "packages" / "sources" / "registry.yaml",
)

DEFAULT_LANES = {"fast-signal", "builder-practice", "strategy", "primary-source"}
ALLOWED_INTAKE = {"full", "show-notes-only", "human-notes", "webhook-push"}
ALLOWED_STATUS = {"active", "paused", "retired"}

REQUIRED_KEYS = ("id", "name", "type", "lane", "url", "intake", "status")
KEBAB_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
URL_RE = re.compile(r"^https?://", re.IGNORECASE)


def load_yaml(text: str) -> Any:
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError:
        return _fallback_yaml(text)
    return yaml.safe_load(text)


def _fallback_yaml(text: str) -> dict[str, Any]:
    """Minimal YAML reader for the registry shape only.

    Supports:
      key: scalar
      sources:
        - key: value
          key: value
      lanes:
        - key: value
    Lists nested under a top-level key. Anything else returns an error and
    asks the user to install pyyaml.
    """

    root: dict[str, Any] = {}
    current_key: str | None = None
    current_list: list[dict[str, Any]] | None = None
    current_item: dict[str, Any] | None = None

    for raw_line_no, raw in enumerate(text.splitlines(), start=1):
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        if indent == 0:
            if ":" not in stripped:
                raise ValueError(f"line {raw_line_no}: unsupported YAML shape (need pyyaml)")
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip()
            if value == "":
                root[key] = []
                current_key = key
                current_list = root[key]
                current_item = None
            else:
                root[key] = _coerce(value)
                current_key = None
                current_list = None
                current_item = None
            continue

        if stripped.startswith("- "):
            if current_list is None:
                raise ValueError(f"line {raw_line_no}: list item outside list (need pyyaml)")
            current_item = {}
            current_list.append(current_item)
            rest = stripped[2:]
            if rest and ":" in rest:
                key, _, value = rest.partition(":")
                current_item[key.strip()] = _coerce(value.strip())
            continue

        if current_item is None:
            raise ValueError(f"line {raw_line_no}: unsupported nesting (need pyyaml)")
        if ":" not in stripped:
            raise ValueError(f"line {raw_line_no}: unsupported YAML shape (need pyyaml)")
        key, _, value = stripped.partition(":")
        key = key.strip()
        value = value.strip()
        if value == "" or value == "{}":
            current_item[key] = {}
        else:
            current_item[key] = _coerce(value)

    return root


def _coerce(value: str) -> Any:
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.lstrip("-").isdigit():
        return int(value)
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    return value


def find_registry() -> Path | None:
    for path in CANDIDATE_PATHS:
        if path.is_file():
            return path
    return None


def validate(registry: dict[str, Any], rel: str, violations: list[str]) -> None:
    if not isinstance(registry, dict):
        violations.append(f"{rel}: top-level must be a mapping")
        return

    if not isinstance(registry.get("version"), int):
        violations.append(f"{rel}: `version` must be an integer")

    sources = registry.get("sources")
    if not isinstance(sources, list):
        violations.append(f"{rel}: `sources` must be a list")
        return

    allowed_lanes = set(DEFAULT_LANES)
    declared_lanes = registry.get("lanes")
    if isinstance(declared_lanes, list):
        ids = {
            entry.get("id")
            for entry in declared_lanes
            if isinstance(entry, dict) and isinstance(entry.get("id"), str)
        }
        if ids:
            allowed_lanes = ids

    seen_ids: set[str] = set()
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            violations.append(f"{rel}/sources[{index}]: must be a mapping")
            continue

        sid = source.get("id")
        if not isinstance(sid, str) or not KEBAB_RE.match(sid):
            violations.append(
                f"{rel}/sources[{index}]: `id` must be a kebab-case string "
                f"(got {sid!r})"
            )
        else:
            if sid in seen_ids:
                violations.append(f"{rel}/sources[{index}]: duplicate id `{sid}`")
            seen_ids.add(sid)

        for key in REQUIRED_KEYS:
            if key not in source:
                violations.append(
                    f"{rel}/sources[{index}] ({sid!r}): missing required key `{key}`"
                )

        lane = source.get("lane")
        if isinstance(lane, str) and lane not in allowed_lanes:
            violations.append(
                f"{rel}/sources[{index}] ({sid!r}): lane `{lane}` not in "
                f"{sorted(allowed_lanes)}"
            )

        intake = source.get("intake")
        if isinstance(intake, str) and intake not in ALLOWED_INTAKE:
            violations.append(
                f"{rel}/sources[{index}] ({sid!r}): intake `{intake}` not in "
                f"{sorted(ALLOWED_INTAKE)}"
            )

        status = source.get("status")
        if isinstance(status, str) and status not in ALLOWED_STATUS:
            violations.append(
                f"{rel}/sources[{index}] ({sid!r}): status `{status}` not in "
                f"{sorted(ALLOWED_STATUS)}"
            )

        url = source.get("url")
        if isinstance(url, str) and not URL_RE.match(url):
            violations.append(
                f"{rel}/sources[{index}] ({sid!r}): url must start with http(s)://"
            )

        quality = source.get("quality")
        if quality is not None and not isinstance(quality, dict):
            violations.append(
                f"{rel}/sources[{index}] ({sid!r}): `quality` must be a mapping"
            )


def main() -> int:
    path = find_registry()
    if path is None:
        print(
            "validate_registry OK (no registry yet — Phase 0; will activate when "
            f"{' or '.join(p.relative_to(ROOT).as_posix() for p in CANDIDATE_PATHS)} lands)"
        )
        return 0

    rel = path.relative_to(ROOT).as_posix()
    try:
        registry = load_yaml(path.read_text(encoding="utf-8"))
    except ValueError as exc:
        print(f"validate_registry: {rel}: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # pragma: no cover - defensive
        print(f"validate_registry: {rel}: failed to parse ({exc})", file=sys.stderr)
        return 1

    violations: list[str] = []
    validate(registry, rel, violations)

    if violations:
        print("validate_registry: violations found", file=sys.stderr)
        for v in violations:
            print(f"  - {v}", file=sys.stderr)
        return 1

    sources = registry.get("sources") if isinstance(registry, dict) else None
    count = len(sources) if isinstance(sources, list) else 0
    print(f"validate_registry OK ({count} source(s) in {rel})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
