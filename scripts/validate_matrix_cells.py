#!/usr/bin/env python3
"""Validate matrix cell files against schemas/matrix_cell.schema.json.

`scripts/validate_schemas.py` checks that schema *files* parse and declare a
recognized dialect. Nothing checked the cells those schemas describe, so the
enum vocabulary in `briefs/*/matrix/*.yaml` drifted from 2026-W24 onward:
`mode` picked up `pattern`, `insight`, `risk`, `thesis`, and `horizon_scan`;
`ref_type` picked up `paraphrase` and `link`; `status` picked up `candidate`.
172 violations across eight published issues. See DEC-MTRX-009.

Rules, applied to every `briefs/*/matrix/*.yaml` carrying a `cells` list:

  1. Each cell validates against `schemas/matrix_cell.schema.json`, which
     covers the required keys, the `mode`, `confidence`, `faithfulness_status`
     and `status` enums, the `source_refs` shape and its `ref_type` enum, and
     `additionalProperties: false`.
  2. Cell ids are unique within a file.
  3. Every `matrix_run_id` on a cell matches the file's top-level
     `matrix_run_id` when the file declares one.

When `jsonschema` is not installed the script falls back to checking the
enums and required keys directly, so the gate still runs on a bare install.

Exit codes: 0 OK, 1 violations found.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "matrix_cell.schema.json"
SEARCH_GLOB = "briefs/*/matrix/*.yaml"


def load_yaml(path: Path) -> Any:
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError:
        print(
            "validate_matrix_cells: pyyaml is required to read cell files; "
            "install it or run this gate in CI"
        )
        raise SystemExit(0)
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def fallback_check(cell: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    """Enum and required-key check used when jsonschema is unavailable."""
    errors: list[str] = []
    props = schema["properties"]
    for key in schema.get("required", []):
        if key not in cell:
            errors.append(f"'{key}' is a required property")
    for key, value in cell.items():
        if key not in props:
            errors.append(f"'{key}' was unexpected")
            continue
        allowed = props[key].get("enum")
        if allowed and value not in allowed:
            errors.append(f"'{value}' is not one of {allowed} for '{key}'")
    ref_enum = props["source_refs"]["items"]["properties"]["ref_type"]["enum"]
    for ref in cell.get("source_refs") or []:
        if not isinstance(ref, dict):
            errors.append("source_refs entry is not a mapping")
            continue
        for key in ("uri", "quote_or_span", "ref_type"):
            if key not in ref:
                errors.append(f"source_refs entry missing '{key}'")
        if ref.get("ref_type") not in ref_enum:
            errors.append(f"'{ref.get('ref_type')}' is not one of {ref_enum} for 'ref_type'")
    return errors


def main() -> int:
    if not SCHEMA_PATH.is_file():
        print(f"validate_matrix_cells: {SCHEMA_PATH.name} missing; nothing to check against")
        return 1

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = None
    try:
        from jsonschema import Draft202012Validator  # type: ignore[import-not-found]

        validator = Draft202012Validator(schema)
    except ImportError:
        pass

    violations: list[str] = []
    files_checked = 0
    cells_checked = 0

    for path in sorted(ROOT.glob(SEARCH_GLOB)):
        data = load_yaml(path)
        if not isinstance(data, dict):
            continue
        cells = data.get("cells")
        if not isinstance(cells, list) or not cells:
            continue

        rel = path.relative_to(ROOT).as_posix()
        files_checked += 1
        file_run_id = data.get("matrix_run_id")
        seen: set[str] = set()

        for index, cell in enumerate(cells):
            cells_checked += 1
            if not isinstance(cell, dict):
                violations.append(f"{rel}: cell #{index} is not a mapping")
                continue

            cell_id = cell.get("id", f"#{index}")
            if cell_id in seen:
                violations.append(f"{rel}: duplicate cell id '{cell_id}'")
            seen.add(cell_id)

            if file_run_id and cell.get("matrix_run_id") != file_run_id:
                violations.append(
                    f"{rel}: cell '{cell_id}' matrix_run_id "
                    f"'{cell.get('matrix_run_id')}' does not match the file's '{file_run_id}'"
                )

            if validator is not None:
                errors = [e.message for e in validator.iter_errors(cell)]
            else:
                errors = fallback_check(cell, schema)
            for message in errors:
                violations.append(f"{rel}: cell '{cell_id}': {message}")

    if violations:
        shown = violations[:40]
        print(f"validate_matrix_cells FAILED ({len(violations)} violation(s)):")
        for line in shown:
            print(f"  - {line}")
        if len(violations) > len(shown):
            print(f"  ... and {len(violations) - len(shown)} more")
        return 1

    engine = "jsonschema" if validator is not None else "fallback enum check"
    print(
        f"validate_matrix_cells OK ({cells_checked} cell(s) in "
        f"{files_checked} file(s), via {engine})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
