"""Validate the tool registry (.agents/tools.yaml) in ai-field-brief.

Reads `.agents/tools.yaml` as a top-level list of tool entries, then
validates each entry against the cross-repo `tool.schema.json` sourced
from athena-site. The schema is fetched at run time from
`https://raw.githubusercontent.com/AthenaTheOwl/athena-site/main/ops/schemas/tool.schema.json`,
with a local cache fallback at `ops/schemas-cache/tool.schema.json`.

Exit codes: 0 OK, 1 violations found.
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TOOLS_PATH = ROOT / ".agents" / "tools.yaml"
CACHE_PATH = ROOT / "ops" / "schemas-cache" / "tool.schema.json"
REMOTE_URL = (
    "https://raw.githubusercontent.com/AthenaTheOwl/athena-site/main/"
    "ops/schemas/tool.schema.json"
)
FETCH_TIMEOUT_SECONDS = 5


def load_remote_schema() -> dict[str, Any] | None:
    try:
        req = urllib.request.Request(
            REMOTE_URL, headers={"User-Agent": "ai-field-brief/validate_tools"}
        )
        with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT_SECONDS) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
        print(
            f"validate_tools: remote schema fetch failed ({exc.__class__.__name__}); "
            f"falling back to cache at {CACHE_PATH.relative_to(ROOT).as_posix()}",
            file=sys.stderr,
        )
        return None


def load_cached_schema() -> dict[str, Any]:
    if not CACHE_PATH.is_file():
        raise SystemExit(
            f"validate_tools: cached schema missing at "
            f"{CACHE_PATH.relative_to(ROOT).as_posix()}. Re-cache from "
            f"{REMOTE_URL} or restore the file."
        )
    return json.loads(CACHE_PATH.read_text(encoding="utf-8"))


def load_schema() -> dict[str, Any]:
    remote = load_remote_schema()
    if remote is not None:
        return remote
    return load_cached_schema()


def main() -> int:
    if not TOOLS_PATH.is_file():
        print("validate_tools OK (no .agents/tools.yaml — registry not installed)")
        return 0

    try:
        import jsonschema  # type: ignore[import-not-found]
    except ImportError as exc:
        raise SystemExit(
            "validate_tools: jsonschema is required. "
            "Install with `pip install jsonschema>=4.21`."
        ) from exc

    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError as exc:
        raise SystemExit(
            "validate_tools: PyYAML is required. "
            "Install with `pip install pyyaml`."
        ) from exc

    schema = load_schema()
    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema)

    rel = TOOLS_PATH.relative_to(ROOT).as_posix()
    try:
        data = yaml.safe_load(TOOLS_PATH.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        print(f"validate_tools: {rel}: YAML parse error: {exc}", file=sys.stderr)
        return 1

    if not isinstance(data, list):
        print(
            f"validate_tools: {rel}: top-level must be a YAML list of tool entries",
            file=sys.stderr,
        )
        return 1

    violations: list[str] = []
    seen_ids: set[str] = set()

    for index, entry in enumerate(data):
        if not isinstance(entry, dict):
            violations.append(f"{rel}[{index}]: must be a mapping")
            continue
        errors = list(validator.iter_errors(entry))
        for err in errors:
            location = "/".join(str(part) for part in err.absolute_path) or "<root>"
            violations.append(f"{rel}[{index}].{location}: {err.message}")
        tid = entry.get("id")
        if isinstance(tid, str):
            if tid in seen_ids:
                violations.append(f"{rel}[{index}]: duplicate tool id `{tid}`")
            seen_ids.add(tid)

    if violations:
        print("validate_tools: violations found", file=sys.stderr)
        for v in violations:
            print(f"  - {v}", file=sys.stderr)
        return 1

    print(f"validate_tools OK ({len(data)} tool(s) in {rel})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
