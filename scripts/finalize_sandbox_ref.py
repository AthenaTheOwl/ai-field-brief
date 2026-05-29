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

The CLI is idempotent in default mode: running it twice on the same
record is a no-op because no PENDING placeholders remain after the
first pass. Records that already carry a real SHA are not touched.

A ``--force`` flag re-anchors every ``repo://<repo>@<sha>/`` URI to
the new SHA (not just PENDING). Use ``--force`` to close the
recursive tail: when committing the rewritten records bumps HEAD by
one more SHA, the next pass with ``--force`` re-anchors records to
the previous commit, which is now the sample-containing commit at
that moment.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import run_evidence  # noqa: E402


PENDING = run_evidence.SANDBOX_SHA_PENDING


# URI shape we rewrite. Matches the portable form from DEC-CDCP-014
# with either PENDING or a 40-char hex SHA in the @<sha>/ position.
_REWRITE_URI_RE = re.compile(
    r"repo://(?P<repo>[a-z][a-z0-9-]*)@(?P<sha>[a-f0-9]{40}|PENDING)/"
)


def _rewrite_uri(value: str, sha: str, *, force: bool) -> tuple[str, bool]:
    """Rewrite a single URI string, swapping the SHA segment.

    By default only ``@PENDING/`` segments are rewritten (the
    second-pass closure of the two-pass protocol). When ``force`` is
    True every ``repo://<repo>@<any-sha>/`` segment is re-anchored to
    the new SHA; this is the recursive-tail closure (commit N+1
    rewrites records to the SHA of commit N, which is the
    sample-containing commit at the moment the rewriter runs).

    Returns ``(new_value, changed)`` so the caller can count rewrites
    without re-comparing strings.
    """
    if force:
        def _swap(match: re.Match[str]) -> str:
            return f"repo://{match.group('repo')}@{sha}/"

        new_value, n = _REWRITE_URI_RE.subn(_swap, value)
        return new_value, n > 0 and new_value != value
    placeholder = f"@{PENDING}/"
    replacement = f"@{sha}/"
    if placeholder in value:
        return value.replace(placeholder, replacement), True
    return value, False


def _walk_and_rewrite(node: Any, sha: str, *, force: bool) -> int:
    """Recursively rewrite URIs anywhere in a JSON tree.

    Returns the number of string replacements made. Strings are
    rewritten in-place via the parent container; dicts and lists are
    walked.
    """
    count = 0
    if isinstance(node, dict):
        for key, value in node.items():
            if isinstance(value, str):
                new_value, changed = _rewrite_uri(value, sha, force=force)
                if changed:
                    node[key] = new_value
                    count += 1
            else:
                count += _walk_and_rewrite(value, sha, force=force)
    elif isinstance(node, list):
        for idx, value in enumerate(node):
            if isinstance(value, str):
                new_value, changed = _rewrite_uri(value, sha, force=force)
                if changed:
                    node[idx] = new_value
                    count += 1
            else:
                count += _walk_and_rewrite(value, sha, force=force)
    return count


def rewrite_record(record_path: Path, sha: str, *, force: bool = False) -> int:
    """Rewrite one Run record file; return the count of URIs updated."""
    record = json.loads(record_path.read_text(encoding="utf-8"))
    count = _walk_and_rewrite(record, sha, force=force)
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
    parser.add_argument(
        "--force",
        action="store_true",
        help=(
            "re-anchor every repo://<repo>@<sha>/ URI to the new SHA, "
            "not just PENDING placeholders. Used to close the recursive "
            "tail when committing the rewritten records bumps HEAD by "
            "one more SHA (commit N+1 re-anchors records to commit N "
            "which is now the sample-containing commit)."
        ),
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
        count = rewrite_record(path, sha, force=args.force)
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
