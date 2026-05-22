"""Validate JSON Schema files committed to ai-field-brief.

Phase 0 scope:
  1. Every `*.schema.json` under packages/, apps/, inngest/, or schemas/
     must parse as JSON.
  2. Each schema must declare a top-level `$schema` and a `title`.
  3. The `$schema` value must be one of the recognized JSON Schema dialect
     URIs (draft-07 or 2020-12). This keeps the planning surface from
     drifting between dialects before code lands.
  4. If a sibling `*.fixtures.json` exists next to a schema, every fixture
     in the array must validate against the schema (skipped if the
     `jsonschema` package is not installed — printed as a soft warning,
     not a failure, so Phase 0 can pass with zero Python deps).

Exit codes: 0 OK, 1 violations found.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

ALLOWED_DIALECTS = {
    "http://json-schema.org/draft-07/schema#",
    "https://json-schema.org/draft/2019-09/schema",
    "https://json-schema.org/draft/2020-12/schema",
}

SEARCH_GLOBS = (
    "packages/**/*.schema.json",
    "apps/**/*.schema.json",
    "inngest/**/*.schema.json",
    "schemas/**/*.schema.json",
)

SKIP_PARTS = {"node_modules", "dist", "build", ".turbo", ".next", "__pycache__"}


def discover_schemas() -> list[Path]:
    files: set[Path] = set()
    for pattern in SEARCH_GLOBS:
        for path in ROOT.glob(pattern):
            if any(part in SKIP_PARTS for part in path.parts):
                continue
            if path.is_file():
                files.add(path)
    return sorted(files)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_schema(path: Path, violations: list[str]) -> dict[str, Any] | None:
    rel = path.relative_to(ROOT).as_posix()
    try:
        doc = load_json(path)
    except json.JSONDecodeError as exc:
        violations.append(f"{rel}: invalid JSON ({exc.msg} at line {exc.lineno})")
        return None
    if not isinstance(doc, dict):
        violations.append(f"{rel}: top-level must be an object")
        return None

    dialect = doc.get("$schema")
    if not isinstance(dialect, str):
        violations.append(f"{rel}: missing top-level `$schema` string")
    elif dialect not in ALLOWED_DIALECTS:
        violations.append(
            f"{rel}: unsupported `$schema` value `{dialect}`. "
            f"Allowed: {', '.join(sorted(ALLOWED_DIALECTS))}."
        )

    if not isinstance(doc.get("title"), str):
        violations.append(f"{rel}: missing top-level `title` string")

    return doc


def validate_fixtures(
    schema_path: Path, schema_doc: dict[str, Any], violations: list[str]
) -> None:
    fixture_path = schema_path.with_name(schema_path.name.replace(".schema.json", ".fixtures.json"))
    if not fixture_path.is_file():
        return

    rel = fixture_path.relative_to(ROOT).as_posix()
    try:
        fixtures = load_json(fixture_path)
    except json.JSONDecodeError as exc:
        violations.append(f"{rel}: invalid JSON ({exc.msg} at line {exc.lineno})")
        return

    if not isinstance(fixtures, list):
        violations.append(f"{rel}: top-level must be a JSON array of fixture objects")
        return

    try:
        import jsonschema  # type: ignore[import-not-found]
    except ImportError:
        print(
            f"validate_schemas: jsonschema not installed; skipping fixture validation "
            f"for {rel}",
            file=sys.stderr,
        )
        return

    validator_cls = jsonschema.validators.validator_for(schema_doc)
    validator_cls.check_schema(schema_doc)
    validator = validator_cls(schema_doc)
    for index, fixture in enumerate(fixtures):
        errors = list(validator.iter_errors(fixture))
        for err in errors:
            location = "/".join(str(part) for part in err.absolute_path) or "<root>"
            violations.append(f"{rel}[{index}].{location}: {err.message}")


def main() -> int:
    violations: list[str] = []
    schemas = discover_schemas()

    if not schemas:
        print("validate_schemas OK (0 schemas — Phase 0)")
        return 0

    for schema_path in schemas:
        doc = validate_schema(schema_path, violations)
        if doc is not None:
            validate_fixtures(schema_path, doc, violations)

    if violations:
        print("validate_schemas: violations found", file=sys.stderr)
        for v in violations:
            print(f"  - {v}", file=sys.stderr)
        return 1

    print(f"validate_schemas OK ({len(schemas)} schema(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
