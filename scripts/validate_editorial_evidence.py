#!/usr/bin/env python3
"""Check the published briefs' evidence references, including legacy formats.

This gate checks reference integrity, not semantic entailment. The separate
editorial review must read the claims against their source material. Original
run records are not rewritten when an old issue receives a current backfill.
"""
from __future__ import annotations

import argparse
import ipaddress
from pathlib import Path
import re
from urllib.parse import urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
WEEK = re.compile(r"^\d{4}-W\d{2}$")
EVIDENCE = re.compile(r"^[ \t]*\*\*Evidence:?\*\*:?[ \t]*(.*)$", re.M | re.I)
PLACEHOLDERS = {"todo", "tbd", "pending", "unknown", "placeholder"}
FENCE = re.compile(r"^[ \t]*(`{3,}|~{3,})(.*)$")
NUMERIC_HOST = re.compile(r"(?:0x[0-9a-f]+|[0-9]+)(?:\.(?:0x[0-9a-f]+|[0-9]+)){0,3}", re.I)


def outside_fenced_code(text: str) -> str:
    """Ignore example Evidence lines, including nested shorter fence markers."""
    visible: list[str] = []
    fence: tuple[str, int] | None = None
    for line in text.splitlines(keepends=True):
        match = FENCE.match(line)
        if fence is not None:
            if match and match[1][0] == fence[0] and len(match[1]) >= fence[1] and not match[2].strip():
                fence = None
            continue
        if match and (match[1][0] != "`" or "`" not in match[2]):
            fence = (match[1][0], len(match[1]))
            continue
        visible.append(line)
    return "".join(visible)


def is_public_http_uri(uri: object) -> bool:
    """Check literal destinations without resolving names or fetching sources."""
    if not isinstance(uri, str):
        return False
    try:
        parsed = urlsplit(uri)
        host = (parsed.hostname or "").casefold().rstrip(".")
    except ValueError:
        return False
    if parsed.scheme not in {"https", "http"} or not host:
        return False
    if host in {"localhost", "localhost.localdomain"} or host.endswith((".localhost", ".localhost.localdomain")):
        return False
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        # Numeric shorthand (127.1, integer or hex IPv4) must not pass as a
        # domain name after strict IP parsing rejects it. Do not use DNS here.
        return bool(host) and not NUMERIC_HOST.fullmatch(host)
    if isinstance(address, ipaddress.IPv6Address) and address.ipv4_mapped is not None:
        address = address.ipv4_mapped
    return address.is_global and not address.is_multicast and not address.is_reserved and not getattr(address, "is_site_local", False)


def signal_sections(text: str, week: str) -> list[tuple[str, str]]:
    """Recognize the published layouts without imposing newer headings.

    W20/W21 used major headings for their five lead picks. Later issues
    place numbered subheadings inside Top signals. Code examples are
    removed before either layout is split, so a runbook's headings and
    Evidence examples cannot create or satisfy a digest section.
    """
    visible = outside_fenced_code(text)
    top = re.search(r"^##[ \t]+Top signals\b[^\n]*$", visible, re.M | re.I)
    if top:
        tail = visible[top.end():]
        end = re.search(r"^##[ \t]+", tail, re.M)
        body = tail[:end.start()] if end else tail
        headings = list(re.finditer(r"^###[ \t]+([^\n]+)$", body, re.M))
    elif week in {"2026-W20", "2026-W21"}:
        body = visible
        stop = re.search(r"^##[ \t]+(?:Worth your time|Three more\b|Questions to ask\b|Closing thought\b|Postscript\b)", body, re.M | re.I)
        if stop:
            body = body[:stop.start()]
        headings = list(re.finditer(r"^##[ \t]+([^\n]+)$", body, re.M))
        if not headings:
            return [("legacy digest", body)]
    else:
        return []
    return [
        (heading[1].strip(), body[heading.end():headings[index + 1].start() if index + 1 < len(headings) else len(body)])
        for index, heading in enumerate(headings)
    ]


def check_brief(brief_dir: Path) -> list[str]:
    label = brief_dir.name
    text = (brief_dir / "brief.md").read_text(encoding="utf-8")
    lines = EVIDENCE.findall(outside_fenced_code(text))
    if not lines:
        return [f"{label}: no explicit Evidence line for the reviewed issue"]
    matrix_paths = sorted((brief_dir / "matrix").glob("*.yaml"))
    if not matrix_paths:
        return [f"{label}: Evidence lines have no matrix cell files"]
    errors: list[str] = []
    sections = signal_sections(text, label)
    if not sections:
        errors.append(f"{label}: no recognizable Top signal sections")
    for title, section in sections:
        if not EVIDENCE.search(section):
            errors.append(f"{label}: Top signal {title!r} has no Evidence line")
    cells: dict[str, dict] = {}
    for matrix_path in matrix_paths:
        try:
            data = yaml.safe_load(matrix_path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            errors.append(f"{label}: {matrix_path.name} cannot be read: {exc}")
            continue
        if not isinstance(data, dict) or "cells" not in data:
            continue  # Selection, source and action artifacts are separate.
        if not isinstance(data["cells"], list):
            errors.append(f"{label}: {matrix_path.name} cells must be a list")
            continue
        for cell in data["cells"]:
            if not isinstance(cell, dict) or not isinstance(cell.get("id"), str):
                errors.append(f"{label}: matrix cell has no string id")
                continue
            if cell["id"] in cells:
                errors.append(f"{label}: duplicate cell id {cell['id']}")
            cells[cell["id"]] = cell
    cited: set[str] = set()
    for line in lines:
        ids = [value.strip("` .\t") for value in line.split(",") if value.strip()]
        if not ids:
            errors.append(f"{label}: empty Evidence line")
        cited.update(ids)
    for cell_id in sorted(cited):
        cell = cells.get(cell_id)
        prefix = f"{label}: Evidence cell {cell_id}"
        if cell is None:
            errors.append(f"{prefix} does not exist")
            continue
        if cell.get("faithfulness_status") != "passed":
            errors.append(f"{prefix} is not faithfulness-passed")
        # AGENTS.md defines verification by faithfulness_status. The older
        # lifecycle vocabulary can still say created after that review.
        if cell.get("status") == "rejected":
            errors.append(f"{prefix} is rejected")
        if not isinstance(cell.get("content"), str) or not cell["content"].strip():
            errors.append(f"{prefix} has no content")
        refs = cell.get("source_refs")
        if not isinstance(refs, list) or not refs:
            errors.append(f"{prefix} has no source reference")
            continue
        for ref in refs:
            if not isinstance(ref, dict):
                errors.append(f"{prefix} has a malformed source reference")
                continue
            uri, span = ref.get("uri"), ref.get("quote_or_span")
            if not is_public_http_uri(uri):
                errors.append(f"{prefix} has no public HTTP source URI")
            if not isinstance(span, str) or not span.strip() or span.strip().lower() in PLACEHOLDERS:
                errors.append(f"{prefix} has no usable source span or locator")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    briefs = args.root / "briefs"
    if not briefs.is_dir():
        print("validate_editorial_evidence FAILED: no briefs directory")
        return 1
    weeks = sorted(p for p in briefs.iterdir() if p.is_dir() and WEEK.fullmatch(p.name) and (p / "brief.md").is_file())
    if not weeks:
        print("validate_editorial_evidence FAILED: no canonical briefs")
        return 1
    errors = [error for week in weeks for error in check_brief(week)]
    if errors:
        print(f"validate_editorial_evidence FAILED ({len(errors)} findings):")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"validate_editorial_evidence OK ({len(weeks)} canonical briefs; reference integrity only)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
