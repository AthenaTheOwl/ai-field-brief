"""Rewrite PENDING sandbox_image_ref placeholders to the actual SHA.

Second pass of the two-pass emit protocol from DEC-PUB-008. The emitter
(``scripts/run_evidence.py``) writes ``repo://ai-field-brief@PENDING/``
into ``sandbox_image_ref`` and every ``inputs[].ref`` and
``outputs[].artifact_id`` URI on the Run record because the actual
sample-containing commit SHA is not known until after the record itself
is committed. This CLI closes the off-by-one in a second commit by
reading the just-landed SHA (``git rev-parse HEAD`` by default, or an
explicit ``--sha`` override) and rewriting every PENDING placeholder
in-place across one Run record or every Run record under
``ops/run-records/``.

Typical invocation (after committing the regenerated Run records)::

    python scripts/finalize_sandbox_ref.py --all
    python scripts/finalize_sandbox_ref.py --run-id run-874c5e341e13

The CLI is idempotent: running it twice on the same record is a no-op
because no PENDING placeholders remain after the first pass. Records
that already carry a real SHA are not touched.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import run_evidence  # noqa: E402


PENDING = run_evidence.SANDBOX_SHA_PENDING


def _rewrite_uri(value: str, sha: str) -> tuple[str, bool]:
    """Rewrite a single URI string, swapping PENDING for the real SHA.

    Returns ``(new_value, changed)`` so the caller can count rewrites
    without re-comparing strings.
    """
    placeholder = f"@{PENDING}/"
    replacement = f"@{sha}/"
    if placeholder in value:
        return value.replace(placeholder, replacement), True
    return value, False


def _walk_and_rewrite(node: Any, sha: str) -> int:
    """Recursively rewrite PENDING URIs anywhere in a JSON tree.

    Returns the number of string replacements made. Strings are
    rewritten in-place via the parent container; dicts and lists are
    walked.
    """
    count = 0
    if isinstance(node, dict):
        for key, value in node.items():
            if isinstance(value, str):
                new_value, changed = _rewrite_uri(value, sha)
                if changed:
                    node[key] = new_value
                    count += 1
            else:
                count += _walk_and_rewrite(value, sha)
    elif isinstance(node, list):
        for idx, value in enumerate(node):
            if isinstance(value, str):
                new_value, changed = _rewrite_uri(value, sha)
                if changed:
                    node[idx] = new_value
                    count += 1
            else:
                count += _walk_and_rewrite(value, sha)
    return count


def rewrite_record(record_path: Path, sha: str) -> int:
    """Rewrite one Run record file; return the count of URIs updated."""
    record = json.loads(record_path.read_text(encoding="utf-8"))
    count = _walk_and_rewrite(record, sha)
    if count == 0:
        return 0
    record_path.write_text(
        json.dumps(record, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="finalize_sandbox_ref",
        description=(
            "rewrite PENDING sandbox_image_ref + URI placeholders in "
            "Run records to the actual sample-containing commit SHA"
        ),
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--run-id", default=None, help="rewrite one record by id")
    group.add_argument(
        "--all",
        action="store_true",
        help="rewrite every record under --run-records-dir",
    )
    parser.add_argument(
        "--sha",
        default=None,
        help=(
            "explicit SHA to write (default: current `git rev-parse HEAD` "
            "for the repo)"
        ),
    )
    parser.add_argument(
        "--run-records-dir",
        type=Path,
        default=run_evidence.RUN_RECORDS_DIR,
        help="override the run-records directory (default: ops/run-records/)",
    )
    args = parser.parse_args(argv)

    sha = args.sha or run_evidence.current_head_sha()
    if not sha or len(sha) != 40 or sha == PENDING:
        print(
            f"finalize_sandbox_ref: refusing to write a non-SHA value "
            f"({sha!r}); pass --sha or run inside a git working tree.",
            file=sys.stderr,
        )
        return 1

    records_dir: Path = args.run_records_dir
    if not records_dir.is_dir():
        print(
            f"finalize_sandbox_ref: records directory not found: {records_dir}",
            file=sys.stderr,
        )
        return 1

    if args.run_id:
        targets = [records_dir / f"{args.run_id}.json"]
    elif args.all:
        targets = sorted(records_dir.glob("*.json"))
    else:
        targets = sorted(records_dir.glob("*.json"))

    total = 0
    touched = 0
    for path in targets:
        if not path.is_file():
            print(
                f"finalize_sandbox_ref: skipping missing record {path}",
                file=sys.stderr,
            )
            continue
        count = rewrite_record(path, sha)
        if count:
            try:
                rel = path.relative_to(run_evidence.ROOT).as_posix()
            except ValueError:
                rel = path.as_posix()
            print(f"finalize_sandbox_ref: rewrote {count} URI(s) in {rel}")
            total += count
            touched += 1
    print(
        f"finalize_sandbox_ref OK: sha={sha} records_touched={touched} "
        f"uri_rewrites={total}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
